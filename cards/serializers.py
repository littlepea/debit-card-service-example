from rest_framework import serializers
from cards.models import Transaction, Card


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('amount', 'user', 'time', 'type', 'id', 'card',)


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ('balance', 'id', 'parent_id', 'child_id',)


class DepositSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=5, decimal_places=2,
                                      help_text='Amount of funds to deposit to the child\'s card')
