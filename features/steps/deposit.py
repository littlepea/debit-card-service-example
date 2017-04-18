import decimal

from behave import when, then

from cards.models import Card
from features.steps import utils


@when(u'parent deposits {amount}')
def parent_deposit(context, amount):
    context.deposit_amount = utils.parse_money_string(amount)
    context.response = utils.api_post('card-top-up',
                                      pk=context.card.id,
                                      user=context.parent,
                                      amount=context.deposit_amount)


@then(u'the deposit will be successful')
def deposit_successful(context):
    context.test.assertEquals(context.deposit_amount, decimal.Decimal(context.response.data['amount']))


@then(u'the deposit will fail')
def deposit_failed(context):
    context.test.assertEquals(400, context.response.status_code)
    context.test.assertIn('amount', context.response.data['errors'])


@then(u'child\'s balance will be {balance}')
def child_balance(context, balance):
    balance = utils.parse_money_string(balance)
    card = Card.objects.get(id=context.card.id)
    context.test.assertEquals(balance, card.balance)
