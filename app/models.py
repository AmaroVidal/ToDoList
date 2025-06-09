from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class EstadoTarea(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    color_bootstrap = models.CharField(
        max_length=30,
        default='secondary',
        help_text="Nombre del color de Bootstrap, por ejemplo: 'success', 'warning', 'danger'"
    )
    orden = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['orden']
        verbose_name = 'Estado de Tarea'
        verbose_name_plural = 'Estados de Tareas'

class Tarea(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    vencimiento = models.DateField()
    estado = models.ForeignKey(EstadoTarea, on_delete=models.PROTECT, related_name='tareas')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tareas')
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.titulo} ({self.estado.nombre})"

    class Meta:
        ordering = ['vencimiento']
