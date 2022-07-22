from django.urls import path, include

from rest_framework.routers import DefaultRouter

from comment.views import CommentViewSet
from feed.views import ListFeedViewSet


router = DefaultRouter()
router.register('', CommentViewSet)
router.register('all', ListFeedViewSet, 'all')

app_name = 'feed'


urlpatterns = [
    path('', include(router.urls)),
]
