from datetime import date

from rest_framework import serializers

from .models import Agricultor, Cultivo


class AgricultorSerializer(serializers.ModelSerializer):
    # Viene del annotate(Count("cultivos")) del ViewSet
    total_cultivos = serializers.IntegerField(read_only=True)

    class Meta:
        model = Agricultor
        fields = ["id", "nombre", "parcela", "contacto", "total_cultivos"]


class CultivoSerializer(serializers.ModelSerializer):
    agricultor_nombre = serializers.CharField(source="agricultor.nombre", read_only=True)
    agricultor_parcela = serializers.CharField(source="agricultor.parcela", read_only=True)
    tipo_display = serializers.CharField(source="get_tipo_display", read_only=True)
    estado_display = serializers.CharField(source="get_estado_display", read_only=True)
    ofrece_display = serializers.CharField(source="get_ofrece_display", read_only=True)
    unidad_display = serializers.CharField(source="get_unidad_display", read_only=True)

    class Meta:
        model = Cultivo
        fields = [
            "id",
            "nombre",
            "tipo",
            "tipo_display",
            "estado",
            "estado_display",
            "fecha_siembra",
            "ofrece",
            "ofrece_display",
            "cantidad",
            "unidad",
            "unidad_display",
            "agricultor",
            "agricultor_nombre",
            "agricultor_parcela",
        ]

    def validate_fecha_siembra(self, valor):
        if valor > date.today():
            raise serializers.ValidationError("La fecha de siembra no puede ser futura.")
        return valor

    def validate(self, attrs):
        # En PATCH puede faltar algún campo: se completa con el valor ya guardado
        ofrece = attrs.get("ofrece", getattr(self.instance, "ofrece", "nada"))
        cantidad = attrs.get("cantidad", getattr(self.instance, "cantidad", 0))
        if ofrece != "nada" and cantidad == 0:
            raise serializers.ValidationError(
                {"cantidad": "Indica cuánto ofreces para intercambiar (mayor que 0)."}
            )
        return attrs
