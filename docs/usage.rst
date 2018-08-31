=====
Usage
=====

To use django-mentions in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'mentions.apps.MentionsConfig',
        ...
    )

Add django-mentions's URL patterns:

.. code-block:: python

    from mentions import urls as mentions_urls


    urlpatterns = [
        ...
        url(r'^', include(mentions_urls)),
        ...
    ]
