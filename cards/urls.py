from django.conf.urls import url, include
from rest_framework import routers

from cards import views


router = routers.DefaultRouter()
router.register(r'cards', views.CardViewSet)
router.register(r'transactions', views.TransactionViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
]