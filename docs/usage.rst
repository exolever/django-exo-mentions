=====
Usage
=====

To use django-mentions in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'mentions',
        ...
    )

Register the models in which you want to detect mentions

.. code-block:: python

    from mentions.registry import register

    register(model, field, callback, pattern)