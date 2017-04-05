import mock
from django.test import SimpleTestCase

from authentication.factories import ParentUserFactory, ChildUserFactory
from cards import services


@mock.patch('django.db.models.query.QuerySet.filter')
class GetUserCardsTestCase(SimpleTestCase):
    def test_get_parent_cards(self, filter_method):
        parent = ParentUserFactory.build()
        services.get_user_cards(parent)
        filter_method.assert_called_once_with(parent_id=parent.id)

    def test_get_child_cards(self, filter_method):
        child = ChildUserFactory.build()
        services.get_user_cards(child)
        filter_method.assert_called_once_with(child_id=child.id)
