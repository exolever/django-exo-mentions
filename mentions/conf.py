import logging

# 3rd. libraries imports
from appconf import AppConf

# django imports
from django.conf import settings  # noqa

logger = logging.getLogger(__name__)


class MentionsConfig(AppConf):
    DEFAULT_PATTERN = r'class="mention" data-user=[\'"]?([^\'" >]+)'
