from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_topic(**params):
    defaults = {
        'name': 'Test topic',
        'link': 'Test link'
    }

    defaults.update(params)
    return models.Topic.objects.create(**defaults)


def create_user(**params):
    defaults = {
        'username': 'testusername',
        'password': 'testpass'
    }

    defaults.update(params)
    return get_user_model().objects.create_user(**defaults)


def create_feed(**params):
    defaults = {
        'title': "Weather",
        'link': "test",
        'description': 'Tomorrow forecast',
        'topic': create_topic()
    }

    defaults.update(params)
    return models.Feed.objects.create(**defaults)


class ModelTests(TestCase):

    def test_create_user_successful(self):
        '''Test creating a new user is successful'''
        username = 'Test User'
        password = 'Test password'

        user = get_user_model().objects.create_user(
            username=username,
            password=password
        )

        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))

    def test_create_superuser_successful(self):
        '''Test creating a superuser is successful'''
        username = 'Test User'
        password = 'Test password'

        user = get_user_model().objects.create_superuser(
            username=username,
            password=password
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_feed_str_repr(self):
        '''Test the string representation of Feed instances'''
        feed = create_feed()

        self.assertEqual(str(feed), feed.title)

    def test_comment_str_repr(self):
        '''Test the string representation of Comment instances'''
        comment = models.Comment.objects.create(
            content='Good stuff',
            commenter=create_user(),
            commented_on=create_feed()
            )

        self.assertEqual(
            str(comment), f'{comment.content} by {comment.commenter.username}'
            )

    def test_topic_str_repr(self):
        '''Test the string representation of Topic instances'''
        topic = models.Topic.objects.create(
            name='Sport',
            link='Test'
            )

        self.assertEqual(str(topic), topic.name)
