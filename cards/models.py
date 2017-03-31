from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
import uuid
import decimal


class Card(models.Model):
    """
    Osper card
    """
    # TODO: Allow more than one parent to access a card
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    child = models.ForeignKey(User, verbose_name=_('Child'), help_text=_('Child user of this card'))
    parent = models.ForeignKey(User, verbose_name=_('Parent'), help_text=_('Parent user of this card'))
    balance = models.DecimalField(decimal_places=2, default=decimal.Decimal(0),
                                  verbose_name=_('Balance'), help_text=_('Current card balance'))

    class Meta:
        verbose_name = _('Card')
        verbose_name_plural = _('Cards')


class Transaction(models.Model):
    """
    Osper card transaction
    """
    EXPENSE = 'expense'
    TOP_UP = 'top-up'
    TYPES_CHOICES = (
        (EXPENSE, _('Expense')),
        (TOP_UP, _('Top-up')),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, verbose_name=_('User'), help_text=_('User who has made the transaction'))
    card = models.ForeignKey(Card, verbose_name=_('Card'), help_text=_('Card used in this transaction'))
    type = models.CharField(max_length=10, choices=TYPES_CHOICES, default=EXPENSE,
                            verbose_name=_('Type'), help_text=_('Type of transaction ("expense" by default)'))
    time = models.DateTimeField(auto_now=True, verbose_name=_('Time'), help_text=_('Time of transaction'))
    amount = models.DecimalField(decimal_places=2, default=decimal.Decimal(0),
                                 verbose_name=_('Amount'), help_text=_('Transaction amount'))

    class Meta:
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')
