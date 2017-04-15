# Debit Card Service

This codebase is just an example of a Django + DRF service implementation 
for children's debit cards managed by their parents.

This is not a real project, just a code demo.

## Background

It's an API for managing children debit cared by parents based on compliance limits.

A debit card is a prepaid card that holds a balance. 
Parents load their child's debit card using their own debit card, 
ie. money goes from the parent's debit card to their child's debit card. 

This debit card transaction is processed just like a normal e-commerce transaction 
using a standard payment processor like Stripe or Braintree. 

Before we take the money from the parent, we need to check that the load does not exceed compliance limits.

The limits are as follows:
- maximum £500 worth of loads per day
- maximum £800 worth of loads per 30 days
- maximum £2000 worth of loads per 365 days
- maximum balance at any time £1000

This API service handles this use case. 
The service should use Braintree Payments as it's backend processor.  
Braintree supplies a [sandbox environment](https://articles.braintreepayments.com/get-started/try-it-out) and test card numbers that can be used for this project.

For this example we'll use UK as the location and do not need to worry about multiple currencies for now, 
we just use GBP.

## Usage

### Clone the repository

```commandline
git clone https://github.com/littlepea/debit-card-service-example.git
cd debit-card-service-example
```

### Startup

```commandline
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py populate_cards_test_data
python manage.py runserver
```

### Open API docs in your browser

* [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

![](https://www.evernote.com/l/AHR4FBy9FhdFAIRZE2lM5kxpZg2EW_gcqckB/image.png)

### Acquire an access token (JWT)

`POST` the following data to `/auth/token-auth/` endpoint in order to login as one of the parents:

```json
{
  "username": "parent0",
  "password": "i_am_not_safe_to_use"
}
```

Then copy the token:

![](https://media.giphy.com/media/3og0IMUSbN32pj39N6/giphy.gif)

### Authorize with JWT

Click `Authorize` and paste the copied token into the `value` field with `JWT ` prefix:

```
JWT <your_token_here>
```

Now you have access to the `/api/cards/` as a parent:
 
 ![](https://media.giphy.com/media/xUPGcAtsXWZqruzf1u/giphy.gif)
 
### Copy a card ID

![](https://media.giphy.com/media/l4FGsBgcBO2RvBQDm/giphy.gif)

### Try to deposit some funds

![](https://media.giphy.com/media/3o7bueMGWYurkX60lG/giphy.gif)

If you deposit too much (ex: 400 GBP) 
you'll receive a validation error response with 400 status:

![](https://media.giphy.com/media/3oKIPsfxvRFdLmQlRS/giphy.gif)

## Running tests

```commandline
python manage.py test
Creating test database for alias 'default'...
......................
----------------------------------------------------------------------
Ran 22 tests in 0.101s

OK
Destroying test database for alias 'default'...
```

## Using the real Braintree sandbox environment

The easiest way id to create `local_setting.py` from example:

```commandline
cp card_service/local_settings_example.py card_service/local_settings.py
```

Then add your own credentials there:

```python
BRAINTREE_MERCHANT_ID = '<your_merchant_id>'
BRAINTREE_PUBLIC_KEY = '<your_public_key>'
BRAINTREE_PRIVATE_KEY = '<your_private_key>'

PAYMENT_BACKEND = 'payments.backends.BraintreeBackend'
```

Another way is to use ENV variables:

```commandline
export BRAINTREE_MERCHANT_ID="<your_merchant_id>"
export BRAINTREE_PUBLIC_KEY="<your_public_key>"
export BRAINTREE_PRIVATE_KEY"<your_private_key>"
```

After switching to Braintree sandbox at least re-run `populate_cards_test_data` command 
or better yet fully reset the DB:

```commandline
rm db.sqlite3
python manage.py migrate
python manage.py populate_cards_test_data 
```

Note that this will actually create a test customer with a payment method and a test deposit transaction 
in your Braitree sandbox. 

## Architecture notes

* In a micro-service reality `authentication`, `cards` and `payments` applications would be physically separated:
  * Different repositories
  * Independent schemas (no cross-service FK relations)
  * Independent Django projects
  * Communication over network and service discovery (something like Crossbar.io, Consul, K8s or SmartStack)
  * Here they are combined in order to speed-up prototyping and no need for setting up Docker Compose
* Only "happy path" has been considered here, no edge cases or error handling whatsoever
  * But in a real-world application it should be much more sophisticated

## TODO

![](https://www.evernote.com/l/AHQ4Yi2IdVpJvpzcWbq6jkJWmEBnhAfjNTwB/image.png)

## Scenarios

The below Acceptance Tests are still to be automated using BDD (pytest-bdd or django-behave).

### Scenario 1: Parent loads a compliant amount to child's card

* Given child's card has a balance of £500
  - with nothing loaded in the past month
  - and only £1000 loaded in the past year
* When parent loads £300
* Then our service receives £300 through Braintree
  - and child's balance becomes £800

### Scenario 2: Parent loads too much money to child's card for a day

* Given child's card has a balance of £500
  - with £400 already loaded earlier today
* When parent loads £300
* Then the transaction will be declined
  - and child's balance stays £500
  
### Scenario 3: Parent loads too much money to child's card for a month

* Given child's card has a balance of £500
  - with £400 already loaded in the past month
* When parent loads £500
* Then the transaction will be declined
  - and child's balance stays £500
  
### Scenario 4: Parent loads too much money to child's card for a year

* Given child's card has a balance of £500
  - with £1800 already loaded in the past 365 days
* When parent loads £300
* Then the transaction will be declined
  - and child's balance stays £500
  
### Scenario 5: Parent loads too much money to child's card which exceeds the maximum balance

* Given child's card has a balance of £800
* When parent loads £300
* Then the transaction will be declined
  - and child's balance stays £800