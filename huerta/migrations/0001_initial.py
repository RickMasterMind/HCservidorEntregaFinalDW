import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Agricultor",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=120)),
                ("parcela", models.CharField(max_length=40)),
                ("contacto", models.CharField(blank=True, max_length=80)),
            ],
            options={
                "verbose_name_plural": "agricultores",
                "ordering": ["nombre"],
            },
        ),
        migrations.CreateModel(
            name="Cultivo",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=100)),
                (
                    "tipo",
                    models.CharField(
                        choices=[
                            ("hortaliza", "Hortaliza"),
                            ("fruta", "Fruta"),
                            ("aromatica", "Hierba aromática"),
                            ("legumbre", "Legumbre"),
                            ("tuberculo", "Tubérculo"),
                        ],
                        default="hortaliza",
                        max_length=20,
                    ),
                ),
                (
                    "estado",
                    models.CharField(
                        choices=[
                            ("sembrado", "Sembrado"),
                            ("creciendo", "En crecimiento"),
                            ("listo", "Listo para cosechar"),
                            ("cosechado", "Cosechado"),
                        ],
                        default="sembrado",
                        max_length=20,
                    ),
                ),
                ("fecha_siembra", models.DateField()),
                (
                    "ofrece",
                    models.CharField(
                        choices=[
                            ("nada", "No intercambia"),
                            ("semillas", "Semillas"),
                            ("cosecha", "Cosecha"),
                        ],
                        default="nada",
                        max_length=20,
                    ),
                ),
                ("cantidad", models.PositiveIntegerField(default=0)),
                (
                    "unidad",
                    models.CharField(
                        choices=[
                            ("unidades", "unidades"),
                            ("kg", "kg"),
                            ("atados", "atados"),
                            ("sobres", "sobres"),
                        ],
                        default="unidades",
                        max_length=20,
                    ),
                ),
                (
                    "agricultor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cultivos",
                        to="huerta.agricultor",
                    ),
                ),
            ],
            options={
                "ordering": ["-fecha_siembra", "nombre"],
            },
        ),
    ]
