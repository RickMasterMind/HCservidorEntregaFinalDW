from django.db.models import Count
from rest_framework import viewsets

from .models import Agricultor, Cultivo
from .serializers import AgricultorSerializer, CultivoSerializer


class AgricultorViewSet(viewsets.ModelViewSet):
    """CRUD completo de agricultores: list, create, retrieve, update, partial_update, destroy."""

    queryset = Agricultor.objects.annotate(total_cultivos=Count("cultivos"))
    serializer_class = AgricultorSerializer


class CultivoViewSet(viewsets.ModelViewSet):
    """CRUD completo de cultivos. Admite filtrar con ?agricultor=<id> y ?ofrece=semillas|cosecha."""

    serializer_class = CultivoSerializer

    def get_queryset(self):
        queryset = Cultivo.objects.select_related("agricultor")
        agricultor_id = self.request.query_params.get("agricultor")
        ofrece = self.request.query_params.get("ofrece")
        if agricultor_id:
            queryset = queryset.filter(agricultor_id=agricultor_id)
        if ofrece:
            queryset = queryset.filter(ofrece=ofrece)
        return queryset
