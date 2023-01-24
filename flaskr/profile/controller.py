from config import CLOUDINARY_API_CLOUD, CLOUDINARY_API_CLOUD_FOLDER, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET
import cloudinary
import cloudinary.uploader
import cloudinary.api
from flask import Blueprint, render_template, request, flash, redirect, url_for, Response, session
from flask_login import current_user, login_user, login_required, logout_user
from . import profile
from flaskr.models import Users
from .forms import EditProfileForm
import wtforms_json
import json
from flaskr import mysql, get_error_items, get_form_fields
wtforms_json.init() 
from werkzeug.security import generate_password_hash, check_password_hash


cloudinary.config(
    api_secret=CLOUDINARY_API_SECRET,
    cloud_name=CLOUDINARY_API_CLOUD,
    api_key=CLOUDINARY_API_KEY
)

PHOTO_EXTENSIONS = ['jpg', 'png', 'jpeg']
VIDEO_EXTENSIONS = ['mp4']


@profile.route('/profiles/<tag>')
@login_required
def profile_page(tag):
    user = Users.query_get(tag=tag)
    return render_template('profile/profile.html', user=user)




@profile.route('/edit_profile/<tag>', methods=['POST'])
@login_required
def edit_profile_page(tag):
    print(request.form)
    print(request.files)
    user = Users.query_get(tag=tag)
    form = EditProfileForm(request.form)
    print('VALIDATING', form.validate())
    print(get_error_items(form))
    new_first_name=request.form['first_name'].strip()
    new_last_name=request.form['last_name'].strip()
    new_tag=request.form['tag'].strip()
    new_email=request.form['email'].strip()
    new_city=request.form['city'].strip()
    new_state=request.form['state'].strip()
    new_zipcode=request.form['zipcode'].strip()
    new_country=request.form['country'].strip()

    old_pwd=request.form['old_pwd'].strip()
    pwd=request.form['pwd'].strip()
    pwd2=request.form['pwd2'].strip()

    form_fields=get_form_fields(form)
    if form.validate():
        errors=get_error_items(form)
        if not check_password_hash(user.password, old_pwd):
            errors['old_pwd'] = ['Password is incorrect.']
            return Response(json.dumps([errors, form_fields]), status=422, mimetype='application/json')
        if tag != new_tag:
            check=Users.query_get(new_tag)
            if check:
                errors['tag'] = ['Tag is already taken.']
            return Response(json.dumps([errors, form_fields]), status=422, mimetype='application/json')

        if user.email != new_email:
            check= Users.query_filter(email=new_email, exact_match=True)
            print(check.tag)
            if check:
                errors['email'] = ['Email is already taken.']
                return Response(json.dumps([errors, form_fields]), status=422, mimetype='application/json')

        if request.files:
            profile_pic = request.files['profile_pic']
            upload_result = cloudinary.uploader.upload(profile_pic, folder=CLOUDINARY_API_CLOUD_FOLDER)
            new_profile_pic = upload_result["secure_url"]
        else:
            new_profile_pic = None

        password=generate_password_hash(pwd, method='sha256')
        Users.update_user(
            target_tag=tag, 
            new_first_name=new_first_name, 
            new_last_name=new_last_name, 
            new_tag=new_tag,
            new_email=new_email, 
            new_city=new_city, 
            new_state=new_state,
            new_zipcode=new_zipcode, 
            new_country=new_country,
            new_password=password,
            new_profile_picture=new_profile_pic
            )
        mysql.connection.commit()
        current_user.first_name=new_first_name
        current_user.last_name=new_last_name
        current_user.tag=new_tag
        current_user.email=new_email
        current_user.city=new_city
        current_user.state=new_state
        current_user.zipcode=new_zipcode
        current_user.profile_picture=new_profile_pic
        current_user.country=new_country
        current_user.password=password
        
        # login_user(current_user)
        flash(f'Successfully updated profile!', category='success')
        errors=get_error_items(form)
        return Response(status=200)
    else:
        errors=get_error_items(form)
        if not check_password_hash(user.password, old_pwd):
            errors['old_pwd'] = ['Password is incorrect.']
        if tag != new_tag:
            check=Users.query_get(new_tag)
            if check:
                errors['tag'] = ['Tag is already taken.']

        if user.email != new_email:
            check=Users.query_filter(email=new_email, exact_match=True)
            if check:
                errors['email'] = ['Email is already taken.']
        
        return Response(json.dumps([errors, form_fields]), status=422, mimetype='application/json')




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

    

# @profile.route('/remove_profile_photo/<tag>', methods=['GET', 'POST'])
# @login_required
# def remove_profile_photo(tag):
#     if request.method=='POST':
#         Users.update_user(target_tag=tag, new_profile_picture=None)
#         mysql.connection.commit()
#         flash('Profile photo removed successfully!', category='success')
#         return redirect(url_for('profile.edit_profile_page', tag=tag))
#     return redirect(url_for('profile.edit_profile_page', tag=tag))