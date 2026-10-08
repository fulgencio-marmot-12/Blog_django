"""URL configuration for sitio project."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Blog de Facundo Saint Martin"
admin.site.site_title = "Admin del blog"
admin.site.index_title = "Panel de administracion"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls")),
    path("portfolio/", include("pages.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
