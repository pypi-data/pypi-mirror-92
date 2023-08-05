# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tiler_swift', 'tiler_swift.scripts']

package_data = \
{'': ['*']}

install_requires = \
['mercantile>=1.1.6,<2.0.0', 'numpy>=1.19.5,<2.0.0', 'rasterio>=1.1.8,<2.0.0']

entry_points = \
{'console_scripts': ['tiler-swift = tiler_swift.scripts.__main__:main']}

setup_kwargs = {
    'name': 'tiler-swift',
    'version': '0.2.0',
    'description': 'Tiler Swift, the swiftest quadkey tiler in the wild west',
    'long_description': '# tiler-swift\n\nTiler Swift, the swiftest quadkey tiler in the wild west.\n\nFeatures\n- ✔ Get quadkey tiles from raster\n- ✔ Simple and blazingly fast\n\n![](assets/quadkey.jpg)\n\n\n## Table of Contents\n\n1. [Overview](#overview)\n2. [Library](#development)\n3. [Command Line](#command-line)\n4. [Development](#development)\n5. [License](#license)\n\n\n## Overview\n\nThis project provides a Python library and a thin command line wrapper on top of it to cut quadkey raster tiles.\n\nQuadkey tiles are raster files of equal size (width, height) on a specific zoom level; the coordinate reference system is the Mercator Projection.\nThe quadkey identifier is constructed by dividing the world into four, then dividing each cell into four again, and so on, recursively.\n\nSee\n- https://labs.mapbox.com/what-the-tile/\n- https://docs.microsoft.com/en-us/bingmaps/articles/bing-maps-tile-system\n- https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames\n- https://wiki.openstreetmap.org/wiki/Slippy_Map\n\n\n## Library\n\nThe `quadkeys(dataset, z, nodata=0, tile_filter_fn=None)` function provides a generator yielding quadkeys and their associated data.\n\nArgs\n- `dataset`: the rasterio dataset to cut quadkeys from\n- `z`: the zoom level to cut quadkeys at\n- `nodata`: the value to use for filling\n- `tile_filter_fn`: a function `mercantile.Tile -> bool` to filter the quadkey generator with\n\nYields a tuple with\n- `quadkey`: the quadkey name e.g. `1202121012`\n- `data`: the pixel data as a numpy ndarray\n- `profile`: the rasterio profile with metadata e.g. transformation for geo-referencing\n\nExample usage:\n\n```python\nfor quadkey, data, profile in quadkeys(dataset, z=args.zoom):\n    print(quadkey)\n\n    with rasterio.open(args.out, "w", **profile) as out:\n        out.write(data)\n```\n\n\n## Command Line\n\n```\nusage: tiler-swift [-h] -z ZOOM -o OUT [-n NODATA] raster\n\ncuts quadkeys from raster\n\npositional arguments:\n  raster                raster to cut quadkeys from\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -z ZOOM, --zoom ZOOM  zoom level to cut quadkeys at (default: None)\n  -o OUT, --out OUT     directory to write quadkeys to (default: None)\n  -n NODATA, --nodata NODATA\n                        nodata value to use for filling at edges (default: None)\n```\n\nExample usage:\n\n```\nquadkeys input.tif -o output.tif -z 10 -n 0\n```\n\n\n## Development\n\nFor a self-contained and isolated dev environment\n\n    docker-compose build\n\nFor a development shell in the container, run\n\n    docker-compose run --rm --entrypoint bash dev\n    $ quadkey --help\n\nTo run the container manually\n\n    docker run robofarm/quadkey\n\n\n## License\n\nCopyright © 2020 robofarm\n\nDistributed under the MIT License (MIT).\n',
    'author': 'Robofarm',
    'author_email': 'hello@robofarm.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
