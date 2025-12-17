from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from datetime import datetime
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


#Aerolíneas

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


#Países
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


#Aeropuertos

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


#vistas CRUD

def aerolinea_create(request):
    """
    Vista para CREAR una nueva aerolínea.
    GET: Muestra el formulario vacío
    POST: Procesa los datos y crea la aerolínea
    ACTUALIZADO: Código IATA ahora es obligatorio
    """
    if request.method == "POST":
        nombre = request.POST.get("nombre", "").strip()
        codigo_iata = request.POST.get("codigo_iata", "").strip()
        pais_id = request.POST.get("pais")
        anio_fundacion = request.POST.get("anio_fundacion", "").strip()
        aeropuertos_ids = request.POST.getlist("aeropuertos")
        
        if not nombre or not codigo_iata or not pais_id:

            contexto = {
                "error": "El nombre, el código IATA y el país son obligatorios",
                "paises": Pais.objects.all(),
                "aeropuertos": Aeropuerto.objects.all(),
                "anio_actual": datetime.now().year,
            }
            return render(request, "volare/aerolinea_form.html", contexto)
        
        if len(codigo_iata) < 2 or len(codigo_iata) > 3:
            contexto = {
                "error": "El código IATA debe tener 2 o 3 caracteres",
                "paises": Pais.objects.all(),
                "aeropuertos": Aeropuerto.objects.all(),
                "anio_actual": datetime.now().year,
            }
            return render(request, "volare/aerolinea_form.html", contexto)

        pais = get_object_or_404(Pais, pk=pais_id)
        
        aerolinea = Aerolinea(
            nombre=nombre,
            codigo_iata=codigo_iata.upper(),  #mayusculas
            pais=pais,
            anio_fundacion=int(anio_fundacion) if anio_fundacion else None
        )
        aerolinea.save()
        
        #añadir aeropuertos si se seleccionaron
        if aeropuertos_ids:
            aeropuertos = Aeropuerto.objects.filter(pk__in=aeropuertos_ids)
            aerolinea.aeropuertos.set(aeropuertos)
            
        return HttpResponseRedirect(reverse("vuelos:aerolinea_detail", args=[aerolinea.pk]))
    
    #GET: Mostrar formulario vacío
    contexto = {
        "paises": Pais.objects.all(),
        "aeropuertos": Aeropuerto.objects.select_related("pais").all(),
        "anio_actual": datetime.now().year,
    }
    return render(request, "volare/aerolinea_form.html", contexto)


def aerolinea_update(request, pk):
    """
    Vista para ACTUALIZAR una aerolínea existente.
    GET: Muestra el formulario con los datos actuales
    POST: Procesa los cambios y actualiza la aerolínea
    ACTUALIZADO: Código IATA ahora es obligatorio
    """
    aerolinea = get_object_or_404(Aerolinea, pk=pk)
    
    if request.method == "POST":

        nombre = request.POST.get("nombre", "").strip()
        codigo_iata = request.POST.get("codigo_iata", "").strip()
        pais_id = request.POST.get("pais")
        anio_fundacion = request.POST.get("anio_fundacion", "").strip()
        aeropuertos_ids = request.POST.getlist("aeropuertos")
        
        if not nombre or not codigo_iata or not pais_id:
            contexto = {
                "aerolinea": aerolinea,
                "error": "El nombre, el código IATA y el país son obligatorios",
                "paises": Pais.objects.all(),
                "aeropuertos": Aeropuerto.objects.all(),
                "anio_actual": datetime.now().year,
            }
            return render(request, "volare/aerolinea_form.html", contexto)
        
        if len(codigo_iata) < 2 or len(codigo_iata) > 3:
            contexto = {
                "aerolinea": aerolinea,
                "error": "El código IATA debe tener 2 o 3 caracteres",
                "paises": Pais.objects.all(),
                "aeropuertos": Aeropuerto.objects.all(),
                "anio_actual": datetime.now().year,
            }
            return render(request, "volare/aerolinea_form.html", contexto)
        
        #actualizar
        aerolinea.nombre = nombre
        aerolinea.codigo_iata = codigo_iata.upper()  #mayusculas
        aerolinea.pais = get_object_or_404(Pais, pk=pais_id)
        aerolinea.anio_fundacion = int(anio_fundacion) if anio_fundacion else None
        aerolinea.save()
        
        #actualizar aeropuertos
        if aeropuertos_ids:
            aeropuertos = Aeropuerto.objects.filter(pk__in=aeropuertos_ids)
            aerolinea.aeropuertos.set(aeropuertos)
        else:
            aerolinea.aeropuertos.clear()
        
        return HttpResponseRedirect(reverse("vuelos:aerolinea_detail", args=[aerolinea.pk]))
    
    #GET: Mostrar formulario con datos actuales
    contexto = {
        "aerolinea": aerolinea,
        "paises": Pais.objects.all(),
        "aeropuertos": Aeropuerto.objects.select_related("pais").all(),
        "anio_actual": datetime.now().year,
    }
    return render(request, "volare/aerolinea_form.html", contexto)


def aerolinea_delete(request, pk):
    """
    Vista para ELIMINAR una aerolínea.
    """
    if request.method == "POST":
        aerolinea = get_object_or_404(Aerolinea, pk=pk)
        aerolinea.delete()
    
        return HttpResponseRedirect(reverse("vuelos:aerolinea_list"))
    
    #Si no es POST, redirigir a la lista
    return HttpResponseRedirect(reverse("vuelos:aerolinea_list"))


def buscar_aerolineas(request):
    """
    Vista AJAX para buscar aerolíneas en tiempo real.
    Devuelve JSON con los resultados filtrados.
    """
    query = request.GET.get('q', '').strip()
    
    if query:
        #buscar por nombre o codigo IATA
        aerolineas = Aerolinea.objects.select_related("pais").filter(
            nombre__icontains=query
        ) | Aerolinea.objects.select_related("pais").filter(
            codigo_iata__icontains=query
        )
    else:
        #devolver todas
        aerolineas = Aerolinea.objects.select_related("pais").all()
    
    #construir lista de resultados para JSON
    resultados = []
    for aerolinea in aerolineas:
        resultados.append({
            'id': aerolinea.pk,
            'nombre': aerolinea.nombre,
            'codigo_iata': aerolinea.codigo_iata if aerolinea.codigo_iata else '',
            'pais': aerolinea.pais.nombre,
            'anio_fundacion': aerolinea.anio_fundacion if aerolinea.anio_fundacion else None,
        })
    
    return JsonResponse({'results': resultados})