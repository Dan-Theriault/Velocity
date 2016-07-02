#!/usr/bin/env python3

"""Implementation of a class for sourcing configuration from a given file.

Author: Dan Theriault
Feature-incomplete and under active development.
"""

import configparser


class VelocityConf:
    """Class for handling I/O to configuration files."""

    def __init__(self, configfile):
        """Class Instantiation.

        configfile is most likely in $HOME/.velocity
        """
        self.file = configfile
        self.parser = configparser.ConfigParser()
        self.parser.read(self.file)
        self.config = {}

    def defaultbook(self):
        """Used primarily when 'book' argument to velocity() is None."""
        return self.parser['Defaults']['book']

    def getbooks(self):
        """return a list of books based off the configfile."""
        sections = self.parser.sections()
        sections.remove('Defaults')
        return sections

    def read(self, book):
        """Read configuration information and return as a dict."""
        self.config = {
            'path': self.parser[book]['path'],
            'extension': self.parser[book]['extension'],
            'args': []
        }

        # Get editor for book if available: else, use global default
        if 'editor' in self.parser[book]:
            self.config['editor'] = self.parser[book]['editor']
        else:
            self.config['editor'] = self.parser['Defaults']['editor']

        i = 1
        while 'arg' + str(i) in self.parser[book]:
            self.config['args'].append(self.parser[book]['arg'+str(i)])
            i = i + 1

        if 'template' in self.parser[book]:
            self.config['template'] = self.parser[book]['template']

        return self.config

    def write(self, book):
        """Dummy method for writing configuration to file."""
        pass
