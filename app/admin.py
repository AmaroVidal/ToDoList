from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import EstadoTarea, Tarea

admin.site.register(EstadoTarea)
admin.site.register(Tarea)