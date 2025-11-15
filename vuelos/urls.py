from django.urls import path
from . import views

app_name = "vuelos"

urlpatterns = [
    path("", views.index, name="index"),

    # Aerolíneas
    path("aerolineas/", views.aerolinea_list, name="aerolinea_list"),
    path("aerolineas/<int:pk>/", views.aerolinea_detail, name="aerolinea_detail"),

    # Países
    path("paises/", views.pais_list, name="pais_list"),
    path("paises/<int:pk>/", views.pais_detail, name="pais_detail"),

    # Aeropuertos
    path("aeropuertos/", views.aeropuerto_list, name="aeropuerto_list"),
    path("aeropuertos/<int:pk>/", views.aeropuerto_detail, name="aeropuerto_detail"),
]
