from django.shortcuts import get_object_or_404
from rest_framework import (mixins, viewsets, authentication,
                            permissions, status)
from rest_framework.decorators import action
from rest_framework.response import Response


from core.models import FeedSource
from feedsource.serializers import FeedSourceSerializer


class FeedSourceViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    '''Manage the FeedSource instances'''
    queryset = FeedSource.objects.all()
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FeedSourceSerializer

    @action(detail=True)
    def subscribe(self, request, pk=None):
        feedsrc = get_object_or_404(FeedSource, pk=pk)
        feedsrc.followed_by.add(self.request.user)
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)
