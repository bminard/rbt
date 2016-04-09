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
from types import BooleanType, DictionaryType, DictType, IntType, ListType


class Composite(object):
    """ Create a composite object from the resource.
    """
    def __init__(self, session):
        """ Initialize the composite object.

        Use the same session object for all getter and setter operations.
        """
        super(Composite, self).__init__()
        self._session = session
    def href_component(self, href, method):
        """ Construct a HREF component.
        """
        if 'DELETE' == method:
            return lambda query_dict = dict(): self._session.delete(href, data = query_dict).json()
        elif 'GET' == method:
            return lambda query_dict = dict(): self._session.get(href, data = query_dict).json()
        elif 'POST' == method:
            return lambda post_data_dict = dict(): self._session.post(href, data = post_data_dict).json()
        elif 'PUT' == method:
            return lambda put_data_dict = dict(): self._session.put(href, data = put_data_dict).json()
        assert 0, "unsupported http method: {}".format(method)
    def list_component(self, name, response):
        """ Construct a list component.
        """
        args = list()
        for element in response:
            if type(element) is DictType or type(element) is DictionaryType:
                args.append(self.component(name, element))
            else:
                args.append(name)
        return args
    def component(self, resource_name, response, extra_args = dict()):
        """ Construct component.
        """
        field_names = ' '.join(list(extra_args) + list(response))
        args = dict(extra_args)
        for x in response:
            if type(response[x]) is DictType or type(response[x]) is DictionaryType:
                args[x] = self.component(x, response[x])
            elif type(response[x]) is ListType:
                args[x] = self.list_component(x, response[x])
            else:
                if 'href' == x:
                    method = response['method'].lower()
                    field_names += ' ' + method
                    args[method] = self.href_component(response['href'], response['method'])
                args[x] = response[x]
        tuple_descriptor = collections.namedtuple(resource_name, field_names)
        return tuple_descriptor(**args)
