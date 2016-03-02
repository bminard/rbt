#-------------------------------------------------------------------------------
# rbt: test_resource.py
#
# Tests for resource.py.
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
import resource


def test_resource_get_value_error(review_board_url):
    """ No JSON object could be decoded.
    """
    # httpbin.org always returns a JSON formated response
    with pytest.raises(ValueError):
        resource.get('text/html; charset=utf-8')(review_board_url)


@pytest.fixture
def get():
    """ Generate the get() function created by the resource component.
    """
    return resource.get('application/vnd.reviewboard.org.root+json')


def test_resource_get_bad_content_type(get, review_board_url):
    """ HTTP request is wrong content type.
    """
    # httpbin.org always returns a JSON formated response
    with pytest.raises(resource.BadContentType):
        get(review_board_url)


def test_resource_get_without_query_dict(get, review_board_url):
    """ JSON object decoded without request parameters.
    """
    try:
        get(review_board_url + '/api/')
    except ValueError:
        pytest.fail("Unexpected ValueError.")


def test_resource_get_ok_with_query_dict(get, review_board_url):
    """ JSON object decoded with request parameters.
    """
    try:
        get(review_board_url + '/api/', { 'foo': 'bar' })
    except ValueError:
        pytest.fail("Unexpected ValueError.")
