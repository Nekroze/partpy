"""SourceString stores the entire string to be parsed in memory and provides
some simple methods for retrieving and moving current position."""
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'

import cython as cy


@cy.cclass
class SourceString(object):
    """Stores the parse string and its length followed by current position
    in the string and if the end of the string has been reached.

    It also stores the current row and column position as manually counted.
    """
    string = cy.declare(str)
    cy.declare(length = cy.int,
               pos = cy.int, row = cy.int, col = cy.int,
               eos = cy.int)

    def __init__(self):
        self.string = ''
        self.length = 0
        self.pos = 0
        self.col = 0
        self.row = 0
        self.eos = 0

    @cy.ccall
    @cy.returns(cy.int)
    def end(self):
        return self.eos

    @cy.ccall
    @cy.returns(cy.int)
    def line(self):
        return self.row

    @cy.ccall
    @cy.returns(cy.int)
    def column(self):
        return self.col

    @cy.ccall
    @cy.returns(cy.int)
    def position(self):
        return self.pos

    @cy.ccall
    @cy.returns(str)
    def base_string(self):
        return self.string

    @cy.ccall
    @cy.locals(filename = str)
    def load_file(self, filename):
        """Read in file contents and set the current string."""
        with open(filename, 'r') as sourcefile:
            self.set_string(sourcefile.read())
        return self

    @cy.ccall
    @cy.locals(string = str)
    def set_string(self, string):
        """Set the working string and its length then reset positions."""
        self.string = string
        self.length = len(string)
        self.reset_position()
        return self

    @cy.ccall
    @cy.locals(string = str)
    def add_string(self, string):
        """Add to the working string and its length and reset eos."""
        self.string += string
        self.length += len(string)
        self.eos = 0

    @cy.ccall
    def reset_position(self):
        """Reset all current positions."""
        self.pos = 0
        self.col = 0
        self.row = 0
        self.eos = 0

    @cy.ccall
    @cy.locals(length = cy.int)
    @cy.returns(cy.int)
    def has_space(self, length = 1):
        """Returns boolean if self.pos + length < working string length."""
        return self.pos + length-1 < self.length

    @cy.ccall
    @cy.locals(length = cy.int)
    def eat_length(self, length):
        """Move current position by length and set eos if not has_space()."""

        self.col += length
        self.pos += length

        if not self.has_space():  # Set eos if there is no more space left.
            self.eos = 1

    @cy.ccall
    @cy.locals(string = str, length = cy.int)
    def eat_string(self, string):
        """Move current position by length of string and count lines by \n."""
        if string == '\n':  # Handle single newline.
            self.col = -1
            self.row += 1
            self.eat_length(1)
        elif '\n' in string:  # Handle string containing a newline.
            char = cy.declare(str)
            for char in string:  # Recursively call eat to handle each char.
                self.eat_string(char)
        else:
            length = len(string)
            self.eat_length(length)  # Any other string just eat the length.

    @cy.ccall
    @cy.returns(str)
    def get_char(self):
        """Return the current character in the working string."""
        if not self.has_space():
            return ''

        return self.string[self.pos]

    @cy.ccall
    @cy.locals(length = cy.int, trim = cy.int, pos = cy.int, distance = cy.int)
    @cy.returns(str)
    def get_length(self, length, trim = 0):
        """Return string at current position + length.
        If trim == true then get as much as possible before eos"""
        if not self.has_space():
            return ''

        pos = self.pos
        distance = pos + length
        if not trim and not self.has_space(length):
            return ''
        return self.string[pos:distance]

    @cy.ccall
    @cy.locals(pos = cy.int)
    @cy.returns(str)
    def get_string(self):
        """Return non space chars from current position until a whitespace."""
        if not self.has_space():
            return ''

        pos = self.pos
        string = self.string
        # Get a char for each char in the current string from pos onward
        #  solong as the char is not whitespace.
        # The following is not yet supported with cython 0.18.0
        #from itertools import takewhile
        #chars = (y for y in takewhile(lambda x: not x.isspace(), string[pos:]))
        chars = []
        for char in string[pos:]:
            if char.isspace():
                break
            else:
                chars.append(char)
        return ''.join(chars)

    def generator(self, offset = 0):
        """A generator for the current position to the end, pure python."""
        for char in self.string[self.pos + offset:]:
            yield char

    @cy.ccall
    @cy.locals(offset = cy.int)
    @cy.returns(str)
    def rest_of_string(self, offset = 0):
        """A copy of the current position till the end of the string."""
        return self.string[self.pos + offset:]

    @cy.ccall
    @cy.locals(output = list, pos = cy.int, end = cy.int, string = str)
    @cy.returns(str)
    def get_line(self):
        """Return the entirety of the current line."""
        pos = self.pos - self.col
        string = self.string
        end = self.length

        output = []
        while string[pos] != '\n':
            output.append(string[pos])
            pos += 1
            if pos == end:
                break

        return ''.join(output)

    @cy.ccall
    @cy.locals(past = cy.int, future = cy.int,
        string = str, pos = cy.int, lines = cy.int, linesback = cy.int,
        output = list, end = cy.int)
    @cy.returns(str)
    def get_surrounding_lines(self, past = 1, future = 1):
        """Return the current line and x,y previous and future lines."""
        string = self.string
        pos = self.pos - self.col
        end = self.length

        linesback = 0
        while linesback > -past:
            if pos <= 0:
                break
            elif string[pos - 2] == '\n':
                linesback -= 1
            pos -= 1

        output = []
        lines = future + 1
        while linesback < lines:
            if pos >= end:
                output.append(string[pos - 1])
                break
            elif string[pos] == '\n':
                linesback += 1
            output.append(string[pos])
            pos += 1

        return ''.join(output[:-1])