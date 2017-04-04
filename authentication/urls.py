from django.conf.urls import url, include
from rest_framework_jwt import views


urlpatterns = [
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^token-auth/', views.obtain_jwt_token),
    url(r'^token-verify/', views.verify_jwt_token),
    url(r'^token-refresh/', views.refresh_jwt_token),
]