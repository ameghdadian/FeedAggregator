from core.models import FeedSource


class FeedSourceHelper:
    @staticmethod
    def get_user_followed_feedsrc(user):
        return FeedSource.objects.filter(followed_by__id=user.id)
