import os
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework_swagger.views import get_swagger_view


schema_view = get_swagger_view(title='Osper Card Service API')


urlpatterns = [
    url(os.environ.get('DJANGO_URL_PREFIX', ''), include([
        url(r'^admin/', admin.site.urls),
        url(r'^api/', include('cards.urls')),
        url(r'^auth/', include('authentication.urls')),
        url(r'^$', schema_view)
    ])),
]
