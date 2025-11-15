from django.contrib import admin
from .models import Pais, Aeropuerto, Aerolinea

@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
    list_display = ("nombre", "codigo_iso")
    search_fields = ("nombre", "codigo_iso")


@admin.register(Aeropuerto)
class AeropuertoAdmin(admin.ModelAdmin):
    list_display = ("codigo_iata", "nombre", "ciudad", "pais")
    list_filter = ("pais",)
    search_fields = ("codigo_iata", "nombre", "ciudad")


@admin.register(Aerolinea)
class AerolineaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "codigo_iata", "pais")
    list_filter = ("pais",)
    search_fields = ("nombre", "codigo_iata")
    filter_horizontal = ("aeropuertos",)
