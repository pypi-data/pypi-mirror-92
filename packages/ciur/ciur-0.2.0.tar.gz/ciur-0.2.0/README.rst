====
Ciur
====

.. image:: ./docs/images/wooden-sieve-old-ancient-isolated-white-background.jpg
   :target: https://bitbucket.org/ada/python-ciur
   :alt: Ciur

.. contents::

..

    *Ciur is a scrapper layer in code development*

    *Ciur is a lib because it has less black magic than a framework*

It exports all scrapper related code into separate layer.

If you are annoyed by
`Spaghetti code <https://en.wikipedia.org/wiki/Spaghetti_code>`_,
sql inside php and inline css inside html
THEN you also are annoyed by xpath/css code inside crawler.

Ciur gives the taste of `Lasagna code <http://c2.com/cgi/wiki?LasagnaCode>`_
generally by enforcing encapsulation for scrapping layer.

For more information visit the
`documentation <http://python-ciur.readthedocs.io/>`_.


Nutshell
========

Ciur uses own DSL, here is a small example of a ``example.org.ciur`` query:

.. code-block:: yaml

    root `/html/body` +1
        name `.//h1/text()` +1
        paragraph `.//p/text()` +1

This command

.. code-block :: bash

    $ ciur -p http://example.org -r https://bitbucket.org/ada/python-ciur/raw/HEAD/docs/docker/example.org.ciur

Will produce a json

.. code-block :: json

    {
        "root": {
            "name": "Example Domain",
            "paragraph": "This domain is established to be used for illustrative
                           examples in documents. You may use this
                           domain in examples without prior coordination or
                          asking for permission."
        }
    }


Installation
============

.. code-block::

    pip install ciur

Install via docker

.. code-block:: bash

    $ docker run -it python:3.9 bash
    root@e4d327153f2f:/# pip install ciur
    root@e4d327153f2f:/# ciur --help

    root@e4d327153f2f:/# ciur --help
    usage: ciur [-h] -p PARSE -r RULE [-w] [-v]

    *Ciur is a scrapper layer based on DSL for extracting data*

    *Ciur is a lib because it has less black magic than a framework*

    If you are annoyed by `Spaghetti code` than we can taste `Lasagna code`
    with help of Ciur

    https://bitbucket.org/ada/python-ciur

    optional arguments:
      -h, --help            show this help message and exit
      -p PARSE, --parse PARSE
                            url or local file path required document for html, xml, pdf. (f.e. http://example.org or /tmp/example.org.html)
      -r RULE, --rule RULE  url or local file path file with parsing dsl rule (f.e. /tmp/example.org.ciur or http:/host/example.org.ciur)
      -w, --ignore_warn     suppress python warning warnings and ciur warnings hints
      -v, --version         show program's version number and exit


Ciur use MIT License
====================

This means that code may be included in proprietary code without any additional restrictions.

Please see `LICENSE <./LICENSE>`_.


Contribution
============

The code of **Cuir** was concepted in 2012,
and is going to continue developing.

All contributions are welcome and should be done via Bitbucket (Pull Request, Issues).

A second alternative as exception (maybe if bitbucket is not available)
can be done via email ciur[mail symbol]asta-s.eu.
