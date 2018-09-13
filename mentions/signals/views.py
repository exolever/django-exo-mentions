from ..wrapper import MentionsWrapper


def post_save_model_detect_mentions(sender, instance, created, *args, **kwargs):
    from ..registry import REGISTRY

    if created:
        try:
            field = REGISTRY[instance.__class__].get('field')
            callback = REGISTRY[instance.__class__].get('callback')

            MentionsWrapper(
                instance=instance,
                user_from=instance.created_by,
                text=getattr(instance, field),
                callback=callback).detect_mentions()

        except KeyError:
            pass
