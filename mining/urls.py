from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    path("admin/", admin.site.urls),
    path("", include("landing.urls")),
    path("api/", include("api.urls")),
]
