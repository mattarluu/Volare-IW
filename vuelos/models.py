from django.db import models

class Pais(models.Model):
    nombre = models.CharField(max_length=100)
    codigo_iso = models.CharField(max_length=3, unique=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.codigo_iso})"


class Aeropuerto(models.Model):
    codigo_iata = models.CharField(max_length=3, unique=True)
    nombre = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=100, blank=True)
    pais = models.ForeignKey(
        Pais,
        on_delete=models.CASCADE,
        related_name="aeropuertos"
    )

    class Meta:
        ordering = ["codigo_iata"]

    def __str__(self):
        return f"{self.codigo_iata} - {self.nombre}"


class Aerolinea(models.Model):
    nombre = models.CharField(max_length=200)
    codigo_iata = models.CharField(max_length=3, blank=True, null=True)
    pais = models.ForeignKey(
        Pais,
        on_delete=models.CASCADE,
        related_name="aerolineas"
    )
    aeropuertos = models.ManyToManyField(
        Aeropuerto,
        related_name="aerolineas",
        blank=True
    )
    # Puedes añadir más cosas si quieres (año fundación, web, etc.)
    anio_fundacion = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre
