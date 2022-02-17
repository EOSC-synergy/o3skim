#!/usr/bin/env python3
"""
Collect and standardize measurement ozone data from multiple sources:
"""
import argparse
import logging
import sys

from o3skim.measures_sbuv import sbuv_function


class StripArgument(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values.strip())


# Script logger setup
logger = logging.getLogger("o3measure")

# Parser for script inputs
parser = argparse.ArgumentParser(
    prog=f"o3measure", description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="See '<command> --help' to read about a specific sub-command.")
parser.add_argument(
    "-v", "--verbosity", type=str, default='INFO',
    choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
    help="Sets the logging level (default: %(default)s)")
parser.add_argument(
    "-n", "--variable-name", type=str, default='tco3_zm', action=StripArgument,
    help="Variable name inside netCDF output (default: %(default)s)")
parser.add_argument(
    "-o", "--output", type=str, default='measures.nc', action=StripArgument,
    help="Target netCDF file (default: %(default)s)")
subparsers = parser.add_subparsers(dest='command', help='Sub-commands')


# Arguments for subcommand SBUV
sbuv_parser = subparsers.add_parser('SBUV', help='SBUV Source input')
sbuv_parser.set_defaults(command=sbuv_function)
sbuv_parser.add_argument(
    "-s", "--delimiter", type=str, default=r'\s+',
    help="Delimiter to use (default: %(default)s)")
sbuv_parser.add_argument(
    "textfile", nargs=1, type=str, action='store',
    help="File .txt with sbuv measurements to load")


def main():
    args = parser.parse_args()
    if args.command is not None:
        run_command(**vars(args))
    else:
        parser.print_help()
    sys.exit(0)  # Shell return 0 == success


def run_command(command, **options):
    # Set logging level
    logging.basicConfig(
        level=getattr(logging, options['verbosity']),
        format='%(asctime)s %(name)-24s %(levelname)-8s %(message)s')

    # Common operations
    logger.info("Program start")

    # Loading of DataArray and attributes
    logger.info("Data loading and standardization of measurements")
    dataset = command(**options)

    # Saving
    logger.info("Staving result into %s.nc", options['output'])
    dataset.to_netcdf(options['output'])

    # End of program
    logger.info("End of program")


if __name__ == '__main__':
    main()
