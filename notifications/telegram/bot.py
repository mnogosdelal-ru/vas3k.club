import logging

import telegram
from django.conf import settings

log = logging.getLogger()

if settings.TELEGRAM_TOKEN:
    kwargs = {}
    if settings.TELEGRAM_API_BASE_URL:
        kwargs["base_url"] = settings.TELEGRAM_API_BASE_URL
    bot = telegram.Bot(token=settings.TELEGRAM_TOKEN, **kwargs)
else:
    bot = None
