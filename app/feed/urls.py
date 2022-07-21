from django.urls import path, include

from rest_framework.routers import DefaultRouter

from comment.views import CommentViewSet


router = DefaultRouter()
router.register('', CommentViewSet)


app_name = 'feed'


urlpatterns = [
    path('', include(router.urls)),
]
