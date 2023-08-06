import os
import logging as log

from .cli import args
from .parsers import Parser


def main():
    loglev = log.DEBUG if args.verbose else log.INFO
    log.basicConfig(
        format="%(asctime)s:%(name)s:%(levelname)s:%(funcName)s:%(message)s",
        level=loglev,
    )

    log.debug("running main")

    os.chdir(args.rootdir)

    parser = Parser(dry=args.dry, quiet=args.quiet)

    filenames = (x.name for x in os.scandir() if x.is_file())

    for root, dirs, files in os.walk(os.getcwd()):
        for name in files:
            filename = os.path.join(root, name)
            log.debug(f"filename={filename}")

            parser.parse_file(filename)
