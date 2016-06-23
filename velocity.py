#!/usr/bin/env python3

"""velocity.py implements the main logic of the program."""

import subprocess
import os.path as path
from os import makedirs
from shutil import copy
from velocityconf import bookconf

configdir = path.expanduser('~') + '/.velocity'


def velocity(filename, book='Notes'):
    """Velocity implements the logic for opening pages.

    filename -- string representation of file, no extension
    config -- configuration sourced from velocity.config

    The config MUST specify a bookpath and an extension.
    The program will attempt to provide sane defaults for editor, editor_args,
    and, if applicable, template, but makes no guarantees.
    """
    # Configuration Variables
    source = bookconf(configdir+'/velocity.conf')
    config = source.read(book)

    bookpath = config['bookpath']
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

    # The Velocity logic!
    if path.exists(page):
        subprocess.Popen([editor, *editor_args])
    else:
        if template is not None:
            copy(template, page)
        else:
            newfile = open(page, 'a')
            newfile.close()
        subprocess.Popen([editor, *editor_args])
