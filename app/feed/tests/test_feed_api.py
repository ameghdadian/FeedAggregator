from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import FeedSource, Feed
from feed.serializer import ListFeedSerializer, RetriveSingleFeedSerializer


ALL_FEEDS_URL = reverse('feed:all-list')
UNREAD_URL = reverse('feed:all-unread')


def detail_feed_url(feed_id):
    '''Retrieve single feed url'''
    return reverse('feed:all-detail', args=[feed_id])


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


def create_feed(feed_src, id, **params):
    defaults = {
        'title': f'Test title {id}',
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

    def test_unauthorized_feed_getall_fails(self):
        '''Test that unauthrized user can not access feed items'''
        res = self.client.get(ALL_FEEDS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_feed_retrieve_fails(self):
        '''Test that unauthrized user can not access detail feed view'''
        feed_src1 = create_feedsource()
        feed = create_feed(feed_src1, 1)

        url = detail_feed_url(feed.id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_unread_api_fails(self):
        '''Test that unauthorized user cannot access unread endpoint'''
        res = self.client.get(UNREAD_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateFeedApiTests(TestCase):
    '''Test private Feed API'''

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_gettingall_feeds_successful(self):
        '''
        Test that a user can only see its own followed feeds
        '''
        feed_src1 = create_feedsource()
        feed_src2 = create_feedsource()
        feed_src3 = create_feedsource()

        feed_src1.followed_by.add(self.user)
        feed_src2.followed_by.add(self.user)

        create_feed(feed_src1, 1)
        create_feed(feed_src2, 2)
        create_feed(feed_src3, 3)
        res = self.client.get(ALL_FEEDS_URL)
        user_feeds = Feed.objects.\
            filter(topic__in=[feed_src1.id, feed_src2.id]).order_by('-title')
        serializer = ListFeedSerializer(user_feeds, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data['results'])

    def test_retrieving_feeds_successful(self):
        '''
        Test that an authorized user can only see a single feed
        '''
        feed_src1 = create_feedsource()
        feed_src1.followed_by.add(self.user)

        feed = create_feed(feed_src1, 1)

        url = detail_feed_url(feed.id)
        res = self.client.get(url)

        serializer = RetriveSingleFeedSerializer(feed)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)

    def test_retrieve_unread_successful(self):
        '''Test that authorized user can access unread endpoint successfully'''
        feed_src1 = create_feedsource()
        feed_src2 = create_feedsource()
        feed_src1.followed_by.add(self.user)

        feed1 = create_feed(feed_src1, 1)
        create_feed(feed_src1, 2)
        create_feed(feed_src2, 3)

        feed1.read_by.add(self.user.id)

        res = self.client.get(UNREAD_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 1)
