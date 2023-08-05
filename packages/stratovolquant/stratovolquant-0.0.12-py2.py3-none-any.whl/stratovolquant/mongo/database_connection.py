import os
import json
from pymongo import MongoClient
from arctic import Arctic


class DatabaseConnection:
    __instance = None
    __mongo_client = None
    __arctic_client = None

    @staticmethod
    def get_instance(credentials_filename=None):
        if DatabaseConnection.__instance is None:
            DatabaseConnection(credentials_filename)
        return DatabaseConnection.__instance

    def __init__(self, credentials_filename=None):
        if DatabaseConnection.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            DatabaseConnection.__instance = self

        if credentials_filename is None:
            private_dirs = ['../../data/private/', '../data/private/', 'data/private/', '../../../data/private/',
                            'private/']
            i = 0
            while i < len(private_dirs):
                private_dir = private_dirs[i]
                if os.path.isdir(private_dir):
                    break
                i = i + 1
            filename = 'mongo.json'
            self.credentials_filename = private_dir + filename
        else:
            self.credentials_filename = credentials_filename
        self.cache_dir = None

    def get_client(self, use_arctic=False):
        with open(self.credentials_filename) as f:
            d = json.load(f)
            login = d['login']
            pwd = d['pwd']
            cluster = d['cluster']
            self.cache_dir = d['cache_dir']

        connection_str = 'mongodb+srv://' + login + ':' + pwd + '@' + cluster + '.mongodb.net/test'
        if not use_arctic:
            if DatabaseConnection.__mongo_client is None:
                DatabaseConnection.__mongo_client = MongoClient(connection_str)
            return DatabaseConnection.__mongo_client
        else:
            if DatabaseConnection.__arctic_client is None:
                DatabaseConnection.__arctic_client = Arctic(connection_str)
            return DatabaseConnection.__arctic_client
