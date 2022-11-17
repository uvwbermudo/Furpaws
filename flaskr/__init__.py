from flask import Flask
from config import DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOST, SECRET_KEY


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']=SECRET_KEY

    from .auth import auth

    app.register_blueprint(auth, url_prefix='/')





    return app