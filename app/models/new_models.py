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
    
    def add_user(self, user_info):
        try:
            logging.info(f'\t Inside add user function --> new_model.py')
            self.usercollection.insert_one({"UserData":user_info})
            logging.info('\t user added successfully')
            return "data inserted successfully", 201
        except Exception as e:
            return str(e), 500
    
    def get_user_by_id(self, user_id):
        try:
            logging.info(f"\t inside get user function --> new_model.py")
            user = self.usercollection.find_one({"userID": user_id})
            if user is None:
                logging.error(f'\t User not found in the DB')
                return 'User not found in the DB', 404
            user.pop('_id', None)
            logging.info(f'\t User data fetched successfully')
            return user, 200
        except Exception as e:
            logging.error(f'\t Error: {e}')
            return str(e), 500
        
    def update_user(self, user_id, user_data):
        try:
            logging.info(f"\t inside update user function")
            user_update = self.usercollection.update_one({"userID": user_id}, {"$set": user_data})
            if user_update.matched_count == 0:
               logging.error(f'\t user not found in the db') 
               return 'user not found', 404
            logging.info(f'\t user updated successfully')
            return user_update, 200
        except Exception as e:
            logging.error(f'\t Error: {e}')
            return str(e), 500
    
    def delete_user(self, user_id):
        try:
            logging.info(f"\t inside the delete user function")
            remove = self.usercollection.delete_one({"userID":user_id})
            if remove.deleted_count == 0:
                logging.error(f'\t user not found in db')
                return 'user not found', 404
            logging.info('\t user is deleted successfully')
            return remove, 200
        except Exception as e:
            logging.error(f'\t Error: {e}')
            return str(e), 500


mongodb = DB()