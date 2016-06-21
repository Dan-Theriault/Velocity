"""velocity.py implements the main logic of the program."""

from pathlib import Path
import subprocess
from shutil import copyfile
from velocityconfig import VelocityConfig

velocity_dir = '/home/dtheriault3/Documents/CODE/Velocity'


def velocity(filename, bookname='Notes', config='default'):
    """Velocity implements the logic for opening pages.

    filename -- string representation of file, no extension
    config -- configuration sourced from velocity.config

    The config MUST specify a bookpath and an extension.
    The program will attempt to provide sane defaults for editor, editor_args,
    and, if applicable, template, but makes no guarantees.
    """
    # Configuration Variables
    source = VelocityConfig(velocity_dir+'/velocity.conf')
    config = source.read(bookname)

    book = Path(config['bookpath'])
    page = book/(filename+config['extension'])

    editor = config['editor']
    editor_args = config['args']
    editor_args[-1] = editor_args[-1] + ' ' + (page.as_posix())

    if 'template' in config:
        template = config['template']
    else:
        template = None

    # The Velocity logic!
    if page.exists():
        subprocess.Popen([editor, *editor_args])
    else:
        if template is not None and template.exists():
            copyfile(template.as_posix(), page.as_posix())
        else:
            newfile = open(page.as_posix(), 'a')
            newfile.close()
        subprocess.Popen([editor, *editor_args])


def get_config(config):
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
