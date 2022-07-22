from django.conf import settings
import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

celery_app = Celery('app')


class CeleryRouter:
    _cache = {}

    @staticmethod
    def route_task(name, args, kwargs, options, task=None, **kw):
        if name in CeleryRouter._cache:
            return CeleryRouter._cache[name]

        route_info = {'routing_key': settings.DEFAULT_ROUTING_KEY,
                      'queue': settings.CELERY_TASK_DEFAULT_QUEUE}
        defined_rk = options.get('routing_key')
        if defined_rk:
            for queue in settings.CELERY_TASK_QUEUES:
                if queue.routing_key == defined_rk:
                    route_info = {'routing_key': defined_rk,
                                  'queue': queue.name}
                    CeleryRouter._cache[name] = route_info
                    return route_info

        CeleryRouter._cache[name] = route_info
        return route_info


@celery_app.on_after_finalize.connect
def setup_periodic_task(sender, **kwargs):
    from feed.tasks import fetch_feeds
    sender.add_periodic_task(60, fetch_feeds.s())


celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
celery_app.conf.update({
    'task_routes': CeleryRouter.route_task
})
