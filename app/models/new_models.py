from pymongo import MongoClient
import logging
import certifi
import app.config as config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DB:
    def __init__(self):
        self.db = self.setup_db()
        self.usercollection = self.db[config.MONGO_USER_COLLECTION]

    
    def setup_db(self):
        logging.info(f"\t Requested for db connection")
        client = MongoClient(config.MONGO_URI)
        client_access = client[config.MONGO_DB_NAME]

        return client_access
    
    def insert_user(self, user_data):
        try:
            self.usercollection.insert_one(user_data)
            return "data inserted successfully", 201
        except Exception as e:
            return e, 500

mongodb = DB()