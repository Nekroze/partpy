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
