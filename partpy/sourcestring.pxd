"""SourceString stores the entire string to be parsed in memory and provides
some simple methods for retrieving and moving current position."""
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

    @cy.locals(length = cy.int)
    cpdef eat_string(self, str string)

    cpdef str get_char(self)

    @cy.locals(pos = cy.long, distance = cy.int)
    cpdef str get_length(self, int length, int trim = *)

    @cy.locals(pos = cy.long, string = str, chars = list)
    cpdef str get_string(self)

    cpdef str rest_of_string(self, int offset = *)

    @cy.locals(line = cy.long, output = list)
    cpdef SourceLine get_line(self, long lineno)

    @cy.locals(line = cy.long, linestring = list, linestrings = list)
    cpdef list get_lines(self, long first, long last)

    @cy.locals(pos = cy.int, string = str, end = cy.long, output = list)
    cpdef SourceLine get_current_line(self)

    @cy.locals(output = list, string = str, linestring = list, row = cy.int,
        end = cy.long, pos = cy.long, lines = cy.int, linesback = cy.int)
    cpdef list get_surrounding_lines(self, int past = *, int future = *)


cdef class SourceLine(SourceString):
    cdef public int lineno

    cpdef strip_trailing_ws(self)

    cpdef str get_first_char(self)

    cpdef str get_last_char(self)
