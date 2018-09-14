=============================
django-mentions
=============================

.. image:: https://badge.fury.io/py/django-mentions.svg
    :target: https://badge.fury.io/py/django-mentions

.. image:: https://travis-ci.org/marfyl/django-mentions.svg?branch=master
    :target: https://travis-ci.org/marfyl/django-mentions

.. image:: https://codecov.io/gh/marfyl/django-mentions/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/marfyl/django-mentions

Documentation
-------------

The full documentation is at https://django-mentions.readthedocs.io.

Quickstart
----------

Install django-mentions::

    pip install django-mentions

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'mentions',
        ...
    )

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox
