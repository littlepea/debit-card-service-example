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
