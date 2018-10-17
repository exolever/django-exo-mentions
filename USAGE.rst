=====
Usage
=====

To use django-exo-mentions in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'exo_mentions',
        ...
    )

Add this url to your api urls:

.. code-block:: python
    urlpatterns = [
        ...
        url(r'^mentions', include('exo_mentions.api.urls', namespace='mentions')),
        ...
    ]


Define a signal for the callback

.. code-block:: python

    from django.dispatch import receiver
    from django.core.signals import request_finished

    @receiver(request_finished)
    def post_detect_mention_callback(sender, **kwargs):
        """ You will receive information of the mention
        user_from: kwargs.get('user_from')
            User that mentions
        object_pk: kwargs.get('object_pk')
            User's Pk that has been mentioned
        target: kwargs.get('target')
            The object where the mention was made
        """

        # Your code here

Register a model and field in which you want to detect mentions. If you want to get trace about who is the user that has made the mention, ensure the model registered define a property or a model field called created_by.
You can override the pattern if you want.

.. code-block:: python

    from django.apps import AppConfig
    from exo_mentions.registry import register

    class MyAppConfig(AppConfig):
        name = 'myapp'

        def ready(self):
            model = Post
            field = 'description'
            callback = post_detect_mention_callback

            register(model, field, callback)

At this point the library will notify to the callback each time there is a mention in the field of the registered model. Thats all! :)

.. code-block:: python

    def register(model, field, callback, pattern):
    """
    This method handles the mentions about the model in the field and notify to the callback when there is any mention

    Parameters
    ----------
    model : Models
        The model to register for detect mentions
    field : str
        Field of the model to detect mentions
    callback : function
        Callback function to notify when there are mentions
    pattern : regular expression
        The pattern to codify the mentions (default r'class="mention" data-user=[\'"]?([^\'" >]+)')

    """
