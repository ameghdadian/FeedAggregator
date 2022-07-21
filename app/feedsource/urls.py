from django.urls import path, include
from rest_framework.routers import DefaultRouter

from feedsource.views import FeedSourceViewSet

router = DefaultRouter()
router.register('', FeedSourceViewSet)

app_name = 'feedsource'

urlpatterns = [
    path('', include(router.urls)),
]
