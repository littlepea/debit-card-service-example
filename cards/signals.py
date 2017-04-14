from django.db.models.signals import post_save
from django.dispatch import receiver

from cards.models import Transaction
from cards.services import update_card_balance


@receiver(post_save, sender=Transaction)
def update_card_balance_when_transaction_saved(sender, **kwargs):
    update_card_balance(kwargs['instance'])
