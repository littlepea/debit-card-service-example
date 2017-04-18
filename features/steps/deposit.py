import decimal

from behave import when, then
from rest_framework.test import APIClient

from cards.models import Card
from features.steps import utils


@when(u'parent deposits {amount}')
def parent_deposit(context, amount):
    amount = utils.parse_money_string(amount)
    client = APIClient()
    client.force_authenticate(context.parent)
    response = client.post('/api/cards/{}/top-up/'.format(context.card.id), {'amount': amount}, format='json')
    context.test.assertEquals(amount, decimal.Decimal(response.data['amount']))


@then(u'child\'s balance becomes {balance}')
def child_balance(context, balance):
    balance = utils.parse_money_string(balance)
    card = Card.objects.get(id=context.card.id)
    context.test.assertEquals(balance, card.balance)
