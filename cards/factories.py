import factory


class CardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'cards.Card'


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'cards.Transaction'
