from rest_framework import serializers
from cards.models import Transaction, Card


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('amount', 'user_id', 'time', 'type', 'id', 'card_id',)


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ('balance', 'id', 'parent_id', 'child_id',)


class DepositSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=5, decimal_places=2,
                                      help_text='Amount of funds to deposit to the child\'s card')

    def validate_amount(self, value):
        """
        Checks that amount doesn't exceed the max deposit limit
        """
        limit = self.initial_data['max_deposit']
        if value > limit:
            raise serializers.ValidationError('Deposit amount exceeds the current limit: {:.2f} GBP'.format(limit))

        return value
