#-------------------------------------------------------------------------------
# rbt: links.py
#
# Get a link from the links in the resource.
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
from resource import Resource


class Links(Resource):
    """ Construct a linked resource object.
    """
    def __init__(self, parent, resource_name, content_type):
        """ Initialize a linked resource from the parent link.
        """
        self._parent = parent
        self._resource_name = resource_name
        super(Links, self).__init__(parent.session, self._resource_name, content_type)
    def fetch(self, query_dict = None):
        """ Getter for the linked resource.
        """
        return getattr(self._parent.composite().links, self._resource_name).get(query_dict)
    def session(self):
        """ The HTTP session.
        """
        return self._parent.session()
