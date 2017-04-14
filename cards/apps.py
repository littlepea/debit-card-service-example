from __future__ import unicode_literals

from django.apps import AppConfig


class CardsConfig(AppConfig):
    name = 'cards'

    def ready(self):
        from cards import signals
