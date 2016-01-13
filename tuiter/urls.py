"""tuiter URL Configuration."""

from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static

from tuiter import settings

from tuits import urls as tuiter_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('', include(tuiter_urls, namespace='tuiter'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # NOQA
