from datetime import datetime, timedelta

from django.db import transaction

from payments.services import pay
from cards.models import Card, Transaction
from cards import constants
from deposit import CardDepositLimitCalculator


def get_user_cards(user):
    """
    Returns user's cards

    :param user: User instance
    :return: Cards queryset
    """
    lookup = {'{}_id'.format(user.type): user.id}
    return Card.objects.filter(**lookup)


def get_card_by_id(card_id):
    """
    Return a Card by it's ID

    :param card_id: Card ID
    :return: Card instance
    """
    return Card.objects.get(pk=card_id)


def get_max_deposit_limit(card):
    """
    Returs the max deposit limit for a card

    :param card: Card instance or ID
    :return: Deposit limit
    """
    if not isinstance(card, Card):
        card = get_card_by_id(card)

    # TODO: extract transactions querying into a separate service method
    date_from = datetime.today() - timedelta(days=365)
    transactions = list(card.card_transactions.filter(time__gte=date_from).values('time', 'amount'))
    calc = CardDepositLimitCalculator(card.balance, transactions)
    return calc.max_deposit_limit


def create_deposit_transaction(id, card, amount):
    """
    Saves a deposit transaction

    :param id: Transaction ID
    :param card: Card instance
    :param amount: Amount that was deposited
    """
    return Transaction(card=card,
                       user=card.parent,
                       type=constants.TYPE_TOP_UP,
                       amount=amount,
                       transaction_id=id)


@transaction.atomic
def deposit_funds(card_id, amount):
    """
    Deposit funds to a card

    :param card_id: Card ID
    :param amount: Amount to deposit
    """
    card = get_card_by_id(card_id)
    transaction_id = pay(amount, card.parent.customer_id)
    deposit = create_deposit_transaction(transaction_id, card, amount)
    deposit.save()
    return deposit


def update_card_balance(transaction):
    """
    Applies a transaction to reflect of card balance

    :param transaction: Transaction instance
    """
    card = get_card_by_id(transaction.card_id)
    card.balance += transaction.amount
    card.save()