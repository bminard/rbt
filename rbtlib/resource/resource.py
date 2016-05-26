#-------------------------------------------------------------------------------
# rbtlib: resource.py
#
# Get a namedtuple response from a URL.
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
    """HTTP response contains unexpected content type."""


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
    """Generalized resource.

    Provide uniform getter and setter methods over HTTP to Review Board. To
    achieve this, the methods are decorated to handle the response at different
    levels:

    - sending HTTP commands (e.g, GET and POST)
    - handling the HTTP response (e.g., content type and status code)
    - payload conversion to a whole-part hierarchy

    The whole-part hierarchy is in a namedtuple containing the Review Board response.

    The composite contains a copy of the JSON response from Review Board. This
    permits clients to access the response using a namedtuple or dictionary.

    Attributes:
        session: HTTP session.
        name: Resource name.
    """

    def __init__(self, session, name):
        super(Resource, self).__init__()
        self._session = session
        self._name = name

    @property
    def name(self):
        return self._name

    @staticmethod
    def is_dict(item):
        """Determine if item's type is a dictionary type.

        Args:
            item: item to make type determination on

        Returns:
            True is the item is a dictionary type; False otherwise.
        """
        return type(item) is DictType or type(item) is DictionaryType

    def composite(fetch):
        """Build the whole-part hierarchy from the HTTP response.

        Args:
            fetch: a function object defining an HTTP command.

        Returns:
            A function object generating a composite from the obtained data.
        """
        @wraps(fetch)
        def _composite(self, href, payload = dict()):
            """Generate the composite object from the HTTP response.

            Args:
                href: A hypertext reference used by the HTTP command.
                payload: A dictionary containing HTTP command parameters.

            Returns:
                A composite object containing the whole-part hierarchy.
            """
            response = fetch(self, href, payload)
            assert True == self.is_dict(response)
            return self.component(self._name, response, { 'json': response })
        return _composite

    def contruct_dict_from_http_response(fetch):
        """Decorator returning a dictionary containing the HTTP response.

        Args:
            fetch: a function object defining an HTTP command.

        Returns:
            A dictionary containing the payload returned by the HTTP command.
        """
        @wraps(fetch)
        def _contruct_dict_from_http_response(self, href, payload = dict()):
            """Construct a dictionary from the HTTP response.

            Args:
                href: A hypertext reference used by the HTTP command.
                payload: A dictionary containing HTTP command parameters.

            Returns:
                A dictionary defining the response to the HTTP command.
            """
            return fetch(self, href, payload).json()
        return _contruct_dict_from_http_response

    def validate_http_content_type(fetch):
        """Decorator validating the response's HTTP content type.

        Args:
            fetch: a function object defining an HTTP command.

        Returns:
            A function object for checking the HTTP Content-Type.
        """
        @wraps(fetch)
        def _validate_http_content_type(self, href, payload = dict()):
            """Validate the HTTP content type.

            Args:
                href: A hypertext reference used by the HTTP command.
                payload: A dictionary containing HTTP command parameters.

            Returns:
                A dictionary defining the response to the HTTP command.

            Raises:
                BadContentType: The expected and returned HTTP content
                type do not match.
            """
            response =  fetch(self, href, payload)
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
    def delete(self, href):
        """Execute HTTP DELETE command using session parameters.

        Args:
            href: A hypertext reference used by the HTTP command.

        Returns:
            The HTTP response to the HTTP command.
        """
        return self._session.delete(href)

    @stat.is_valid
    @composite
    @contruct_dict_from_http_response
    @validate_http_content_type
    def get(self, href, params_dict = dict()):
        """Execute HTTP GET command using session parameters.

        Args:
            href: A hypertext reference used by the HTTP command.
            params_dict: A dictionary containing HTTP command parameters.

        Returns:
            The HTTP response to the HTTP command.
        """
        return self._session.get(href, params = params_dict)

    @stat.is_valid
    @composite
    @contruct_dict_from_http_response
    @validate_http_content_type
    def post(self, href, data_dict = dict()):
        """Execute HTTP POST command using session parameters.

        Args:
            href: A hypertext reference used by the HTTP command.
            data_dict: A dictionary containing HTTP command parameters.

        Returns:
            The HTTP response to the HTTP command.
        """
        return self._session.post(href, data = data_dict)

    @stat.is_valid
    @composite
    @contruct_dict_from_http_response
    @validate_http_content_type
    def put(self, href, query_dict = dict()):
        """Execute HTTP PUT command using session parameters.

        Args:
            href: A hypertext reference used by the HTTP command.
            query_dict: A dictionary containing HTTP command parameters.

        Returns:
            The HTTP response to the HTTP command.
        """
        return self._session.put(href, data = query_dict)

    def list_component(self, name, response):
        """Construct a list component from the response.

        Args:
            name: the key string identifying the list in the response.
            response: a list.

        Returns:
            A dictionary containing list components.
        """
        args = list()
        for element in response:
            if self.is_dict(element):
                args.append(self.component(name, element))
            else:
                args.append(name)
        return args

    def replace(self, s):
        """Replace forbidden characters in namedtuple names and field names.

        Args:
            s: a string.

        Returns:
            A string with the required substitutions.
        """
        return s.replace("-", "_")

    def component(self, name, response, extra_args = dict()):
        """Build the whole-part hierarchy making up the composite object.

        Recursively create a whole-part hierarchy of the response. Extra
        arguments can be embedded within the whole-part hierarchy at this level
        only.

        Args:
            name: the component name.
            response: the response defining the component.
            extra_args: arguments to add to the component.

        Returns:
            A namedtuple comprising the whole-part hierarchy contained with the
            response along with any extra arguments.
        """
        field_names = ' '.join(list(extra_args) + list(response))
        args = dict(extra_args)
        for x in response:
            y = self.replace(x)
            if self.is_dict(response[x]):
                args[y] = self.component(x, response[x])
            elif type(response[x]) is ListType:
                args[y] = self.list_component(x, response[x])
            else:
                args[y] = response[x]
        tuple_descriptor = collections.namedtuple(self.replace(name),
                self.replace(field_names))
        return tuple_descriptor(**args)


class ResourceFactory(Resource):
    """Resource specialization by URL and HTTP command.

    Permit resource class instances to behave as functions. This separates
    resource construction from use. This relegates construction to the library
    and leaves client programs to focus on consuming resource outputs.

    Attributes:
        session: HTTP session.
        name: Resource name.
        url: Resource URL.
        method: the HTTP method required to fetch the resource.
        fetch: the HTTP command to fetch the resource.
    """
    def __init__(self, session, name, url, method):
        """Construct the resource.

        Use the method to define a closure on the URL for the HTTP command.
        """
        super(ResourceFactory, self).__init__(session, name)
        if 'DELETE' == method:
            self._fetch = lambda: self.delete(url)
        elif 'GET' == method:
            self._fetch = lambda params_dict = dict(): self.get(url,
                                                                params_dict)
        elif 'POST' == method:
            self._fetch = lambda data_dict = dict(): self.post(url, data_dict)
        elif 'PUT' == method:
            self._fetch = lambda data_dict = dict(): self.put(url, data_dict)
        else:
            assert 0, "unknown HTTP {0} command needed by {1} resource".format(method, name)

    def __call__(self, payload = dict()):
        """Populate the resource.

        The parent resource includes the entire Review Board response and an
        instance of the ResourceFactory class for each linked resource.

        The top-level component is an amalgamation of the composite defined by
        the Review Board response and ResourceFactory objects for each child
        resource contained therein.

        The Review Board response is available through the json attribute of the
        top-level component only.

        Args:
            payload: the payload provided to the HTTP command defined by fetch.

        Returns:
            A namedtuple comprising the whole-part hierarchy containing the
            HTTP command response and ResourceFactory objects for each linked
            child resource.
        """
        return self.get_links(self._name, self._fetch(payload))

    def get_links(self, name, response):
        """Generate namedtuple for each linked resource.

        Args:
            name: the name of the component to check for links.
            response: the namedtuple containing the named component.

        Returns:
            A namedtuple comprising the whole-part hierarchy containing the
            HTTP command response and ResourceFactory objects for each linked
            child resource.
        """
        args = dict()
        for item in response._fields:
            if 'links' == item:
                for link in getattr(response, "links"):
                    link_name = type(link).__name__
                    if 'self' == link_name:
                        args[link_name] = ResourceFactory(self._session,
                                                          self.name, link.href,
                                                          link.method)
                    else:
                        args[link_name] = ResourceFactory(self._session,
                                                          link_name, link.href,
                                                          link.method)
                resource_tuple = self.component(item, args)
                tuple_descriptor = collections.namedtuple(item,
                                                  resource_tuple._fields +
                                                  response._fields)
                return tuple_descriptor(*(resource_tuple +
                                                    response))
            elif isinstance(getattr(response, item), tuple):
                resource_tuple = self.get_links(item, getattr(response, item))
                tuple_descriptor = collections.namedtuple(item,
                                                  resource_tuple._fields +
                                                  response._fields)
                return tuple_descriptor(*(resource_tuple + response))
        return response
