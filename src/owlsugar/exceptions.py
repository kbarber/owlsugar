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

This package and its modules are designed for storing our user-defined global
exceptions.

OwlSugarException is the base class - all classes *must* inherit from this to 
gain the most effectiveness.

Some exceptions may be better placed inside the module close to the class that
is throwing them - regardless they must still inherit from OwlSugarException.
"""

__docformat__ = 'restructuredtext en'
__version__ = '$Rev: 174 $'


class OwlSugarException(Exception):
    """Base exception for all of the OWL sugar exceptions.
    
    This can either be used directly - or inherited from (recommended).
    
    For inheritance it is needed to allow users to segregate OWL sugar related
    errors from standard errors without the need to know every single exception
    we provide.
    
    """
    pass


class InvalidOwlParseException(OwlSugarException):
    """This exception is raised when a parsed files contents are invalid."""
    pass


class DuplicateIdException(OwlSugarException):
    """This exception is raised when an element is being added, but the ID is 
    already taken.
    
    """
    pass


class SchemaException(OwlSugarException):
    """This exception is raised when someone tries to do something that goes 
    against the schema definition.
    
    """
    pass


class DuplicateImportException(OwlSugarException):
    """
    This exception is raised when a document is being imported into a document
    that has already has the import entry.
    """
    pass


class SchemaWebException(OwlSugarException):
    """
    This exception is raised when a SchemaWeb error has been encountered.
    """
    pass