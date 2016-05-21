#-------------------------------------------------------------------------------
# rbtlib: test_resource.py
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
from resource import Resource, BadContentType
from types import DictionaryType, DictType, ListType


@pytest.fixture
def resource(session):
    """Construct the resource instance.

    Args:
        session: HTTP session to use with this resource.

    Returns:
        A resource object.
    """
    return Resource(session, 'root')


def test_resource_getter_bad_content_type(server, resource):
    """Execute HTTP GET on bad content."""
    with pytest.raises(BadContentType):
        resource.get(server.url)


@pytest.fixture
def server_response(server, resource):
    """Execute HTTP GET on valid content.

    Args:
        server: Review Board server.
        resource: resource object.

    Returns:
        The HTTP response returned by the server.
    """
    return resource.get(server.url + '/api/')


def test_resource_post_bad_content_type(server, resource):
    """Execute HTTP POST on bad content."""
    with pytest.raises(BadContentType):
        resource.post(server.url)


def test_resource_getter_attribute_error(server_response):
    """Execute HTTP GET on non-existent link."""
    with pytest.raises(AttributeError):
        server_response.foo


def test_resource_get_dict(server_response):
    """Confirm stat availablity in the JSON dictionary."""
    assert 'ok' == server_response.json['stat']


def test_resource_get_dict_and_named_tuple_stat_equivalence(server_response):
    """Confirm JSON dictionary and named tuple have the same stat value."""
    assert server_response.stat == server_response.json['stat']


def equivalent(lhs, rhs):
    """Traverse the composite and the JSON response from the server.

    Compare the JSON response from the Review Board instance with the
    composite object created by the Resource class.

    Args:
        lhs: the JSON response.
        rhs: the composite object containing the JSON response.

    Returns:
        True whenever the JSON dictionary and the whole-part hierarchy composite
        contain the same data; False otherwise.
    """
    for x in lhs:
        if type(lhs[x]) is DictType or type(lhs[x]) is DictionaryType:
            if False == equivalent(lhs[x], getattr(rhs, x)):
                return False
        elif type(lhs[x]) is ListType:
            for y in lhs[x]:
                if type(y) is DictType or type(y) is DictionaryType:
                    if False == equivalent(y, getattr(rhs, x)[0]):
                        return False
                else:
                    if getattr(getattr(rhs, x), y) != lhs[x][y]:
                        return False
        else:
            if getattr(rhs, x) != lhs[x]:
                return False
    return True


def test_resource_get_dict_and_named_tuple_deep_equivalence(server_response):
    """Confirm JSON dictionary and named tuple have the same content."""
    assert True == equivalent(server_response.json, server_response)


def test_resource_get_named_tuple(server_response, root_resource_component):
    """Confirm named tuple contains expected components."""
    assert None != getattr(server_response, root_resource_component, None)


def test_linked_resource(server_response, root_resource_link):
    """Confirm named tuple contains expected linked components."""
    assert None != getattr(server_response.links, root_resource_link, None)


def test_linked_resource_href(server_response, root_resource_link):
    """Confirm named tuple linked components contain hypertext references."""
    assert None != getattr(getattr(server_response.links,
        root_resource_link, None), 'href', None)


def test_linked_resource_method(server_response, root_resource_link):
    """Confirm named tuple linked components contain HTTP method definitions."""
    assert None != getattr(getattr(server_response.links,
        root_resource_link, None), 'method', None)
