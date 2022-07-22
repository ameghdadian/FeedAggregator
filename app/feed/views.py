from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, authentication, permissions

from core.models import Feed, FeedSource
from feed.serializer import ListFeedSerializer, RetriveSingleFeedSerializer


class ListFeedViewSet(
                    viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin
        ):
    '''Feed viewset'''
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ListFeedSerializer

    def get_queryset(self):
        user = self.request.user
        followed_feedsrc = FeedSource.objects.filter(followed_by__id=user.id)\
            .values_list('id', flat=True)
        return Feed.objects.filter(topic__id__in=followed_feedsrc)\
            .order_by('-title')

    def get_object(self):
        queryset = Feed.objects.all()
        feed = get_object_or_404(queryset, pk=self.kwargs['pk'])
        feed.read_by.add(self.request.user)
        return feed

    def get_serializer_class(self):
        serializers = {
            'list': ListFeedSerializer,
            'retrieve': RetriveSingleFeedSerializer
        }

        return serializers.get(self.action)
