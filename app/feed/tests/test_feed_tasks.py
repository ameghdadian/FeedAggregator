from unittest.mock import patch

from django.test import TestCase
from django.core.management import call_command
from requests.exceptions import Timeout
from celery.exceptions import Retry

from feed.tasks import fetch_feeds
from core.models import FeedSource


class FetchFeedsPeriodicTaskTest(TestCase):
    '''Test fetch_feeds task is working as expected'''
    @patch('feed.tasks.feedparser.parse')
    def test_fetch_feeds_successful(self, mock_parse):
        '''
        Test fetching feed items is successful
        '''
        call_command('fillfeedsource')
        feedsrc_cnt = FeedSource.objects.all().count()

        fetch_feeds()
        self.assertEqual(feedsrc_cnt, mock_parse.call_count)

    @patch('feed.tasks.feedparser')
    def test_fetch_feeds_empty_feedsrc(self, mock_feedparser):
        '''
        Test that fillfeedsource command needs to be run to
        populate FeedSource table. Failing to run this command
        raises RunTimeError
        '''
        with self.assertRaises(RuntimeError):
            fetch_feeds()

    @patch('feed.tasks.feedparser')
    @patch('feed.tasks.fetch_feeds.retry')
    def test_fetch_feeds_retry(self, mock_ff_retry, mock_feedparser):
        '''
        Test that fetch_feeds retries whenever an exception
        happens
        '''
        call_command('fillfeedsource')

        mock_ff_retry.side_effect = Retry
        mock_feedparser.parse.side_effect = Timeout
        with self.assertRaises(Retry):
            fetch_feeds()
