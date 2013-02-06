"""Matcher utilizes SourceString to provide some simple string matching
functionality."""
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'

import cython as cy
from .sourcestring import SourceString


@cy.cclass
class Matcher(object):
    source = cy.declare(SourceString)
    
    def __init__(self, source = None):
        if isinstance(source, SourceString):
            self.set_source(source)
        elif isinstance(source, str):
            self.new_source(source)
    
    @cy.ccall
    @cy.returns(SourceString)
    def get_source(self):
        return self.source
    
    @cy.ccall
    @cy.locals(string = str)
    def new_source(self, string):
        self.source = SourceString()
        self.source.set_string(string)
    
    @cy.ccall
    @cy.locals(source = SourceString)
    def set_source(self, source):
        self.source = source
        
    @cy.ccall
    @cy.locals(string = str, current = str, word = cy.int)
    @cy.returns(cy.int)
    def match_string(self, string, word = 0):
        current = ''
        if word:
            current = self.source.get_string()
        else:
            current = self.source.get_length(len(string))
        return current == string
        
    @cy.ccall
    @cy.locals(strings = list, current = str, word = cy.int)
    @cy.returns(str)
    def match_any_string(self, strings, word = 0):
        for string in strings:
            if self.match_string(string, word):
                return string
        return ''
        
    @cy.ccall
    @cy.locals(chars = str)
    @cy.returns(str)
    def match_any_char(self, chars):
        for char in chars:
            if self.match_string(char):
                return char
        return ''
