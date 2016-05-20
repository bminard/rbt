#-------------------------------------------------------------------------------
# rbtlib: stat.py
#
# Validate the stat key returned with a Review Board resource.
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


def is_valid(fetch):
    """Decorator to validate the Review Board response status.

    Args:
        fetch: an HTTP command to execute.

    Returns:
        A function object capable of ensuring the response is valid.
    """
    @wraps(fetch)
    def _is_valid(self, url, query_dict = None):
        """Check the stat returned by Review Board.

        Args:
            href: A hypertext reference used by the HTTP command.
            query_dict: A dictionary containing HTTP command parameters.

        Returns:
            The Review Board response.
        """
        response = fetch(self, url, query_dict)
        assert 'ok' == response.stat or 'fail' == response.stat
        return response
    return _is_valid
