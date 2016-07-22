#!/usr/bin/env python3

"""dxdt.py is notational velocity for every file.

The script should currently support any filetype or editor,
as well as templates and a basic CLI.
"""

import os
import shutil
import subprocess
from dxdt import config

source = config.source()


def dxdt(page, book=source.default_book()):
    """dxdt implements the logic for opening pages.

    page should NOT include an extension.
    """
    # Configuration Variables
    book_config = source.read(book)

    bookpath = book_config['path']
    if not os.path.exists(bookpath):
        os.makedirs(bookpath)
    page = bookpath + '/' + page + book_config['extension']

    editor = book_config['editor']
    editor_args = book_config['args']
    if len(editor_args) > 0:
        editor_args[-1] = editor_args[-1] + ' \'' + page + '\''
    else:
        editor_args = [page]

    # Logic for opening / creating files
    if os.path.exists(page):
        subprocess.Popen([editor, *editor_args])
    else:
        if 'template' in book_config:
            template = source.dir + '/Templates/' + book_config['template']
            if not os.path.exists(template) or not os.path.isfile(template):
                template = None
            shutil.copy(template, page)
        else:
            new_file = open(page, 'a')
            new_file.close()
        subprocess.Popen([editor, *editor_args])
