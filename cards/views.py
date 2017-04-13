from rest_framework import viewsets
from rest_framework import mixins
from rest_framework_extensions.mixins import NestedViewSetMixin
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated

from cards.serializers import TransactionSerializer, CardSerializer, DepositSerializer
from cards.models import Transaction, Card
from cards import services
from cards.permissions import IsParentCardOwner


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

    def get_object(self):
        obj = super(CardViewSet, self).get_object()
        return obj

    @detail_route(methods=['post'], permission_classes=[IsParentCardOwner, IsAuthenticated], url_path='top-up')
    def top_up(self, request, pk=None):
        """
        Deposit funds to a card

        Data example:

            {
                "amount": 25.5
            }
        """
        card = services.get_card_by_id(pk)
        self.check_object_permissions(request, card)
        serializer = DepositSerializer(data=request.data)
        if serializer.is_valid():
            return services.deposit_funds(pk, amount=serializer.validated_data['amount'])
        return


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
