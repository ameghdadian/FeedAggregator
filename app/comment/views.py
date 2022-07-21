from rest_framework import (viewsets,
                            authentication,
                            permissions,
                            status
                            )
from rest_framework.decorators import action
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from core.models import Comment, Feed
from comment.serializers import (
    ListCommentSerializer,
    SubmitCommentSerializer,
)


class CommentViewSet(viewsets.GenericViewSet):
    '''Viewset for Comment instances'''
    queryset = Comment.objects.all()
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        serializers = {
            'comments': ListCommentSerializer,
            'submit_comment': SubmitCommentSerializer,
        }

        return serializers[self.action]

    @action(detail=True)
    def comments(self, request, pk=None):
        '''Return a certain feed item comments'''
        queryset = self.get_queryset().filter(commented_on__id=pk)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer_class()
            serializer = serializer(queryset, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='submit-comment')
    def submit_comment(self, request, pk=None):
        '''Submit a comment using this action'''
        user = self.request.user
        feed = get_object_or_404(Feed, pk=pk)

        serializer = self.get_serializer_class()
        serializer = serializer(data=self.request.data)

        if serializer.is_valid():
            content = serializer.validated_data.get('content')
            Comment.objects.create(
                content=content, commenter=user, commented_on=feed
                )
            return Response(
                serializer.validated_data, status=status.HTTP_201_CREATED
                )

        return Response(serializer.errors)
