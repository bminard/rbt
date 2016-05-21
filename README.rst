What is RBTLIB?
---------------

.. image:: https://travis-ci.org/bminard/rbtlib.svg?branch=master
    :target: https://travis-ci.org/bminard/rbtlib
    :alt: Travis CI Build Status

.. image:: https://readthedocs.org/projects/rbtlib/badge/?version=latest
    :target: http://rbtlib.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

**rbtlib** is a client-side Python package for `Review Board`_.
Use it to write your own Review Board clients.

**rbt** is a simple RBTools clone that uses **rbtlib**.
Use it to collect the Root List and Review Requests List Resources.
Limit Review Requests using **rbt** options snd post review requests.

Documentation for **rbtlib** and **rbt** is available on `readthedocs.org`_.

Pre-requisites
--------------

**rbtlib** and **rbt** require Python to run.
See ``setup.py`` for dependencies.

Installing
----------

**rbtlib** can be installed from PyPi (Python package index)::

    > pip install rbtlib

Alternatively, download the source distribution either from PyPi or
the main Github project page. When you unzip the source distribution, run::

    > python setup.py install

Running rbt without installing
------------------------------

**rbt** supports direct invocation without installing it.

Unzip the **rbt** distribution into a directory.
Let's assume its full path is ``/path/to/rbt``.
Run::

    > /path/to/python /path/to/rbt

This will invoke **rbt** as expected.
This command can also be tied to an alias or placed in a shell (or batch) script.

How to use it?
--------------

**rbt** is meant to be executed from the command line. Running it with no
arguments or with ``--help`` prints a detailed usage message.
Run::

    > rbt review-requests reviews.reviewboard.org --counts-only
    {
      "count": 144,
      "stat": "ok"
    }

to get a count of reviews.
Or::

    > rbt review-requests reviews.reviewboard.org --time-added-from 2016-02-27
    {
      "links": {
        "create": {
          "href": "https://reviews.reviewboard.org/api/review-requests/",
          "method": "POST"
        },
        "next": {
          "href": "https://reviews.reviewboard.org/api/review-requests/?start=25&max-results=25&time-added-from=2016-02-27",
          "method": "GET"
        },
        "self": {
          "href": "https://reviews.reviewboard.org/api/review-requests/?time-added-from=2016-02-27",
          "method": "GET"
        }
      },
      "review_requests": [
        ...
      ],
      "stat": "ok",
      "total_results": 32
    }

to get a list of reviews from the specified date.

Post a review::

    > rbt post demo.reviewboard.org /path/to/patch
    Username: guest6894
    Password: ****
    Repeat for confirmation: ****
    posted review 1755

Write your own client using the **rbtlib** API.

License
-------

**rbtlib** is open-source software. See the ``LICENSE`` file for more details.

Acknowledgements
----------------

**rbtlib** wouldn't exist if it weren't for the Review Board team's Web API
documentation.
It's well documented.
Thank you!

.. _Review Board: https://www.reviewboard.org
.. _readthedocs.org: http://rbtlib.readthedocs.io/en/latest/
