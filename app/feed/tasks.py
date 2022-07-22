from django.conf import settings
from django.db.utils import IntegrityError
from billiard.exceptions import SoftTimeLimitExceeded
from requests.exceptions import Timeout

import feedparser

import logging

from app import celery_app as app
from core.models import FeedSource, Feed

logger = logging.getLogger(__name__)


@app.task(bind=True, routing_key=settings.FEED_ROUTING_KEY, max_retries=2)
def fetch_feeds(self):
    '''
    Get FeedSources from their table and fetch corresponding feeds.
    Get remaining_feedsources in case of retry operation.
    '''
    feed_sources = FeedSource.objects.all()
    logger.warning('Starting to fetch feed items.')

    try:
        if feed_sources.exists():
            for fs in feed_sources:
                logger.warning(f'Fetching {fs.name} feed items ...')
                feeds = feedparser.parse(fs.link)
                for feed_item in feeds.entries:
                    try:
                        Feed.objects.create(
                            title=feed_item.title,
                            link=feed_item.link,
                            description=feed_item.summary,
                            topic=fs
                        )
                    except IntegrityError as e:
                        logger.warning(f'{e}')
        else:
            raise RuntimeError('Did you run fillfeedsource Django command?')
    except (SoftTimeLimitExceeded, Timeout, Exception) as e:
        raise self.retry(exc=e, countdown=1 * 2 ** self.request.retries)
