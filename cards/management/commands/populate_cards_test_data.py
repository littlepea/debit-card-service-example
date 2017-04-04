from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from cards import factories
from cards import models


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
        models.Card.objects.all().delete()

    def _populate_users_and_cards(self, amount=1):
        for i in range(amount):
            parent = factories.ParentUserFactory.build()
            parent.set_password(DEFAULT_PASSWORD)
            parent.save()
            child = factories.ChildUserFactory.build()
            child.set_password(DEFAULT_PASSWORD)
            child.save()
            card = factories.CardFactory(child=child, parent=parent)
            pass
