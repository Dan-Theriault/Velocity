#!/usr/bin/env python3

"""velocity.py is notational velocity for everything.

The script currently should support any filetype or editor,
as well as templates and a basic CLI.
"""

import argparse
import subprocess
import os.path as path
from os import makedirs
from shutil import copy
from velocityconf import VelocityConf

# Implement more flexible configuration file location (system, cross-platform)
configdir = path.expanduser('~') + '/.velocity'
source = VelocityConf(configdir+'/velocity.conf')


def velocity(filename, book=source.defaultbook()):
    """Velocity implements the logic for opening pages.

    Filename should NOT include an extension.
    """
    # Configuration Variables
    config = source.read(book)

    bookpath = config['path']
    if not path.exists(bookpath):
        makedirs(bookpath)
    page = bookpath + '/' + filename + config['extension']

    editor = config['editor']
    editor_args = config['args']
    if len(editor_args) > 0:
        editor_args[-1] = editor_args[-1] + ' ' + page
    else:
        editor_args = [page]

    if 'template' in config:
        template = configdir + '/Templates/' + config['template']
        if not path.exists(template) or not path.isfile(template):
            template = None
    else:
        template = None

    # Logic for opening / creating files
    if path.exists(page):
        subprocess.Popen([editor, *editor_args])
    else:
        if template is not None:
            copy(template, page)
        else:
            newfile = open(page, 'a')
            newfile.close()
        subprocess.Popen([editor, *editor_args])

if __name__ == '__main__':
    # If run as __main__, a CLI is made available
    parser = argparse.ArgumentParser(
        description='Notational Velocity for everything')

    parser.add_argument('--book', '-b',
                        metavar='NOTEBOOK',
                        choices=source.getbooks(),
                        help='Velocity notebook (defined in velocity.conf)')
    parser.add_argument('page',
                        help='The page (or pages) to open with velocity')
    args = parser.parse_args()

    if args.book is not None:
        velocity(args.page, args.book)
    else:
        velocity(args.page)
