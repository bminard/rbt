#-------------------------------------------------------------------------------
# rbt: resource.py
#
# Get a named tuple response from a URL.
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
import collections
from functools import wraps
import stat
from types import DictionaryType, DictType, ListType


class BadContentType(Exception):
    """ HTTP response contains unexpected content type. """


content_type = {
        'accounts': 'application/vnd.reviewboard.org.hosting-service+json',
        'api_tokens': 'application/json',
        'archived_review_requests': 'application/json',
        'blocks': 'application/json',
        'branches': 'application/vnd.reviewboard.org.repository+json',
        'commits': 'application/vnd.reviewboard.org.repository+json',
        'changes': 'application/vnd.reviewboard.org.review-request-changes+json',
        'create': 'application/vnd.reviewboard.org.review-request+json',
        'default_reviewers': 'application/vnd.reviewboard.org.default-reviewers+json',
        'delete': 'application/json',
        'depends_on': 'application/json',
        'diff_context': 'application/json',
        'diff_file_attachments': 'application/json',
        'diff_validation': 'application/json',
        'diffs': 'application/vnd.reviewboard.org.diffs+json',
        'draft': 'application/json',
        'extensions': 'application/json',
        'file_attachments': 'application/json',
        'groups': 'application/vnd.reviewboard.org.review-groups+json',
        'hosting_services': 'application/vnd.reviewboard.org.hosting-services+json',
        'hosting_service_accounts': 'application/vnd.reviewboard.org.hosting-service-accounts+json',
        'info': 'application/vnd.reviewboard.org.server-info+json',
        'last_update': 'application/json',
        'muted_review_requests': 'application/json',
        'remote_repositories': 'application/vnd.reviewboard.org.hosting-service-account+json',
        'repository': 'application/vnd.reviewboard.org.repository+json',
        'repositories': 'application/vnd.reviewboard.org.repositories+json',
        'review_requests': 'application/vnd.reviewboard.org.review-requests+json',
        'review_request': 'application/vnd.reviewboard.org.review-request+json',
        'reviews': 'application/json',
        'root': 'application/vnd.reviewboard.org.root+json',
        'screenshots': 'application/json',
        'search': 'application/vnd.reviewboard.org.search+json',
        'session': 'application/vnd.reviewboard.org.session+json',
        'submitter': 'application/json',
        'target_groups': 'application/json',
        'target_people': 'application/json',
        'update': 'application/json',
        'users': 'application/vnd.reviewboard.org.users+json',
        'validation': 'application/json',
        'watched': 'application/json',
        'webhooks': 'application/vnd.reviewboard.org.webhooks+json',
}


class Resource(object):
    """ Generalized Review Board resource.

    Provide uniform getter and setter methods over HTTP to the Review
    Board instance. To achieve this, the methods are decorated to handle the
    response at different levels:

    # sending HTTP commands (e.g, GET and POST)
    # handling the HTTP response (e.g., content type and status code)
    # payload conversion to a whole-part hierarchy

    The whole-part hierarchy is contained within a collection of nested named
    tuples that exactly reflect the response returned by the Review Board
    instance.

    The composite contains a copy of the JSON response from the Review Board
    instance. This permits clients to access the response using a named tuple or
    a dictionary.
    """
    def __init__(self, session, name):
        super(Resource, self).__init__()
        self._session = session
        self._name = name
    @property
    def name(self):
        return self._name
    def composite(fetch):
        """ Build the whole-part hierarchy from Review Board response. """
        @wraps(fetch)
        def _composite(self, href, query_dict = dict()):
            response = fetch(self, href, query_dict)
            assert type(response) is DictType or type(response) is DictionaryType
            return self.component(self._name, response, { 'json': response })
        return _composite
    def contruct_dict_from_http_response(fetch):
        """ Decorator returning a dictionary containing the response. """
        @wraps(fetch)
        def _contruct_dict_from_http_response(self, href, query_dict = dict()):
            return fetch(self, href, query_dict).json()
        return _contruct_dict_from_http_response
    def validate_http_content_type(fetch):
        """ Decorator validating the response's HTTP content type. """
        @wraps(fetch)
        def _validate_http_content_type(self, href, query_dict = dict()):
            response =  fetch(self, href, query_dict)
            response.raise_for_status()
            if content_type[self._name] != response.headers['Content-Type']:
                raise BadContentType(href, response.headers['Content-Type'],
                        content_type[self._name], self._name)
            return response
        return _validate_http_content_type
    @stat.is_valid
    @composite
    @contruct_dict_from_http_response
    @validate_http_content_type
    def delete(self, href, query_dict = dict()):
        """ Execute HTTP DELETE using session parameters. """
        return self._session.delete(href, data = query_dict)
    @stat.is_valid
    @composite
    @contruct_dict_from_http_response
    @validate_http_content_type
    def get(self, href, query_dict = dict()):
        """ Execute HTTP GET using session parameters. """
        return self._session.get(href, params = query_dict)
    @stat.is_valid
    @composite
    @contruct_dict_from_http_response
    @validate_http_content_type
    def post(self, href, query_dict = dict()):
        """ Execute HTTP POST using session parameters. """
        return self._session.post(href, data = query_dict)
    @stat.is_valid
    @composite
    @contruct_dict_from_http_response
    @validate_http_content_type
    def put(self, href, query_dict = dict()):
        """ Execute HTTP PUT using session parameters. """
        return self._session.put(href, data = query_dict)
    def list_component(self, name, response):
        """ Construct a list component.
        """
        args = list()
        for element in response:
            if type(element) is DictType or type(element) is DictionaryType:
                args.append(self.component(name, element))
            else:
                args.append(name)
        return args
    def replace(self, s):
        """ Replace forbidden characters in named tuple names and field names.
        """
        return s.replace("-", "_")
    def component(self, name, response, extra_args = dict()):
        """ Build the whole-part hierarchy making up the composite object. """
        field_names = ' '.join(list(extra_args) + list(response))
        args = dict(extra_args)
        for x in response:
            y = self.replace(x)
            if type(response[x]) is DictType or type(response[x]) is DictionaryType:
                args[y] = self.component(x, response[x])
            elif type(response[x]) is ListType:
                args[y] = self.list_component(x, response[x])
            else:
                args[y] = response[x]
        tuple_descriptor = collections.namedtuple(self.replace(name),
                self.replace(field_names))
        return tuple_descriptor(**args)


class ResourceFactory(Resource):
    """ Review Board resource specialization by URL and HTTP command.

    Permit resource class instances to behave as if they were functions. This
    separates resource construction from use. This relegates construction to to
    the library and leaves client programs to focus on consuming resource
    outputs.
    """
    def __init__(self, session, name, url, method):
        """ Construct the resource. """
        super(ResourceFactory, self).__init__(session, name)
        if 'GET' == method:
            self._fetch = lambda query_dict = dict(): self.get(url, query_dict)
        elif 'POST' == method:
            self._fetch = lambda data_dict = dict(): self.post(url, data_dict)
        else:
            assert 0, "unknown HTTP {0} command needed by {1} resource".format(method, name)
    def __call__(self, query_dict = dict()):
        """ Use the getter to populate the resource.

        The parent resource includes the entire Review Board instance response
        along with an instance of the Resource class for any resource linked to
        the parent resource through the links attribute.
        """
        response = self._fetch(query_dict)
        args = dict()
        if None != getattr(response, 'links', None):
            for links in response.links:
                link_name = type(links).__name__
                if 'self' == link_name:
                    args[link_name] = ResourceFactory(self._session, self.name,
                        links.href, links.method)
                else:
                    args[link_name] = ResourceFactory(self._session, link_name,
                        links.href, links.method)
        resource_tuple = self.component(self._name, args)
        tuple_descriptor = collections.namedtuple(self._name,
            resource_tuple._fields + response._fields)
        return tuple_descriptor(*(resource_tuple + response))
