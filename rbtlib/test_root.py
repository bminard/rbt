#-------------------------------------------------------------------------------
# rbtlib: test_root.py
#
# Tests for root.py.
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
from root import Root


@pytest.fixture
def root(session, server):
    """Construct a Root List Resource object."""
    return Root(session, server.url)


query_dicts = [ None, { 'counts-only': 'True' } ]


@pytest.mark.parametrize("query_dict", query_dicts)
def test_root_dict(root, query_dict):
    """Confirm the stat in the JSON component.

    The root instance is provided a query dictionary to ensure that our APIs can
    support it. This isn't required by the Review Board API but seems like one
    obvious change that might occur in the future.

    (I know, YAGNI. Couldn't resist the temptation to predict the future.)
    """
    assert 'ok' == root(query_dict).json['stat']


@pytest.mark.parametrize("query_dict", query_dicts)
def test_root_named_tuple(root, query_dict):
    """Confirm the stat in the named tuple component."""
    assert 'ok' == root(query_dict).stat


@pytest.mark.parametrize("query_dict", query_dicts)
def test_root_dict_and_named_tuple_equivalence(root, query_dict):
    """Confirm the stat in the JSON and named tuple are equal."""
    assert root(query_dict).stat == root(query_dict).json['stat']


@pytest.mark.parametrize("query_dict", query_dicts)
def test_root_get_named_tuple(root, query_dict, root_resource_component):
    """Confirm named tuple contains expected components."""
    assert None != getattr(root(query_dict), root_resource_component, None)


@pytest.fixture(params = [ 'href', 'method' ])
def link_component(request):
    """Provide top-level Root List Resource links components."""
    return request.param


@pytest.mark.parametrize("query_dict", query_dicts)
def test_linked_root_link_component(root, query_dict, root_resource_link,
        link_component):
    """Confirm named tuple's links contains requisite components."""
    assert None != getattr(getattr(getattr(root(query_dict), 'links', None),
        root_resource_link, None), link_component, None)


@pytest.mark.parametrize("query_dict", query_dicts)
def test_root_links_review_requests(server, root, query_dict):
    """Use get method to access a linked resource and confirm it's status.

    Use long form of access to a linked resource.
    """
    assert server.url + '/api/review-requests/' == root(query_dict).links.review_requests.href


@pytest.mark.parametrize("query_dict", query_dicts)
def test_root_linked_resources(root, query_dict, extended_root_resource):
    """Confirm root resource includes linked resource objects."""
    assert None != getattr(root(query_dict), extended_root_resource, None)


@pytest.mark.parametrize("root_query", query_dicts)
@pytest.mark.parametrize("review_request_query", query_dicts)
def test_root_and_review_requests_callable(root, root_query, review_request_query):
    """Show relationship between long form and short form access to a resource.
    """
    assert 'ok' == root(root_query).review_requests(review_request_query).stat


@pytest.mark.parametrize("root_query", query_dicts)
@pytest.mark.parametrize("review_query", query_dicts)
def test_review_requests_count_only(root, root_query, review_query):
    """Confirm that request parameters return an expected result.
    """
    request = root(root_query).review_requests(review_query)
    assert 'ok' == request.stat and 0 <= request.count


@pytest.mark.parametrize("root_query", query_dicts)
@pytest.mark.parametrize("review_query", query_dicts)
def test_root_resources_are_callable(login, root, root_query, root_resource_link, review_query):
    """Confirm root resource links are callable."""
    if root_resource_link in ['search', 'webhooks' ]:
        pytest.skip("{0} service unsupported".format(root_resource_link))
    assert 'ok' == getattr(root(root_query), root_resource_link, None)(review_query).stat


@pytest.mark.parametrize("root_query", query_dicts)
def test_review_request_no_create_link(root, root_query):
    """Expect an error when requesting linked content and restricted content."""
    with pytest.raises(AttributeError):
        root(root_query).review_requests({ 'counts-only': 'True' }).create()


@pytest.fixture(params = [
    'create', # requires HTTP POST
    'self', # requires HTTP GET
])
def review_requests_resource_link(request):
    """Provide top-level Review Request List Resource links."""
    return request.param


@pytest.mark.parametrize("root_query", query_dicts)
def test_review_requests_resource_are_callable(login, root, root_query, review_requests_resource_link):
    """Confirm review requests resource links are callable."""
    review_requests = getattr(root(root_query), 'review_requests', None)
    assert 'ok' == getattr(review_requests(), review_requests_resource_link, None)().stat


@pytest.mark.parametrize("root_query", query_dicts)
def test_review_request_create(login, root, root_query):
    """Create an empty review request."""
    review_requests = root(root_query).review_requests()
    create = review_requests.create()
    assert 'ok' == create.stat and 0 <= create.review_request.id
