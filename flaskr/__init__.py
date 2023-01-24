from flask import Flask
from config import DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOST, SECRET_KEY,FLASK_PORT, SOCKET_LOCAL
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import create_database, database_exists
from flaskr.sql_init import create_db
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_mysql_connector import MySQL
from flask_socketio import SocketIO

db_url = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
mysql = MySQL()
app = Flask(__name__)
socketio = SocketIO(app,cors_allowed_origins='*')
socket_add = SOCKET_LOCAL
flask_port = FLASK_PORT


def create_app():
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['MYSQL_HOST'] = DB_HOST
    app.config['MYSQL_USER'] = DB_USERNAME
    app.config['MYSQL_PASSWORD'] = DB_PASSWORD
    app.config['MYSQL_DATABASE'] = DB_NAME
    create_db()
    mysql.init_app(app)
    CSRFProtect(app)

    from .auth import auth
    from .home import home
    from .profile import profile
    from .jobs import jobs
    from .friends import friends
    from .messages import msgs
    from .profile import profile

    app.register_blueprint(profile, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(home, url_prefix='/')
    app.register_blueprint(jobs, url_prefix='/')
    app.register_blueprint(friends, url_prefix='/')

    app.register_blueprint(msgs, url_prefix='/')
    from .models import Users

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    login_manager.login_message = None

    @login_manager.user_loader
    def load_user(tag):
        return Users.query_get(tag)

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
