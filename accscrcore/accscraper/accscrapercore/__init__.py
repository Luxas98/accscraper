import threading
from pymongo import MongoClient


class RequestStorage(object):
    _local = threading.local()

    @staticmethod
    def snapshot():
        thread_local_storage = getattr(RequestStorage._local, 'storage', None)
        if not thread_local_storage:
            RequestStorage._local.storage = {}

        RequestStorage._local.old_storage = {}
        RequestStorage._local.old_storage.update(RequestStorage._local.storage)

    @staticmethod
    def recover():
        old_thread_local_storage = getattr(RequestStorage._local, 'old_storage', None)
        if old_thread_local_storage:
            RequestStorage._local.storage = old_thread_local_storage

    @staticmethod
    def append_data(data):
        thread_local_storage = getattr(RequestStorage._local, 'storage', None)
        if not thread_local_storage:
            RequestStorage._local.storage = {}

        RequestStorage._local.storage.update(data)

    @staticmethod
    def get_data():
        thread_local_storage = getattr(RequestStorage._local, 'storage', None)
        if not thread_local_storage:
            RequestStorage._local.storage = thread_local_storage = {}

        return thread_local_storage

    @staticmethod
    def init_task_storage(data):
        RequestStorage._local.storage = data


class MongoStorage(object):
    _storage = None

    @property
    def db(self):
        if MongoStorage._storage is None:
            MongoStorage._storage = MongoClient('mongo')
        return MongoStorage._storage

    def get_client_apartments_ids(self, client):
        apartments = self.db.rental_apartments.apartments.find({'client': client})
        # TODO: some preprocessing?
        return {apartment['id'] for apartment in apartments}

    def insert_apartment(self, apartment):
        apartment_id = self.db.rental_apartments.apartments.insert_one(apartment).inserted_id
        return apartment_id
