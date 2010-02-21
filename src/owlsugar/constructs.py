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


from owlsugar.universe import OwlUniverse
from owlsugar.types import ValidatedList
from owlsugar.model import ModelConfig

# TODO: We need a better way to specify these file locations
# Grab the model configuration
_model = ModelConfig("/home/ken/Development/eclipse-workspace/owlsugar-library/conf/owl11.xml",
        schema="/home/ken/Development/eclipse-workspace/owlsugar-library/conf/ObjectModel.xsd")


#------------------------------------------------------------ Construct Classes


class ClassConstruct(object):
    """This class represents an OWL class construct or function.
    
    """
    def __init__(self, *oargs, **nargs):
        """Initialise an OWL function.
        
            args: an argument list for auto-populating associations upon creation
                of an object.
        
        """
        # Some helper variables to make typing easier
        self._universe = OwlUniverse.get_universe()
        
        # If we are an abstract - then throw an exception
        if self.is_abstract() is True:
            raise Exception("Cannot instantiate an abstract class")
        
        # Prepare data stores
        self._references = dict()
        self._data = dict()
        for attr in self.associations():
            self._data[attr.id()] = None
            setattr(self, attr.id(), attr(self))
        
        # For each named argument, run its method
        for k,v in nargs.iteritems():
            self.association(k, v)
    
        # TODO: We should be mandating that objects are instantiated with
        #    mandatory associations provided as arguments at creation time.
        #    This involves some sort of positive validation I suppose.
    
        # And register the instance in the universe
        self._universe.add_object(self)
        
    def newinit(self, *oargs):
        # Testing new ordered args functionality - I've forked this from the
        # main __init__ for dev purposes.
        
        # This allows you to type:
        
        #     Namespace("foo", "<http://bob.sh/#>")
         
        # instead of using the named arguments.
        num_args = len(oargs)
            
        # TODO: need max associations #
        max_ass = 2
        
        # TODO: need min associations #
        min_ass = 1

        # Start with a basic arity check
        if num_args == max_ass:
            # Easy ... we just set each association in order with the input 
            # argument list.
            
            # TODO: Get full list of associations (in order).
            # TODO: Iterate across each association and apply them (in order)
            # for n, attr in association_list:
            #     self.associations(attr, oargs[n])
            self.associations('prefix', oargs[0])
            self.associations('IRI', oargs[1])
        elif num_args >= min_ass:
            # This means some of the optional associations are not included.
            # Now - we need to work out which ones are missing.
            
            # TODO: Get full list of associations (in order).
            # TODO: Need to get type checking working for the next thing to work.
            # TODO: Iterate across each association and apply them (in order): 
            # for n, attr in association_list:
            #     self.associations(attr, oargs[n])            
            #     if we get a type exception:
            #         if the association is optional, skip this association but keep
            #            the list index the same.
            #         if the association is not optional ... then bail - this is 
            #            just a normal invalid type, and not a consequence of
            #            a missing optional argument.
            # TODO: Have a neat way of working out weither an association is
            #    optional.

            pass
        elif num_args < min_ass:
            # Not enough mandatory arguments provided - throw an error.
            raise Exception("We require %s arguments minimum but there are "
                "only %s provided." % (min_ass, num_args))
        elif num_args > max_ass:
            # Too many arguments have been provided.
            raise Exception("Too many arguments (%s) provided. Maximum number "
                "of arguments is %s" % (num_args, max_ass))
        
    
    #------------------------------- Class Methods/Attributes for Introspection


    @classmethod
    def id(cls):
        """Return the OWL function name for this class, or the class that this
        object was instantiated from.
        
            Returns: a string containing classes OWL function name
        
        """
        return cls._id

    _id = None #: The class construct name

    @classmethod
    def is_abstract(cls):
        """Tests to see if this class is abstract.
        
        """
        try:
            if _model.class_attr(cls.id())['abstract'] == "true":
                return True
            else:
                return False
        except KeyError:
            return False

    @classmethod
    def associations(cls, filter="", optional=True):
        """Return a list of association objects for this class.
        
        """
        #TODO: Actually make the arguments work
        associations = list()
        for i in _model.associations(cls.id()):
            associations.append(getattr(cls, i))
            
        return associations
        
    @classmethod
    def ref_classes(cls):
        """Return a list of classes that may reference this class.
        
        """
        universe = OwlUniverse.get_universe()
        refs = list()
        for i in _model.references(cls.id()):
            refs.append(universe.get_class(i))
            
        return refs
    
    @classmethod
    def child_classes(cls):
        """Return a list of child classes.
        
        """
        universe = OwlUniverse.get_universe()
        children = list()
        for i in _model.class_children(cls.id()):
            children.append(universe.get_class(i))
            
        return children

    #----------------------------------------------------- Data-storage Methods

    
    def association(self, name, value):
        """Dynamic function that is called to set and get function properties.
        
        """
        # Grab this dynamic methods metadata context
        conf = _model.association_attr(self.id(), name)
    
        # If we have a value, that implies we are a setter
        if(value is not None):
            # List, set or singleton?
            if (conf.has_key('maxCardinality')) and (conf['maxCardinality'] == '1'): # singleton
                # Store away the value
                # TODO: Check types for singletons - and other validations
                self._data[name] = value
                
                # Add myself (that is my instantiated self) to the reference data 
                # structure of the class (the value). This allows that class to see
                # who is referencing it using my reverse association methods.
                if hasattr(value, 'add_reference'):
                    value.add_reference(name, self)
                        
            else:
                if isinstance(value, list) is False:
                    raise Exception("Value is not a list")
                
                # Wrap the setter value in a ValidatedList object to provide
                # enhanced validation and trigger support.
                self._data[name] = ValidatedList(self, name, 
                    self._universe.get_class(conf['type']), value)
            
        return self._data[name]
    
    def ref_objects(self, classname):
        """Dynamic function that is called to get classes that reference this 
        object.
        
            classname: the class name of the objects that need to be returned
            Returns: list of objects that point at this object
        
        """
        if self._references.has_key(classname):
            return self._references[classname]

        return None

    def add_reference(self, association, obj):
        """Add a reference to the existing list of references.
        
            obj: the object that is references our object
            association: the association that is being used to reference us
        
        """
        conf = _model.association_attr(obj.id(), association)
        
        if conf.has_key('headCardinality') and (conf['headCardinality'] == "1"):
            #print "head", self.id(), association, object.id(), object
            if (self._references.has_key(obj.id()) and 
                (self._references[obj.id()] is not None)):
                raise Exception("Exceeded head cardinality for this association.")
            else:
                self._references[obj.id()] = obj
        else:
            
            # TODO: Deal with the headCardinality properly - check # references
            if self._references.has_key(obj.id()):
                # TODO: Get some duplication testing for this list.
                #print "exists", object.id(), object
                self._references[obj.id()].append(object)
            else:
                # First element - so create a list
                #print "first", self.id(), association, object.id(), object
                self._references[obj.id()] = [obj]    


class AssociationConstruct(object):
    """This class represents an association between two class constructs.
    
    """
    
    def __init__(self, parent):
        self._parent = parent
        self._data = None
    
    def __call__(self):
        print "call", self, self._parent
        value = None
        # If we have a value, that implies we are a setter
        if(value is not None):
            # List, set or singleton?
            if (self.max_cardinality() == 1): # singleton
                # Store away the value
                # TODO: Check types for singletons - and other validations
                self._data = value
                
                # Add myself (that is my instantiated self) to the reference data 
                # structure of the class (the value). This allows that class to see
                # who is referencing it using my reverse association methods.
                """
                if hasattr(value, 'add_reference'):
                    value.add_reference(name, self)
                """
                        
            else:
                if isinstance(value, list) is False:
                    raise Exception("Value is not a list")
                
                # Wrap the setter value in a ValidatedList object to provide
                # enhanced validation and trigger support.
                self._data = ValidatedList(self, name, 
                    self._universe.get_class(conf['type']), value)
            
        return self._data
        
    @classmethod
    def id(cls):
        """Name of the association.
        
        """
        return cls._id

    _id = None #: The class construct name

    @classmethod
    def classid(cls):
        """Name of the class this association belongs to.
        
        """        
        return cls._classid
    
    _classid = None

    @classmethod
    def min_cardinality(cls):
        """Minimum amount of classes for this association.
        
        """
        return _model.association_attr(cls.classid(), 
            cls.id())['minCardinality']

    @classmethod
    def max_cardinality(cls):
        """Maximum amount of classes for this association.
        
        """        
        try:
            return _model.association_attr(cls.classid(), 
                cls.id())['maxCardinality']
        except KeyError:
            return None

    @classmethod
    def head_cardinality(cls):
        """Number of classes that may hold this association with another named
        class construct.
        
        """
        try:
            return _model.association_attr(cls.classid(), 
                cls.id())['headCardinality']
        except KeyError:
            return None

    @classmethod
    def is_unique(cls):
        """Are members of this association required to be unique?
        
        """
        try:
            if _model.association_attr(cls.classid(), 
                cls.id())['unique'] == "true":
                return True
            else:
                return False
        except KeyError:
            return True

    @classmethod
    def class_type(cls):
        """Return the class that this association pertains to.
        
        """
        universe = OwlUniverse.get_universe()
        return universe.get_class(_model.association_attr(cls.classid(), 
            cls.id())['type'])
            

#------------------------------------------------------- Create Dynamic Classes

# Generate all of the OWL dynamic function classes.
_owlclasses = dict()

# Iterate across all classes defined in our XML data model, and create them
# one by one. 
for classname in _model.classes():
    # If there are parents defined in the model, use them - otherwise fall
    # back to the standard ClassConstruct parent.
    parents = _model.class_parents(classname)
    if len(parents) == 0:
        parents = ['ClassConstruct']
    
    # Start building up the dictionary
    class_dict = {
        '_id': classname,
        '__doc__': "ClassConstruct: %s" % classname
        }
    
    # Setup dynamic association methods
    for assocname in _model.associations(classname):
        class_dict[assocname] = type(
            "%s.%s" % (classname, assocname), 
            (AssociationConstruct, ), 
            {
                '_id': assocname,
                '_classid': classname,
                '__doc__': "AssocationConstruct: %s" % assocname
            })
        
    # Setup dynamic reference methods    
    for refs in _model.references(classname):
        dm = None
        # TODO: When doing an eval - its unsafe not to check variables
        exec("dm = lambda self: self.ref_objects('%s')" % refs)
        # TODO: The documentation needs to be half-decent
        dm.__doc__ = "Reverse function for: %s" % refs
        class_dict[refs] = dm             
    
    # Create the new class construct   
    locals()[classname] = type(classname, 
        tuple([ locals()[i] for i in parents ]), class_dict)
    
    # Update our classes dictionary
    # TODO: There must be a better way.
    _owlclasses[classname] = locals()[classname]  

#------------------------------------------------------- Custom Child Functions

class Label(AnnotationByConstant):
    """This is a common annotation with a fixed URI of rdf:label.
    
    """
    def __init__(self, constant):
        """Create an annotation and use rdf:label as a URI.
        
        """
        Annotation.__init__(self, annotationURI=URI(uri="rdf:label"), 
            annotationValue=Constant(value=constant))

_owlclasses['Label'] = Label

class Comment(AnnotationByConstant):
    """This is a common annotation with a fixed URI of rdf:comment.
    
    """
    def __init__(self, constant):
        """Create an annotation and use rdf:comment as a URI.
        
        """
        Annotation.__init__(self, annotationURI=URI(uri="rdf:comment"), 
            annotationValue=Constant(value=constant))

_owlclasses['Comment'] = Comment


# This is to keep the IDE quiet
__all__ = ['Datatype', 'URI', 'OWLEntity', 'AnnotationByConstant', 'OWLClass', 
    'Axiom', 'Constant', 'Description', 'DataRange', 'DataProperty', 
    'AnnotationByEntity', 'ObjectProperty', 'Individual', 'Declaration', 
    'Ontology', 'Annotation', 'Label', 'Namespace', 'ModelConfig']

    