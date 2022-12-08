from config import CLOUDINARY_API_CLOUD, CLOUDINARY_API_CLOUD_FOLDER, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET
import cloudinary
import cloudinary.uploader
import cloudinary.api
from flaskr.models import Users, Posts, CreatePost, Photos, Videos, Comments
from flaskr import mysql
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
    get_user_info = Users.query_get(current_user.tag)
    # Querying main feed posts
    main_feed = Posts.query_filter(
        all=True, order_by='date_posted', order='DESC')
    for post in main_feed:
        print(post.photos)
    if request.method == 'POST':
        photos = request.files.getlist('files[]')
        videos = request.files.getlist('add_videos')
        print(photos)
        if form.validate_on_submit():
            # Adding data to Posts table
            print('VALID')
            storing_variable = Posts(
                post_content=form.post_description.data.replace('"', "''"), author_tag=get_user_info.tag)
            storing_variable.add()
            mysql.connection.commit()
            last_inserted_post = Posts.last_inserted()
            # Adding data to CreatePost table
            create_post = CreatePost(post_id=last_inserted_post.post_id,
                                     author_tag=storing_variable.author_tag)
            create_post.add()
            # Adding data to Photos table
            last_post = Posts.query_filter(
                author_tag=current_user.tag, order_by='date_posted', order='DESC')[0]
            for every_upload in photos:
                print(every_upload.filename.split(".")[-1].lower())
                if every_upload and every_upload.filename.split(".")[-1].lower() in PHOTO_EXTENSIONS:
                    upload_result = cloudinary.uploader.upload(
                        every_upload, folder=CLOUDINARY_API_CLOUD_FOLDER)
                    add_photo_data = Photos(
                        photo_url=upload_result["secure_url"], parent_post=last_post.post_id)
                    add_photo_data.add()
            # Adding data to Videos table
            for every_upload in videos:
                print(every_upload.filename.split(".")[-1].lower())
                if every_upload and every_upload.filename.split(".")[-1].lower() in VIDEO_EXTENSIONS:
                    upload_result = cloudinary.uploader.upload(
                        every_upload, folder=CLOUDINARY_API_CLOUD_FOLDER, resource_type="video")
                    add_video_data = Videos(
                        video_url=upload_result["secure_url"], parent_post=last_post.post_id)
                    add_video_data.add()
            mysql.connection.commit()
            form.post_description.data = ''
            flash(f'Post added successfully!!', category='success')
            return redirect(url_for('home.home_page'))
        errors = get_error_items(form)
        print(errors)
    return render_template('home/home.html', edit_form=edit_form, form=form, main_feed=main_feed)


@home.route('/home/<int:post_id>', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    Posts.delete(post_id)
    mysql.connection.commit()
    flash(f'Post deleted successfully', category='success')
    return redirect(url_for('home.home_page'))


@home.route('/home/update/<post_id>', methods=['POST'])
@login_required
def edit_post(post_id):
    form = EditPostForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_content = request.form['post_description'].replace('"', "''")
            Posts.update_post(post_id, new_content)
            mysql.connection.commit()
            flash('Post Edited Successfully!', category='success')
            return redirect(url_for('home.home_page'))
    return render_template('home/home.html', form=form)


@home.route('/home/create-comment/<post_id>', methods=['POST'])
@login_required
def add_comment(post_id):
    comment_text = request.form.get('comment_textbox')

    if not comment_text:
        flash(f'Comment cannot be empty!', category='error')
    else:
        related_post = Posts.query_get(
            post_id=post_id)
        if related_post:
            new_comment = Comments(
                post_commented=related_post.post_id, author_tag=current_user.tag, comment_content=comment_text.replace('"', "''"))
            new_comment.add()
            mysql.connection.commit()
        else:
            flash(f'Post does not exist!', category='error')

    return redirect(url_for('home.home_page'))


@home.route('/home/delete-comment/<int:comment_id>', methods=['GET', 'POST'])
@login_required
def delete_comment(comment_id):
    Comments.delete(comment_id)
    mysql.connection.commit()
    return redirect(url_for('home.home_page'))
