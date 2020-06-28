import decimal

from behave import given
from freezegun import freeze_time

from cards import constants


@given(u'a child\'s card with a balance of {balance}')
def card_with_balance(context, balance):
    from authentication.factories import ChildUserFactory, ParentUserFactory
    from cards.factories import CardFactory

    context.parent = ParentUserFactory(customer_id='11111111')
    context.child = ChildUserFactory()
    context.card = CardFactory(child=context.child, parent=context.parent, balance=decimal.Decimal(0))


@given(u'a following set of transactions')
def set_of_transactions(context):
    from cards.factories import TransactionFactory

    for row in context.table:
        time = row[0]
        amount = decimal.Decimal(row[1])

        if amount > 0:
            user = context.parent
            transaction_type = constants.TYPE_TOP_UP
        else:
            user = context.child
            transaction_type = constants.TYPE_EXPENSE

        with freeze_time(time):
            transaction = TransactionFactory(card=context.card, user=user, type=transaction_type, amount=amount)


@given(u'today is {date}')
def today(context, date):
    context.freezer = freeze_time(date)
    context.freezer.start()
