"""
:Copyright: |copy| 2007 by Adrian Hare and Kenneth Barber. All rights reserved.

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

:Version: $Rev: 174 $

This is a utility module designed to allow us to make namespace resolution
queries against the SchemaWeb REST web services.

:see: `Schema Web <http://www.schemaweb.info/>`__

"""

__docformat__ = 'restructuredtext en'
__version__ = '$Rev: 174 $'

from xml.sax import make_parser
from xml.sax.handler import ContentHandler

from owlsugar.exceptions import SchemaWebException


SWBASE = "http://www.schemaweb.info/webservices/rest/"


def schemalocation(nsuri):
    """This static function will perform a REST query against SchemaWeb to find
    the proper location of an Ontology based on its public namespace URI.
    
    """
    resturl = SWBASE + "GetSchemaLocation.aspx?namespace="
    parser = make_parser()
    handler = SwResponseHandler()
    parser.setContentHandler(handler)
    try:
        parser.parse(resturl + "%s" % nsuri)
        return handler.location
    except SchemaWebException:
        return nsuri

    
class SwResponseHandler(ContentHandler):
    """Parses SchemWeb REST services return messages for locations, raising an 
    exception if the URL does not exist in SchemaWeb.
    
    """
    def __init__(self):
        """Initialise variables to prepare FSM."""
        self._islocation = False
        self.location = None

    def startElement(self, name, attr):
        """Find a location or error XML element.
        
        This either prepares the handler to deal with a location response or
        returns an exception if the element is an error element.
        
        """
        if name == 'location':
            self._islocation = True
        elif name == 'error':
            raise SchemaWebException("SchemaWeb has returned an error "
                "retreiving the schema you have specified.")
        else:
            self._islocation = False

    def characters(self, char):
        """Load all characters located in the location element into the 
        location attribute.
        
        """
        if self._islocation:
            self.location = char