#-------------------------------------------------------------------------------
# rbt: test_links.py
#
# Tests for links.py.
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
import http
import pytest
import links
import root


@pytest.fixture
def resource():
    return 'review_requests'


@pytest.fixture
def content_type():
    return 'application/vnd.reviewboard.org.review-requests+json'


def test_root_links_key_present(resource, content_type, review_board_url):
    """ Handle case when link resource is present.
    """
    links.get(resource, content_type)(review_board_url)


def test_root_links_key_missing(review_board_url):
    """ Handle case when link resource is unavailable.
    """
    with pytest.raises(links.BadLinkName):
        links.get('foobar', 'text/html')(review_board_url)


def test_get_through_link_without_query_dict(resource, content_type, review_board_url):
    """ Handle case when link resource is present.
    """
    links.get(resource, content_type)(review_board_url)


def test_get_through_link_without_query_dict(resource, content_type, review_board_url):
    """ Handle case when link resource is present.
    """
    links.get(resource, content_type)(review_board_url, { 'counts-only': 'True' })


def test_get_through_link_without_query_dict(resource, content_type, review_board_url):
    """ Handle case when link resource is present.
    """
    links.get(resource, content_type)(review_board_url, { 'mycounts-only': 'True' })
