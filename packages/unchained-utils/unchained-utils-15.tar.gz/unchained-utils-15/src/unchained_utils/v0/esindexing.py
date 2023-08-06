import logging
import os

from django.db import transaction

from django.db.models.signals import post_save, post_delete

from django.conf import settings

logger = logging.getLogger('base')


def index_post_receiver(sender, instance, **kwargs):
    instance.indexing()


def connect_senders(senders):
    for sender in senders:
        post_save.connect(index_post_receiver, sender=sender)
        post_delete.connect(index_post_receiver, sender=sender)


class IndexingAppMixing:
    models_to_index = []

    def ready(self):
        connect_senders(self.models_to_index)


class IndexingMixin:
    def index_object(self):
        # TODO index only changed values, and selected ones
        return None

    def indexing(self, bulk=False):
        obj = self.index_object()

        def object_save():
            try:
                obj.save()
            except Exception as e:
                logger.error('error while indexing {}'.format(e))

        if obj:
            if not bulk:
                if settings.ENABLE_INDEXING:
                    transaction.on_commit(
                        lambda: logger.info('start indexing an instance of {}...'.format(str(self._meta))))
                    transaction.on_commit(object_save)
                else:
                    logger.warning('indexing disabled')
            else:
                return obj.to_dict(include_meta=True)


if os.environ.get('ELASTIC_SEARCH_HOST'):
    from elasticsearch_dsl import connections

    ELASTIC_SEARCH_CONNECTION = connections.create_connection(hosts=[os.environ.get('ELASTIC_SEARCH_HOST')], timeout=30,
                                                              max_retries=10,
                                                              send_get_body_as='POST', retry_on_timeout=True,
                                                              maxsize=25)
    ELASTIC_SEARCH_BULK_OPTIONS = {
        'request_timeout': 120,
        'max_retries': 10,
        'chunk_size': 100000000
    }


class BaseBulkIndexing():
    index = None
    model = None
    quota = 5000

    def _bulk(self, actions):
        from elasticsearch.helpers import bulk
        bulk(client=ELASTIC_SEARCH_CONNECTION, **{
            'request_timeout': 120,
            'max_retries': 10,
            'chunk_size': 100000000
        },
             actions=actions)

    def run(self):

        self.index.init()
        cpt = 0
        objects_iterator = self.model.all_objects.all().iterator()
        next_object = next(objects_iterator, None)

        actions = []
        while next_object:
            cpt += 1
            actions.append(next_object.indexing(bulk=True))
            if cpt % self.quota == 0:
                self._bulk(actions)
                actions = []
            next_object = next(objects_iterator, None)

        if actions:
            self._bulk(actions)
