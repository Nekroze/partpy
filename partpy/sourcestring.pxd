__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'

import cython as cy


cdef class SourceString(object):
    cdef public str string
    cdef public long length, pos, row
    cdef public int col, eos

    cpdef load_file(self, str filename)

    cpdef set_string(self, str string)

    cpdef add_string(self, str string)

    cpdef reset_position(self)

    cpdef int has_space(self, int length = *)

    cpdef eat_length(self, int length)

    cpdef eat_string(self, str string)

    cpdef str get_char(self)

    cpdef str get_length(self, int length, int trim = *)

    @cy.locals(chars = list)
    cpdef str get_string(self)

    cpdef str rest_of_string(self, int offset = *)

    @cy.locals(line = cy.long, output = list)
    cpdef SourceLine get_line(self, long lineno)

    @cy.locals(linestring = list, linestrings = list, output = list)
    cpdef list get_lines(self, first, last)

    @cy.locals(pos = cy.int, string = str, end = cy.long, output = list)
    cpdef SourceLine get_current_line(self)

    @cy.locals(output = list, string = str, linestring = list, row = cy.int,
        end = cy.long, pos = cy.long, lines = cy.int, linesback = cy.int)
    cpdef list get_surrounding_lines(self, int past = *, int future = *)

    cpdef int match_string(self, str string, int word = *)

    @cy.locals(length = cy.int, currentlength = cy.int, current = str)
    cpdef str match_any_string(self, strings, int word = *)

    @cy.locals(current = str)
    cpdef str match_any_char(self, str chars)

    @cy.locals(pattern = str, output = list, firstchar = str)
    cpdef str match_pattern(self, first, str rest = ?)

    @cy.locals(output = list, firstchar = str)
    cpdef str match_function(self, first, rest = ?)

    @cy.locals(indents = cy.int, spaces = cy.int)
    cpdef int count_indents(self, int spacecount, int tabs = *)

    @cy.locals(indents = cy.int, spaces = cy.int, charlen = cy.int)
    cpdef tuple count_indents_length(self, int spacecount, int tabs = *)


cdef class SourceLine(SourceString):
    cdef public int lineno

    cpdef strip_trailing_ws(self)

    cpdef str get_first_char(self)

    cpdef str get_last_char(self)
