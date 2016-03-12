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
import rbtlib.composite
import resource
import stat


@stat.key
@rbtlib.composite.construct('Root')
def get(url, query_dict = None):
    """ Return a JSON formated `Root Resource`_ from a Review Board instance.

    _Root Resource: https://www.reviewboard.org/docs/manual/2.5/webapi/2.0/resources/root/#webapi2.0-root-resource/

    URL is the fully qualified domain name, including the scheme, of the Review Board
    instance to query.

    query_dict are parameters passed with the URL.
    """
    try:
        # Do not assert root resources here. Instead, assert at the point of use
        # so responses needn't be consistent in all call contexts.
        return resource.get('application/vnd.reviewboard.org.root+json')(url + '/api/', query_dict)
    except:
        raise
