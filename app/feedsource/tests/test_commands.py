from django.test import TestCase
from django.core import management

from unittest.mock import patch

from core.models import FeedSource


class TestCommands(TestCase):
    def test_fill_feedsource_successful(self):
        '''Testing fillfeedsource command'''
        with patch.object(FeedSource.objects, 'create') as mock_fn:
            management.call_command('fillfeedsource')

            mock_fn.assert_called()
