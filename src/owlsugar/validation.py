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

Data validation library with exceptions.

For Users
=========

This class provides a bunch of functions that can be used to provide 
validation. The idea was to be lightweight - to both the user and the 
validation writer.

The alerting mechanism is quite simple - silent when nothing is wrong - noisy
when a validation has failed. You can of course tailer this level of "noise"
and more importantly - where it goes and when it appears.

Two facilitate this, we have provided two modes of operation, normal and 
chained.

Normal Mode
-----------

In normal mode, if the validation is unsuccessful then the function will
raise a ValidationException containing the error.

Using exceptions instead of just a boolean means the user doesn't even need to
deal with a validation error if he doesn't want to. The application will simply
die with an exception by default.

.. python::

    Valid().filepath("/tmp/foo")
    
If the user wants to catch a failed validation, then he simply needs to wrap
the function in a 'try: except' block:

.. python::

    try:
        Valid().filepath("/tmp/foo")
    except ValidationException, i:
        print i

At the moment there is no grouping of validations, all validations are
available in this module.

Chaining Mode
-------------

Often times you want to run a number of validations, and defer the error or 
exception until you are at a certain stage. This is really handy as it allows
the return of multiple errors at once - allowing us to make modifications on a
number of inputs before trying again.

The trick is in using an object for more then a single validation:

.. python::

    valid = Valid(chain=True)
    valid.filepath("/tmp/foo")
    valid.rdfgraph(mygraph)
    valid.validate()
    
Initialising the `Valid` object with the *chain=true* setting tells the object
to not raise exceptions by default, but instead to store any errors away until
the function *validate()* is called. Only then will an exception be raised and
any users will be aware there is a problem.

If you don't want to get an exception, then you can use either of the following
two methods:

.. python::

    valid = Valid(chain=True)
    valid.filepath("/tmp/foo")
    valid.rdfgraph(mygraph)
    errors = valid.validate(exception=False)
    for i in errors:
        print i
        
By making the *exception* parameter false, it returns a list of errors instead.

.. python::

    valid = Valid(chain=True)
    valid.filepath("/tmp/foo")
    valid.rdfgraph(mygraph)
    try:
        valid.validate()
    except ValidationException:
        for i in valid.errors:
            print i
            
It all depends on your own personal preference.

You'll notice I used the *valid.errors* notation. This is basically a list 
attribute on the instance that you can access. In fact - you could access this
attribute part way through a chain - if you were so inclined.

For developers
==============

To add new tests, obviously you can look at an existing one. The guidelines
are:

- Always prefix your function with *valid_* to keep the naming consistent.
- Always raise a `ValidationException` so users can catch it.
- You don't have to return a boolean so don't bother.
- Make the message in the exception meaningful.
- Its good practice to do as many validations as possible (even if the data
  fails early) and raise an exception including all the errors with the input.
  This way a user can correct all the necessary errors without having to do the
  old recursive "error-fix-error-fix" thing.

The ValidationException object can also be used in your code. This is useful
for putting more complex validation that doesn't belong in this library.

For example, say your function can take 2 arguments and at least 1 is required
for it to run. You can simply use the ValidationException object like any 
exception to return a more meaningful exception to the user for catching in a
'try: except' block.
"""

__docformat__ = 'restructuredtext en'
__version__ = '$Rev: 179 $'

from os import getcwd
from os.path import isfile, exists
import re

from rdflib import Namespace
from rdflib.Graph import ConjunctiveGraph, Graph

from owlsugar.exceptions import OwlSugarException


class Valid(object):
    """Provide validation methods and error chaining facility."""
    
    def __init__(self, chain=False):
        """Initialiase, optionally enabling chaining.
        
        At the moment there are two modes: chained and normal.
        
        :Parameters:
            chain : bool
                Turns on chaining mode. This disable immediate exceptions and
                stores errors in a list instead.
                
        """
        # Privates
        self._errors = []    #: list to keep errors in
        self._chain = chain  #: chain mode status
        
        self.errors = self._errors #: Error list for public use

    #--------------------------------------------------- Validation: Filesystem

    def filepath(self, thing):
        """Validate a file path.
        
        - *thing* must be a string
        - *thing* must point to something on the filesystem
        - *thing* must be a file
        
        """
        self.stringtype(thing)
        if not exists(thing):
            self.not_valid("The string provided does not point to anything "
                "on the filesystem: %s (cwd: %s)" % (thing, getcwd()))
        elif not isfile(thing):
            self.not_valid("The path provided exists but points to something "
                "other than a file: %s (cwd: %s)" % (thing, getcwd()))
    
    #------------------------------------------------- Validations: RDF and OWL
    
    # Most validation stuff is defined in the XML schema documentation:
    #
    # http://www.w3.org/TR/xmlschema-2/
    
    def owlgraph(self, thing):
        """Validate an OWL graph (not just RDF graphs).
        
        - *graph* must be an rdfgraph
        
        """
        self.rdfgraph(thing)
    
    def rdfgraph(self, thing):
        """Validate a graph, ensuring it is of type Graph.
        
        - *thing* must be of type Graph
        
        """
        self.classtype(thing, Graph)

    def rdfinputformat(self, thing):
        """Validate input format.
        
        Use in rdflib.Graph.ConjunctiveGraph.parse calls.
        
        - Must be a string
        - Must be one of:
            - **xml**: RDF/XML
            - **n3**: N3
            - **nt**: NTriples
            - **trix**: TriX
            - **rdfa**: RDFa
            
        """
        self.stringtype(thing)
        self.in_list(thing, ['xml', 'n3', 'nt', 'trix', 'rdfa'])

    def rdfnamespace(self, thing):
        """Validate rdflib namespace.
        
        - *thing* must be a Namespace object
        
        """
        self.classtype(thing, Namespace)
    
    def rdfoutputformat(self, thing):
        """Validate output format.
        
        Used in ConjunctiveGraph.serialise calls.
        
        - Must be a string
        - Must be one of:
            - **pretty-xml**: for nicer xml output
            - **xml**: not quite as nice?
            - **n3**: my favourite as its easy to read
            - **nt**: NTriple format
            - **turle**: Turtle format
            
        """
        self.stringtype(thing)
        self.in_list(thing, ['pretty-xml', 'xml', 'n3', 'nt', 'turtle'])
        
    def rdfid(self, thing):
        """Validate an rdf:ID.
        
        According to:
        
        http://www.w3.org/TR/rdf-concepts/ 
        
        a URI is compatible with the XML anyURI. The ID is the fragment part of
        a URI is defined in:
        
        http://www.w3.org/TR/xmlschema-2/
        
        Which if you follow the bases, that the final pattern is documented
        here: 
        
        http://www.w3.org/TR/REC-xml-names/#NT-NCName

        Now this is a real treat to try and work out. So for now I'm going to 
        use a basic regexp. In the future we will have to support unicode and
        do a proper regexp check.
        
        - Must be a string
        - Must match this regexp: [a-zA-Z][\w\.\-]*
        
        """
        self.stringtype(thing)
        if not re.compile("[a-zA-Z][\w\.\-]*").match(thing):
            self.not_valid("An rdfid must start with an alphabetical "
                "character and then only contain alphanumeric, fullstop or "
                "hyphen characters.")
    
    #--------------------------------------------- Validations: Primitive Types
    
    def stringtype(self, thing):
        """str"""
        self.classtype(thing, str)
        
    def listtype(self, thing):
        """list"""
        self.classtype(thing, list)
        
    def booltype(self, thing):
        """bool"""
        self.classtype(thing, bool)

    #----------------------------------------------------- Validations: Utility
    
    def in_list(self, thing, validlist):
        """Takes a "thing" and makes sure its one of "validlist".
        
        - check individual arguments
            - *thing* can be any type
            - *validlist* must be a list
        - *thing* must exist at least once in *validlist*
        
        """
        # Chained validation
        valid = Valid(chain=True)
        valid.has_contents(thing)
        valid.listtype(validlist)
        valid.validate()
        
        if not validlist.count(thing):
            self.not_valid("%s is not a valid choice. Must be one of %s." % 
                (thing, ', '.join(validlist)))

    def classtype(self, thing, classtype):
        """Check if object "thing" has a class of "classtype". 
        
        *classtype* can either be a single entity or a list or classes.
        
        - *thing*.__class__ must match classtype or one of classtype[]
        
        """
        # Do our own class validation, because thats our job.
        
        # Its a list
        if classtype.__class__ == list: # its a list
            if not classtype.count(thing.__class__):
                # Get a list of __class__ values from the classtype list
                ctlist = [ str(i) for i in classtype ]
                self.not_valid("Thing has a class type of %s, must be one of "
                    "the following: %s." % ", ".join(ctlist))
        # Its something else
        else:
            if thing.__class__ != classtype:
                self.not_valid("Thing has a class type of %s, must be type "
                    "%s." % (thing.__class__, classtype))
                
    def has_contents(self, thing):
        """Check if *thing* contains something.
        
        - *thing* must not be null or empty
        
        """
        if thing == None:
            self.not_valid("Thing of type %s cannot be null." 
                % thing.__class__)
        elif not thing:
            self.not_valid("Thing of type %s cannot be empty." 
                % thing.__class__)
            
    #---------------------------------------------------------- Functions: Core
    
    def not_valid(self, message, forceraise=False):
        """Raise an exception directly using the error message provided in 
        *message*, or add the error to the chain of errors.
        
        This function is called when a validation has failed.
       
        :Parameters:
            message : object
                (str or str[]) Error message.
            forceraise : bool
                If set to true - it will force an exception regardless of the
                any other settings. This is used to raise exceptions after a
                chain of validations.
                
        """
        # Recursive head-fuck so I've commented heavily.
        
        # Minimal chaining here, as it will cause infinite loops. Also, we'll 
        # have to always raise exceptions 'cos if you get this part wrong 
        # you'll want to know straight away.
        
        # For fatals - Only direct exceptions are to be raised. we should not
        # call ourself directly to avoid infinite recursion and error hiding.
        
        # Make sure the message is either a list or string.
        self.classtype(message, [list, str])
        
        # Error list has been passed for appending either for chaining purposes
        # or direct output.
        errors = self._errors
        if errors:
            # Make sure errors is a list.
            self.classtype(errors, list)
        else:
            # Empty error list for inserting new items.
            errors = []
    
        # Extend for lists
        if message.__class__ == list:
            errors.extend(message)
        # Append for strings
        elif message.__class__ == str:
            errors.append(message)
        # Unreachable point 
        else:
            raise FaultyValidatorException("For some reason the validation "
                "function `not_valid` didn't validate its 'message'.")
    
        # Are there errors?
        if not len(errors):
            raise FaultyValidatorException("For some reason even after doing "
                "its own internal validation the function `not_valid` still "
                "does not have any errors in its internal list.")
    
        # If we are in chaining mode and we are not being forced to raise, 
        # return the errors list to the caller.
        if self._chain and not forceraise:
            return errors
        # If we are not in chaining mode, raise an exception with all of the 
        # errors we have accumulated as a list.
        else:
            raise ValidationException("\n".join(errors))

    def validate(self, exception=True):
        """Do an immediate validation of the chain.
        
        If previous validations had found errors, they will now be either:
        
        - raised as an exception
        - returned to the caller as a list of strings
        
        The idea is to do bunch of validations and return all the errors so
        a user can fix more problems in one go.
        
        As validate is usually run on purpose (and so reasonably controlled)
        you could wrap a validate-with-exception call in a 'try: except' block
        and then poke at the `errors` instance variable. This would all depend
        on the style you are after.
        
        :Parameters:
            exception : bool
                (default is true) If true, raise an exception if there are 
                errors. If false, return a string of error messages.
        :return: (str[] or None) List of error strings or None if there were no 
                 errors.
                 
        """
        if len (self._errors):
            if exception:
                self.not_valid(self._errors, forceraise=True)
            else:
                return self._errors
            
#------------------------------------------------------------------- Exceptions

class ValidationException(OwlSugarException):
    """Validation Exception. 
    
    Raised when data being validated does not pass a its checks. This can be a
    soft error at times depending on your application so you may want to wrap
    it in a 'try: except' block.
    
    """
    pass


class FaultyValidatorException(OwlSugarException):
    """Serious exceptions found in the validator will raise this exception.
    
    This exception might mean there is a bug in the validator.
    
    """
    pass