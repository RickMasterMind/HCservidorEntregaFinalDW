from datetime import date, timedelta

from django.core.management.base import BaseCommand

from huerta.models import Agricultor, Cultivo


class Command(BaseCommand):
    help = "Carga datos de ejemplo (útil para la demostración en video)."

    def handle(self, *args, **options):
        hoy = date.today()
        agricultores = {
            "Marta Ríos": ("Parcela 1", "300 111 2233"),
            "Don Efraín Gómez": ("Parcela 2", "310 222 3344"),
            "Luisa Cardona": ("Parcela 3", "320 333 4455"),
        }
        creados = {}
        for nombre, (parcela, contacto) in agricultores.items():
            obj, _ = Agricultor.objects.get_or_create(
                nombre=nombre, defaults={"parcela": parcela, "contacto": contacto}
            )
            creados[nombre] = obj

        cultivos = [
            ("Tomate chonto", "hortaliza", "listo", 70, "cosecha", 5, "kg", "Marta Ríos"),
            ("Albahaca", "aromatica", "creciendo", 30, "semillas", 4, "sobres", "Marta Ríos"),
            ("Fríjol cargamanto", "legumbre", "sembrado", 12, "nada", 0, "unidades", "Don Efraín Gómez"),
            ("Papa criolla", "tuberculo", "cosechado", 120, "cosecha", 8, "kg", "Don Efraín Gómez"),
            ("Cilantro", "aromatica", "listo", 40, "cosecha", 10, "atados", "Luisa Cardona"),
            ("Lulo", "fruta", "creciendo", 90, "semillas", 3, "sobres", "Luisa Cardona"),
        ]
        nuevos = 0
        for nombre, tipo, estado, dias, ofrece, cantidad, unidad, dueno in cultivos:
            _, creado = Cultivo.objects.get_or_create(
                nombre=nombre,
                agricultor=creados[dueno],
                defaults={
                    "tipo": tipo,
                    "estado": estado,
                    "fecha_siembra": hoy - timedelta(days=dias),
                    "ofrece": ofrece,
                    "cantidad": cantidad,
                    "unidad": unidad,
                },
            )
            nuevos += int(creado)

        self.stdout.write(self.style.SUCCESS(f"Datos de ejemplo listos ({nuevos} cultivos nuevos)."))
