#-------------------------------------------------------------------------------
# rbt: conftest.py
#
# Common pytest fixtures.
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
from rbtlib import Links, Root
import requests
import pytest


@pytest.fixture
def review_board_fqdn():
    return 'reviews.reviewboard.org'


@pytest.fixture
def review_board_url(review_board_fqdn):
    return 'https://' + review_board_fqdn + '/api/'


@pytest.fixture
def session():
    return requests.Session()


@pytest.fixture
def root(session, review_board_url):
    return Root(session, review_board_url)


@pytest.fixture
def links(root):
    """ Construct the Links object.
    """
    return Links(root, 'review_requests', 'application/vnd.reviewboard.org.review-requests+json')
