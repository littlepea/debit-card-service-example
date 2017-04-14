import decimal
import datetime

import mock
from django.test import SimpleTestCase
from freezegun import freeze_time

from authentication.factories import ParentUserFactory, ChildUserFactory
from cards.models import Transaction
from cards import services, permissions
from cards.deposit import CardDepositLimitCalculator
from cards.factories import CardFactory
from cards import constants


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


class PermissionsTestCase(SimpleTestCase):
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


@freeze_time('2017.02.01')
class CardDepositLimitTestCase(SimpleTestCase):
    def test_new_card(self):
        calc = CardDepositLimitCalculator(decimal.Decimal(0))
        self.assertEqual(500, calc.max_deposit_limit)

    def test_daily_limit(self):
        calc = CardDepositLimitCalculator(decimal.Decimal(400), transactions=[
            {'date': datetime.datetime(2017, 01, 20, 9), 'amount': decimal.Decimal(200)},
            {'date': datetime.datetime(2017, 01, 31, 9), 'amount': decimal.Decimal(200)}
        ])
        self.assertEqual(300, calc.max_deposit_limit)

    def test_monthly_limit(self):
        calc = CardDepositLimitCalculator(decimal.Decimal(600), transactions=[
            {'date': datetime.datetime(2016, 12, 10, 9), 'amount': decimal.Decimal(200)},
            {'date': datetime.datetime(2017, 01, 10, 9), 'amount': decimal.Decimal(200)},
            {'date': datetime.datetime(2017, 01, 20, 9), 'amount': decimal.Decimal(200)}
        ])
        self.assertEqual(400, calc.max_deposit_limit)

    def test_yearly_limit(self):
        calc = CardDepositLimitCalculator(decimal.Decimal(200), transactions=[
            {'date': datetime.datetime(2016, 02, 10, 9), 'amount': decimal.Decimal(600)},
            {'date': datetime.datetime(2016, 03, 10, 9), 'amount': decimal.Decimal(600)},
            {'date': datetime.datetime(2016, 04, 20, 9), 'amount': decimal.Decimal(600)},
            {'date': datetime.datetime(2017, 01, 20, 9), 'amount': decimal.Decimal(-800)},
            {'date': datetime.datetime(2017, 01, 21, 9), 'amount': decimal.Decimal(-800)}
        ])
        self.assertEqual(200, calc.max_deposit_limit)

    def test_balance_limit(self):
        calc = CardDepositLimitCalculator(decimal.Decimal(800), transactions=[
            {'date': datetime.datetime(2016, 02, 10, 9), 'amount': decimal.Decimal(800)},
        ])
        self.assertEqual(200, calc.max_deposit_limit)

    def test_montly_limit_in_complex_scenario(self):
        calc = CardDepositLimitCalculator(decimal.Decimal(399.17), transactions=[
            {'date': datetime.datetime(2016, 03, 10, 9), 'amount': decimal.Decimal(600.50)},
            {'date': datetime.datetime(2017, 01, 20, 9), 'amount': decimal.Decimal(499.50)},
            {'date': datetime.datetime(2017, 01, 21, 9), 'amount': decimal.Decimal(-800.88)},
            {'date': datetime.datetime(2017, 01, 31, 9), 'amount': decimal.Decimal(100.05)}
        ])
        self.assertEqual(200.45, round(calc.max_deposit_limit, 2))


class CardDepositServiceTestCase(SimpleTestCase):
    def test_create_deposit_transaction(self):
        parent = ParentUserFactory.build()
        child = ChildUserFactory.build()
        card = CardFactory.build(parent=parent, child=child)
        transaction_id = '12345678'
        amount = decimal.Decimal(10)
        transaction = services.create_deposit_transaction(transaction_id, card, amount)
        self.assertIsInstance(transaction, Transaction)
        self.assertEqual(transaction_id, transaction.transaction_id)
        self.assertEqual(amount, transaction.amount)
        self.assertEqual(constants.TYPE_TOP_UP, transaction.type)
