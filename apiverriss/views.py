from rest_framework import viewsets
from .models import Usuario, Evento
from .serializers import UsuarioSerializer, EventoSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from apiverriss import serializers


# Páginas HTML
def home(request):
    return render(request, 'home.html')

def iniciar_sesion(request):
    return render(request, 'iniciar_sesion.html')

def registro(request):
    return render(request, 'registro.html')

def perfil(request):
    return render(request, 'perfil.html')

# ViewSets de la API REST
class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(organizador=self.request.user)



class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def get_permissions(self):
        if self.action in ['create']:
            return [AllowAny()]  # Permitir acceso público para registro
        return super().get_permissions()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Información adicional
        token['username'] = user.username
        token['email'] = user.email
        return token

    def validate(self, attrs):
        username_or_email = attrs.get("username")
        password = attrs.get("password")
        user_model = get_user_model()

        # Verificar si el usuario ingresó un email o un username
        try:
            if '@' in username_or_email:
                user = user_model.objects.get(email=username_or_email)
            else:
                user = user_model.objects.get(username=username_or_email)
        except user_model.DoesNotExist:
            raise serializers.ValidationError({"detail": "Credenciales inválidas."})

        # Validar contraseña
        if not user.check_password(password):
            raise serializers.ValidationError({"detail": "Credenciales inválidas."})

        if not user.is_active:
            raise serializers.ValidationError({"detail": "Cuenta inactiva."})

        # Agregar usuario al contexto para que el serializer JWT lo maneje
        attrs["user"] = user
        return super().validate(attrs)