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

:Version: $Rev: 179 $

A number of tests to test the SchemaWeb functionality. Must have web access
for these tests to work in most cases.

:see: `Schema Web <http://www.schemaweb.info/>`__

"""

__docformat__ = 'restructuredtext en'
__version__ = '$Rev: 179 $'

from unittest import TestCase

from owlsugar.schemaweb import schemalocation
from owlsugar import Ontology


class SchemaLocation(TestCase):
    """These tests are designed to test the public URI to real schema location 
    resolution facility provided by our wrapper around the SchemaWeb REST web
    services.
    
    """
    
    #------------------------------------------------------- Success Test Cases
    def test_schemalocation(self):
        """Test using schemalocation to resolve public namespace ID's to real
        URI locations.
        
        """
        tests = [
            ('http://www.w3.org/2000/01/rdf-schema#', 
                'http://www.w3.org/TR/rdf-schema/rdfs-namespace.xml'),
            ('http://www.w3.org/2002/07/owl#', 
                'http://www.w3.org/2002/07/owl.rdf'),
            ('http://xmlns.com/foaf/0.1/', 
                'http://xmlns.com/foaf/0.1/index.rdf'),
            ('http://xmlns.com/wot/0.1/', 
                'http://xmlns.com/wot/0.1/index.rdf'),
            ]
        for pub, real in tests:
            self.assertEqual(schemalocation(pub), real)

    #------------------------------------------------------- Failure Test Cases
    def test_unknown_schemalocation(self):
        """This test case will attempt to retreive a URL that is known not to 
        exist in SchemaWeb. 
        
        The expected result should be the original submission indicating that
        we should just try the public ID.
        
        """
        tests = [
            'http://iambogus.com/rdf/',
            'http://totallybogus.info/rdf/',
            'http://iamabogusurl.org/rdf/#',
            ]
        for test in tests:
            self.assertEqual(schemalocation(test), test)


class PublicUriLoad(TestCase):
    """Test using a known mismatched public URI/real location mapping with the
    Document load function.
    
    """
    
    #------------------------------------------------------------------ Fixture
    def setUp(self):
        """Creating a working document."""
        self.work = Ontology()
        self.work.outputformat = 'n3'

    def tearDown(self):
        """Reset a working document."""
        self.work = None

    #------------------------------------------------------- Success test cases
    def test_foaf(self):
        """Test loading the FOAF public id into a document."""
        self.work.load("http://xmlns.com/foaf/0.1/")
        pubcls = self.work.cls.get("Public")
        self.assertEqual(str(pubcls.nsuri), 
            "http://xmlns.com/foaf/0.1/#Public")