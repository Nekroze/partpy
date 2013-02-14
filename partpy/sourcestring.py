"""SourceString stores the entire string to be parsed in memory and provides
some simple methods for retrieving and moving current position."""
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'


class SourceString(object):
    """Stores the parse string and its length followed by current position
    in the string and if the end of the string has been reached.

    It also stores the current row and column position as manually counted.
    """
    def __init__(self, string = None):
        self.string = ''
        if string is not None:
            self.set_string(string)
        self.length = 0
        self.pos = 0
        self.col = 0
        self.row = 0
        self.eos = 0

    def load_file(self, filename):
        """Read in file contents and set the current string."""
        with open(filename, 'r') as sourcefile:
            self.set_string(sourcefile.read())

    def set_string(self, string):
        """Set the working string and its length then reset positions."""
        self.string = string
        self.length = len(string)
        self.reset_position()

    def add_string(self, string):
        """Add to the working string and its length and reset eos."""
        self.string += string
        self.length += len(string)
        self.eos = 0

    def reset_position(self):
        """Reset all current positions."""
        self.pos = 0
        self.col = 0
        self.row = 0
        self.eos = 0

    def has_space(self, length = 1):
        """Returns boolean if self.pos + length < working string length."""
        return self.pos + length-1 < self.length

    def eat_length(self, length):
        """Move current position by length and set eos if not has_space()."""

        self.col += length
        self.pos += length

        if not self.has_space():  # Set eos if there is no more space left.
            self.eos = 1

    def eat_string(self, string):
        """Move current position by length of string and count lines by \n."""
        if string == '\n':  # Handle single newline.
            self.col = -1
            self.row += 1
            self.eat_length(1)
        elif '\n' in string:  # Handle string containing a newline.
            for char in string:  # Recursively call eat to handle each char.
                self.eat_string(char)
        else:
            length = len(string)
            self.eat_length(length)  # Any other string just eat the length.

    def get_char(self):
        """Return the current character in the working string."""
        if not self.has_space():
            return ''

        return self.string[self.pos]

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

    def rest_of_string(self, offset = 0):
        """A copy of the current position till the end of the string."""
        return self.string[self.pos + offset:]

    def get_current_line(self):
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

        return SourceLine(''.join(output), self.row)

    def get_surrounding_lines(self, past = 1, future = 1):
        """Return the current line and x,y previous and future lines."""
        string = self.string
        pos = self.pos - self.col
        end = self.length
        row = self.row

        linesback = 0
        while linesback > -past:
            if pos <= 0:
                break
            elif string[pos - 2] == '\n':
                linesback -= 1
            pos -= 1

        output = []
        linestring = []
        lines = future + 1
        while linesback < lines:
            if pos >= end:
                linestring.append(string[pos - 1])
                output.append(
                    SourceLine(''.join(linestring[:-1]), row + linesback))
                break
            elif string[pos] == '\n':
                linestring.append(string[pos])
                pos += 1
                output.append(
                    SourceLine(''.join(linestring), row + linesback))
                linesback += 1
                linestring = []
            linestring.append(string[pos])
            pos += 1

        return output

    def __repr__(self):
        return self.string


class SourceLine(SourceString):
    """Contains an entire line of a source with handy line specific methods."""

    def __init__(self, string, lineno):
        super(SourceLine, self).__init__(string)
        self.lineno = lineno

    def strip_trailing_ws(self):
        """Remove trailing whitespace from internal string."""
        self.string = self.string.rstrip()

    def get_first_char(self):
        """Return the first non-whitespace character of the line."""
        for char in self.string:
            if not char.isspace():
                return char

    def get_last_char(self):
        """Return the last non-whitespace character of the line."""
        for char in reversed(self.string):
            if not char.isspace():
                return char

    def __str__(self):
        """Return a string of this line including linenumber."""
        lineno = self.lineno
        padding = 0
        if lineno < 1000:
            padding = 1
        if lineno < 100:
            padding = 2
        if lineno < 10:
            padding = 3

        return str(lineno) + (' ' * padding) + '|' + self.string
