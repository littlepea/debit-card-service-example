from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from cards import factories
from cards import models


DEFAULT_PASSWORD = 'i_am_not_safe_to_use'


class Command(BaseCommand):
    help = "Populate cards test data."

    def handle(self, *args, **options):
        self._reset_db()
        self._populate_users()
        self._populate_cards()
        pass

    @staticmethod
    def _reset_db():
        User.objects.filter(is_superuser=False).delete()
        models.Card.objects.all().delete()

    def _populate_users(self):
        self.parent = factories.ParentUserFactory()
        self.parent.set_password(DEFAULT_PASSWORD)
        self.child = factories.ChildUserFactory()
        self.child.set_password(DEFAULT_PASSWORD)

    def _populate_cards(self):
        self.card = factories.CardFactory(child=self.child, parent=self.parent)
