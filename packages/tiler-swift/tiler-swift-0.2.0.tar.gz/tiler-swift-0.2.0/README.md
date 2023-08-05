# tiler-swift

Tiler Swift, the swiftest quadkey tiler in the wild west.

Features
- ✔ Get quadkey tiles from raster
- ✔ Simple and blazingly fast

![](assets/quadkey.jpg)


## Table of Contents

1. [Overview](#overview)
2. [Library](#development)
3. [Command Line](#command-line)
4. [Development](#development)
5. [License](#license)


## Overview

This project provides a Python library and a thin command line wrapper on top of it to cut quadkey raster tiles.

Quadkey tiles are raster files of equal size (width, height) on a specific zoom level; the coordinate reference system is the Mercator Projection.
The quadkey identifier is constructed by dividing the world into four, then dividing each cell into four again, and so on, recursively.

See
- https://labs.mapbox.com/what-the-tile/
- https://docs.microsoft.com/en-us/bingmaps/articles/bing-maps-tile-system
- https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames
- https://wiki.openstreetmap.org/wiki/Slippy_Map


## Library

The `quadkeys(dataset, z, nodata=0, tile_filter_fn=None)` function provides a generator yielding quadkeys and their associated data.

Args
- `dataset`: the rasterio dataset to cut quadkeys from
- `z`: the zoom level to cut quadkeys at
- `nodata`: the value to use for filling
- `tile_filter_fn`: a function `mercantile.Tile -> bool` to filter the quadkey generator with

Yields a tuple with
- `quadkey`: the quadkey name e.g. `1202121012`
- `data`: the pixel data as a numpy ndarray
- `profile`: the rasterio profile with metadata e.g. transformation for geo-referencing

Example usage:

```python
for quadkey, data, profile in quadkeys(dataset, z=args.zoom):
    print(quadkey)

    with rasterio.open(args.out, "w", **profile) as out:
        out.write(data)
```


## Command Line

```
usage: tiler-swift [-h] -z ZOOM -o OUT [-n NODATA] raster

cuts quadkeys from raster

positional arguments:
  raster                raster to cut quadkeys from

optional arguments:
  -h, --help            show this help message and exit
  -z ZOOM, --zoom ZOOM  zoom level to cut quadkeys at (default: None)
  -o OUT, --out OUT     directory to write quadkeys to (default: None)
  -n NODATA, --nodata NODATA
                        nodata value to use for filling at edges (default: None)
```

Example usage:

```
quadkeys input.tif -o output.tif -z 10 -n 0
```


## Development

For a self-contained and isolated dev environment

    docker-compose build

For a development shell in the container, run

    docker-compose run --rm --entrypoint bash dev
    $ quadkey --help

To run the container manually

    docker run robofarm/quadkey


## License

Copyright © 2020 robofarm

Distributed under the MIT License (MIT).
