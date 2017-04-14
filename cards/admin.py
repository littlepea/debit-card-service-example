from django.contrib import admin
from .models import Transaction, Card


class TransactionAdmin(admin.ModelAdmin):
    queryset = Transaction.objects.all()
    list_display = ('amount', 'user', 'time', 'type', 'id', 'card',)


class CardAdmin(admin.ModelAdmin):
    queryset = Card.objects.all()
    list_display = ('balance', 'id', 'parent', 'child',)


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Card, CardAdmin)
