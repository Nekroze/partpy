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
        if word:
            return self.source.get_string() == string
        return self.source.get_length(len(string)) == string
        
    @cy.ccall
    @cy.locals(strings = list, word = cy.int, 
               length = cy.int, currentlength = cy.int, current = str)
    @cy.returns(str)
    def match_any_string(self, strings, word = 0):
        current = ''
        if word:
            current = self.source.get_string()
            return current if self.source.get_string() in strings else ''
        
        sorted(strings, key = len)
        
        currentlength = 0
        length = 0
        for string in strings:
            length = len(string)
            if length != currentlength:
                current = self.source.get_length(length)
            if string == current:
                return string
        return ''
        
    @cy.ccall
    @cy.locals(chars = str, current = str)
    @cy.returns(str)
    def match_any_char(self, chars):
        current = self.source.get_char()
        return current if current in chars else ''
        
    @cy.ccall
    @cy.locals(first = str, rest = str, 
               pattern = str, output = list, offset = cy.int, firstchar = str)
    @cy.returns(str)
    def match_pattern(self, first, rest = None):
        ftype = type(first)
        if rest is None and ftype is tuple or ftype is list:
            first, rest = first
            
        firstchar = self.source.get_char()
        if not firstchar in first:
            return ''
            
        output = [firstchar]
        offset = 1
        pattern = first if rest is None else rest
        
        for char in self.source.generator(offset):
            if char in pattern:
                output.append(char)
            else:
                break
        return ''.join(output)
        
    @cy.ccall
    @cy.locals(output = list, offset = cy.int, firstchar = str)
    @cy.returns(str)
    def match_function(self, first, rest = None):
        ftype = type(first)
        if rest is None and ftype is tuple or ftype is list:
            first, rest = first
            
        firstchar = self.source.get_char()
        if not first(firstchar):
            return ''
            
        output = [firstchar]
        offset = 1
        pattern = first if rest is None else rest
        
        for char in self.source.generator(offset):
            if pattern(char):
                output.append(char)
            else:
                break
        return ''.join(output)
