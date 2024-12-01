from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import EventoViewSet, UsuarioViewSet, home, registro, iniciar_sesion, perfil
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.views import LogoutView

# Configurar el router para las rutas de la API
router = routers.DefaultRouter()
router.register(r'eventos', EventoViewSet, basename='EventoViewSet')
router.register(r'usuarios', UsuarioViewSet, basename='UsuarioViewSet')

# Configurar las rutas
urlpatterns = [
    # Páginas HTML
    path('', home, name='home'),
    path('registro/', registro, name='registro'),
    path('iniciar_sesion/', iniciar_sesion, name='iniciar_sesion'),
    path('cerrar-sesion/', LogoutView.as_view(next_page='home'), name='cerrar_sesion'),
    path('perfil/', perfil, name='perfil'),

    # Rutas de la API
    path('api/', include(router.urls)),  # Endpoints generados por el router
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Token JWT
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh Token

    # Admin
    path('admin/', admin.site.urls),
]
