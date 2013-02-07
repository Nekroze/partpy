"""Matcher utilizes SourceString to provide some simple string matching
functionality."""
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'

import cython as cy
from .sourcestring import SourceString


@cy.cclass
class Matcher(SourceString):
    """Subclass of SourceString and methods to assist
    with pattern/string matching against the SoruceString."""
    
    @cy.ccall
    @cy.locals(string = str, current = str, word = cy.int)
    @cy.returns(cy.int)
    def match_string(self, string, word = 0):
        """Returns 1 if string can be matches against SourceString's
        current position.
        
        If word is >= 1 then it will only match string followed by whitepsace"""
        if word:
            return self.get_string() == string
        return self.get_length(len(string)) == string
        
    @cy.ccall
    @cy.locals(strings = list, word = cy.int, 
               length = cy.int, currentlength = cy.int, current = str)
    @cy.returns(str)
    def match_any_string(self, strings, word = 0):
        """Attempts to match each string in strings in order of length.
        Will return the string that matches or an empty string if no match.
        Sorts strings list by string length, consider immutability.
        
        Will only match if string is followed by a whitespace."""
        current = ''
        if word:
            current = self.get_string()
            return current if self.get_string() in strings else ''
        
        sorted(strings, key = len)
        
        currentlength = 0
        length = 0
        for string in strings:
            length = len(string)
            if length != currentlength:
                current = self.get_length(length)
            if string == current:
                return string
        return ''
        
    @cy.ccall
    @cy.locals(chars = str, current = str)
    @cy.returns(str)
    def match_any_char(self, chars):
        """Match and return the current SourceString char if its in chars."""
        current = self.get_char()
        return current if current in chars else ''
        
    @cy.ccall
    @cy.locals(first = str, rest = str, 
               pattern = str, output = list, offset = cy.int, firstchar = str)
    @cy.returns(str)
    def match_pattern(self, first, rest = None):
        """Match each char sequentially from current SourceString position 
        until the pattern doesnt match and return all maches.
        
        First may be a list or tuple that will get unpacked to first, rest.
        
        If rest is defined then first is used only to match the first arg
        and the rest of the chars are matched against rest."""
        ftype = type(first)
        if rest is None and ftype is tuple or ftype is list:
            first, rest = first
            
        firstchar = self.get_char()
        if not firstchar in first:
            return ''
            
        output = [firstchar]
        offset = 1
        pattern = first if rest is None else rest
        
        for char in self.string[self.pos +offset:]:
            if char in pattern:
                output.append(char)
            else:
                break
        return ''.join(output)
        
    @cy.ccall
    @cy.locals(output = list, offset = cy.int, firstchar = str)
    @cy.returns(str)
    def match_function(self, first, rest = None):
        """Match each char sequentially from current SourceString position 
        until the pattern doesnt match and return all maches.
        
        First may be a list or tuple that will get unpacked to first, rest.
        
        This version takes functions instead of string patterns.
        Each function must take one argument, a string, and return a
        value that can be evauluated as True or False.
        
        If rest is defined then first is used only to match the first arg
        and the rest of the chars are matched against rest."""
        ftype = type(first)
        if rest is None and ftype is tuple or ftype is list:
            first, rest = first
            
        firstchar = self.get_char()
        if not first(firstchar):
            return ''
            
        output = [firstchar]
        offset = 1
        pattern = first if rest is None else rest
        
        for char in self.string[self.pos +offset:]:
            if pattern(char):
                output.append(char)
            else:
                break
        return ''.join(output)
