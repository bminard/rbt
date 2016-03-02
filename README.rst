Introduction: what is rbt?
--------------------------

**rbt** is a simple RBTools clone. **rbtlib** is a client-side library
for Review Board.

Use **rbt** to collect the Root Resource, Review Requests. Limit review
request using a few parameters.

Pre-requisites
--------------

**rbt** requires Python to run. See ``setup.py`` for dependencies.

Installing
----------

**rbt** can be installed from PyPi (Python package index)::

    > pip install rbt

Alternatively, download the source distribution either from PyPi or
the main Github project page. When you unzip the source distribution, run::

    > python setup.py install

Running without installing
--------------------------

**rbt** supports direct invocation without installing it.

Unzip the **rbt** distribution into a directory. Let's assume its full
path is ``/path/to/rbt``. You can now run::

    > /path/to/python /path/to/rbt

And this will invoke **rbt** as expected. This command can also be tied to an
alias or placed in a shell (or batch) script.

How to use it?
--------------

**rbt** is meant to be executed from the command line. Running it with no
arguments or with ``--help`` prints a detailed usage message. You can run::

    > rbt review-requests reviews.reviewboard.org --counts-only

to get a count of reviews. Or::

    > rbt review-requests reviews.reviewboard.org --time-added-from 2016-02-27

to get a list of reviews from the specified date.

Write your own clients using the **rbtlib** APIs.

License
-------

**rbt** is open-source software. See the ``LICENSE`` file for more details.
