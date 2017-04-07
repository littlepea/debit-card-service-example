from django.utils.translation import ugettext_lazy as _


# Transaction types
TYPE_EXPENSE = 'expense'
TYPE_TOP_UP = 'top-up'
TYPES_CHOICES = (
    (TYPE_EXPENSE, _('Expense')),
    (TYPE_TOP_UP, _('Top-up')),
)

# Deposit limits
DEPOSIT_DAY_LIMIT = 500
DEPOSIT_MONTH_LIMIT = 800
DEPOSIT_YEAR_LIMIT = 2000
DEPOSIT_BALANCE_LIMIT = 1000
