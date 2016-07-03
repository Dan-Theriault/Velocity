"""CLI to make new dxdt notebooks."""
import argparse
from os import path
from dxdtconf import dxdtConf

configdir = path.expanduser('~') + '/.dxdt'
source = dxdtConf(configdir+'/dxdt.conf')


def main():
    """CLI for creating dxdt notebooks."""
    newp = argparse.ArgumentParser(description='Bind a new dxdt notebook.')
    newp.add_argument('name',
                      help='Name of dxdt book.')
    newp.add_argument('path',
                      help='Absolute path to dxdt book.')
    newp.add_argument('extension',
                      help='Extension for pages of dxdt book.')

    args = newp.parse_args()
    source.newbook(args.name, args.path, args.extension)
