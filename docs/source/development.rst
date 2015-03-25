Development
===========

The ``memtop`` tool was initially developed by Tibor Bamhor. In March 2015,
the tool was migrated from code.google.com to GitHub and is maintained by
Martin Thoma

It is developed on GitHub: https://github.com/MartinThoma/memtop

You can file issues and feature requests there. Alternatively, you can send
me an email: info@martin-thoma.de

Contributions
-------------

Everybody is welcome to contribute to ``memtop``. You can do so by

* Testing it and giving me feedback / opening issues on GitHub.

* Improving existing code.

* Suggesting something else how you can contribute.


I suggest reading the issues page https://github.com/MartinThoma/memtop/issues
for more ideas how you can contribute.


Tools
-----

* ``nosetests`` for unit testing
* ``pylint`` to find code smug
* GitHub for hosting the source code
* https://pythonhosted.org/memtop for hosting the documentation


Code coverage can be tested with

.. code:: bash

    $ nosetests --with-coverage --cover-erase --cover-package memtop --logging-level=INFO --cover-html

and uploaded to coveralls.io with

.. code:: bash

    $ coveralls


Documentation
-------------

The documentation is generated with `Sphinx <http://sphinx-doc.org/latest/index.html>`_.
On Debian derivates it can be installed with

.. code:: bash

    $ sudo apt-get install python-sphinx

Sphinx makes use of `reStructured Text <http://openalea.gforge.inria.fr/doc/openalea/doc/_build/html/source/sphinx/rest_syntax.html>`_

The documentation can be built with ``make html``.



Current State
-------------

* lines of code without tests: LOC
* lines of test code: LOT
* test coverage: cov
* pylint score: lint

::

    date,              LOC,  LOT, cov, lint, cheesecake_index, changes
    2015-03-25 11:48,  392,    0,  0%, 8.44,                -, some PEP8 changes
    2015-03-25 11:56,  412,    0,  0%, 8.24,                -, maximum line length of 80 chars
    2015-03-25 12:28,  385,    0,  0%, 7.84,                -, use argparse for argument parsing; put code in main()
    2015-03-25 13:42,  390,    0,  0%, 8.52,                -, Pythonized
    2015-03-25 14:48,  879,   25, 46%, 8.52,          295/595, created Packet
