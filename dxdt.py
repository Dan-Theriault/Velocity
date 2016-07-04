#!/usr/bin/env python3

"""dxdt.py is notational velocity for every file.

The script should currently support any filetype or editor,
as well as templates and a basic CLI.
"""

import argparse
import subprocess
from os import makedirs, path
from shutil import copy
from dxdtconf import dxdtConf

# Implement more flexible configuration file location (system, cross-platform)
configdir = path.expanduser('~/.dxdt')
source = dxdtConf(configdir+'/dxdt.conf')


def dxdt(filename, book=source.defaultbook()):
    """dxdt implements the logic for opening pages.

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
