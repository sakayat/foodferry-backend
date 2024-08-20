from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth", include("rest_framework.urls")),
    path("api/", include("accounts.urls")),
    path("api/", include("restaurant.urls")),
    path("api/", include("carts.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
