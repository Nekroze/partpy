"""Matcher utilizes SourceString to provide some simple string matching
functionality."""
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'

import cython as cy
from .sourcestring cimport SourceString


cdef class Matcher(SourceString):

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
