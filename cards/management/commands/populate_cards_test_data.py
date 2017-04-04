from django.core.management.base import BaseCommand

from authentication.models import User
from authentication.factories import ChildUserFactory, ParentUserFactory
from cards.models import Card
from cards.factories import CardFactory


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
        Card.objects.all().delete()

    def _populate_users_and_cards(self, amount=1):
        for i in range(amount):
            parent = ParentUserFactory.build()
            parent.set_password(DEFAULT_PASSWORD)
            parent.save()
            child = ChildUserFactory.build()
            child.set_password(DEFAULT_PASSWORD)
            child.save()
            card = CardFactory(child=child, parent=parent)
            pass
