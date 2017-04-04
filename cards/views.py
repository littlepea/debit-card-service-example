from rest_framework import viewsets
from rest_framework import mixins
from rest_framework_extensions.mixins import NestedViewSetMixin
from rest_framework.decorators import detail_route

from cards.serializers import TransactionSerializer, CardSerializer
from cards.models import Transaction, Card


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
        user = self.request.user
        cards = user.parent_cards if user.is_parent else user.child_cards
        return cards.all()

    @detail_route(methods=['post'], url_path='top-up')  # TODO: add permission_classes=[IsParentCardOwner]
    def top_up(self, request, pk=None):
        """
        Deposit funds to a card

        :param request: API Request instance
        :param pk: Card ID
        :return: API Response
        """
        raise NotImplementedError('top-up action is not implemented yet')


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
