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
        if source is not None:
            self.set_source(source)
        
    @cy.ccall
    @cy.locals(source = SourceString)
    def set_source(self, source):
        self.source = source
