from flaskr.models import Posts, Users, CreatePost, Photos
from flaskr import db
from .forms import AddPostForm
from flask import Blueprint, render_template, request, flash, redirect, url_for, Response
from flask_login import current_user, login_user, login_required, logout_user
from . import home
import wtforms_json
import json
from sqlalchemy.exc import IntegrityError
wtforms_json.init()


@home.route('/home', methods=['GET', 'POST'])
@login_required
def home_page():
    form = AddPostForm()
    # Getting user info
    get_user_info = Users.query.filter_by(
        tag=current_user.tag).first()
    # Querying main feed posts
    main_feed = Posts.query.order_by(Posts.date_posted)
    if form.validate_on_submit():
        # Adding data to Posts table
        storing_variable = Posts(
            post_content=form.post_description.data, author_tag=get_user_info.tag)
        db.session.add(storing_variable)
        db.session.commit()
        # Adding data to CreatePost table
        create_post_collection = CreatePost(post_id=storing_variable.post_id,
                                            author_tag=storing_variable.author_tag)
        db.session.add(create_post_collection)
        db.session.commit()
        # Adding data to Photos table
        add_photo_data = Photos(
            photo_url=form.add_photos.data, parent_post=storing_variable.post_id)
        db.session.add(add_photo_data)
        db.session.commit()
        form.post_description.data = ''
        flash(f'Post added successfully!!', category='success')
        return redirect(url_for('home.home_page'))
    return render_template('home/home.html', form=form, main_feed=main_feed)


@home.route('/home/<int:post_id>', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    posts = Posts.query.get_or_404(post_id)
    print(posts.post_id)
    if posts.author_tag != current_user.tag:
        flash(f'You are not authorized to delete that post!', category='error')
        db.session.rollback()
        return redirect(url_for('home.home_page'))
    else:
        db.session.delete(posts)
        db.session.commit()
        flash(f'Post deleted successfully', category='success')
        return redirect(url_for('home.home_page'))

    # return render_template('home/home.html', posts=posts, form=form)


@home.route('/home/update/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    form = AddPostForm()
    postz = Posts.query.get_or_404(post_id)
    if postz.author_tag != current_user.tag:
        flash(f'You are not authorized to edit that post!', category='error')
        return redirect(url_for('home.home_page'))
    else:
        if form.validate_on_submit():
            postz.post_content = request.form['post_description']
            db.session.commit()
            flash('Post Edited Successfully!', category='success')
            return redirect(url_for('home.home_page'))
    return render_template('home/home.html', form=form)
