"""CLI to dxdt."""

import argparse
from os import path
from dxdtconf import dxdtConf

configdir = path.expanduser('~') + '/.dxdt'
source = dxdtConf(configdir+'/dxdt.conf')


def main():
    """CLI for configuring dxdt notebooks."""
    setp = argparse.ArgumentParser(
        description='Configure an existing dxdt book.')
    setp.add_argument('book',
                      choices=source.getbooks(),
                      help='Name of dxdt notebook.')
    keys = ['path', 'extension', 'editor', 'template', 'args']
    setp.add_argument('key',
                      choices=keys,
                      help='Setting to configure.')
    setp.add_argument('value',
                      nargs='+',
                      help='New value for setting. args key accepts ' +
                      'multiple values, all other keys require one value.')

    args = setp.parse_args()
    source.write(args.book, args.key, args.value)
