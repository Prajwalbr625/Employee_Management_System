from flask import Flask
from app.routes import employee_routes, department_routes, new_route, report_route


app = Flask(__name__)


app.register_blueprint(employee_routes.app_employee)
app.register_blueprint(department_routes.app_department)
app.register_blueprint(new_route.app_user)
app.register_blueprint(report_route.app_report)

if __name__ == '__main__':

    app.run(host='0.0.0.0',  port=8080, debug=True)