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
from functools import wraps
import rbtlib.composite
import resource
import root
import stat


class BadLinkName(Exception):
    """ Exception for missing resource in root resource's links key.
    """
    def __init__(self, url, link_name):
        self._url = url
        self._link_name = link_name


def get(link_name, content_type):
    """ Generate a getter to obtain a linked resource.

        Preconditions:
        - links is a key in the Root Resource dictionary

        Exceptions:
        - BadLinkName: link_name is not in the Root Resource's links dictionary
    """
    @stat.key
    @rbtlib.composite.construct(link_name)
    @wraps(get)
    def _get(url, query_dict = None):
        """ Return a JSON formated resource linked to the `Root Resource`_

        URL is the fully qualified domain name, including the scheme, of the Review Board
        instance to query.

        query_dict are parameters passed with the URL.

        _Root Resource: https://www.reviewboard.org/docs/manual/2.5/webapi/2.0/resources/root/#webapi2.0-root-resource/
        """
        try:
            response = root.get(url)
            assert response.links, "root resource missing links key!"
            try:
                assert 'GET' == getattr(response.links, link_name).method, "expecting HTTP GET method!"
                return resource.get(content_type)(getattr(response.links, link_name).href, query_dict)
            except AttributeError:
                raise BadLinkName(url, link_name)
            raise BadLinkName(url, link_name)
        except:
            raise
    return _get
