from config import CLOUDINARY_API_CLOUD, CLOUDINARY_API_CLOUD_FOLDER, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET
import cloudinary
import cloudinary.uploader
import cloudinary.api
from flaskr.models import Users, Posts, CreatePost, Photos, Videos, Comments, Likes, SharePost
from flaskr import mysql, get_error_items
from .forms import AddPostForm, EditPostForm, EditCommentForm
from flask import Blueprint, render_template, request, flash, redirect, url_for, Response, request, session, jsonify
from flask_login import current_user, login_user, login_required, logout_user
from . import home
from config import CLOUDINARY_API_CLOUD_FOLDER
from sqlalchemy import desc
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
    user_sugg = Users.query_all()[:3]
    all_posts = main_feed + share_posts
    all_posts = list(set(all_posts))
    all_posts = list(sorted(all_posts, key=lambda x: x.get_creation_date(), reverse=True))
    return render_template('home/home.html', edit_comment_form=edit_comment_form, edit_form=edit_form, form=form, main_feed=main_feed, user_sugg=user_sugg, share_posts=share_posts, all_posts=all_posts)


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
    storing_variable = SharePost(
        sharer_tag=current_user.tag, shared_post_id=post_id)
    storing_variable.add()
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


@home.route('/home/search', methods=['GET'])
@login_required
def search_layout():
    session['search_query'] = request.args['searchbar']
    return render_template('home/search.html', search_result=session['search_query'])


@home.route('/photos/delete/confirm/<photo_id>', methods=['POST'])
@login_required
def confirm_delete_photo(photo_id):
    return render_template('home/macros/confirm_delete_img.html', photo_id=photo_id)


@home.route('/photos/delete/cancel/<photo_id>', methods=['POST'])
@login_required
def cancel_delete_photo(photo_id):
    return render_template('home/macros/cancel_delete_img.html', photo_id=photo_id)


@home.route('/photos/delete/<photo_id>', methods=['POST'])
@login_required
def delete_photo(photo_id):
    if request.method == 'POST':
        print('Deleting', photo_id)
        Photos.delete(photo_id)
        mysql.connection.commit()
        return Response(status=200)


@home.route('/videos/delete/confirm/<video_id>', methods=['POST'])
@login_required
def confirm_delete_video(video_id):
    return render_template('home/macros/confirm_delete_vid.html', video_id=video_id)


@home.route('/videos/delete/cancel/<video_id>', methods=['POST'])
@login_required
def cancel_delete_video(video_id):
    return render_template('home/macros/cancel_delete_vid.html', video_id=video_id)


@home.route('/videos/delete/<video_id>', methods=['POST'])
@login_required
def delete_video(video_id):
    if request.method == 'POST':
        print('Deleting', video_id)
        Videos.delete(video_id)
        mysql.connection.commit()
        return Response(status=200)


@home.route('/search/<filter>', methods=['GET'])
@login_required
def search(filter):
    query = session['search_query']
    query_user = []
    query_post = []
    if filter == 'pet_owners':
        query_user.extend(Users.query_filter(account_type='pet_owner', name=query))
        query_user.extend(Users.query_filter(account_type='pet_owner', tag=query))
        query_user.extend(Users.query_filter(account_type='pet_owner', email=query))

    if filter == 'freelancers':
        query_user = Users.query_filter(account_type='freelancer', name=query)
        query_user.extend(Users.query_filter(account_type='freelancer', tag=query))
        query_user.extend(Users.query_filter(account_type='freelancer', email=query))

    if filter == 'all':
        query_user.extend(Users.query_filter(name=query))
        query_user.extend(Users.query_filter(email=query))
        query_user.extend(Users.query_filter(tag=query))
        query_post.extend(Posts.query_filter(post_content=query))
        query_post.extend(Posts.query_filter(author_tag=query))
        by_name = []
        by_name.extend(Users.query_filter(name=query))
        by_name.extend(Users.query_filter(email=query))
        for user in by_name:
            query_post.extend(user.posts)

    if filter == 'posts':
        query_post.extend(Posts.query_filter(post_content=query))
        query_post.extend(Posts.query_filter(author_tag=query))
        by_name = []
        by_name.extend(Users.query_filter(name=query))
        by_name.extend(Users.query_filter(email=query))
        for user in by_name:
            query_post.extend(user.posts)
    query_post = list(set(query_post))
    for idx,post in enumerate(query_post):
        if not post.post_content or post.post_content.isspace():
            print(post.date_posted)
            if not post.videos or not post.photos:
                query_post.pop(idx)

    query_post = sorted(query_post, key=lambda post: post.date_posted, reverse=True)
    
    query_user = list(set(query_user))

    return render_template('home/search_results.html', query_post=query_post, query_user=query_user)


@home.route('/home/create-comment/<post_id>', methods=['POST'])
@login_required
def add_comment(post_id):
    data = request.get_json()
    comment_text = data
    post = Posts.query_filter(
        post_id=post_id)[0]
    if not comment_text:
        return jsonify({'error': 'Comment cannot be empty!'})
    else:
        related_post = Posts.query_get(
            post_id=post_id)
        if related_post:
            new_comment = Comments(
                post_commented=related_post.post_id, author_tag=current_user.tag, comment_content=comment_text.replace('"', "''"))
            new_comment.add()
            mysql.connection.commit()
            get_comment_id = Comments.query_filter(
                post_commented=related_post.post_id, author_tag=current_user.tag, comment_content=comment_text.replace('"', "''"))
            comment_id = get_comment_id[0].comment_id
        else:
            flash(f'Post does not exist!', category='error')

    return jsonify({"id": comment_id, "commented": current_user.tag in map(lambda x: x.author_tag, post.comments),  "comments": len(post.comments), "comment": comment_text, "author_tag": current_user.tag, "commented_post": related_post.post_id, "date_commented": new_comment.date_commented.strftime("%d, %b %Y").lower()})

@home.route('/posts/create-comment/<post_id>', methods=['POST'])
@login_required
def add_comment_on_visited_post(post_id):
    data = request.get_json()
    comment_text = data
    post = Posts.query_filter(
        post_id=post_id)[0]
    if not comment_text:
        return jsonify({'error': 'Comment cannot be empty!'})
    else:
        related_post = Posts.query_get(
            post_id=post_id)
        if related_post:
            new_comment = Comments(
                post_commented=related_post.post_id, author_tag=current_user.tag, comment_content=comment_text.replace('"', "''"))
            new_comment.add()
            mysql.connection.commit()
            get_comment_id = Comments.query_filter(
                post_commented=related_post.post_id, author_tag=current_user.tag, comment_content=comment_text.replace('"', "''"))
            comment_id = get_comment_id[0].comment_id
        else:
            flash(f'Post does not exist!', category='error')

    return jsonify({"id": comment_id, "commented": current_user.tag in map(lambda x: x.author_tag, post.comments),  "comments": len(post.comments), "comment": comment_text, "author_tag": current_user.tag, "commented_post": related_post.post_id, "date_commented": new_comment.date_commented.strftime("%d, %b %Y").lower()})

@home.route('/home/delete-comment/<int:comment_id>/<post_id>', methods=['GET', 'DELETE'])
@login_required
def delete_comment(comment_id, post_id):
    post = Posts.query_filter(
        post_id=post_id)[0]
    Comments.delete(comment_id)
    mysql.connection.commit()
    element_id = "main-feed-comments-" + post_id
    return jsonify({"id": comment_id, "commented_post": post_id, "element_id": element_id, "comments": len(post.comments), "commented": current_user.tag in map(lambda x: x.author_tag, post.comments)})

@home.route('/home/delete-share/<int:share_id>', methods=['post'])
@login_required
def delete_share(share_id):
    SharePost.delete(share_id=share_id)
    mysql.connection.commit()
    return redirect(url_for('home.home_page'))

@home.route('/home/update-comment/<comment_id>/<post_id>', methods=['PUT'])
@login_required
def edit_comment(comment_id, post_id):
    data = request.json['text']
    new_comment_content = data
    Comments.update_comment(comment_id, new_comment_content)
    mysql.connection.commit()
    return jsonify({"id": comment_id, "newComment": new_comment_content, "author_tag": current_user.tag, "post_commented": post_id})


@home.route('/home/like-post/<post_id>', methods=['GET', 'POST'])
@login_required
def like(post_id):
    post = Posts.query_filter(
        post_id=post_id)[0]
    like = Likes.query_filter(
        author_tag=current_user.tag, post_liked=post_id, order_by='date_liked')
    if current_user.tag in map(lambda x: x.author_tag, post.likes):
        for every_like in post.likes:
            if current_user.tag == every_like.author_tag:
                Likes.delete(every_like.id)
                mysql.connection.commit()
    else:
        like = Likes(author_tag=current_user.tag, post_liked=post_id)
        like.add()
        mysql.connection.commit()

    return jsonify({"likes": len(post.likes), "liked": current_user.tag in map(lambda x: x.author_tag, post.likes)})


@home.route('/posts/<post_id>', methods=['GET', 'POST'])
@login_required
def view_post(post_id):
    form = AddPostForm()
    edit_form = EditPostForm()
    edit_comment_form = EditCommentForm()
    respective_post = Posts.query_filter(
        post_id=post_id, order_by='date_posted', order='DESC')
    return render_template("home/posts.html", respective_post=respective_post, edit_comment_form=edit_comment_form, edit_form=edit_form, form=form)


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


@home.route('/posts/delete-comment/<int:comment_id>/<post_id>', methods=["GET", "DELETE"])
@login_required
def delete_comment_on_visited_post(comment_id, post_id):
    post = Posts.query_filter(
        post_id=post_id)[0]
    Comments.delete(comment_id)
    mysql.connection.commit()
    element_id = "comments-" + post_id
    return jsonify({"id": comment_id, "commented_post": post_id, "element_id": element_id, "comments": len(post.comments), "commented": current_user.tag in map(lambda x: x.author_tag, post.comments)})


@home.route('/posts/update-comment/<comment_id>/<post_id>', methods=['PUT'])
@login_required
def edit_comment_on_visited_post(comment_id, post_id):
    data = request.json['text']
    new_comment_content = data
    Comments.update_comment(comment_id, new_comment_content)
    mysql.connection.commit()

    return jsonify({"id": comment_id, "newComment": new_comment_content, "author_tag": current_user.tag, "post_commented": post_id})

@home.route('/posts/like-post/<post_id>', methods=['POST'])
@login_required
def like_on_visited_post(post_id):
    post = Posts.query_filter(
        post_id=post_id)[0]
    like = Likes.query_filter(
        author_tag=current_user.tag, post_liked=post_id, order_by='date_liked')
    if current_user.tag in map(lambda x: x.author_tag, post.likes):
        for every_like in post.likes:
            if current_user.tag == every_like.author_tag:
                Likes.delete(every_like.id)
                mysql.connection.commit()
    else:
        like = Likes(author_tag=current_user.tag, post_liked=post_id)
        like.add()
        mysql.connection.commit()

    return jsonify({"likes": len(post.likes), "liked": current_user.tag in map(lambda x: x.author_tag, post.likes)})
