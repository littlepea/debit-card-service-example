import braintree
from django.conf import settings


# TODO: `backends` should be a package with a separate module for each backend


class CustomerCreationError(Exception):
    pass


class CreditCardError(Exception):
    pass


class PaymentError(Exception):
    pass


class BraintreeBackend(object):
    """
    Braintree payment backend
    """
    def __init__(self):
        braintree.Configuration.configure(braintree.Environment.Sandbox,
                                          merchant_id=settings.BRAINTREE_MERCHANT_ID,
                                          public_key=settings.BRAINTREE_PUBLIC_KEY,
                                          private_key=settings.BRAINTREE_PRIVATE_KEY)
        self.client_token = braintree.ClientToken.generate()

    def create_customer(self, email, customer_id=None, first_name=None, last_name=None, **kwargs):
        """
        Creates a customer

        :param email: Customer email
        :param customer_id: Customer ID
        :param first_name: First Name
        :param last_name: Last Name
        :param kwargs: Other info
        :return: Customer ID
        """
        result = braintree.Customer.create(self.get_customer_options(email, customer_id=customer_id,
                                                                     first_name=None, last_name=None, **kwargs))
        if result.is_success:
            return result.customer.id

        raise CustomerCreationError(result.message)

    @staticmethod
    def get_customer_options(email, customer_id=None, **kwargs):
        options = {
            "email": email
        }
        if customer_id:
            options['id'] = customer_id
        options.update(kwargs)
        return options

    def create_credit_card(self, number, customer_id, expiration_date, **kwargs):
        """
        Creates a credit/debit card

        :param number: Credit card number
        :param customer_id: Customer ID
        :param expiration_date: Expiration date (ex: 02/22)
        :param kwargs: Other info
        :return: Last 4 digits of the card number
        """
        options = {
            'number': number,
            'customer_id': customer_id,
            'expiration_date': expiration_date
        }
        options.update(kwargs)
        result = braintree.CreditCard.create(options)
        if result.is_success:
            return result.credit_card.last_4

        raise CreditCardError(result.message)

    def create_transaction(self, amount, customer_id):
        """
        Create transaction for the specified amount

        :param amount: Amount to be paid
        :param customer_id: ID of the customer who's payment method will be charged
        :return: Transaction ID
        """
        result = braintree.Transaction.sale(self.get_sale_options(amount, customer_id))
        if result.is_success:
            return result.transaction.id

        raise PaymentError(result.message)

    @staticmethod
    def get_sale_options(amount, customer_id):
        return {
            'amount': amount,
            'customer_id': customer_id,
            'billing': {
                'country_code_alpha2': 'GB'
            },
            'options': {
                'submit_for_settlement': True
            }
        }


class DummyBackend(object):
    def __init__(self):
        self.client_token = 'qwertyuiop1234567890'

    def create_transaction(self, amount, customer_id):
        return 'qwerty12'

    def create_customer(self, email, customer_id=None, first_name=None, last_name=None, **kwargs):
        return customer_id or 'qwerty12'

    def create_credit_card(self, number, customer_id, expiration_date, **kwargs):
        return number[-4:]


BACKEND_CACHE = {}


def backend_factory():
    """
    Return the backend instance based on settings
    """
    backend = getattr(settings, 'PAYMENT_BACKEND', 'payments.backends.DummyBackend')

    if backend not in BACKEND_CACHE:
        module_path, class_name = backend.rsplit('.', 1)
        module = __import__(
            str(module_path), globals(), locals(), [str(class_name)])
        class_ = getattr(module, class_name)
        BACKEND_CACHE[backend] = class_()

    return BACKEND_CACHE[backend]