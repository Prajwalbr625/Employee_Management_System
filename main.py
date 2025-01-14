from app.routes import routes
from flask import Flask
from app.routes import routes


app = Flask(__name__)


app.register_blueprint(routes.app_routes)

if __name__ == '__main__':
    app.run(host='0.0.0.0',  port=8080, debug=True)