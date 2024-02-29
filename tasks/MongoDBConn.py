import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import Config
class MongoDB(object):
    """
    MongoDB 数据库对象
    """

    def __init__(self, host=Config.MongoDB_URL, port=27017, db_name=Config.MongoDB_DBNAME):
        """
        构造函数，初始化 MongoDB 连接
        """
        self.client = MongoClient(host, port)
        self.db = self.client[db_name]

    def find_one(self, collection_name, filter=None):
        """
        查询单个文档
        """
        return self.db[collection_name].find_one(filter)

    def find(self, collection_name, filter=None, projection=None):
        """
        查询多个文档
        """
        return list(self.db[collection_name].find(filter, projection))

    def insert_one(self, collection_name, document):
        """
        插入单个文档
        """
        return self.db[collection_name].insert_one(document).inserted_id

    def insert_many(self, collection_name, documents):
        """
        插入多个文档
        """
        return self.db[collection_name].insert_many(documents).inserted_ids

    def update_one(self, collection_name, filter, update):
        """
        更新单个文档
        """
        return self.db[collection_name].update_one(filter, {'$set': update})

    def update_many(self, collection_name, filter, update):
        """
        更新多个文档
        """
        return self.db[collection_name].update_many(filter, {'$set': update})

    def delete_one(self, collection_name, filter):
        """
        删除单个文档
        """
        return self.db[collection_name].delete_one(filter)

    def delete_many(self, collection_name, filter):
        """
        删除多个文档
        """
        return self.db[collection_name].delete_many(filter)

    def count_documents(self, collection_name, filter=None):
        """
        统计文档数量
        """
        return self.db[collection_name].count_documents(filter)

    def close(self):
        """
        关闭 MongoDB 连接
        """
        self.client.close()

# 示例用法：
# mongodb = MongoDB()
# result = mongodb.find('your_collection_name', {'key': 'value'})
# print(result)
