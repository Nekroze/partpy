__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'

cimport cython as cy


cdef class SourceString(object):
    cdef public str string
    cdef public long length, pos, row
    cdef public int col, eos

    cpdef load_file(self, str filename)

    cpdef set_string(self, str string)

    cpdef add_string(self, str string)

    cpdef reset_position(self)

    cpdef int has_space(self, int length = *)

    @cy.locals(pos = cy.long, col = cy.int, row = cy.long, char = str)
    cpdef eat_length(self, int length)

    @cy.locals(pos = cy.long, col = cy.int, row = cy.long, char = str)
    cpdef eat_string(self, str string)

    cpdef eat_line(self)

    cpdef str get_char(self)

    cpdef str get_length(self, int length, int trim = *)

    @cy.locals(chars = list, char = str)
    cpdef str get_string(self)

    cpdef str rest_of_string(self, int offset = *)

    @cy.locals(line = cy.long, output = list, char = str)
    cpdef SourceLine get_line(self, long lineno)

    @cy.locals(pos = cy.int, string = str, end = cy.long, output = list)
    cpdef SourceLine get_current_line(self)

    @cy.locals(linestring = list, linestrings = list, output = list, char = str,
        line = cy.long)
    cpdef list get_lines(self, first, last)

    @cy.locals(string = str, pos = cy.long, end = cy.long, row = cy.int,
        linesback = cy.int, output = list, linestring = list, lines = cy.int)
    cpdef list get_surrounding_lines(self, int past = *, int future = *)

    @cy.locals(output = list, line = list, lineno = cy.long, char = str)
    cpdef list get_all_lines(self)

    cpdef int match_string(self, str string, int word = *)

    @cy.locals(length = cy.int, currentlength = cy.int, current = str,
    string = str)
    cpdef str match_any_string(self, list strings, int word = *)

    @cy.locals(current = str)
    cpdef str match_any_char(self, str chars)

    @cy.locals(pattern = str, output = list, firstchar = str, char = str)
    cpdef str match_pattern(self, first, str rest = ?, int least = *)

    @cy.locals(output = list, firstchar = str, char = str)
    cpdef str match_function(self, first, rest = ?, int least = *)

    @cy.locals(indents = cy.int, spaces = cy.int, char = str)
    cpdef int count_indents(self, int spacecount, int tabs = *)

    @cy.locals(indents = cy.int, spaces = cy.int, charlen = cy.int, char = str)
    cpdef tuple count_indents_length(self, int spacecount, int tabs = *)

    @cy.locals(lines = list, line = SourceLine)
    cpdef count_indents_last_line(self, int spacecount, int tabs = *, int back = *)

    @cy.locals(lines = list, line = SourceLine)
    cpdef count_indents_length_last_line(self, int spacecount, int tabs = *,  int back = *)

    @cy.locals(char = str)
    cpdef skip_whitespace(self, int newlines = *)


cdef class SourceLine(SourceString):
    cdef public int lineno

    cpdef strip_trailing_ws(self)

    @cy.locals(char = str)
    cpdef str get_first_char(self)

    @cy.locals(char = str)
    cpdef str get_last_char(self)
