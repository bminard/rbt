#-------------------------------------------------------------------------------
# rbt: test_review_requests.py
#
# Tests for review_requests.py.
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
import pytest
from review_requests import ReviewRequests
from root import Root
from types import DictType


@pytest.fixture
def review_requests(session, review_board_url):
    """ Construct the Review Requests object.
    """
    return ReviewRequests(Root(session, review_board_url))


getter_query_dicts = [ None, { 'counts-only': 'True' } ]


@pytest.mark.parametrize("getter_query_dict", getter_query_dicts)
def test_review_requests_fetch_ok(getter_query_dict, review_requests):
    """ Test review requests getter.
    """
    assert type(review_requests.fetch(getter_query_dict)) == DictType
    assert review_requests.composite().json == review_requests.composite().links.self.get()
    assert review_requests.composite().json == review_requests.get().json


@pytest.mark.parametrize("getter_query_dict", getter_query_dicts)
def test_review_requests_composite_ok(getter_query_dict, review_requests, root):
    """ Test review requests getter.
    """
    assert review_requests.composite().links.self.get(getter_query_dict) == review_requests.fetch(getter_query_dict)
    assert root.composite().links.review_requests.get(getter_query_dict) == review_requests.fetch(getter_query_dict)
