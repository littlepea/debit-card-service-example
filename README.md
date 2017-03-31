# Osper Card Service

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
* Then Osper receives  £300 through Braintree
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