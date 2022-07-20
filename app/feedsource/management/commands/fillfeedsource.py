from django.core.management.base import BaseCommand

from core.models import FeedSource


INITIAL_VALUES = (
    ('Business', 'https://www.wired.com/feed/category/business/latest/rss'),
    ('Artificial Intelligence',
     'https://www.wired.com/feed/tag/ai/latest/rss'),
    ('Culture', 'https://www.wired.com/feed/category/culture/latest/rss'),
    ('Gear', 'https://www.wired.com/feed/category/gear/latest/rss'),
    ('Ideas', 'https://www.wired.com/feed/category/ideas/latest/rss'),
    ('Science', 'https://www.wired.com/feed/category/science/latest/rss'),
    ('Security', 'https://www.wired.com/feed/category/security/latest/rss'),
)


class Command(BaseCommand):
    '''
    This command needs to be run on server start-up to fill the FeedSource
    table with the sources that we are going to fetch the feeds from.
    '''
    help = 'Fill FeedSource table with its initial values'

    def handle(self, *args, **options):
        for name, link in INITIAL_VALUES:
            FeedSource.objects.create(name=name, link=link)

        self.stdout.write(self.style.SUCCESS(
            'Successfully added initial data to FeedSource table.'
            ))
