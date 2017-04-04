from django.conf.urls import url, include
from rest_framework_extensions.routers import ExtendedSimpleRouter

from cards import views


router = ExtendedSimpleRouter()
router.register(r'cards', views.CardViewSet, base_name='card')\
      .register(r'transactions',
                views.TransactionViewSet,
                base_name='card-transactions',
                parents_query_lookups=['card_id'])

urlpatterns = [
    url(r'', include(router.urls)),
]