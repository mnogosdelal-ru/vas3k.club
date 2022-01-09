# https://developers.cloudpayments.ru/#api

import base64
import hashlib
import hmac
import logging
from dataclasses import dataclass
from datetime import timedelta
from enum import Enum
from uuid import uuid4

import requests
from django.conf import settings
from requests.auth import HTTPBasicAuth

from payments.products import club_subscription_activator
from users.models.user import User

log = logging.getLogger()

CLOUDPAYMENTS_PRODUCTS = {
    "club1": {
        "code": "club1",
        "description": "Месяц членства в Клубе",
        "amount": 1000,
        "recurrent": False,
        "activator": club_subscription_activator,
        "data": {
            "timedelta": timedelta(days=31),
        },
    },
    "club3": {
        "code": "club3",
        "description": "3 месяца членства в Клубе",
        "amount": 2000,
        "recurrent": False,
        "activator": club_subscription_activator,
        "data": {
            "timedelta": timedelta(days=31 * 3),
        },
    },
    "club12": {
        "code": "club12",
        "description": "Год членства в Клубе",
        "amount": 6000,
        "recurrent": False,
        "activator": club_subscription_activator,
        "data": {
            "timedelta": timedelta(days=365),
        },
    },
    "club1_recurrent": {
        "code": "club1",
        "description": "Месяц членства в Клубе",
        "amount": 1000,
        "recurrent": False,
        "activator": club_subscription_activator,
        "data": {
            "timedelta": timedelta(days=31),
        },
        "regular": "monthly",
    },
    "club3_recurrent": {
        "code": "club3",
        "description": "3 месяца членства в Клубе",
        "amount": 2000,
        "recurrent": False,
        "activator": club_subscription_activator,
        "data": {
            "timedelta": timedelta(days=31 * 3),
        },
        "regular": "monthly",
    },
    "club12_recurrent": {
        "code": "club12",
        "description": "Год членства в Клубе",
        "amount": 6000,
        "recurrent": False,
        "activator": club_subscription_activator,
        "data": {
            "timedelta": timedelta(days=365),
        },
        "regular": "yearly",
    },
}


class TransactionStatus(Enum):
    PENDING = "Pending"
    REFUNDED = "Refunded"
    APPROVED = "Approved"
    UNKNOWN = "Unknown"


@dataclass
class Invoice:
    id: str
    url: str


class CloudPaymentsService:
    @classmethod
    def create_payment(cls, product_code: str, user: User) -> Invoice:
        product_data = CLOUDPAYMENTS_PRODUCTS[product_code]

        order_id = uuid4().hex

        log.info("Try to create payment %s %s", product_code, order_id)

        payload = {
            "Amount": product_data["amount"],
            "Currency": "RUB",
            "Description": product_data["description"],
            "RequireConfirmation": False,
            "InvoiceId": order_id,
            "SuccessRedirectUrl": "https://club.mnogosdelal.ru/intro/",
            "Email": user.email,
        }

        response = requests.post(
            "https://api.cloudpayments.ru/orders/create",
            auth=HTTPBasicAuth(settings.CLOUDPAYMENTS_API_ID, settings.CLOUDPAYMENTS_API_PASSWORD),
            data=payload,
        )

        log.info("Payment answer %s %s", response.status_code, response.text)

        response.raise_for_status()

        invoice = Invoice(
            id=order_id,
            url=response.json()["Model"]["Url"],
        )
        return invoice

    @classmethod
    def verify_webhook(cls, request) -> bool:
        log.info("Verify request")

        secret = bytes(settings.CLOUDPAYMENTS_API_PASSWORD, 'utf-8')

        signature = base64.b64encode(hmac.new(secret, request.body, digestmod=hashlib.sha256).digest())
        log.info('Signature %s against %s', signature, request.META.get('HTTP_CONTENT_HMAC'))

        return signature == bytes(request.META.get('HTTP_CONTENT_HMAC'), 'utf-8')

    @classmethod
    def accept_payment(cls, action: str, payload: dict) -> [TransactionStatus, dict]:
        log.info("Accept action %s, payment %r", action, payload)

        status = TransactionStatus.UNKNOWN

        if action == 'pay':
            status = TransactionStatus.APPROVED

        log.info("Status %s", status)

        return status, {"code": 0}
