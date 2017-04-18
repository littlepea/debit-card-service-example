import decimal


def parse_money_string(amount):
    return decimal.Decimal(amount[1:])
