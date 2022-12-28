from config import CLOUDINARY_API_CLOUD, CLOUDINARY_API_CLOUD_FOLDER, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET
import cloudinary
import cloudinary.uploader
import cloudinary.api
from flaskr.models import Users, Posts, CreatePost, Photos, Videos, Comments, Likes, SharePost
from flaskr import mysql
from .forms import AddPostForm, EditPostForm, EditCommentForm
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
    edit_comment_form = EditCommentForm()
    # Getting user info
    get_user_info = Users.query_get(current_user.tag)
    # Querying main feed posts
    main_feed = Posts.query_filter(
        all=True, order_by='date_posted', order='DESC')
    share_posts = SharePost.query_filter(
        all=True, order_by='date_created', order='DESC')
    if request.method == 'POST':
        photos = request.files.getlist('files[]')
        videos = request.files.getlist('add_videos')
        print(photos)
        if form.validate_on_submit():
            # Adding data to Posts table
            print('VALID')
            if form.post_description.data:
                storing_variable = Posts(
                    post_content=form.post_description.data.replace('"', "''"), author_tag=get_user_info.tag)
            else:
                storing_variable = Posts(author_tag=get_user_info.tag)
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
    return render_template('home/home.html', edit_comment_form=edit_comment_form, edit_form=edit_form, form=form, main_feed=main_feed, share_posts=share_posts)


@home.route('/home/<int:post_id>', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    related_posts = SharePost.query_filter(
        shared_post_id=post_id, order_by='date_created', order='DESC')
    if related_posts:
        for post in related_posts:
            Posts.delete(post.reference_id)
            mysql.connection.commit()
    Posts.delete(post_id)
    mysql.connection.commit()
    flash(f'Post deleted successfully', category='success')
    return redirect(url_for('home.home_page'))


@home.route('/home/share-post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def share_post(post_id):
    related_post = Posts.query_get(
        post_id=post_id)
    shared_post = Posts(post_content=related_post.post_content,
                        author_tag=related_post.author_tag)
    shared_post.add()
    mysql.connection.commit()
    inserted_post = Posts.last_inserted()
    storing_variable = SharePost(
        sharer_tag=current_user.tag, shared_post_id=related_post.post_id, reference_id=inserted_post.post_id)
    storing_variable.add()
    mysql.connection.commit()
    parent_photos = Photos.query_filter(parent_post=post_id)
    parent_videos = Videos.query_filter(parent_post=post_id)
    if parent_photos:
        for every_photo in parent_photos:
            photo_data = Photos(photo_url=every_photo.photo_url,
                                parent_post=inserted_post.post_id)
            photo_data.add()
            mysql.connection.commit()
    if parent_videos:
        for every_video in parent_videos:
            video_data = Videos(video_url=every_video.video_url,
                                parent_post=inserted_post.post_id)
            video_data.add()
            mysql.connection.commit()
    flash(f'Post shared successfully', category='success')
    return redirect(url_for('home.home_page'))


@home.route('/home/update/<post_id>', methods=['POST'])
@login_required
def edit_post(post_id):
    related_posts = SharePost.query_filter(
        shared_post_id=post_id, order_by='date_created', order='DESC')
    form = EditPostForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_content = request.form['post_description'].replace('"', "''")
            Posts.update_post(post_id, new_content)
            if related_posts:
                for post in related_posts:
                    Posts.update_post(post.reference_id, new_content)
                    mysql.connection.commit()
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


@home.route('/home/update-comment/<comment_id>', methods=['POST'])
@login_required
def edit_comment(comment_id):
    form = EditCommentForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_comment_content = request.form['edit_comment_textbox'].replace(
                '"', "''")
            Comments.update_comment(comment_id, new_comment_content)
            mysql.connection.commit()
            flash('Comment Edited Successfully!', category='success')
            return redirect(url_for('home.home_page'))
    return render_template('home/home.html', form=form)


@home.route('/home/like-post/<post_id>', methods=['GET'])
@login_required
def like(post_id):
    post = Posts.query_get(
        post_id=post_id)
    like = Likes.query_filter(
        author_tag=current_user.tag, post_liked=post_id, order_by='date_liked')
    if not post:
        flash(f'Post does not exist.', category='error')
    else:
        like = Likes(author_tag=current_user.tag, post_liked=post_id)
        like.add()
        mysql.connection.commit()

    return redirect(url_for('home.home_page'))


@home.route('/home/unlike-post/<id>', methods=['GET'])
@login_required
def unlike(id):
    like = Likes.query_get(
        id=id)
    if not like:
        flash(f'Error.', category='error')
    else:
        Likes.delete(id)
        mysql.connection.commit()

    return redirect(url_for('home.home_page'))


@home.route('/posts/<post_id>', methods=['GET', 'POST'])
@login_required
def view_post(post_id):
    form = AddPostForm()
    edit_form = EditPostForm()
    edit_comment_form = EditCommentForm()
    post = Posts.query_filter(
        post_id=post_id, order_by='date_posted', order='DESC')
    return render_template("home/posts.html", post=post, edit_comment_form=edit_comment_form, edit_form=edit_form, form=form)


@home.route('/posts/update/<post_id>', methods=['POST'])
@login_required
def edit_on_visited_post(post_id):
    related_posts = SharePost.query_filter(
        shared_post_id=post_id, order_by='date_created', order='DESC')
    form = EditPostForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_content = request.form['post_description'].replace('"', "''")
            Posts.update_post(post_id, new_content)
            if related_posts:
                for post in related_posts:
                    Posts.update_post(post.reference_id, new_content)
                    mysql.connection.commit()
            mysql.connection.commit()
            flash('Post Edited Successfully!', category='success')
            return redirect(url_for('home.view_post', post_id=post_id))
    return render_template('home/posts.html', form=form)


@home.route('/posts/create-comment/<post_id>', methods=['POST'])
@login_required
def add_comment_on_visited_post(post_id):
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

    return redirect(url_for('home.view_post', post_id=post_id))


@home.route('/posts/delete-comment/<int:comment_id>/<post_id>', methods=['GET', 'POST'])
@login_required
def delete_comment_on_visited_post(comment_id, post_id):
    Comments.delete(comment_id)
    mysql.connection.commit()
    return redirect(url_for('home.view_post', post_id=post_id))


@home.route('/posts/update-comment/<comment_id>/<post_id>', methods=['POST'])
@login_required
def edit_comment_on_visited_post(comment_id, post_id):
    form = EditCommentForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_comment_content = request.form['edit_comment_textbox'].replace(
                '"', "''")
            Comments.update_comment(comment_id, new_comment_content)
            mysql.connection.commit()
            flash('Comment Edited Successfully!', category='success')
            return redirect(url_for('home.view_post', post_id=post_id))
    return render_template('home/posts.html', form=form, post_id=post_id)


@home.route('/posts/like-post/<post_id>', methods=['GET'])
@login_required
def like_on_visited_post(post_id):
    post = Posts.query_get(
        post_id=post_id)
    like = Likes.query_filter(
        author_tag=current_user.tag, post_liked=post_id, order_by='date_liked')
    if not post:
        flash(f'Post does not exist.', category='error')
    else:
        like = Likes(author_tag=current_user.tag, post_liked=post_id)
        like.add()
        mysql.connection.commit()

    return redirect(url_for('home.view_post', post_id=post_id))


@home.route('/posts/unlike-post/<id>/<post_id>', methods=['GET'])
@login_required
def unlike_on_visited_post(id, post_id):
    like = Likes.query_get(
        id=id)
    if not like:
        flash(f'Error.', category='error')
    else:
        Likes.delete(id)
        mysql.connection.commit()

    return redirect(url_for('home.view_post', post_id=post_id))
