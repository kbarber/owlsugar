"""
:Copyright: |copy| 2008 by Adrian Hare and Kenneth Barber.

.. |copy| unicode:: 0xA9 .. copyright sign

:license: 
    This file is part of OWLSugar.

    OWLSugar is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    OWLSugar is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

:Version: $Rev$

"""

__docformat__ = 'restructuredtext en'
__version__ = '$Rev$'


# TODO: This entire code needs a rework - I don't think we are using it yet.

class NS:
    """A short-cut to allow us to (using python ways) define namespace URI's 
    and URI's for elements.
    
    """
    # TODO: Can we get this handling curries? That is ns:Blah style convetions?
    # TODO: Perhaps consider testing elements on the RHS of the URI? Not sure
    #        if this will work dynamically. Perhaps a way to pass a set of 
    #        acceptable elements?
    # TODO: Should be returning IRI's (see RFC 3987) instead of URI's as this 
    #        is now the "fully-qualified" format used in OWL 1.1. IRI's are 
    #        more or less more unicode friendly, and have angle-brackets around
    #        them.
    
    def __init__(self, ns):
        self.ns = ns
    
    def __getattr__(self, attr):
        """Returns a combined URI plus element in the NCName format.
        
        """
        return self.ns + attr
    
    def __repr__(self):
        return "blah"

# The common namespaces
rdf = NS("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = NS("http://www.w3.org/2000/01/rdf-schema#")
owl = NS("http://www.w3.org/2002/07/owl#")
owl11 = NS("http://www.w3.org/2006/12/owl11#")
owl11xml = NS("http://www.w3.org/2006/12/owl11-xml#")