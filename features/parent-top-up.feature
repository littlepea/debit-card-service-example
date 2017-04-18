Feature: Debit Card deposit by parent
    As a Parent
    I can deposit funds to my child's debit card
    So that she can make her own financial decisions

    Scenario: Parent loads a compliant amount to child's card
        Given a child's card with a balance of £500
            And a following set of transactions
                | date          | amount    |
                | 2016-04-01    | 500       |
                | 2016-06-01    | 500       |
                | 2016-08-01    | -500      |
            And today is 2017-03-01
        When parent deposits £300
        Then the deposit will be successful
            And child's balance will be £800

    Scenario: Parent loads too much money to child's card for a day
        Given a child's card with a balance of £500
            And a following set of transactions
                | date          | amount    |
                | 2016-06-01    | 100       |
                | 2017-03-01    | 400       |
            And today is 2017-03-01
        When parent deposits £300
        Then the deposit will fail
            And child's balance will be £500

    Scenario: Parent loads too much money to child's card for a month
        Given a child's card with a balance of £500
            And a following set of transactions
                | date          | amount    |
                | 2016-06-01    | 100       |
                | 2017-02-15    | 400       |
            And today is 2017-03-01
        When parent deposits £500
        Then the deposit will fail
            And child's balance will be £500
