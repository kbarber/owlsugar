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

Tests on Individuals.

"""

__docformat__ = 'restructuredtext en'
__version__ = '$Rev: 179 $'

from unittest import TestCase

from rdflib import Literal

from owlsugar import Ontology
from owlsugar.exceptions import *


class IndividualCreation(TestCase):
    """These tests are designed to test the creation of individuals in a 
    document.
    
    """
    
    #------------------------------------------------------------------ Fixture
    def setUp(self):
        """Create a working document and a document for import.
        
        Load a sample schema and import it.

        """
        self.work = Ontology()
        self.work.outputformat = 'n3'
        self.work.imp(uri="data/SystemConfiguration.owl", prefix="sc")

    def tearDown(self):
        """Reset working document."""
        self.work = None

    #------------------------------------------------------- Success test cases
    def test_add_individual(self):
        """Add a new individual once and ensure the result matches what we 
        expect.
        
        """
        self.work.ind.new(rdfid="asdf", cls=self.work.cls.get(rdfid="Host"))
        # Note - there is a space at the end of the "owl:imports" line.
        self.assertEqual(self.work.out(), """
@prefix : <#>.
@prefix owl: <http://www.w3.org/2002/07/owl#>.
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.
@prefix sc: <http://www.organictechnology.net/ontologies/SystemConfiguration.owl#>.

 <#> a owl:Ontology;
     owl:imports <http://www.organictechnology.net/ontologies/SystemConfiguration.owl>. 

 :asdf a sc:Host. """)

    #------------------------------------------------------- Failure test cases
    def test_add_same_ind_twice(self):
        """Add the same individual multiple times and see if the document is 
        still correct.
        
        We should see a DuplicateIdException.
        
        """
        self.work.ind.new(rdfid="asdf", cls=self.work.cls.get(rdfid="Host"))
        self.assertRaises(DuplicateIdException, self.work.ind.new, 
            rdfid="asdf", cls=self.work.cls.get(rdfid="Host"))
        self.assertEqual(self.work.out(), """
@prefix : <#>.
@prefix owl: <http://www.w3.org/2002/07/owl#>.
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.
@prefix sc: <http://www.organictechnology.net/ontologies/SystemConfiguration.owl#>.

 <#> a owl:Ontology;
     owl:imports <http://www.organictechnology.net/ontologies/SystemConfiguration.owl>. 

 :asdf a sc:Host. """)


class IndividualSlotManipulation(TestCase):
    """These tests are designed to test changes for Individuals on a slot 
    level.
    
    """
    
    #------------------------------------------------------------------ Fixture
    def setUp(self):
        """Creating a working and import document.
        
        Load and import a sample schema, and initialise some individuals.

        """
        self.work = Ontology()
        self.work.outputformat = 'n3'
        self.work.imp(uri="data/SystemConfiguration.owl", prefix="sc")
        
        self.host = self.work.ind.new(rdfid="myhost", 
            cls=self.work.cls.get(rdfid="Host"))
        
        self.kernel = self.work.ind.new(rdfid="Linux-2-6-22-9-91-fc7", 
            cls=self.work.cls.get(rdfid="Kernel"))
        
        self.cpuarch = self.work.ind.new(rdfid="i686", 
            cls=self.work.cls.get(rdfid="CpuArch"))

    def tearDown(self):
        """Reset working and import documents and their individuals."""
        self.host = None
        self.kernel = None
        self.cpuarch = None
        self.work = None

    #------------------------------------------------------- Success test cases
    def test_set_slot(self):
        """Set a whole bunch of slots and test to see if the output is what we 
        expect.
        
        """
        self.cpuarch.set(self.work.prop.get('cpuarchName'), Literal("i686"))
        self.kernel.set(self.work.prop.get('kernelAbbrev'), Literal("Linux"))
        self.kernel.set(self.work.prop.get('kernelVersion'), 
            Literal("2.6.22.9-91.fc7"))
        self.kernel.set(self.work.prop.get('hasCpuArch'), self.cpuarch.nsuri)
        self.host.set(self.work.prop.get('hostName'), Literal("myhost"))
        self.host.set(self.work.prop.get('hasKernel'), self.kernel.nsuri)
        self.assertEqual(self.work.out(), """
@prefix : <#>.
@prefix owl: <http://www.w3.org/2002/07/owl#>.
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.
@prefix sc: <http://www.organictechnology.net/ontologies/SystemConfiguration.owl#>.

 <#> a owl:Ontology;
     owl:imports <http://www.organictechnology.net/ontologies/SystemConfiguration.owl#>. 

 :myhost a sc:Host;
     sc:hasKernel :Linux-2-6-22-9-91-fc7;
     sc:hostName "myhost". 

 :Linux-2-6-22-9-91-fc7 a sc:Kernel;
     sc:hasCpuArch :i686;
     sc:kernelAbbrev "Linux";
     sc:kernelVersion "2.6.22.9-91.fc7". 

 :i686 a sc:CpuArch;
     sc:cpuarchName "i686". """)

    #------------------------------------------------------- Failure test cases
    def test_set_inv_prop_slot(self):
        """Attempt to set a slot for a property which doesn't belong to the 
        class in which the slot's individual belongs.
        
        """
        self.assertRaises(SchemaException, self.cpuarch.set, 
            self.work.prop.get('kernelAbbrev'), Literal("Linux"))

    def test_set_inv_prop_slot_union(self):
        """Attempt to set a slot for a property which doesn't belong to the 
        class in which the slot's individual belongs. 
        
        Specifically, test a property that uses unionOf for its domain setting.
        
        """
        self.assertRaises(SchemaException, self.cpuarch.set, 
            self.work.prop.get('hasKernel'), self.kernel.nsuri)
