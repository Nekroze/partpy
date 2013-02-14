"""Matcher utilizes SourceString to provide some simple string matching
functionality."""
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'

from .sourcestring import SourceString

class SourceLine(SourceString):

    def __init__(self, string, lineno):
        super(SourceLine, self).__init__(string)
        self.lineno = lineno

    def strip_trailing_ws(self):
        self.string = self.string.rstrip()

    def get_first_char(self):
        for char in self.string:
            if not char.isspace():
                return char

    def get_last_char(self):
        for char in reversed(self.string):
            if not char.isspace():
                return char

    def __repr__(self):
        lineno = self.lineno
        padding = 0
        if lineno < 1000:
            padding = 1
        if lineno < 100:
            padding = 2
        if lineno < 10:
            padding = 3

        return str(lineno) + (' ' * padding) + '|' + self.string
