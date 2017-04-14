from __future__ import unicode_literals

import uuid
import decimal

from django.db import models
from django.utils.translation import ugettext_lazy as _

from authentication.models import User
from cards import constants


class Card(models.Model):
    """
    Debit card
    """
    # TODO: Allow more than one parent to access a card
    # TODO: Remove FKs to User model
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    child = models.ForeignKey(User, on_delete=models.CASCADE, related_name='child_cards',
                              verbose_name=_('Child'), help_text=_('Child user of this card'))
    parent = models.ForeignKey(User, related_name='parent_cards',
                               verbose_name=_('Parent'), help_text=_('Parent user of this card'))
    balance = models.DecimalField(max_digits=6, decimal_places=2, default=decimal.Decimal(0),
                                  verbose_name=_('Balance'), help_text=_('Current card balance'))

    class Meta:
        verbose_name = _('Card')
        verbose_name_plural = _('Cards')


class Transaction(models.Model):
    """
    Card transaction
    """
    # TODO: Update card balance when transaction is created (signals)
    # TODO: Remove FKs to User model
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='card_transactions',
                             verbose_name=_('Card'), help_text=_('Card used in this transaction'))
    user = models.ForeignKey(User, related_name='user_transactions',
                             verbose_name=_('User'), help_text=_('User who has made the transaction'))
    type = models.CharField(max_length=10, choices=constants.TYPES_CHOICES, default=constants.TYPE_EXPENSE,
                            verbose_name=_('Type'), help_text=_('Type of transaction ("expense" by default)'))
    time = models.DateTimeField(auto_now=True, verbose_name=_('Time'), help_text=_('Time of transaction'))
    amount = models.DecimalField(max_digits=5, decimal_places=2, default=decimal.Decimal(0),
                                 verbose_name=_('Amount'), help_text=_('Transaction amount'))
    transaction_id = models.CharField(max_length=8, verbose_name=_('Transaction ID'),
                                      help_text=_('Transaction ID associated with the payment gateway'))

    class Meta:
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')
