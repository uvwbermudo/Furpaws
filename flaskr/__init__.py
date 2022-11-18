from flask import Flask
from config import DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOST, SECRET_KEY
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import create_database, database_exists
import pymysql
from flask_wtf.csrf import CSRFProtect


db_url = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}" 
db = SQLAlchemy()

if not database_exists(db_url):
    print('DB CREATED')
    create_database(db_url)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']=SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI']= db_url
    db.init_app(app)
    CSRFProtect(app)

    from .auth import auth

    from .models import Users
    app.register_blueprint(auth, url_prefix='/')


    with app.app_context():
        db.create_all()



    return app


def get_error_items(form):
    errors = {}
    for fieldName, errorMessages in form.errors.items():
        errors[fieldName] = errorMessages
    return errors

def get_form_fields(form):
    fields = []
    for keys in form.data.keys():
        fields.append(keys)
    return fields