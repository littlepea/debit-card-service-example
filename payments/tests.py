import decimal

from django.test import SimpleTestCase, override_settings

from payments.backends import BraintreeBackend, backend_factory
from payments.services import pay
from payments.constants import TEST_CUSTOMER_ID, TEST_CREDIT_CARD


class BraintreeBackendTestCase(SimpleTestCase):
    @override_settings(PAYMENT_BACKEND='payments.backends.DummyBackend')
    def setUp(self):
        self.backend = backend_factory()

    def test_client_token(self):
        self.assertIsNotNone(self.backend.client_token)

    def test_get_sale_options(self):
        amount = decimal.Decimal(10)
        customer_id = TEST_CUSTOMER_ID
        options = BraintreeBackend.get_sale_options(amount, customer_id)
        self.assertEqual(amount, options['amount'])
        self.assertEqual(customer_id, options['customer_id'])
        self.assertTrue(options['options']['submit_for_settlement'])

    def test_successful_payment(self):
        self.assertIsNotNone(
            self.backend.create_transaction(decimal.Decimal(10), customer_id=TEST_CUSTOMER_ID))

    def test_get_customer_options(self):
        email = 'name@example.com'
        customer_id = TEST_CUSTOMER_ID
        first_name = 'John'
        options = BraintreeBackend.get_customer_options(email, customer_id=customer_id, first_name=first_name)
        self.assertEqual(email, options['email'])
        self.assertEqual(customer_id, options['id'])
        self.assertEqual(first_name, options['first_name'])

    def test_customer__credit_card_creation(self):
        self.assertIsNotNone(
            self.backend.create_customer('name@example.com', customer_id=TEST_CUSTOMER_ID))
        self.assertIsNotNone(
            self.backend.create_credit_card(TEST_CREDIT_CARD, customer_id=TEST_CUSTOMER_ID, expiration_date='02/22'))

    @override_settings(PAYMENT_BACKEND='payments.backends.BraintreeBackend')
    def test_backend_factory(self):
        self.assertIsInstance(backend_factory(), BraintreeBackend)


class PaymentServiceTestCase(SimpleTestCase):
    @override_settings(PAYMENT_BACKEND='payments.backends.DummyBackend')
    def test_successful_payment(self):
        self.assertIsNotNone(
            pay(decimal.Decimal(10), customer_id=TEST_CUSTOMER_ID))
