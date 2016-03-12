#-------------------------------------------------------------------------------
# rbt: composite.py
#
# Use the Composite pattern to describe a resource.
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
import collections
from functools import wraps
from types import DictType


def composite(resource_name, response, extra_keyword_args = dict()):
    """ Return a component containing the entire resource description.

      - resource_name: the Review Board resource from which the composite
      is constructed.

      - response: the Review Board response containing the resouce description.

      - extra_keyword_args: meta-data to add to the composite.
    """
    field_names = str()
    keyword_args = dict(extra_keyword_args)
    for key in extra_keyword_args:
        field_names += ' ' + key
    for x in response:
        field_names += ' ' + x
        if type(response[x]) is DictType:
            keyword_args[x] = composite(x, response[x])
        else:
            keyword_args[x] = response[x]
    tuple_descriptor = collections.namedtuple(resource_name, field_names)
    return tuple_descriptor(**keyword_args)


def construct(resource_name):
    """ Decorator combining the get function with composite construction.

      - resource_name: the Review Board resource for which the composite
      is to be constructed.
    """
    def _construct(get):
        """ Allow the contruct decorator to take an argument.

          - get: the function implementing the HTTP GET method
        """
        @wraps(get)
        def __construct(url, query_dict = None):
            """ Construct a composite object for the resource_name using the get
            request to the Review Board instance.

            A JSON object is embedded into the top-level composition to provide
            access to the response in its original form.

            URL is the fully qualified domain name, including the scheme, of the Review Board
            instance to query.

            query_dict are parameters passed with the URL.
            """
            response = get(url, query_dict)
            return composite(resource_name, response, { 'json': response })
        return __construct
    return _construct
