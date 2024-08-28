from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth", include("rest_framework.urls")),
    path("api/accounts/", include("accounts.urls")),
    path("api/restaurant/", include("restaurant.urls")),
    path("api/cart/", include("carts.urls")),
    path("api/", include("orders.urls")),
    path("api/", include("admin.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
