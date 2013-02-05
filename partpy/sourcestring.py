"""SourceString stores the entire string to be parsed in memory and provides
some simple methods for retrieving and moving current position."""

from itertools import takewhile


class SourceString(object):
    """Stores the parse string and its length followed by current position
    in the string and if the end of the string has been reached.

    It also stores the current row and column position as manually counted.
    """
    string = ''
    length = 0
    eos = False
    pos = 0
    col = 0
    row = 0

    def load_file(self, filename):
        """Read in file contents and set the current string."""
        return self.set_string(open(filename, 'r').read())

    def set_string(self, string):
        """Set the working string and its length then reset positions."""
        self.string = string
        self.length = len(string)
        self.reset_position()
        return self

    def add_string(self, string):
        """Add to the working string and its length and reset eos."""
        self.string += string
        self.length += len(string)
        self.eos = False

    def reset_position(self):
        """Reset all current positions."""
        self.pos = 0
        self.col = 0
        self.row = 0
        self.eos = False

    def has_space(self, length = 1):
        """Returns boolean if self.pos + length < working string length."""
        return self.pos + length-1 < self.length

    def eat_length(self, length):
        """Move current position by length and set eos if not has_space()."""
        self.col += length
        self.pos += length

        if not self.has_space():  # Set eos if there is no more space left.
            self.eos = True

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

    def get_length(self, length, trim = False):
        """Return string at current position + length."""
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
        gen = (y for y in takewhile(lambda x: not x.isspace(), string[pos:]))
        return ''.join(gen)
