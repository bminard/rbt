#-------------------------------------------------------------------------------
# rbt: root.py
#
# Get the Root Resource from a Review Board instance.
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


class Root(Resource):
    """ The Root List Resource for the Review Board instance.
    """
    name = 'root'
    content_type = 'application/vnd.reviewboard.org.root+json'
    def __init__(self, session, url):
        """ Contruct a Root List Resource.
        """
        super(Root, self).__init__(session, self.name, self.content_type)
        self._session = session
        self._url = url + '/api/'
    def fetch(self, query_dict = None):
        """ Getter for the Root List Resource.
        """
        return self._session.get(self._url, params = query_dict).json()
    def get(self, query_dict = None):
        """ Getter for the Root List Resource.
        """
        return self.composite(query_dict)
    @property
    def session(self):
        """ Return the HTTP session.
        """
        return self._session
