from rest_framework import viewsets, mixins, authentication, permissions

from core.models import Feed, FeedSource
from feed.serializer import ListFeedSerializer


class ListFeedViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ListFeedSerializer

    def get_queryset(self):
        user = self.request.user
        followed_feedsrc = FeedSource.objects.filter(followed_by__id=user.id)\
            .values_list('id', flat=True)
        return Feed.objects.filter(topic__id__in=followed_feedsrc)\
            .order_by('-title')
