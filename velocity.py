#!/usr/bin/env python3

"""velocity.py implements the main logic of the program."""

import subprocess
from os.path import expanduser
from pathlib import Path
from shutil import copy
from velocityconfig import VelocityConfig

configdir = expanduser('~') + '/.velocity'


def velocity(filename, book='Notes'):
    """Velocity implements the logic for opening pages.

    filename -- string representation of file, no extension
    config -- configuration sourced from velocity.config

    The config MUST specify a bookpath and an extension.
    The program will attempt to provide sane defaults for editor, editor_args,
    and, if applicable, template, but makes no guarantees.
    """
    # Configuration Variables
    source = VelocityConfig(configdir+'/velocity.conf')
    config = source.read(book)

    bookpath = Path(config['bookpath'])
    page = bookpath/(filename+config['extension'])

    editor = config['editor']
    editor_args = config['args']
    if len(editor_args) > 0:
        editor_args[-1] = editor_args[-1] + ' ' + (page.as_posix())
    else:
        editor_args = [page.as_posix()]

    if 'template' in config:
        template = Path(configdir + '/Templates/' + config['template'])
        if not template.exists() and template.is_file():
            template = None
    else:
        template = None

    # The Velocity logic!
    if page.exists():
        subprocess.Popen([editor, *editor_args])
    else:
        if template is not None:
            copy(template.as_posix(), page.as_posix())
        else:
            newfile = open(page.as_posix(), 'a')
            newfile.close()
        subprocess.Popen([editor, *editor_args])


def get_config():
    """dummy method to provide an example configuration.

    This method has been replaced with velocityconfig's read method.
    It is retained only as a debugging fallback.
    """
    config = {
        'bookpath': '/home/dtheriault3/Notes',
        'extension': '.md',
        'editor': 'gnome-terminal',
        'editor_args': ['-e', 'vim '],
        }
    return config
