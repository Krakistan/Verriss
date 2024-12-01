from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.models import AbstractUser

from nucleo import settings


class Evento(models.Model):
    PRIVACIDAD_OPCIONES = [
        ('publico', 'Público'),
        ('privado', 'Privado'),
    ]

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    ubicacion = models.CharField(max_length=255)
    fecha_hora = models.DateTimeField()
    organizador = models.ForeignKey(
        'Usuario',
        on_delete=models.CASCADE,  # Clave foránea que apunta al modelo Usuario
        related_name='eventos_creados'
    )
    privacidad = models.CharField(max_length=7, choices=PRIVACIDAD_OPCIONES, default='publico')  # Público o privado
    imagen = models.ImageField(upload_to='eventos_imagenes/', blank=True, null=True)  # Imagen opcional
    precio_entrada = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Precio opcional

    def imagen_url(self):
        if self.imagen:
            return f"{settings.MEDIA_URL}{self.imagen}"
        return f"{settings.STATIC_URL}images/default_evento.jpg" 

    def __str__(self):
        return f"{self.titulo} por {self.organizador.username}"



class Usuario(AbstractUser):
    PRIVACIDAD_OPCIONES = [
        ('publico', 'Público'),
        ('privado', 'Privado'),
    ]

    avatar = models.ImageField(upload_to='usuarios_avatar/', blank=True, null=True)
    biografia = models.TextField(blank=True, null=True)
    privacidad = models.CharField(max_length=7, choices=PRIVACIDAD_OPCIONES, default='publico')

    # Campo para relaciones de seguimiento
    siguiendo = models.ManyToManyField(
        'self', symmetrical=False, related_name='seguidores', blank=True
    )

    # Grupos y permisos personalizados
    groups = models.ManyToManyField(
        Group, related_name='usuarios_apiverriss', blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission, related_name='usuarios_permisos_apiverriss', blank=True
    )

    def esta_siguiendo(self, usuario):
        """
        Verifica si el usuario actual está siguiendo a otro usuario.
        """
        return self.siguiendo.filter(pk=usuario.pk).exists()

    def __str__(self):
        return self.username