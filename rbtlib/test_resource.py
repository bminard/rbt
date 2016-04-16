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
from types import DictType
from links import Links
import requests
from root import Root


def pytest_generate_tests(metafunc):
    if 'resource' in metafunc.fixturenames:
        metafunc.parametrize("resource", ['root', 'links'], indirect=True)


@pytest.fixture
def resource(request, session, server):
    if 'root' == request.param:
        return Root(session, server.url)
    if 'links' == request.param:
        return Links(Root(session, server.url), 'review_requests', 'application/vnd.reviewboard.org.review-requests+json')
    raise ValueError("invalid internal test config")


def test_resource_composite_ok(resource):
    """ Expected status of a successful request.
    """
    assert 'ok' == resource.composite().stat


def test_resource_fetch(resource):
    """ Handle case when link resource is present.
    """
    assert type(resource.fetch()) == DictType


def test_resource_get_ok(resource):
    """ Expected status of a successful request.
    """
    assert 'ok' == resource.get().stat


query_dicts = [ None, { 'counts-only': 'True' } ]


@pytest.mark.parametrize("query_dict", query_dicts)
def test_resource_fetch_matches_get_json(resource, query_dict):
    """ Expected type of a successful request.
    """
    assert resource.fetch(query_dict) == resource.get(query_dict).json
