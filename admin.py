from django.contrib import admin

from .models import Agricultor, Cultivo


@admin.register(Agricultor)
class AgricultorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "parcela", "contacto")
    search_fields = ("nombre", "parcela")


@admin.register(Cultivo)
class CultivoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "agricultor", "tipo", "estado", "ofrece", "cantidad", "unidad")
    list_filter = ("tipo", "estado", "ofrece")
    search_fields = ("nombre",)
