import datetime
from flaskr import db
from flask_login import UserMixin
from sqlalchemy.ext.associationproxy import association_proxy


class Users(db.Model, UserMixin):
    __tablename__ = 'users'
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

    create_post_assoc = db.relationship('CreatePost', back_populates='author')
    created_posts = association_proxy('create_post_assoc', 'post')

    def get_id(self):
        return self.tag


class Posts(db.Model):
    __tablename__ = 'posts'
    author_tag = db.Column(db.String(25), db.ForeignKey('users.tag'))
    post_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    post_content = db.Column(db.Text(), nullable=True)
    date_posted = db.Column(db.DateTime(), nullable=False,
                            default=datetime.datetime.utcnow)

    create_post_assoc = db.relationship('CreatePost', back_populates='post')
    author = association_proxy('create_post_assoc', 'author')

    photos = db.relationship('Photos', back_populates='post')
    videos = db.relationship('Videos', back_populates='post')



class CreatePost(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    author_tag = db.Column(db.String(25), db.ForeignKey('users.tag'))
    post_id = db.Column(db.Integer(), db.ForeignKey(
        'posts.post_id', ondelete='cascade'))
    date_created = db.Column(db.DateTime(), default=datetime.datetime.utcnow)

    author = db.relationship('Users', back_populates='create_post_assoc')
    post = db.relationship('Posts', back_populates='create_post_assoc')


class Photos(db.Model):
    __tablename__ = 'photos'
    photo_id = db.Column(db.Integer(), primary_key=True,
                         nullable=False, autoincrement=True)
    parent_post = db.Column(db.Integer(), db.ForeignKey(
        'posts.post_id', ondelete='cascade'))
    photo_url = db.Column(db.String(150), nullable=True)

    post = db.relationship('Posts', back_populates='photos')


class Videos(db.Model):
    __tablename__ = 'videos'
    video_id = db.Column(db.Integer(), primary_key=True,
                         nullable=False, autoincrement=True)
    parent_post = db.Column(db.Integer(), db.ForeignKey(
        'posts.post_id', ondelete='cascade'))
    video_url = db.Column(db.String(150), nullable=True)

    post = db.relationship('Posts', back_populates='videos')




