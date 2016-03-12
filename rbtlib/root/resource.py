#-------------------------------------------------------------------------------
# rbt: resource.py
#
# Get a JSON formated response from a URL.
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
import http
import requests


class BadContentType(Exception):
    """ Exception thrown when expected and actual content types differ.
    """
    def __init__(self, url, status, expected, actual):
        self._url = url
        self._status_code = status
        self._expected_content_type = expected
        self._actual_content_type = actual


def get(expected_content_type):
    """ Generate a getter for the expected content type.
    """
    @wraps(get)
    def _get(url, query_dict = None):
        """ Return a JSON formated response.

        URL is the fully qualified domain name, including the scheme, of the Review Board
        instance to query.

        query_dict are parameters passed with the URL.
    
        Exceptions:
          - BadContentType: whenever the expected and actual content type differ
          - ValueError: whenever the JSON decode fails
        """
        try:
            response = http.get(url, query_dict)
            if response.headers['Content-Type'] != expected_content_type:
                raise BadContentType(url,
                        response.status_code,
                        expected_content_type,
                        response.headers['Content-Type'])
            return response.json()
        except ValueError:
            raise
    return _get
