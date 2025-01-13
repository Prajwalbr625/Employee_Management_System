from flask import Blueprint, jsonify
from app.utils.test_runner import run_tests

app_report = Blueprint('app_report', __name__)

@app_report.route('/report', methods=['GET'])
def report():
    test_results = run_tests()
    return jsonify({"test_results": test_results})