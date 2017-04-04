from __future__ import unicode_literals

import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from authentication import constants


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=10, choices=constants.USER_TYPE_CHOICES, default=constants.TYPE_PARENT,
                            verbose_name=_('Type'), help_text=_('Type of user ("parent" by default)'))

    @property
    def is_parent(self):
        return self.type == constants.TYPE_PARENT
