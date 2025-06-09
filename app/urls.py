from django.urls import path
from .views import *

urlpatterns = [
    path("",home, name="home"),
    path("login/", iniciar_session, name="login"),
    path("registro/", registro, name="registro"),
    path('logout/', cerrar_session, name='logout'),
    path('crear/', crear_tarea, name='crear_tarea'),
    path('tarea/<int:tarea_id>/iniciar/', iniciar_tarea, name='iniciar_tarea'),
    path('tarea/<int:tarea_id>/completar/', completar_tarea, name='completar_tarea'),
    path('tareas/<int:id>/editar/', actualizar_tarea, name='actualizar_tarea'),
    path('tareas/<int:id>/eliminar/', eliminar_tarea, name='eliminar_tarea'),
]