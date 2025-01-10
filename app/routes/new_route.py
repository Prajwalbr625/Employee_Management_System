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

    message, status_code = mongodb.insert_user(user_data=user_data)
    if status_code == 201:
        return jsonify({"message":message}, status_code)
    else:
        return jsonify({"error":message}, 500)