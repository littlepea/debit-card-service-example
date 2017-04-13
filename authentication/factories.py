import factory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'authentication.User'

    username = factory.Sequence(lambda n: 'user{}'.format(n))
    first_name = 'John'
    last_name = 'Doe'
    email = factory.LazyAttribute(lambda u: '{}@example.com'.format(u.username))


class ParentUserFactory(UserFactory):
    username = factory.Sequence(lambda n: 'parent{}'.format(n))
    type = 'parent'


class ChildUserFactory(UserFactory):
    username = factory.Sequence(lambda n: 'child{}'.format(n))
    type = 'child'
