from cards.models import Card


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
    card = Card.objects.get(pk=card_id)
    return card


def deposit_funds(card_id, amount):
    """
    Deposit funds to a card

    :param card_id: Card ID
    :param amount: Amount to deposit
    """
    raise NotImplementedError('top-up action is not implemented yet')
