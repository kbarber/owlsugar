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

"""

__docformat__ = 'restructuredtext en'
__version__ = '$Rev: 179 $'

from unittest import TestCase

from owlsugar import Ontology
from owlsugar.exceptions import DuplicateImportException


class LocalImports(TestCase):
    """This will test importing other schema documents and creation of 
    individuals in a blank document.
    
    """
    
    #------------------------------------------------------------------ Fixture
    def setUp(self):
        """Creating working document and document for importing."""
        self.work = Ontology()
        self.work.outputformat = 'n3'

    def tearDown(self):
        """Reset working document and import document."""
        self.work = None

    #------------------------------------------------------- Success test cases

    def test_multiple_imports(self):
        """Import multiple schemas.
        
        Compares it with the expected n3 output.
        
        """
        self.work.imp(uri="http://xmlns.com/foaf/0.1/", prefix="foaf")
        self.work.imp(uri="http://purl.org/dc/elements/1.1/", prefix="dc")
        self.assertEqual(self.work.out(), """
@prefix owl: <http://www.w3.org/2002/07/owl#>.
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.

 <#> a owl:Ontology;
     owl:imports <http://purl.org/dc/elements/1.1/#>,
         <http://xmlns.com/foaf/0.1/#>. """)

    def test_single_import(self):
        """Using a blank document, import a schema from the local file system. 
        
        Compares it with the expected n3 output.
        
        """
        self.work.imp(uri="http://xmlns.com/foaf/0.1/", prefix="foaf")
        self.assertEqual(self.work.out(), """
@prefix owl: <http://www.w3.org/2002/07/owl#>.
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.

 <#> a owl:Ontology;
     owl:imports <http://xmlns.com/foaf/0.1/>. """)
        
    #------------------------------------------------------- Failure test cases
        
    def test_duplicate_import(self):
        """Using a blank document, import a schema from the local file system.
        
        Compares it with the expected n3 output.
        
        """
        self.work.imp(uri="http://xmlns.com/foaf/0.1/", prefix="foaf")
        self.assertRaises(DuplicateImportException, self.work.imp, 
            uri="http://xmlns.com/foaf/0.1/", prefix="sc")
        self.assertEqual(self.work.out(), """
@prefix owl: <http://www.w3.org/2002/07/owl#>.
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.

 <#> a owl:Ontology;
     owl:imports <http://xmlns.com/foaf/0.1/>. """)
