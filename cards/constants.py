from django.utils.translation import ugettext_lazy as _


TYPE_EXPENSE = 'expense'
TYPE_TOP_UP = 'top-up'
TYPES_CHOICES = (
    (TYPE_EXPENSE, _('Expense')),
    (TYPE_TOP_UP, _('Top-up')),
)
