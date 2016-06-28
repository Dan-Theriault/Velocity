#!/usr/bin/env python3

"""Implementation of a class for sourcing configuration from a given file."""

import configparser


class bookconf:
    """Class for handling configuration files."""

    def __init__(self, configfile):
        """Instantiation."""
        self.file = configfile
        self.parser = configparser.ConfigParser()
        self.parser.read(self.file)
        self.config = {}

    def getbooks(self):
        """return a list of books based off the configfile."""
        sections = self.parser.sections()
        sections.remove('Defaults')
        return sections

    def read(self, bookname):
        """Read configuration information and return as a dictionary."""
        if bookname is None:
            bookname = self.parser['Defaults']['book']

        self.config = {
            'bookpath': self.parser[bookname]['bookpath'],
            'extension': self.parser[bookname]['extension'],
            'args': []
        }

        # Get editor for book if available: else, use global default
        if 'editor' in self.parser[bookname]:
            self.config['editor'] = self.parser[bookname]['editor']
        else:
            self.config['editor'] = self.parser['Defaults']['editor']

        i = 1
        while 'arg' + str(i) in self.parser[bookname]:
            self.config['args'].append(self.parser[bookname]['arg'+str(i)])
            i = i + 1

        if 'template' in self.parser[bookname]:
            self.config['template'] = self.parser[bookname]['template']

        return self.config

    def write(self, bookname):
        """Dummy method for writing configuration to file."""
        pass
