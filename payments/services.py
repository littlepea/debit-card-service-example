from payments.backends import backend_factory


def pay(amount, customer_id):
    """
    Charges the customer a specified amount

    :param amount: Amount to be paid
    :param customer_id: ID of the customer who's payment method will be charged
    :return: Transaction ID
    """
    backend = backend_factory()
    return backend.create_transaction(amount, customer_id)


def create_customer(user):
    """
    Creates a customer in the gateway vault

    :param user: User instance
    :return: Customer ID
    """
    backend = backend_factory()
    return backend.create_customer(user.email, customer_id=user.customer_id,
                                   first_name=user.first_name, last_name=user.last_name)


def create_credit_card(number, customer_id, expiration_date):
    """
    Creates a customer in the gateway vault

    :param number: Credit card number
    :param customer_id: Customer ID
    :param expiration_date: Expiration date (ex: 02/22)
    :return: Last 4 digits of the card number
    """
    backend = backend_factory()
    return backend.create_credit_card(number, customer_id, expiration_date)