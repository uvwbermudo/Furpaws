from flask import Flask
from config import DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOST, SECRET_KEY
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import create_database, database_exists
import pymysql


db_url = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}" 
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']=SECRET_KEY

    from .auth import auth

    app.register_blueprint(auth, url_prefix='/')




    return app