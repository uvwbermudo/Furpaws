from config import CLOUDINARY_API_CLOUD, CLOUDINARY_API_CLOUD_FOLDER, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET
import cloudinary
import cloudinary.uploader
import cloudinary.api
from flask import Blueprint, render_template, request, flash, redirect, url_for, Response, session
from flask_login import current_user, login_user, login_required, logout_user
from . import profile
from flaskr.models import Users
from ..forms import EditProfileForm, ChangePasswordForm
import wtforms_json
import json
from flaskr import mysql
wtforms_json.init() 


cloudinary.config(
    api_secret=CLOUDINARY_API_SECRET,
    cloud_name=CLOUDINARY_API_CLOUD,
    api_key=CLOUDINARY_API_KEY
)

PHOTO_EXTENSIONS = ['jpg', 'png', 'jpeg']
VIDEO_EXTENSIONS = ['mp4']


@profile.route('/profile/<tag>')

@login_required
def profile_page(tag):
    user = Users.query_get(tag=tag)
    return render_template('profile/profile.html', user=user)




@profile.route('/edit_profile/<tag>', methods=['GET', 'POST'])

@login_required
def edit_profile_page(tag):
    user = Users.query_get(tag=tag)
    form=EditProfileForm(request.form)
    if request.method=='POST':
        new_first_name=request.form['edit_first_name']
        new_last_name=request.form['edit_last_name']
        new_tag=request.form['edit_tag']
        new_email=request.form['edit_email']
        new_city=request.form['edit_city']
        new_state=request.form['edit_state']
        new_zipcode=request.form['edit_zipcode']
        new_country=request.form['edit_country']
        Users.update_user(target_tag=tag, new_first_name=new_first_name, new_last_name=new_last_name, 
            new_tag=new_tag, new_email=new_email, new_city=new_city, new_state=new_state,
            new_zipcode=new_zipcode, new_country=new_country)
        mysql.connection.commit()
        current_user.first_name=new_first_name
        current_user.last_name=new_last_name
        current_user.tag=new_tag
        current_user.email=new_email
        current_user.city=new_city
        current_user.state=new_state
        current_user.zipcode=new_zipcode
        current_user.country=new_country
        
        login_user(current_user)
        print(new_first_name)
        flash(f'Profile Updated!!', category='success')
        return redirect(url_for('profile.edit_profile_page', tag=new_tag))
        
    return render_template('profile/edit_profile.html', form=form, user=user)


@profile.route('/change_password/<tag>', methods=['GET', 'POST'])

@login_required
def change_password(tag):
    form = ChangePasswordForm()
    if form.validate_on_submit():
        old_pwd = form.old_pwd.data
        new_pwd1 = form.edit_pwd1.data
        new_pwd2 = form.edit_pwd2.data
        current_password = current_user.password
        if old_pwd != current_password:
            flash('Old password does not match', 'danger')
            return redirect(url_for('profile.change_password', tag=tag))
        if new_pwd1 != new_pwd2:
            flash('New passwords do not match', 'danger')
            return redirect(url_for('profile.change_password', tag=tag))
        Users.update_user(target_tag=tag, old_pwd=old_pwd, new_pwd1=new_pwd1, new_pwd2=new_pwd2)
        mysql.connection.commit()
        flash(f'Password Updated!!', 'success')
        return redirect(url_for('profile.edit_profile_page'))
    return render_template('profile/edit_profile.html', form=form)


@profile.route('/change_profile_photo/<tag>', methods=['GET', 'POST'])

@login_required
def change_profile_photo(tag):
    if request.method=='POST':
        new_profile_photo=request.files.getlist('edit_profile_picture')
        print(tag)
        for every_upload in new_profile_photo:
            if every_upload and every_upload.filename.split(".")[-1].lower() in PHOTO_EXTENSIONS:
                upload_result = cloudinary.uploader.upload(
                    every_upload, folder=CLOUDINARY_API_CLOUD_FOLDER)
                Users.update_user(target_tag=tag, new_profile_picture=upload_result["secure_url"])
                mysql.connection.commit()
            return redirect(url_for('profile.edit_profile_page', tag=tag))

        return redirect(url_for('profile.edit_profile_page', tag=tag))

    

@profile.route('/remove_profile_photo/<tag>', methods=['GET', 'POST'])

@login_required
def remove_profile_photo(tag):
    if request.method=='POST':
        Users.update_user(target_tag=tag, new_profile_picture=None)
        mysql.connection.commit()
        flash('Profile photo removed successfully!', category='success')
        return redirect(url_for('profile.edit_profile_page', tag=tag))
    return redirect(url_for('profile.edit_profile_page', tag=tag))