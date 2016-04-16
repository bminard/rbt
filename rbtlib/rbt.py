#-------------------------------------------------------------------------------
# rbt: rbt.py
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
from review_requests import ReviewRequests
from root import Root
import sys
from urlparse import urlparse


def canonify_url(ctx, url):
    """ Create a canonical URL for consumption by the library.

    If the URL is missing a scheme try HTTPS then HTTP.
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


def beautify(resource, query_dict = None):
    """ Beautify response.
    """
    return json.dumps(resource.get(query_dict).json, sort_keys = True, indent = 2)


def login(ctx, url, username, password):
    """ User login.

    Returns HTTP status code, not an indicator of a successful login.
    """
    URL = url + '/account/login/'
    r = ctx.obj['session'].get(URL)
    if 200 == r.status_code:
        login_data  =  dict(username = username, password = password,
            csrfmiddlewaretoken = ctx.obj['session'].cookies['csrftoken'], next = '/')
        r = ctx.obj['session'].post(URL, data = login_data, headers = dict(Referer = URL))
    return r.status_code


def url_argument(f):
    """ Apply the URL argument to each command in the group.
    """
    def callback(ctx, param, url):
        return canonify_url(ctx, url)
    return click.argument('url', callback=callback)(f)


@click.group()
@click.pass_context
def rbt(ctx):
    """ Declare the command group.
    """
    ctx.obj['session'] = requests.Session()


@rbt.command()
@url_argument
@click.pass_context
def root(ctx, url):
    """ Show root resource.
    """
    print beautify(Root(ctx.obj['session'], url))
    sys.exit


@rbt.command(name = 'review-requests')
@click.option('--counts-only', is_flag = True,
    help='If specified, a single count field is returned with the number of results.')
@click.option('--time-added-from',
    help='Earliest date/time the review request is added.')
@click.option('--time-added-to',
    help='Latest date/time the review request is added.')
@url_argument
@click.pass_context
def review_requests(ctx, url, counts_only, time_added_from, time_added_to):
    """ Show review requests resource.

    The date and time format is YYYY-MM-DD HH:MM:SS or
    {yyyy}-{mm}-{dd}T{HH}:{MM}:{SS} with an optional timezone appended as
    -{HH:MM}.
    """
    query_dict = dict()
    if counts_only:
        query_dict['counts-only'] = True
    if time_added_from:
        query_dict['time-added-from'] = time_added_from
    if time_added_to:
        query_dict['time-added-to'] = time_added_to
    print beautify(ReviewRequests(Root(ctx.obj['session'], url)), query_dict)
    sys.exit


def file_argument(f):
    """ Get the file name to post to Review Board.
    """
    def callback(ctx, param, file_name):
        return file_name
    return click.argument('file_name', callback=callback)(f)


@rbt.command()
@click.pass_context
@click.option('--username', prompt=True)
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True)
@url_argument
@file_argument
def post(ctx, url, file_name, username, password):
    """ Post file to Review Board.
    """
    review_requests = ReviewRequests(Root(ctx.obj['session'], url)).get()
    if 200 == login(ctx, url, username, password):
        response =  review_requests.links.create.post({
            'file': (file_name, open(file_name, 'rb'),
                magic.from_file(file_name, mime = True), {'Expires': '0'})
            })
    else:
        print sys.stderr, 'failed to login'
    sys.exit
