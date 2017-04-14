import decimal
import random

from django.core.management.base import BaseCommand

from authentication.models import User
from authentication.factories import ChildUserFactory, ParentUserFactory
from payments.services import create_customer, create_credit_card
from payments.constants import TEST_CREDIT_CARD
from cards.models import Card, Transaction
from cards.factories import CardFactory, TransactionFactory
from cards import constants
from cards.services import deposit_funds


DEFAULT_PASSWORD = 'i_am_not_safe_to_use'


class Command(BaseCommand):
    help = "Populate cards test data."

    def handle(self, *args, **options):
        self._reset_db()
        self._populate_users_and_cards(3)
        pass

    @staticmethod
    def _reset_db():
        User.objects.filter(is_superuser=False).delete()
        Transaction.objects.all().delete()
        Card.objects.all().delete()

    def _populate_users_and_cards(self, amount=1):
        customer_id = str(random.randint(10000000, 99999999))
        parent = ParentUserFactory.build(customer_id=customer_id)
        parent.set_password(DEFAULT_PASSWORD)
        parent.save()
        create_customer(parent)
        create_credit_card(TEST_CREDIT_CARD, customer_id, expiration_date='02/22')

        child = ChildUserFactory.build()
        child.set_password(DEFAULT_PASSWORD)
        child.save()

        card = CardFactory(child=child, parent=parent, balance=decimal.Decimal(70))
        deposit_funds(card.id, amount=decimal.Decimal(100))

        TransactionFactory(card=card, user=child,
                           type=constants.TYPE_EXPENSE, amount=decimal.Decimal(-10))
        TransactionFactory(card=card, user=child,
                           type=constants.TYPE_EXPENSE, amount=decimal.Decimal(-20))
