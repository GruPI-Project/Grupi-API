# projeto/urls.py
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from views import get_csrf_token

urlpatterns = [
    path('csrf/', get_csrf_token, name='api-csrf'),
    path('admin/', admin.site.urls),
    path('api/v1/', include('core.urls')),
    path('api/v1/auth/', include('dj_rest_auth.urls')),
    path('api/v1/auth/registration/', include('dj_rest_auth.registration.urls')),

    # Documentação da API
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]