import datetime

from cards import constants


class CardDepositLimitCalculator(object):
    """
    Helps calculate the max deposit limit
    """
    def __init__(self, balance, transactions=None):
        self.balance = balance
        self.transactions = transactions or []

    @property
    def max_deposit_limit(self):
        return min([
            self.daily_limit,
            self.monthly_limit,
            self.yearly_limit,
            self.balance_limit
        ])

    @property
    def daily_limit(self):
        return constants.DEPOSIT_DAY_LIMIT - self._deposited_in_the_past_days(1)

    @property
    def monthly_limit(self):
        return constants.DEPOSIT_MONTH_LIMIT - self._deposited_in_the_past_days(30)

    @property
    def yearly_limit(self):
        return constants.DEPOSIT_YEAR_LIMIT - self._deposited_in_the_past_days(365)

    @property
    def balance_limit(self):
        return constants.DEPOSIT_BALANCE_LIMIT - self.balance

    def _deposited_in_the_past_days(self, days=1):
        return sum([
            t['amount']
            for t in self.transactions
            if self._date_within_days(t['time'], days)
            and t['amount'] > 0
        ])

    @staticmethod
    def _date_within_days(date, days):
        return (datetime.datetime.now() - date.replace(tzinfo=None)).days < days
