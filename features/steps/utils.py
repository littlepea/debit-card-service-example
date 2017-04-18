import decimal

from rest_framework.reverse import reverse
from rest_framework.test import APIClient


def parse_money_string(amount):
    return decimal.Decimal(amount[1:])


def api_post(viewname, pk, user, **kwargs):
    client = APIClient()
    client.force_authenticate(user)
    return client.post(reverse(viewname, [pk]), kwargs, format='json')
