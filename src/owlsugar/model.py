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

Note:

This module requires python-lxml (redhat package) or equivalent. Plus the 
required C libraries such as libxml2.

"""

__docformat__ = 'restructuredtext en'
__version__ = '$Rev$'


from lxml import etree
          

class ModelConfig(object):
    """This object provides a raw read-only interface to accessing the internal 
    data model's configuration.
    
    This class provides a wrapper around the XML storage mechanism to provide
    a level of abstraction.
    
    The model configuration is in XML so simply instantiate this class using
    the filename of a valid ObjectModel XML file.

    """

    def __init__(self, filename, schema=None):
        """Open the model, and cache all of the configuration data.
        
        The model is accessed using the lxml libraries.
        
        Initialisation basically scoures through the XML populating our own
        internal cache, indexed for our own purposes.
        
        Once this is done, the XML configuration file is closed and all data
        is access from the cache.
        
        """
        # Initiate the XML side of things
        self._xml = etree.ElementTree(file=filename)
        
        # If a schema has been supplied - lets validate.
        if schema is not None:
            etree.XMLSchema(etree.parse(schema)).assertValid(self._xml)
        
        # Cache classes dictionary
        self._dict_classes = dict()
        for i in self._xml.findall(self._mdlns('class')):
            self._dict_classes[i.attrib['id']] = dict(i.attrib)

        # Cache associations dictionary
        self._dict_associations = dict()
        for cls in self.classes():
            associations = list() # Associations must be recorded in order
            for attr in self._find_class(cls).\
                findall(self._mdlns('association')):
                
                associations.append(dict(attr.attrib))
            self._dict_associations[cls] = associations

        # Cache references dictionary
        self._dict_references = dict()
        for cls in self.classes():
            self._dict_references[cls] = set()
        for cls in self.classes():
            for attr in self.associations(cls):
                try:
                    self._dict_references[
                        self.association_attr(cls, attr)['type']].add(cls)
                except KeyError:
                    self._dict_references[
                        self.association_attr(cls, attr)['type']] = set([cls])

        # Close the XML file (by removing references). It should not be 
        # required after initialisation.
        delattr(self, '_xml')

    #-------------------------------------------------------------- Basic Lists


    # The list-based classes retreive information from the cache for clean
    # presentation to API users.

    def classes(self):
        """List the classes as with list_classes, but reorder them to ensure
        that objects higher up in the inheritance chain come first.
        
            Returns: a list of classes ordered by inheritance, seniors first
            
        """
        orig_list = self._dict_classes.keys() #: Unordered list
        new_list = [] #: New ordered list

        # Keep iterating until the original list is empty
        iter_check = 0 #: Iteration check, to avoid infinite loops
        while(len(orig_list) > 0):
            # Check for infinite loops
            iter_check += 1
            if iter_check >= 20:
                raise Exception("This loops has iterated %s times. Possible "\
                    "infinite loop scenario." % iter_check)
            
            for i in orig_list:
                parents = self.class_parents(i)
                
                # If the item has no parents, or has parents already in the 
                # new list ... move the item to the new list. Otherwise, keep
                # looking.
                if ((len(parents) == 0) or 
                    (parents == [n for n in parents if n in new_list])):
                    
                    new_list.append(i)
                    orig_list.remove(i)

        return new_list
                
    def class_parents(self, classname):
        """List the parents of the class specified in order of seniority.
        
            classname: class to retrieve parents
            Returns: list of parent class names
            
        """
        conf = self.class_attr(classname)
        
        if conf.has_key('parentage'):
            parent_string = conf['parentage']
            parents = parent_string.split(' ')
            
            for i in parents:
                # Validate the parent
                if i not in self._dict_classes.keys():
                    raise Exception("Class %s has an invalid parent: %s" %
                        (classname, i))
            
                # Using recursion, add any other parents to the list
                parents.extend(self.class_parents(i))
            
            return parents
        else:
            return []

    def class_children(self, classname):
        """List the children of the class specified.
        
            classname: name of parent class
            Returns: list of children class names
            
        """
        # Iterate across all the classes, and see if the class in question
        # is a parent.
        children = set()
        for i in self.classes():
            if classname in self.class_parents(i):
                children.add(i)
                
        return list(children)

    def associations(self, classname):
        """List the associations belonging to a certain class.
        
            classname: name of class to interogate
            Returns: a list of associations names
        
        """
        associations = [ i['id'] for i in self._dict_associations[classname] ]
        
        # Build up the parent associations as well
        for i in self.class_parents(classname):
            associations.extend(self.associations(i))
        
        return associations

    def references(self, classname):
        """Return a list of possible classes that may reference the given
        class based on association types for every class.
        
        Basically - any class which has an association that has a type of 
        the provided "classname" will be added to this list.
        
        This is important to understand the reverse of all relationships.
        
            classname: class that you wish to investigate
            Returns: a set of class names
        
        """
        return self._dict_references[classname].copy()


    #----------------------------------------------- Configuration Dictionaries


    # Configuration dictionaries return key/value information about the 
    # element in the configuration tree.
    
    def class_attr(self, classname):
        """Returns a configuration dictionary of the given class.
        
        The class configuration is quite literally the XML associations that the
        class has set. Possibly associations are defined by the XSD complexType:
        
        http://organictechnology.net/schema/ObjectModel.xsd#ClassType
        
            classname: string containing a classname
            Returns: dictionary of configuration (key=config item, value=value)
        
        """
        return self._dict_classes[classname].copy()

    def association_attr(self, classname, attrname):
        """Returns a configuration dictionary of the given association.
                
            classname: string containing a classname
            attrname: string containing an association name
            Returns: dictionary of configuration (key=config item, value=value)
        
        """
        classlist = [classname]
        classlist.extend(self.class_parents(classname))
        for i in classlist:
            for n in self._dict_associations[i]:
                if n['id'] == attrname:
                    return n.copy()

    #------------------------------------------------- Private Helper Functions


    # _find_class and _find_association are helper classes created to do XML
    # node lookups.
    def _find_class(self, classname):
        """Given a classname, find the XMLNode for the class.
        
        This is an internal function, and should only be used internally.
        
            classname: name of class to search for
            Returns: the first XML Element to match
        
        """   
        for i in self._xml.findall(self._mdlns('class')):
            if i.attrib['id'] == classname:
                return i

    def _find_association(self, classname, attrname):
        """Given a class name and association name, find the XMLNode for the
         association.
        
        This is an internal function, and should only be used internally.
        
            classname: name of the class to search for
            attrname: name of the association to search for
            Returns: the first XML Element to match
        
        """   
        for i in self._find_class(classname).findall(self._mdlns('association')):
            if i.attrib['id'] == attrname:
                return i

    # Local namespace wrapper. Uses QName to wrap it in the ElementTree style:
    # eg: uri = obj._mdlns('NCName')
    _mdlns = lambda self, id: etree.QName(
        "http://organictechnology.net/schema/ObjectModel.xsd", tag=id).__str__()

