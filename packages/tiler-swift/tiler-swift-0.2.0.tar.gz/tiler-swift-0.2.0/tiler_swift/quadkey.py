import math
import logging

import rasterio
import rasterio.crs
import rasterio.warp
import rasterio.coords
import rasterio.windows
import rasterio.transform
import rasterio.vrt

import numpy as np

import mercantile

logger = logging.getLogger("tiler-swift.quadkey")


def quadkeys(dataset, z, nodata=None, tile_filter_fn=None):
    # TODO: we work with one band, we can generalize
    # later; then we have to take care of different
    # nodata values and dtypes on a per band basis
    assert dataset.count == 1, "one band required"

    kwargs = {}

    # WarpedVRT does not work with GCPs by default
    # https://github.com/mapbox/rasterio/issues/2086
    if dataset.transform.is_identity and dataset.gcps:
        kwargs.update({"src_crs": dataset.gcps[1],
                       "src_transform": rasterio.transform.from_gcps(dataset.gcps[0])})

    with rasterio.vrt.WarpedVRT(dataset, crs="EPSG:3857", **kwargs) as vrt:

        # Mercantile requires lng, lat i.e. https://epsg.io/4326
        bounds = rasterio.warp.transform_bounds(vrt.crs, rasterio.crs.CRS({"init": "EPSG:4326"}), *vrt.bounds)

        tiles = mercantile.tiles(*bounds, zooms=[z])

        if tile_filter_fn is not None:
            tiles = (tile for tile in tiles if tile_filter_fn(tile))

        for tile in tiles:
            quadkey = mercantile.quadkey(tile)
            bounds = mercantile.xy_bounds(*tile)

            window = vrt.window(*bounds)

            transform = vrt.window_transform(window.round_lengths(op="ceil"))

            # WarpedVRT does not support boundless reads;
            # work around by manually padding with nodata
            # https://github.com/mapbox/rasterio/issues/2084

            h_orig, w_orig = math.ceil(window.height), math.ceil(window.width)
            col_off_orig, row_off_orig = window.col_off, window.row_off

            window = window.intersection(rasterio.windows.Window(0, 0, vrt.width, vrt.height))

            dcol = int(window.col_off - col_off_orig)
            drow = int(window.row_off - row_off_orig)

            window = window.round_lengths(op="ceil")

            h, w = int(window.height), int(window.width)

            logging.debug(f"Reading quadkey tile data")

            bounded = vrt.read(window=window, out_shape=(dataset.count, h, w))

            # For boundless reads we need a nodata value
            # otherwise we can not fill in at the edges
            # https://github.com/mapbox/rasterio/issues/2087
            dtype = dataset.dtypes[0]
            nodata = nodata if nodata is not None else dataset.nodatavals[0]

            assert nodata is not None, "proper nodata val for dtype is set"

            data = np.full(shape=(dataset.count, h_orig, w_orig),
                           fill_value=nodata, dtype=dtype)

            data[:, drow:drow + h, dcol:dcol + w] = bounded

            profile = vrt.profile
            profile.update({"width": w_orig, "height": h_orig, "nodata": nodata,
                            "dtype": dtype, "transform": transform})

            yield quadkey, data, profile
