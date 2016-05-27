#-------------------------------------------------------------------------------
# rbtlib: rbt.py
#
# Entry point for command-line tool.
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
import click
import json
import magic
import requests
from root import Root
import sys
import user
from urlparse import urlparse


def canonify_url(ctx, url):
    """Create a canonical URL for consumption by the library.

    Args:
        ctx: RBTLIB context.
        url: URL to cannonify.

    Returns:
        The provided URL if it contains a scheme; if the URL is missing a
        scheme generate one.  Try HTTPS then HTTP and include the supported
        scheme with the returned URL.
    """
    url_components = urlparse(url)
    if 0 == len(url_components.scheme):
        scheme = 'https://'
        try:
            ctx.obj['session'].get(scheme + url)
        except requests.exceptions.SSLError:
            scheme = 'http://'
        url = scheme + url
    return url


def beautify(resource):
    """Beautify response.

    Args:
        resource: ResourceFactory instance to beautify.

    Returns:
        A JSON dump of the ResourceFactory instance formatted for readability.
    """
    return json.dumps(resource.json, sort_keys = True, indent = 2)


def login(ctx, url, username, password):
    """User login.

    Log in using the user name and password.

    Args:
        ctx: RBTLIB context.
        url: Review Board URL.
        username: account user name.
        password: account password.

    Returns:
        HTTP status code, not an indicator of a successful login.
    """
    return user.login(ctx.obj['session'], url, username, password)


def url(f):
    """Define the URL callback.

    Args:
        f: callback function.

    Returns:
        The URL callback.
    """
    def callback(ctx, param, url):
        """Apply the URL argument to each command in the group.

        Args:
            ctx: RBTLIB context.
            param: don't know.
            url: URL to cannonify.

        Returns:
            The canonified URL argument to the RBT command.
        """
        return canonify_url(ctx, url)
    return click.argument('url', callback=callback)(f)


@click.group()
@click.pass_context
def rbt(ctx):
    """Declare the command group.

    Ensures the same HTTP session is used by all RBT commands in this session.

    Args:
        ctx: RBTLIB context.
    """
    ctx.obj['session'] = requests.Session()


@rbt.command()
@url
@click.pass_context
def root(ctx, url):
    """Print the Root List Resource.

    Args:
        ctx: RBTLIB context.
        url: Review Board URL.

    Returns:
        Writes to standard output.
    """
    print beautify(Root(ctx.obj['session'], url)())
    sys.exit


@rbt.command(name = 'review-requests')
@click.option('--counts-only', is_flag = True,
    help='If specified, a single count field is returned with the number of results.')
@click.option('--time-added-from',
    help='Earliest date/time the review request is added.')
@click.option('--time-added-to',
    help='Latest date/time the review request is added.')
@url
@click.pass_context
def review_requests(ctx, url, counts_only, time_added_from, time_added_to):
    """Print the Review Requests List Resource.

    The date and time format is YYYY-MM-DD HH:MM:SS or
    {yyyy}-{mm}-{dd}T{HH}:{MM}:{SS} with an optional timezone appended as
    -{HH:MM}.

    Args:
        ctx: RBTLIB context.
        url: Review Board URL.
        counts_only: set to True to obtain review request counts only; False
            otherwise.
        time_added_from: earliest date from which to select review requests.
        time__added_to: latest date from which to select review requests.

    Returns:
        Writes to standard output.
    """
    query_dict = dict()
    if counts_only:
        query_dict['counts-only'] = True
    if time_added_from:
        query_dict['time-added-from'] = time_added_from
    if time_added_to:
        query_dict['time-added-to'] = time_added_to
    print beautify(Root(ctx.obj['session'], url)().review_requests(query_dict))
    sys.exit


def file_name(f):
    """Define the file name callback.

    Args:
        f: callback function.

    Returns:
        The file_name argument to the RBT command.
    """
    def callback(ctx, param, file_name):
        """Get the name of the file to post to Review Board.

        Args:
            ctx: RBTLIB context.
            param: don't know.
            file_name: name of file.

        Returns:
            The file name to the command.
        """
        return file_name
    return click.argument('file_name', callback=callback)(f)


@rbt.command()
@click.pass_context
@click.option('--username', prompt=True)
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True)
@url
@file_name
def post(ctx, url, file_name, username, password):
    """Post file to Review Board.

    Args:
        ctx: RBTLIB context.
        url: Review Board URL.
        username: Review Board user name.
        password: Review Board password.

    Returns:
        The file_name argument to the RBT command.
    """
    review_requests = Root(ctx.obj['session'], url)().review_requests()
    try:
        status_code = login(ctx, url, username, password)
        print status_code
        if requests.codes.ok == status_code:
            create = review_requests.create()
            if 'ok' == create.stat:
                print >> sys.stderr, 'posted review {0}'.format(create.review_request.id)
                print create._fields
                print create.review_request._fields
                update = create.review_request.update({
                    'file': (file_name, open(file_name, 'rb'),
                    magic.from_file(file_name, mime = True), {'Expires': '0'})
                    })
            else:
                print >> sys.stderr, 'failed to post review'
        else:
            print >> sys.stderr, 'failed to login'
    except requests.exceptions.HTTPError as e:
        print e
        raise
    sys.exit
