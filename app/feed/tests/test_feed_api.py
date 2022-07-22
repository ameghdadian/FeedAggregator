from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import FeedSource, Feed
from feed.serializer import ListFeedSerializer


ALL_FEEDS_URL = reverse('feed:all-list')


def create_user(username='test', password='testpass'):
    return get_user_model().objects.create_user(
        username=username, password=password
        )


def create_feedsource():
    feedsrc = FeedSource.objects.create(
        name='Test content',
        link='Test link',
    )

    return feedsrc


def create_feed(feed_src, **params):
    defaults = {
        'title': f'Test title {feed_src.id}',
        'link': 'Test link',
        'description': 'Test description',
        'topic': feed_src,
    }
    defaults.update(params)

    return Feed.objects.create(**defaults)


class PublicFeedApiTests(TestCase):
    '''Test public Feed API'''
    def setUp(self):
        self.client = APIClient()

    def test_unauthorized_feed_retrieve_fails(self):
        '''Test that unauthrized user can not access feed items'''
        res = self.client.get(ALL_FEEDS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateFeedApiTests(TestCase):
    '''Test private Feed API'''

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_retrieving_feeds_successful(self):
        '''
        Test that a user can only see its own followed feeds
        '''
        feed_src1 = create_feedsource()
        feed_src2 = create_feedsource()
        feed_src3 = create_feedsource()

        feed_src1.followed_by.add(self.user)
        feed_src2.followed_by.add(self.user)

        create_feed(feed_src1)
        create_feed(feed_src2)
        create_feed(feed_src3)

        res = self.client.get(ALL_FEEDS_URL)

        user_feeds = Feed.objects.filter(topic__in=[feed_src1.id, feed_src2.id])\
            .order_by('-title')
        serializer = ListFeedSerializer(user_feeds, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data['results'])
