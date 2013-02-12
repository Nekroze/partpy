"""Custom exception for classes inheriting SourceString."""
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'


class PartpyError(Exception):

    def __init__(self, obj, msg = None):
        self.partpyMsg = msg
        self.partpyObj = obj

    def __str__(self):
        output = []
        splitlines = self.partpyObj.get_lines(1, 0).split('\n')
        start = self.partpyObj.row - len(splitlines) + 1
        for line in splitlines:
            padding = 0
            if start < 1000:
                padding = 1
            if start < 100:
                padding = 2
            if start < 10:
                padding = 3
            output.append(str(start) + (' ' * padding) + '|' + line)
            start += 1

        output.append(' ' * (self.partpyObj.col - 1) + '^')
        if self.partpyMsg:
            output.append(self.partpyMsg)

        return '\n'.join(output)
