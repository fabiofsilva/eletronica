from rest_framework import serializers

from core.models import Conserto


class ConsertoSerializer(serializers.ModelSerializer):
    marca_descricao = serializers.ReadOnlyField(source='modelo.marca.descricao')
    modelo_descricao = serializers.ReadOnlyField(source='modelo.descricao')
    defeito_descricao = serializers.ReadOnlyField(source='defeito.descricao')
    url = serializers.URLField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Conserto
        fields = [
            'id',
            'modelo',
            'defeito',
            'slug',
            'diagnostico',
            'marca_descricao',
            'modelo_descricao',
            'defeito_descricao',
            'url',
        ]
