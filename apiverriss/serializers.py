from rest_framework import serializers
from .models import Evento, Usuario

class UsuarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'first_name', 'email']

    
 
class EventoSerializer(serializers.ModelSerializer):
    imagen_url = serializers.SerializerMethodField()

    class Meta:
        model = Evento
        fields = ['id', 'titulo', 'descripcion', 'ubicacion', 'fecha_hora', 'organizador', 
                  'privacidad', 'imagen', 'imagen_url', 'precio_entrada']

    def get_imagen_url(self, obj):
        request = self.context.get('request')
        if obj.imagen:
            return request.build_absolute_uri(obj.imagen.url)
        return request.build_absolute_uri('/static/images/default_evento.jpg')