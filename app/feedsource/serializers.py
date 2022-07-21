from rest_framework import serializers

from core.models import FeedSource


class FeedSourceSerializer(serializers.ModelSerializer):
    '''Serializer to serialize FeedSource instances'''
    class Meta:
        model = FeedSource
        fields = ('id', 'name')
        read_only_fields = ('name',)
