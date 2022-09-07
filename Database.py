import pymongo
import os
import dotenv
from Useful_Function import Function, get_env_full_path


class Database:
    def __init__(self):
        useful_function = Function()
        full_path = get_env_full_path()
        dotenv.load_dotenv(full_path + "/.env")
        self.url_database = "mongodb+srv://%s:%s@%s.klaol.mongodb.net/?retryWrites=true&w=majority" % (
            os.getenv("DATABASE_USER"),
            os.getenv("DATABASE_PASSWORD"),
            os.getenv("DATABASE_NAME")
        )
        self.client = pymongo.MongoClient(self.url_database)
        self.db = self.client[os.getenv("DATABASE_NAME")]
        self.collection = None

    def get_collection(self):
        return self.collection

    def get_all_collections(self):
        return self.client.list_collection_names()

    def set_collection(self, collection_name):
        self.collection = self.db[collection_name]

    def get_all_items(self):
        return self.collection.find()

    def find(self, query):
        return self.collection.find(query)

    def find_one(self, query):
        return self.collection.find_one(query)

    def insert_single(self, data):
        result = self.collection.insert_one(data)
        return result.inserted_id

    def insert_multiples(self, data):
        return self.collection.insert_many(data)

    def update_one(self, query, data):
        return self.collection.update_one(query, data)

    def update_many(self, query, data):
        return self.collection.update_many(query, data)

    def delete_one(self, query):
        return self.collection.delete_one(query)

    def delete_many(self, query):
        return self.collection.delete_many(query)

    def count(self):
        return self.collection.count()

    def drop(self):
        return self.collection.drop()

    def close(self):
        return self.client.close()

    def get_database_name(self):
        return self.client.list_database_names()

    def get_collection_name(self):
        return self.collection.list_collection_names()

    def create_new_collection(self, collection_name):
        return self.client[collection_name]

    def find_by_product_id(self, product_id):
        return self.collection.find({"id": product_id})

    def find_by_object(self, query: dict):
        """
        This method is used to find an object in the database.
        :param query: The query to find the object.
        :return: The object found.
        """
        return self.collection.find_one(query)


    def get_all_documents(self):
        return self.collection.find()