from rest_framework import viewsets
from rest_framework import mixins
from cards.serializers import TransactionSerializer, CardSerializer
from cards.models import Transaction, Card


class CardViewSet(mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Return the given card.

    list:
    Return a list of all the existing cards.

    create:
    Create a new card.
    """
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    http_method_names = ['get', 'post', 'delete']


class TransactionViewSet(mixins.CreateModelMixin,
                         viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Return the given transaction.

    list:
    Return a list of all the existing transactions.

    create:
    Create a new transaction.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
