#!/usr/bin/env python3

"""Command line interface to dxdt.

Subcommands: open, set, get, bind.
"""
import argparse
import os
import argcomplete
from dxdt import dxdt, config

source = config.source()


def main():
    """Argparse CLI to dxdt."""
    # Top-level parser
    parser = argparse.ArgumentParser(
        description='Notational Velocity for every file'
    )
    subparsers = parser.add_subparsers()

    # Open parser
    parser_open = subparsers.add_parser(
        'open',
        usage='usage: dxdt open [-h] [BOOK] PAGE',
        description='Open a page.'
    )
    parser_open.add_argument(
        'book',
        choices=source.get_books(),
        default=source.default_book(),
        nargs='?',
        metavar='BOOK',
        help='Name of dxdt notebook.'
    )

    parser_open.add_argument(
        'page',
        metavar='PAGE',
        nargs='+',
        help='Page to open with dxdt.'
    )
    parser_open.set_defaults(func=opener)

    # Set parser
    parser_set = subparsers.add_parser(
        'set',
        description='Configure a dxdt notebook.'
    )
    parser_set.add_argument(
        'book',
        choices=source.get_books(),
        default=source.default_book(),
        nargs='?',
        metavar='BOOK',
        help='Name of dxdt notebook.'
    )
    parser_set.add_argument(
        '-p', '--path',
        metavar='PATH',
        help='Path to this dxdt notebook (relative supported).'
    )
    parser_set.add_argument(
        '-e', '--editor',
        metavar='EDITOR',
        help='Editor for dxdt pages in this notebook.'
    )
    parser_set.add_argument(
        '--extension',
        metavar='EXTENSION',
        help='Extension for dxdt pages in this notebook.'
    )
    parser_set.add_argument(
        '-t', '--template',
        metavar='TEMPLATE',
        help='Template for dxdt pages in this notebook.'
    )
    parser_set.add_argument(
        '-a', '--arguments',
        metavar='ARGUMENTS',
        nargs='+',
        help='Arguments passed to editor for this notebook.'
    )
    # parser_set.add_argument(
    #     '-d', '--default',
    #     action='store_true',
    #     help='Make book the default dxdt notebook.'
    # )
    parser_set.set_defaults(func=setter)

    # Get parser
    parser_get = subparsers.add_parser(
        'get',
        description='Get list of books, or pages in a book.'
    )
    parser_get.add_argument(
        'book',
        nargs='?',
        choices=source.get_books(),
        metavar='BOOK',
        help='Book to list pages of. Lists all books if not set.'
    )
    parser_get.set_defaults(func=getter)

    # Bind parser
    parser_bind = subparsers.add_parser(
        'bind',
        description='Bind a new book.'
    )
    parser_bind.add_argument(
        'extension',
        help='Extension for pages of dxdt book (inlcude \'.\').'
    )
    parser_bind.add_argument(
        '-b', '--book',
        # default=os.path.basename(args.path), (set below)
        help='Alternate name for new dxdt book (defaults to directory name)'
    )
    parser_bind.add_argument(
        '-p', '--path',
        default=os.getcwd(),
        help='Specify a path, otherwise current directory is used.'
    )
    parser_bind.set_defaults(func=binder)

    # Processing
    argcomplete.autocomplete(parser)
    cli_args = parser.parse_args()
    cli_args.func(cli_args)


def opener(args):
    """Method for opening dxdt pages, calls to dxdt module."""
    args.page = ' '.join(args.page)
    dxdt.dxdt(args.page, args.book)


def setter(args):
    """Method for configuring dxdt notebooks, calls to config module."""
    args = vars(args)

    def is_opt(k):
        """Check if a key is an option."""
        if k == 'book' or k == 'func':
            return False
        elif args[k] is None:
            return False
        else:
            return True
    opts = [k for k in args.keys() if is_opt(k)]
    for option in opts:
        source.write(args['book'], option, args[option])


def getter(args):
    """Method for getting lists of books and pages, calls to config module."""
    if args.book is None:
        books = source.get_books()
        for book in books:
            print(book)
    else:
        pages = source.get_pages(args.book)
        for page in pages:
            print(page)


def binder(args):
    """Method for creating dxdt notebooks."""
    if args.book is None:
        args.book = os.path.basename(args.path)
    source.new_book(args.book, args.path, args.extension)
