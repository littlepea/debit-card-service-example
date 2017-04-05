from cards.models import Card


def get_user_cards(user):
    lookup = {'{}_id'.format(user.type): user.id}
    return Card.objects.filter(**lookup)


def deposit_funds(card_id, amount):
    """
    Deposit funds to a card

    :param card_id: Card ID
    :param amount: Amount to deposit
    """
    raise NotImplementedError('top-up action is not implemented yet')
