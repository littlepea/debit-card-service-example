from __future__ import unicode_literals

import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from authentication import constants


class User(AbstractUser):
    # TODO: move `customer_id` into a separate application `customers.models.Customer`
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=10, choices=constants.USER_TYPE_CHOICES, default=constants.TYPE_PARENT,
                            verbose_name=_('Type'), help_text=_('Type of user ("parent" by default)'))
    customer_id = models.CharField(max_length=8, verbose_name=_('Customer ID'),
                                   help_text=_('Customer ID associated with the payment gateway'))

    @property
    def is_parent(self):
        return self.type == constants.TYPE_PARENT
