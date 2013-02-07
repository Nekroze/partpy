"""Matcher utilizes SourceString to provide some simple string matching
functionality."""
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'

from partpy import Matcher
from partpy import fpattern as fpat
from partpy import spattern as spat

EXAMPLE = '''
Taylor Nekroze Lawson - nekroze@eturnilnetwork.com
Some Random:randomkid@randomail.net
'''
EXPECTED = {'Taylor Nekroze Lawson': 'nekroze@eturnilnetwork.com',
                  'Some Random': 'randomkid@randomail.net'}

class ContactsParser(Matcher):
    
    def parse(self):
        contacts = []
        while not self.end():
            contact = self.parse_contact()
            if not contact:
                break
            contacts.append(contact)
            self.parse_whitespace()
        return dict((key, value) for (key, value) in contacts)
        
    def parse_contact(self):
        self.parse_whitespace()
        name = self.parse_name()
        if not name:
            raise Exception('Expecting a name')
        
        self.parse_whitespace()
        if not self.match_any_char(':-'):
            raise Exception('Expecting : or -, found: ' + self.get_char())
        self.eat_length(1)
        self.parse_whitespace()
        
        email = self.parse_email()
        if not email:
            raise Exception('Expecting an email address')
        return (name, email)
        
    def parse_whitespace(self):
        while True:
            char = self.get_char()
            if not char.isspace():
                break
            else:
                self.eat_string(char)
        
    def parse_name(self):
        name = []
        while True:
            part = self.match_function(fpat.alphau, fpat.alphal)
            if part == '':
                break
            self.eat_string(part)
            name.append(part)
            if self.get_char() == ' ':
                self.eat_length(1)
        if not len(name):
            raise Exception('Expecting a title cased name')
        return ' '.join(name)
        
    def parse_email(self):
        email = []
        name = self.match_function(fpat.alphal)
        if not name:
            raise Exception('Expected a valid name')
        
        email.append(name)
        self.eat_string(name)
        
        nextchar = self.get_char()
        if not nextchar == '@':
            raise Exception('Expecting @, found: ' + nextchar)
            
        email.append(nextchar)
        self.eat_length(1)  # eat the @
        
        site = self.match_pattern(spat.alphal + '.')
        if not site:
            raise Exception('Expecting a site, found: ' + site)
            
        email.append(site)
        self.eat_string(site)
        return ''.join(email)
        
PARSER = ContactsParser().set_string(EXAMPLE)
