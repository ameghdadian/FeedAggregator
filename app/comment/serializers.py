from rest_framework import serializers

from core.models import Comment


class ListCommentSerializer(serializers.ModelSerializer):
    '''Serialize Comment instances'''

    class Meta:
        model = Comment
        fields = ('content', 'commenter',)
        read_only_fields = ('content', 'commenter',)


class SubmitCommentSerializer(serializers.ModelSerializer):
    '''Serializer for submitting a comment on a feed'''

    class Meta:
        model = Comment
        fields = ('content',)
