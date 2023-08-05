import argparse
from pathlib import Path

import tiler_swift.scripts.quadkey


def main():
    Formatter = argparse.ArgumentDefaultsHelpFormatter

    parser = argparse.ArgumentParser(prog="tiler-swift", description="cuts quadkeys from raster", formatter_class=Formatter)

    arg = parser.add_argument

    arg("raster", type=Path, help="raster to cut quadkeys from")
    arg("-z", "--zoom", type=int, required=True, help="zoom level to cut quadkeys at")
    arg("-o", "--out", type=Path, required=True, help="directory to write quadkeys to")
    arg("-n", "--nodata", help="nodata value to use for filling at edges")

    parser.set_defaults(main=tiler_swift.scripts.quadkey.main)

    args = parser.parse_args()
    args.main(args)


if __name__ == "__main__":
    main()
