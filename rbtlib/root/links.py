#-------------------------------------------------------------------------------
# rbt: links.py
#
# Get a link from the  links in the Root Resource.
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
import resource
import root


class BadLinkName(Exception):
    """ Exception for missing resource in root resource's links key.
    """
    def __init__(self, url, link_name):
        self._url = url
        self._link_name = link_name


def key(link_name, content_type):
    """ Generate a getter to obtain a linked resource.

        Preconditions:
        - links is a key in the Root Resource dictionary

        Exceptions:
        - BadLinkName: link_name is not in the Root Resource's links dictionary
    """
    def _get(url, query_dict = None):
        try:
            response = root.get(url)
            assert 'links' in response, "root resource missing links key!"
            if link_name in response['links']:
                assert 'href' in response['links'][link_name], "missing href key!"
                assert 'method' in response['links'][link_name] and 'GET' == response['links'][link_name]['method'], "missing method key!"
                return resource.get(content_type)(response['links'][link_name]['href'], query_dict)
            raise BadLinkName(url, link_name)
        except:
            raise
    return _get
