What is RBTLIB?
---------------

**rbtlib** is a client-side Python package for `Review Board`_.
Use it to write your own Review Board clients.

**rbt** is a simple RBTools clone that uses **rbtlib**.
Use it to collect the Root List and Review Requests List Resources.
Limit Review Requests using **rbt** options snd post review requests.

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

to get a count of reviews.
Or::

    > rbt review-requests reviews.reviewboard.org --time-added-from 2016-02-27

to get a list of reviews from the specified date.

Post a review::

    > rbt post reviews.reviewboard.org /path/to/patch

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
