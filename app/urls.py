from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('schema', SpectacularAPIView.as_view(), name='schema'),
    path('', SpectacularSwaggerView.as_view(url_name='schema')),
    path("admin/", admin.site.urls),
    path("user_auth/", include("users.api.user_profile.urls")),
    path("blog/", include("blog.api.urls")),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
