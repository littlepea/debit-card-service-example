import mock
from django.test import SimpleTestCase

from authentication.factories import ParentUserFactory, ChildUserFactory
from cards import services, permissions
from cards.factories import CardFactory


class GetUserCardsTestCase(SimpleTestCase):
    @mock.patch('django.db.models.query.QuerySet.filter')
    def test_get_parent_cards(self, filter_method):
        parent = ParentUserFactory.build()
        services.get_user_cards(parent)
        filter_method.assert_called_once_with(parent_id=parent.id)

    @mock.patch('django.db.models.query.QuerySet.filter')
    def test_get_child_cards(self, filter_method):
        child = ChildUserFactory.build()
        services.get_user_cards(child)
        filter_method.assert_called_once_with(child_id=child.id)

    @mock.patch('django.db.models.query.QuerySet.get')
    def test_get_existing_card(self, get_method):
        card_id = '551094cc-5729-463e-a4a3-e586dd45ae6c'
        services.get_card_by_id(card_id)
        get_method.assert_called_once_with(pk=card_id)


class PermissionsTestCare(SimpleTestCase):
    def setUp(self):
        self.parent = ParentUserFactory.build()
        self.child = ChildUserFactory.build()
        self.card = CardFactory.build(parent=self.parent, child=self.child)
        self.permission = permissions.IsParentCardOwner()
        self.view_mock = mock.Mock()

    def test_parent_has_owner_permissions(self):
        request = mock.Mock(user=self.parent)
        self.assertTrue(self.permission.has_object_permission(request, self.view_mock, self.card))

    def test_child_doesnt_have_owner_permissions(self):
        request = mock.Mock(user=self.child)
        self.assertFalse(self.permission.has_object_permission(request, self.view_mock, self.card))
