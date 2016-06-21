"""velocity.py implements the main logic of the program."""

from pathlib import Path
import subprocess
from shutil import copyfile


def velocity(filename, config='default'):
    """Velocity implements the logic for opening pages.

    filename -- string representation of file, no extension
    config -- configuration sourced from velocity.config

    The config MUST specify a notebook path and an extension.
    The program will attempt to provide sane defaults for editor, editor_args,
    and, if applicable, template.
    """
    path_config = get_path_config(config)
    book = path_config['book']
    ext = path_config['extension']
    page = book/(filename+ext)

    editor_config = get_editor_config(config, page)
    editor = editor_config['editor']
    editor_args = editor_config['editor_args']
    if 'template' in editor_config:
        template = editor_config['template']
    else:
        template = None

    if page.exists():
        subprocess.Popen(editor, *editor_args])
    else:
        if template is not None and template.exists():
            copyfile(template.as_posix(), page.as_posix())
        else:
            newfile = open(page.as_posix(), 'a')
            newfile.close()
        subprocess.Popen(editor, *editor_args])


def get_path_config(config):
    """get_path_config reads the notebook and extension from the config."""
    # TODO Properly sourcing a configuration
    config = {
            'book': Path('/home/dtheriault3/Notes'),
            'extension': '.md'
            }
    return config


def get_editor_config(config, page):
    """get_editor_config reads editor options from the config."""
    config = {
            'editor': 'gnome-terminal',
            'editor_args': ['-e', 'vim ' + page.as_posix()],
            }
    return config
