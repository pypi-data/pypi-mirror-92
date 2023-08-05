import json
import os

from . import database_connection


class CollectionManager:
    __instance = None
    __cache_dir = None

    @staticmethod
    def get_instance(use_cache=True):
        if CollectionManager.__instance is None:
            CollectionManager(use_cache)
        return CollectionManager.__instance

    def __init__(self, use_cache):
        if CollectionManager.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            CollectionManager.__instance = self

        self.id = 0
        self.use_cache = use_cache

    @staticmethod
    def get_library(name):
        connection = database_connection.DatabaseConnection.get_instance()
        return connection.get_library(name)

    def get_documents(self, library_name, collection_name, search_filter=None):
        # documents = list(self.poc_lib[collection_name].find(search_filter))
        cache_filename = CollectionManager.make_cache_filename(collection_name)
        if not self.use_cache or not os.path.exists(cache_filename):
            documents = list(CollectionManager.get_library(library_name)[collection_name].find())
            for dico in documents:
                del dico["_id"]
            with open(cache_filename, 'w') as cache_file:
                json.dump(documents, cache_file, indent=2)

        with open(cache_filename) as json_file:
            documents = list(json.load(json_file))
            if search_filter is not None:
                for key, value in search_filter.items():
                    documents = [doc for doc in documents if doc[key] == value]

        return documents

    @staticmethod
    def upload_csv(library_name, collection_name, filename, sep=','):
        with open(filename) as f:
            next(f)
            headers = [header.strip() for header in next(f).split(sep)]

            for line in f:
                values = [value.strip() for value in line.split(sep)]
                dico = dict(zip(headers, values))
                CollectionManager.get_library(library_name)[collection_name].insert_one(dico)

    @staticmethod
    def upload_json(library_name, collection_name, filename):
        collection = CollectionManager.get_library(library_name)[collection_name]
        with open(filename) as json_file:
            documents = json.load(json_file)
            for document in documents:
                collection.insert_one(document)

    @staticmethod
    def make_cache_dir():
        if CollectionManager.__cache_dir is None:
            data_dirs = ['data', '../data', '../../data', '../../../data']
            for data_dir in data_dirs:
                if os.path.isdir(data_dir):
                    CollectionManager.__cache_dir = data_dir + '/cache'
                    break

            if not os.path.isdir(CollectionManager.__cache_dir):
                os.mkdir(CollectionManager.__cache_dir)
        return CollectionManager.__cache_dir

    @staticmethod
    def make_cache_filename(collection_name):
        cache_dir = CollectionManager.make_cache_dir()
        return '{0}/{1}.json'.format(cache_dir, collection_name)
