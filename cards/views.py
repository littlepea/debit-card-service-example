from rest_framework import viewsets
from rest_framework import mixins
from rest_framework_extensions.mixins import NestedViewSetMixin
from rest_framework.decorators import detail_route

from cards.serializers import TransactionSerializer, CardSerializer
from cards.models import Transaction, Card
from cards import services


class CardViewSet(NestedViewSetMixin,
                  mixins.CreateModelMixin,
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
    queryset = Card.objects.none()
    serializer_class = CardSerializer
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        return services.get_user_cards(self.request.user)

    @detail_route(methods=['post'], url_path='top-up')  # TODO: add permission_classes=[IsParentCardOwner]
    def top_up(self, request, pk=None, amount=None):
        """
        Deposit funds to a card

        :param request: API Request instance
        :param pk: Card ID
        :param amount: Amount to deposit
        :return: API Response
        """
        return services.deposit_funds(pk, amount)


class TransactionViewSet(NestedViewSetMixin,
                         mixins.CreateModelMixin,
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
