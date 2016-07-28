#!/usr/bin/env python3

"""Implementation of a class for sourcing configuration from a given file.

Author: Dan Theriault
Feature-incomplete and under active development.
"""

import configparser
import os
from dxdt.errors import ConfigError


def source():
    """return configuration file path."""
    config_dir = os.path.expanduser('~/.dxdt')

    if not os.path.exists(config_dir) and os.path.isdir(config_dir):
        os.makedirs(config_dir)
    config_file = config_dir+'/config'
    if not os.path.exists(config_file) and os.path.isfile(config_file):
        init = configparser.ConfigParser()
        init.add_section('default')
        init['default']['editor'] = 'xdg-open'
        init['default']['book'] = ''
        raise ConfigError("No dxdt books found.")

    config_source = BookHandler(config_file)
    return config_source


class BookHandler:
    """Class for handling dxdt's configuration file."""

    def __init__(self, config_file):
        """Class Instantiation.

        configfile is most likely in $HOME/.dxdt/
        """
        self.file = config_file
        self.dir = os.path.dirname(config_file)
        self.parser = configparser.ConfigParser()
        self.parser.read(self.file)

    def default_book(self):
        """Used primarily when 'book' argument to dxdt() is None."""
        try:
            return self.parser['default']['book']
        except KeyError:
            return None

    def get_books(self):
        """return a list of books based off the configfile."""
        sections = self.parser.sections()
        sections.remove('default')
        # if sections == []:
        #     raise ConfigError("No dxdt books found.")
        return sections

    def get_pages(self, book):
        """return a list of existing pages in a book."""
        try:
            path = os.path.expanduser(self.parser[book]['path'])
            ext = self.parser[book]['extension']
        except KeyError:
            raise ConfigError("book \'"+book+"\' is improperly configured.")

        def is_page(f):
            """Determine if a path points to a page in given notebook."""
            f = os.path.join(path, f)
            _, f_ext = os.path.splitext(f)
            if not os.path.isfile(f):
                return False
            elif f_ext != ext:
                return False
            else:
                return True

        raw_pages = [f for f in os.listdir(path) if is_page(f)]

        pages = []
        for page in raw_pages:
            pages.append(page.replace(ext, ''))
        return pages

    def read(self, book):
        """Read configuration information and return as a dict."""
        try:
            config = {
                'path': os.path.expanduser(self.parser[book]['path']),
                'extension': self.parser[book]['extension'],
                'args': []
            }
        except KeyError:
            raise ConfigError("book \'"+book+"\' is improperly configured.")

        # Get editor for book if available: else, use global default
        if 'editor' in self.parser[book]:
            config['editor'] = self.parser[book]['editor']
        else:
            config['editor'] = self.parser['default']['editor']

        i = 1
        while 'arg' + str(i) in self.parser[book]:
            config['args'].append(self.parser[book]['arg'+str(i)])
            i = i + 1

        if 'template' in self.parser[book]:
            config['template'] = self.parser[book]['template']

        return config

    def write(self, book, key, value):
        """Basic implementation of writing new values to config."""
        if key is 'args':
            i = 1
            for arg in value:
                self.parser[book]['arg' + str(i)] = arg
                i = i + 1
        elif key is 'default':
            if value is True:
                self.parser['default']['book'] = book
        else:
            self.parser[book][key] = value
        self.parser.write(open(self.file, 'w'))

    def new_book(self, name, path, extension):
        """Create a book with given name if none exists."""
        sections = self.get_books()
        if name not in sections:
            self.parser.add_section(name)
            self.parser[name]['path'] = path
            self.parser[name]['extension'] = extension
            self.parser.write(open(self.file, 'w'))
        else:
            raise ValueError('book already exists: ' + name)

    def remove_book(self, name):
        """Remove an existing book."""
        sections = self.get_books()
        if name not in sections:
            raise ValueError('book does not exist: ' + name)
        else:
            self.parser.remove_section(name)
            self.parser.write(open(self.file, 'w'))
