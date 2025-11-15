from django.shortcuts import get_object_or_404, render
from .models import Aerolinea, Pais, Aeropuerto


def index(request):
    """
    Portada de Volare: muestra una aerolínea destacada por país.
    Criterio: la primera alfabéticamente por nombre (podrías usar año fundación si quieres).
    """
    paises = Pais.objects.prefetch_related("aerolineas")
    aerolineas_destacadas = []

    for pais in paises:
        aerolinea = pais.aerolineas.order_by("nombre").first()
        if aerolinea:
            aerolineas_destacadas.append(aerolinea)

    contexto = {
        "aerolineas_destacadas": aerolineas_destacadas,
    }
    return render(request, "volare/index.html", contexto)


# --- Aerolíneas ---

def aerolinea_list(request):
    aerolineas = Aerolinea.objects.select_related("pais").prefetch_related("aeropuertos")
    contexto = {
        "aerolineas": aerolineas,
    }
    return render(request, "volare/aerolinea_list.html", contexto)


def aerolinea_detail(request, pk):
    aerolinea = get_object_or_404(
        Aerolinea.objects.select_related("pais").prefetch_related("aeropuertos"),
        pk=pk
    )
    contexto = {
        "aerolinea": aerolinea,
    }
    return render(request, "volare/aerolinea_detail.html", contexto)


# --- Países ---

def pais_list(request):
    paises = Pais.objects.prefetch_related("aerolineas")
    contexto = {
        "paises": paises,
    }
    return render(request, "volare/pais_list.html", contexto)


def pais_detail(request, pk):
    pais = get_object_or_404(Pais.objects.prefetch_related("aerolineas"), pk=pk)
    contexto = {
        "pais": pais,
        "aerolineas": pais.aerolineas.all(),
    }
    return render(request, "volare/pais_detail.html", contexto)


# --- Aeropuertos ---

def aeropuerto_list(request):
    aeropuertos = Aeropuerto.objects.select_related("pais").prefetch_related("aerolineas")
    contexto = {
        "aeropuertos": aeropuertos,
    }
    return render(request, "volare/aeropuerto_list.html", contexto)


def aeropuerto_detail(request, pk):
    aeropuerto = get_object_or_404(
        Aeropuerto.objects.select_related("pais").prefetch_related("aerolineas"),
        pk=pk
    )
    contexto = {
        "aeropuerto": aeropuerto,
        "aerolineas": aeropuerto.aerolineas.all(),
    }
    return render(request, "volare/aeropuerto_detail.html", contexto)
