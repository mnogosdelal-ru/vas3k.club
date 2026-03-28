import logging

import telegram
from django.conf import settings
from telegram.utils.request import Request

log = logging.getLogger()

if settings.TELEGRAM_TOKEN:
    request = Request(proxy_url=settings.TELEGRAM_PROXY) if settings.TELEGRAM_PROXY else None
    bot = telegram.Bot(token=settings.TELEGRAM_TOKEN, request=request)
else:
    bot = None
