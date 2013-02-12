"""SourceString stores the entire string to be parsed in memory and provides
some simple methods for retrieving and moving current position."""
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'

import cython as cy


cdef class SourceString(object):
    cdef public str string
    cdef public long length, pos, row
    cdef public int col, eos

    cpdef int end(self)

    cpdef long line(self)

    cpdef int column(self)

    cpdef long position(self)

    cpdef str base_string(self)

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

    @cy.locals(output = list, string = str,
        end = cy.long, pos = cy.long, lines = cy.int, linesback = cy.int)
    cpdef str get_surrounding_lines(self, int past = *, int future = *)
