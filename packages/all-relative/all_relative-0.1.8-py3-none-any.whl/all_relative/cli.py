import argparse
import os


cli = argparse.ArgumentParser(
    description="convert a static site to use only relative urls",
)
cli.add_argument(
    "rootdir",
    help="path to the root directory",
)
cli.add_argument(
    "-n",
    "--dry",
    help="do a dry-run, i.e., print paths to be renamed",
    action="store_true",
)
cli.add_argument(
    "-q",
    "--quiet",
    help="do not print anything to stdout",
    action="store_true",
)
cli.add_argument(
    "-v",
    "--verbose",
    help="set logging level to DEBUG",
    action="store_true",
)


args = cli.parse_args()
