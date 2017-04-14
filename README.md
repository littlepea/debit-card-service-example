# Debit Card Service

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

## Startup

```console
$ virtualenv venv
$ . venv/bin/activate
$ pip install -r requirements.txt
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver
```

## Features

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