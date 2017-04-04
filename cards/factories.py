import factory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'auth.User'

    username = factory.Sequence(lambda n: 'user{}'.format(n))
    email = factory.LazyAttribute(lambda u: '{}@example.com'.format(u.username))
    is_staff = True


class ParentUserFactory(UserFactory):
    username = factory.Sequence(lambda n: 'parent{}'.format(n))


class ChildUserFactory(UserFactory):
    username = factory.Sequence(lambda n: 'child{}'.format(n))


class CardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'cards.Card'
