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

Tests related to loading documents.

"""

__docformat__ = 'restructuredtext en'
__version__ = '$Rev: 179 $'

from unittest import TestCase
from difflib import Differ

from owlsugar import Ontology
from owlsugar.validation import ValidationException
from owlsugar.exceptions import InvalidOwlParseException

from rdflib import Namespace


class LoadDocument(TestCase):
    """Tests related to loading documents."""
    #------------------------------------------------------------------ Fixture
    def setUp(self):
        """Create a working document."""
        self.work = Ontology()
        self.work.outputformat = 'n3'
        
    def tearDown(self):
        """Reset working document."""
        self.work = None

    #------------------------------------------------------- Success Test Cases
    def test_automatic_uriextractions(self):
        """Test if a locally loaded documents nsuri is set automatically.
        
        OWLSugar has the ability to extract a documents namespace automatically
        if you didn't explicitly define it when you tried to load it from a 
        local file. This will ensure this facility is working.
        
        """
        # List for the file to nsuri mappings.
        tests = [
            ('data/SystemConfiguration.owl',
                "http://www.organictechnology.net/ontologies"
                "/SystemConfiguration.owl#"),
            ('data/countries.owl',
                'http://www.bpiresearch.com/BPMO/2004/03/03/cdl/Countries#'),
            ('data/family.swrl.owl',
                'http://a.com/ontology#'),
            ('data/demoHierarchyVisualization.owl',
                'http://www.ea3888.univ-rennes1.fr/ontology/'
                'demoHierarchyVisualization.owl#'),
            ('data/foaf-index.owl',
                'http://xmlns.com/foaf/0.1/#'),
            ('http://usefulinc.com/ns/doap#',
                'http://usefulinc.com/ns/doap#')
            ]
        for uri, namespace in tests:
            self.work.load(uri)
            self.assertEqual(Namespace(namespace), self.work.nsuri,
                "When loading the file (%s) the URI we extracted from it is "
                "not what we expected.")

    def test_loading_n3(self):
        """Test to see if we can load an n3 document."""
        filepath = 'data/SystemConfiguration.n3'
        self.work.inputformat = 'n3'
        self.work.outputformat = 'n3'
        self.work.load(filepath)
        filestring = open(filepath).read(8192)
        ourstring = self.work.out()
        # The message will dump a diff so we can see any variance.
        self.assertEqual(filestring, ourstring + "\n", 
            "Input file (%s) and parsed output does not match.\n"
            "Diff output is:\n\n%s" % 
            (filepath, "\n".join(
                list(Differ().compare(filestring.split("\n"),
                    ourstring.split("\n")))
                )
            ))

    #------------------------------------------------------- Failure test cases

    def test_invalid_path(self):
        """Test invalid paths for loading. 
        
        This makes sure a ValidationException is raised that picks up that the
        path is not a valid file. It also tests to make sure the original file
        was not clobbered.
        
        """
        tests = [
            'src',         # Directory
            'asdfasdf',    # Invalid path
            'test',  # Soft link (on linux anyway)
            ]
        for i in tests:
            self.assertRaises(ValidationException, self.work.load, i)
            self.assertEqual(self.work.out(), """
@prefix owl: <http://www.w3.org/2002/07/owl#>.
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.

 <#> a owl:Ontology. """,
                 "Invalid path (%s) and ValidationException raised has "
                 "clobbered the original file contents." % i)

    def test_load_invalid_with_xml(self):
        """Test to see if we get an exception when attempting to load a file
        that has invalid contents.
        
        Also check to make sure the existing contents are not clobbered.
        
        """
        self.work.inputformat = 'xml'
        self.assertRaises(InvalidOwlParseException, self.work.load,
            "data/README.txt") 
        self.assertEqual(self.work.out(), """
@prefix owl: <http://www.w3.org/2002/07/owl#>.
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.

 <#> a owl:Ontology. """,
             "Invalid file contents and SAXParseException raised has "
             "clobbered the original file contents.")
        
    def test_load_owlxml_with_n3(self):
        """Try and load an OWL/XML document when we are using 'n3' as an input
        format.
        
        """
        filepath = 'data/SystemConfiguration.owl'
        self.work.inputformat = 'n3'
        self.assertRaises(InvalidOwlParseException, self.work.load, 
            filepath)
        self.assertEqual(self.work.out(), """
@prefix owl: <http://www.w3.org/2002/07/owl#>.
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.

 <#> a owl:Ontology. """,
             "Invalid file contents and SAXParseException raised has "
             "clobbered the original file contents.")
        
    def test_load_text_with_n3(self):
        """Try and load an OWL/XML document when we are using 'n3' as an input 
        format.
        
        """
        self.work.inputformat = 'n3'
        self.assertRaises(InvalidOwlParseException, self.work.load, 
            'data/README.txt')
        self.assertEqual(self.work.out(), """
@prefix owl: <http://www.w3.org/2002/07/owl#>.
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.

 <#> a owl:Ontology. """,
             "Invalid file contents and SAXParseException raised has "
             "clobbered the original file contents.")            
