from django.urls import path
from . import views

app_name = "vuelos"

urlpatterns = [
    path("", views.index, name="index"),

    #aerolineas - READ
    path("aerolineas/", views.aerolinea_list, name="aerolinea_list"),
    path("aerolineas/<int:pk>/", views.aerolinea_detail, name="aerolinea_detail"),
    
    #rutas CRUD
    path("aerolineas/nueva/", views.aerolinea_create, name="aerolinea_create"),
    path("aerolineas/<int:pk>/editar/", views.aerolinea_update, name="aerolinea_update"),
    path("aerolineas/<int:pk>/eliminar/", views.aerolinea_delete, name="aerolinea_delete"),
    
    #rutas AJAX
    path("buscar-aerolineas/", views.buscar_aerolineas, name="buscar_aerolineas"),

    #paises
    path("paises/", views.pais_list, name="pais_list"),
    path("paises/<int:pk>/", views.pais_detail, name="pais_detail"),

    #aeropuertos
    path("aeropuertos/", views.aeropuerto_list, name="aeropuerto_list"),
    path("aeropuertos/<int:pk>/", views.aeropuerto_detail, name="aeropuerto_detail"),
]