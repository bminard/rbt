#-------------------------------------------------------------------------------
# rbt: resource.py
#
# Get a named tuple response from a URL.
#-------------------------------------------------------------------------------
# The MIT License (MIT)
# Copyright (c) 2016 Brian Minard
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#-------------------------------------------------------------------------------
from abc import ABCMeta, abstractmethod
from composite import Composite
import stat


class Resource(object):
    """ Abstract base class for all resources.
    """
    __metaclass__ = ABCMeta
    def __init__(self, session, resource_name, content_type):
        """ Construct the abstract base class.
        """
        self._resource_name = resource_name
        self._composite = Composite(session)
    @stat.is_valid
    def composite(self, query_dict = None):
        """ Construct the composite for the resource.

        A JSON component is added to the resource to preserve the server's
        response.
        """
        response = self.fetch(query_dict)
        return self._composite.component(self._resource_name, response, { 'json': response })
    @abstractmethod
    def fetch(self, query_dict = None):
        """ Different getters are required by Root List Resource and all other resources.

        The Root List Resource obtains its URL from the caller. The other
        resources obtain their URLs from the Root List Resource.
        """
        pass
    def get(self, query_dict = None):
        """ Return a composite of an HTTP request.
        """
        return self.composite(query_dict)
