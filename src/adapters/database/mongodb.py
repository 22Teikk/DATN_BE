import os
from pymongo import MongoClient


class MongoDB:
    def __init__(self):
        mongo_uri = f"mongodb://"
        self.client = MongoClient(mongo_uri)
        self.db = self.client['DATN']
        try:
            self.client.admin.command("ping")
            print(">>> Kết nối tới MongoDB thành công!")
        except Exception as e:
            print(">>> Không thể kết nối tới MongoDB.", e)
            exit(1)

    def get_collection(self, name):
        return self.db[name]
