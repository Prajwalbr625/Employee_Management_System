from flask import Flask, Blueprint, request, jsonify
import logging
import uuid
from app.models.new_models import mongodb

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app_user = Blueprint('app_user', __name__)

@app_user.route('/user', methods=['POST'])
def add_user():
    logging.info(f"in the add_user function")
    user_data = request.get_json()

    message, status_code = mongodb.add_user(user_info=user_data)
    if status_code == 201:
        return jsonify({"message":message}, status_code)
    else:
        return jsonify({"error":message}, 500)

@app_user.route('/user/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    logging.info(f"in the get user data function")
    user, status_code = mongodb.get_user_by_id(user_id=user_id)
    if status_code == 200:
        return jsonify(user), status_code
    else:
        return jsonify({"error": user}), status_code

@app_user.route('/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    logging.info(f'\t in the update user function')
    user_update = request.get_json()
    message, status_code = mongodb.update_user(user_id=user_id, user_data=user_update)
    if status_code == 200:
       return jsonify({'message': message}), status_code
    else:
        return jsonify({"error": message}), status_code 

@app_user.route('/user/<user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    logging.info(f'\t in the delete user by id function')
    message, status_code = mongodb.delete_user(user_id=user_id)
    if status_code == 200:
        return jsonify({'message': message}), status_code
    else:
        return jsonify({"error": message}), status_code 