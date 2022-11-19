from flaskr import db
from flask_login import UserMixin


class Users(db.Model, UserMixin):
    __tablename__='users'
    tag = db.Column(db.String(25), primary_key=True, nullable=False)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150), nullable=False)
    account_type = db.Column(db.String(20), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zipcode = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)

    def get_id(self):
        return self.tag

