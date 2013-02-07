"""Predefined function patterns for use in Matcher.match_function methods."""
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'

import cython as cy

alphal = str.islower
alphau = str.isupper
alpha = str.isalpha

number = str.isdigit
alnum = str.isalnum

@cy.ccall
@cy.returns(cy.int)
@cy.locals(char = str)
def _identifier_first(char):
    return alpha(char) or char == '_'

identifier = (_identifier_first, alnum)

@cy.ccall
@cy.returns(cy.int)
@cy.locals(char = str)
def _qualified_rest(char):
    return alpha(char) or char == '.'

qualified = (_identifier_first, _qualified_rest)

@cy.ccall
@cy.returns(cy.int)
@cy.locals(char = str)
def _integer_first(char):
    return number(char) or char == '-'

integer = (_integer_first, number)
