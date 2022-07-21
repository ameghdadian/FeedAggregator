from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import management

from rest_framework.test import APIClient
from rest_framework import status

from core.models import FeedSource
from feedsource.serializers import FeedSourceSerializer


ALL_TOPICS_URL = reverse('feedsource:feedsource-list')


def get_subscribe_url(feedsrc_id):
    return reverse('feedsource:feedsource-subscribe', args=[feedsrc_id])


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicFeedSourceApiTests(TestCase):
    '''Test the public FeedSource API'''

    def setUp(self):
        self.client = APIClient()

    def test_topics_needs_auth(self):
        '''
        Test that authentication is needed for accessing all-topics url
        '''
        res = self.client.get(ALL_TOPICS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_subscribe_topic_unauthorized(self):
        '''Test that unauthorized user can not subscibe to a FeedSource'''
        url = get_subscribe_url(1)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateFeedSourceApiTests(TestCase):
    '''Test the private FeedSource API'''

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(username='test username', password='test123')
        self.client.force_authenticate(self.user)
        management.call_command('fillfeedsource')

    def test_retrieve_feedsource_successful(self):
        '''Test that retrieving all feedsources is successful'''
        res = self.client.get(ALL_TOPICS_URL)

        feedsources = FeedSource.objects.all()
        serializer = FeedSourceSerializer(feedsources, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    def test_post_all_feedsource_not_allowed(self):
        '''Test that POST is not allowed on all-topics url'''
        res = self.client.post(ALL_TOPICS_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_subscribe_feedsource_not_allowed(self):
        '''Test that POST is not allowed on all-topics url'''
        res = self.client.post(get_subscribe_url(1), {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_subscribe_feedsource_successful(self):
        '''Test that authorized user can subscribe to a feedsource'''
        feedsrc = FeedSource.objects.all()[0]
        res = self.client.get(get_subscribe_url(feedsrc.id))

        user_exists = FeedSource.objects.get(name=feedsrc.name).followed_by. \
            filter(username=self.user.username).exists()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(user_exists)
