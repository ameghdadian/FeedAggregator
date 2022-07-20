from django.db import models
from django.conf import settings


class FeedSource(models.Model):
    name = models.CharField(max_length=30)
    followed_by = models.ManyToManyField(settings.AUTH_USER_MODEL)
    link = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'


class Feed(models.Model):
    title = models.TextField(unique=True)
    link = models.CharField(max_length=255)
    description = models.TextField()
    topic = models.ForeignKey(FeedSource, on_delete=models.CASCADE)
    read_by = models.ManyToManyField(
                                    settings.AUTH_USER_MODEL,
                                    related_name="read_feeds"
                                    )
    favourite_by = models.ManyToManyField(
                                    settings.AUTH_USER_MODEL,
                                    related_name="favorite_feeds"
                                    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}'


class Comment(models.Model):
    content = models.TextField()
    commenter = models.ForeignKey(
                                settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE
                                )
    commented_on = models.ForeignKey(Feed, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.content} by {self.commenter.username}'
