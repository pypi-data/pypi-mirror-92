import logging
from pathlib import Path

import rasterio

from tiler_swift.quadkey import quadkeys


def main(args):
    logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)

    logger = logging.getLogger("tiler-swift.quadkey")

    args.out.mkdir(exist_ok=True)

    logger.info(f"Reading raster from {args.raster}")

    with rasterio.open(args.raster) as dataset:
        logger.info(f"Writing quadkeys to {args.out}")

        for quadkey, data, profile in quadkeys(dataset, z=args.zoom, nodata=args.nodata):
            outpath = args.out / Path(quadkey).with_suffix(args.raster.suffix)

            profile.update({"driver": "GTiff", "tiled": False, "compress": "deflate", "predictor": 2})

            with rasterio.open(outpath, "w", **profile) as out:
                out.write(data)
