"""CLIs to dxdt."""
import argparse
from os import path
from dxdt import dxdt
from dxdtconf import dxdtConf

configdir = path.expanduser('~/.dxdt')
source = dxdtConf(configdir+'/dxdt.conf')


def opener():
    """CLI for opening files."""
    # Main parser
    parser = argparse.ArgumentParser(
        description='Notational Velocity for every file')

    parser.add_argument('book',
                        choices=source.getbooks(),
                        nargs='?',
                        help='Name of dxdt notebook.')
    parser.add_argument('page',
                        help='Page to open with dxdt.')

    args = parser.parse_args()

    if args.book is not None:
        dxdt(args.page, args.book)
    else:
        dxdt(args.page)


def setter():
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


def binder():
    """CLI for creating dxdt notebooks."""
    newp = argparse.ArgumentParser(description='Bind a new dxdt notebook.')
    newp.add_argument('name',
                      help='Name of dxdt book.')
    newp.add_argument('path',
                      help='Path to dxdt book.')
    newp.add_argument('extension',
                      help='Extension for pages of dxdt book.')

    args = newp.parse_args()
    source.newbook(args.name, args.path, args.extension)
