from rest_framework import serializers

from core.models import Feed


class ListFeedSerializer(serializers.ModelSerializer):
    '''Serialize Feed instances'''
    class Meta:
        model = Feed
        fields = ('id', 'title', 'link',)
        read_only_fields = ('title', 'link',)


class RetriveSingleFeedSerializer(serializers.ModelSerializer):
    '''Serialize a single Feed instance'''
    class Meta:
        model = Feed
        fields = ('id', 'title', 'link', 'description')
        read_only_fields = ('title', 'link', 'description')
