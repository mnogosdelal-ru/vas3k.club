import logging

import telegram
from django.conf import settings
from telegram.utils.request import Request

log = logging.getLogger()

if settings.TELEGRAM_TOKEN:
    _request = Request(
        proxy_url=settings.TELEGRAM_PROXY_URL,
        urllib3_proxy_kwargs={"secret": settings.TELEGRAM_PROXY_SECRET},
    )
    bot = telegram.Bot(token=settings.TELEGRAM_TOKEN, request=_request)
else:
    bot = None
