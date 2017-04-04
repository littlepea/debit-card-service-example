import factory


class CardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'cards.Card'
