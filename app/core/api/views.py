from rest_framework.viewsets import ReadOnlyModelViewSet

from core.api.serializers import ConsertoSerializer
from core.models import Conserto


class ConsertoViewSet(ReadOnlyModelViewSet):
    serializer_class = ConsertoSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Conserto.objects.select_related('modelo__marca', 'defeito').busca(
            marca=self.request.query_params.get('marca'),
            modelo=self.request.query_params.get('modelo'),
            defeito=self.request.query_params.get('defeito'),
        )
