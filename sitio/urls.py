"""URL configuration for sitio project."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]

# En desarrollo Django se encarga de servir los archivos estaticos,
# pero las imagenes que sube el administrador viven en media/.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
