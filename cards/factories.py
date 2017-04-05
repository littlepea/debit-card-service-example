import decimal

import factory


class CardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'cards.Card'

    balance = decimal.Decimal(0)


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'cards.Transaction'
