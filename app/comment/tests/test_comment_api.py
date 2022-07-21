from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Feed, FeedSource, Comment
from comment.serializers import ListCommentSerializer


def all_commments_url(feed_id):
    return reverse('feed:comment-comments', args=[feed_id])


def submit_comment_url(feed_id):
    return reverse('feed:comment-submit-comment', args=[feed_id])


def create_user(username="testuser", password="testpass"):
    return get_user_model().objects.create_user(
        username=username, password=password
        )


def create_feedsource(user):
    feedsrc = FeedSource.objects.create(
        name='Test content',
        link='Test link',
    )

    feedsrc.followed_by.add(user)
    return feedsrc


def create_feed(feed_src, **params):
    defaults = {
        'title': 'Test title',
        'link': 'Test link',
        'description': 'Test description',
        'topic': feed_src,
    }
    defaults.update(params)

    return Feed.objects.create(**defaults)


def create_comment(user, feed, content='Test comment content'):
    return Comment.objects.create(
        content=content,
        commenter=user,
        commented_on=feed
    )


class PublicCommentApiTests(TestCase):
    '''Testing public Comment API'''

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_comments_unauthorized(self):
        '''Test unauthorized user can not access comments'''
        url = all_commments_url(1)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_submit_comment_unauthorized(self):
        '''Test that unauthorized user can not submit comment'''
        url = submit_comment_url(1)
        res = self.client.post(url, {})

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCommentApiTests(TestCase):
    '''Test authorized comment API'''

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_retrieve_comments_successful(self):
        '''
        Test that retrieving comments of a feed for an authorized user is
        successful
        '''
        feed_src = create_feedsource(self.user)
        feed = create_feed(feed_src)
        create_comment(self.user, feed)
        create_comment(self.user, feed, 'Test comment2')

        url = all_commments_url(feed.id)
        res = self.client.get(url)

        comments = Comment.objects.filter(commented_on__id=feed.id)
        serializer = ListCommentSerializer(comments, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    def test_submit_comment_successful(self):
        '''Test that submit a comment is allowed for authorized user'''
        feedsrc = create_feedsource(self.user)
        feed = create_feed(feedsrc)
        payload = {
            'content': 'Test payload content',
        }

        url = submit_comment_url(feed.id)
        res = self.client.post(url, payload)

        comment_exists = Comment.objects.filter(content=payload['content']) \
            .exists()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(comment_exists)

    def test_submit_comment_no_feed(self):
        '''
        Test that trying to submit a comment on a non-existent feed fails
        '''
        payload = {
            'content': 'Test payload content',
        }

        url = submit_comment_url(20)  # ID of non-existent feed
        res = self.client.post(url, payload)

        comment_exists = Comment.objects.filter(content=payload['content']) \
            .exists()

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(comment_exists)
