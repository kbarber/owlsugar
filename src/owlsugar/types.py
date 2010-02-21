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


class ValidatedList(list):
    def __init__(self, parent, attribute, type, value):
        self._parent = parent
        self._attribute = attribute
        self._type = type
        
        list.__init__(self, [])
        for i in value:    
            self.append(i)


    def append(self, element):
        """Special override for append.
        
        """
        # Make sure the type is correct
        if isinstance(element, self._type) is False:
            raise Exception("Invalid type:", element.fname())
        
        # Fix up reverse references
        if hasattr(element, 'add_reference'):
            element.add_reference(self._attribute, self._parent)
        
        # Now call the real add        
        return list.append(self, element)
