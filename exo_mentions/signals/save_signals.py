from ..wrapper import MentionsWrapper


def _construct_wrapper(instance):
    from ..registry import get_model_registered
    wrapper = None

    try:
        original_instance = instance.__class__.objects.filter(
            pk=getattr(instance, 'pk')).first()

        mentioned_model = get_model_registered(instance.__class__)
        field = mentioned_model.get('field')
        callback = mentioned_model.get('callback')
        pattern = mentioned_model.get('pattern')

        wrapper = MentionsWrapper(
            instance=instance,
            user_from=getattr(instance, 'created_by', None),
            text=getattr(instance, field),
            original_text=getattr(original_instance, field, None),
            callback=callback,
            pattern=pattern)

    except KeyError:
        pass

    return wrapper


def post_save_model_detect_mentions(sender, instance, created, *args, **kwargs):
    if created:
        wrapper = _construct_wrapper(instance)
        if wrapper:
            wrapper.detect_mentions()


def pre_save_model_detect_mentions(sender, *args, **kwargs):
    instance = kwargs.get('instance', None)

    if instance and instance.pk:
        wrapper = _construct_wrapper(instance)
        if wrapper:
            wrapper.update_mentions()
