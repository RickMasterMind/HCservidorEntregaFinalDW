from django.db import models

TIPOS = [
    ("hortaliza", "Hortaliza"),
    ("fruta", "Fruta"),
    ("aromatica", "Hierba aromática"),
    ("legumbre", "Legumbre"),
    ("tuberculo", "Tubérculo"),
]

ESTADOS = [
    ("sembrado", "Sembrado"),
    ("creciendo", "En crecimiento"),
    ("listo", "Listo para cosechar"),
    ("cosechado", "Cosechado"),
]

OFRECE = [
    ("nada", "No intercambia"),
    ("semillas", "Semillas"),
    ("cosecha", "Cosecha"),
]

UNIDADES = [
    ("unidades", "unidades"),
    ("kg", "kg"),
    ("atados", "atados"),
    ("sobres", "sobres"),
]


class Agricultor(models.Model):
    """Vecino que cuida una parcela de la huerta."""

    nombre = models.CharField(max_length=120)
    parcela = models.CharField(max_length=40)
    contacto = models.CharField(max_length=80, blank=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "agricultores"

    def __str__(self):
        return f"{self.nombre} ({self.parcela})"


class Cultivo(models.Model):
    """Planta sembrada por un agricultor; puede ofrecer semillas o cosecha para intercambiar."""

    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPOS, default="hortaliza")
    estado = models.CharField(max_length=20, choices=ESTADOS, default="sembrado")
    fecha_siembra = models.DateField()
    ofrece = models.CharField(max_length=20, choices=OFRECE, default="nada")
    cantidad = models.PositiveIntegerField(default=0)
    unidad = models.CharField(max_length=20, choices=UNIDADES, default="unidades")
    # Relación 1:N -> un agricultor tiene muchos cultivos
    agricultor = models.ForeignKey(
        Agricultor, on_delete=models.CASCADE, related_name="cultivos"
    )

    class Meta:
        ordering = ["-fecha_siembra", "nombre"]

    def __str__(self):
        return f"{self.nombre} - {self.agricultor.nombre}"
