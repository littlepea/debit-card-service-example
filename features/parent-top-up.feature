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
        When parent deposits £300
        Then child's balance becomes £800