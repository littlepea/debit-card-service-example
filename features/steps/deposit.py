import decimal

from behave import when, then

from cards.models import Card
from features.steps import utils


@when(u'parent deposits {amount}')
def parent_deposit(context, amount):
    amount = utils.parse_money_string(amount)
    response = utils.api_post('card-top-up', pk=context.card.id, user=context.parent, amount=amount)
    context.test.assertEquals(amount, decimal.Decimal(response.data['amount']))


@then(u'child\'s balance becomes {balance}')
def child_balance(context, balance):
    balance = utils.parse_money_string(balance)
    card = Card.objects.get(id=context.card.id)
    context.test.assertEquals(balance, card.balance)
