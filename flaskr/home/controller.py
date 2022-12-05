from config import CLOUDINARY_API_CLOUD, CLOUDINARY_API_CLOUD_FOLDER, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET
import cloudinary
import cloudinary.uploader
import cloudinary.api
from flaskr.models import Posts, Users, CreatePost, Photos, Videos
from flaskr import db
from .forms import AddPostForm, EditPostForm
from flask import Blueprint, render_template, request, flash, redirect, url_for, Response, request
from flask_login import current_user, login_user, login_required, logout_user
from . import home
from config import CLOUDINARY_API_CLOUD_FOLDER
from sqlalchemy import desc
from flaskr import get_error_items
import wtforms_json
import json
from sqlalchemy.exc import IntegrityError
wtforms_json.init()


cloudinary.config(
    api_secret=CLOUDINARY_API_SECRET,
    cloud_name=CLOUDINARY_API_CLOUD,
    api_key=CLOUDINARY_API_KEY
)

PHOTO_EXTENSIONS = ['jpg', 'png', 'jpeg']
VIDEO_EXTENSIONS = ['mp4']


@home.route('/home', methods=['GET', 'POST'])
@login_required
def home_page():
    form = AddPostForm()
    edit_form = EditPostForm()
    # Getting user info
    get_user_info = Users.query.filter_by(
        tag=current_user.tag).first()
    # Querying main feed posts
    main_feed = Posts.query.order_by(Posts.date_posted.desc())
    if request.method == 'POST':
        photos = request.files.getlist('files[]')
        videos = request.files.getlist('add_videos')
        print(photos)
        if form.validate_on_submit():
            # Adding data to Posts table
            print('VALID')
            storing_variable = Posts(
                post_content=form.post_description.data, author_tag=get_user_info.tag)
            db.session.add(storing_variable)
            db.session.commit()
            # Adding data to CreatePost table
            create_post_collection = CreatePost(post_id=storing_variable.post_id,
                                                author_tag=storing_variable.author_tag)
            db.session.add(create_post_collection)
            # Adding data to Photos table
            last_post = Posts.query.filter_by(author_tag=current_user.tag).order_by(
                Posts.date_posted.desc()).first()
            for every_upload in photos:
                print(every_upload.filename.split(".")[-1].lower())
                if every_upload and every_upload.filename.split(".")[-1].lower() in PHOTO_EXTENSIONS:
                    upload_result = cloudinary.uploader.upload(
                        every_upload, folder=CLOUDINARY_API_CLOUD_FOLDER)
                    add_photo_data = Photos(
                        photo_url=upload_result["secure_url"], parent_post=last_post.post_id)
                    db.session.add(add_photo_data)
            # Adding data to Videos table
            # upload_result = None
            for every_upload in videos:
                print(every_upload.filename.split(".")[-1].lower())
                if every_upload and every_upload.filename.split(".")[-1].lower() in VIDEO_EXTENSIONS:
                    # try:
                    upload_result = cloudinary.uploader.upload(
                        every_upload, folder=CLOUDINARY_API_CLOUD_FOLDER, resource_type="video")
                    add_video_data = Videos(
                        video_url=upload_result["secure_url"], parent_post=last_post.post_id)
                    db.session.add(add_video_data)
                # except Exception as e:
                #     upload_failed = True
                #     e = str(e)
                #     if '(413)' in e:
                #         upload_failed_message = "Upload Failed!\nVideo files must not exceed 100 MB"
                #     db.session.rollback()
            # if upload_failed:
            #     print(upload_failed_message)
            #     flash(upload_failed_message, category='error')
            #     return redirect(url_for('home.home_page'))
            db.session.commit()
            form.post_description.data = ''
            flash(f'Post added successfully!!', category='success')
            return redirect(url_for('home.home_page'))
        errors = get_error_items(form)
        print(errors)
    return render_template('home/home.html', edit_form=edit_form, form=form, main_feed=main_feed)


@home.route('/home/<int:post_id>', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    posts = Posts.query.get_or_404(post_id)
    # Related cells and rows to delete
    # CreatePost Table
    post_to_delete = CreatePost.query.filter(
        CreatePost.post_id == post_id).first()
    # Photos Table
    related_photo = Photos.query.filter(Photos.parent_post == post_id).all()
    for photo in related_photo:
        db.session.delete(photo)
    # Videos Table
    related_video = Videos.query.filter(Videos.parent_post == post_id).all()
    for video in related_video:
        db.session.delete(video)
    db.session.delete(posts)
    db.session.delete(post_to_delete)
    db.session.commit()
    flash(f'Post deleted successfully', category='success')
    return redirect(url_for('home.home_page'))

    # return render_template('home/home.html', posts=posts, form=form)


@home.errorhandler(413)
def page_not_found(e):
    # print(e)
    # print(dir(e))
    # return render_template(...)
    return 'File to big: ' + str(e)


@home.route('/home/update/<post_id>', methods=['POST'])
@login_required
def edit_post(post_id):
    form = EditPostForm(request.form)
    user_post = Posts.query.get_or_404(post_id)
    if request.method == 'POST':
        if form.validate_on_submit():
            user_post.post_content = request.form['post_description']
            db.session.commit()
            flash('Post Edited Successfully!', category='success')
            return redirect(url_for('home.home_page'))
    return render_template('home/home.html', form=form)
