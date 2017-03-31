from django.contrib.auth.models import User, Group
from rest_framework import serializers
from cards.models import Transaction, Card

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name',)

class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups',)

class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transaction
        fields = ('amount', 'user', 'time', 'type', 'id', 'card',)

class CardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Card
        fields = ('balance', 'id', 'parent', 'child',)
