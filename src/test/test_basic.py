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

Basic tests.

"""

__docformat__ = 'restructuredtext en'
__version__ = '$Rev: 179 $'

from unittest import TestCase

from owlsugar import Ontology
from owlsugar.validation import ValidationException


class DataDocumentCreation(TestCase):
    """These tests are related to basic document creation.
    
    This will test importing other schema documents and creation of individuals
    in a blank document.
    
    See methods in this class for details.
    
    """
    
    #------------------------------------------------------------------ Fixture
    def setUp(self):
        """Create a working document and a document to use for import."""
        self.work = Ontology()
        self.work.outputformat = 'n3'

    def tearDown(self):
        """Reset working document and import document."""
        self.work = None

    #------------------------------------------------------- Success test cases
    def test_blankdocument_output(self):
        """Test just the basic creation of a blank document. 
        
        Compares with expected n3 output.
        
        """
        self.assertEqual(self.work.out(), """
@prefix owl: <http://www.w3.org/2002/07/owl#>.
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.

 <#> a owl:Ontology. """, 
            "Blank document n3 output does not look like we expect it to.")


class OutputDocument(TestCase):
    """Tests related to outputting documents."""
    
    #------------------------------------------------------------------ Fixture
    def setUp(self):
        """Create a working document."""
        self.work = Ontology()
        self.work.outputformat = 'n3'
        
    def tearDown(self):
        """Reset working document."""
        self.work = None    

    #------------------------------------------------------- Success Test Cases
    def test_out_versus_str(self):
        """Test to make sure the __str__ output is the same as the class.out()
        output.
        
        """
        self.assertEqual(str(self.work), self.work.out(),
            "The output we got from __str__ is not the same as the output "
            "from the out() function.")
    
    #------------------------------------------------------- Failure test cases
    def test_invalid_outputformat(self):
        """Test to make sure we pick up on invalid output formats."""
        
        def setout(fmt):
            """Wrapper around property. Not sure of a nicer way to do this."""
            self.work.outputformat = fmt
        
        self.assertRaises(ValidationException, setout, 'asdf')