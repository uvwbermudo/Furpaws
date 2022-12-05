from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import exc
from flaskr import get_error_items, get_form_fields
from flaskr import db
from flaskr.models import Users
from flask import Blueprint, render_template, request, flash, redirect, url_for, Response
from flask_login import current_user, login_user, login_required, logout_user
from . import auth
import wtforms_json
from .forms import RegisterForm, EmailLogin, TagLogin
import json
wtforms_json.init()


@auth.route('/')
def index():
    return render_template('auth/landing.html')


@auth.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect('/home')
    return render_template('auth/login.html')


@auth.route('/register')
def register():
    form = RegisterForm()
    return render_template('auth/register.html', form=form)


@auth.route('/verify-register', methods=['POST'])
def verify_register():
    temp = request.get_json()
    form = RegisterForm.from_json(temp)
    email = request.json['email']
    tag = request.json['tag']
    password = request.json['password']
    account_type = request.json['account_type']
    last_name = request.json['last_name']
    first_name = request.json['first_name']
    city = request.json['city']
    state = request.json['state']
    zipcode = request.json['zipcode']
    country = request.json['country']
    form_fields = get_form_fields(form)

    check = Users.query.get(tag)
    check_email = Users.query.filter(Users.email == email).first()

    if request.method == 'POST':

        if form.validate():
            if check or check_email:
                errors = get_error_items(form)
                if check:
                    errors['tag'] = ['User tag is already taken.']
                if check_email:
                    errors['email'] = ['Email is already being used.']
                return Response(json.dumps([errors, form_fields]), status=422, mimetype='application/json')

            new_user = Users(
                email=email,
                tag=tag,
                password=generate_password_hash(password, method='sha256'),
                account_type=account_type,
                last_name=last_name,
                first_name=first_name,
                city=city,
                zipcode=zipcode,
                country=country,
                state=state
            )
            db.session.add(new_user)
            db.session.commit()
            flash(f'Successfully registered! you may log in.', category='success')
            return Response(json.dumps(['SUCCESS']), status=200)
        else:
            errors = get_error_items(form)
            if check or check_email:
                if check:
                    errors['tag'] = ['User tag is already taken.']
                if check_email:
                    errors['email'] = ['Email is already being used.']
        return Response(json.dumps([errors, form_fields]), status=422)


@auth.route('/verify-login', methods=['POST'])
def verify_login():
    temp = request.get_json()
    print(temp)
    if 'email' in temp.keys():
        username = request.json['email']
        form = EmailLogin.from_json(temp)
    else:
        username = request.json['tag']
        form = TagLogin.from_json(temp)
    password = request.json['password']
    form_fields = get_form_fields(form)
    if '@' in username:
        check = Users.query.filter(Users.email == username).first()
    else:
        check = Users.query.get(username)
    if request.method == 'POST':
        if form.validate():
            if check:
                if check_password_hash(check.password, password):
                    login_user(check)
                    flash(
                        f'Logged in. Hello, {check.first_name}!', category='success')
                    return Response(json.dumps(['SUCCESS']), status=200)
                else:
                    errors = get_error_items(form)
                    errors['password'] = ['Incorrect password.']
                    return Response(json.dumps([errors, form_fields]), status=404, mimetype='application/json')
            else:
                errors = get_error_items(form)
                if '@' in username:
                    errors['email'] = ['Email does not exist.']
                else:
                    errors['tag'] = ['Tag does not exist.']

                return Response(json.dumps([errors, form_fields]), status=404, mimetype='application/json')

        else:
            errors = get_error_items(form)
            print(errors.keys())
            if (not check and 'tag' not in errors.keys()):
                errors['tag'] = ['Tag does not exist.']
            if (not check and '@' in username) and 'email' not in errors.keys():
                errors['email'] = ['Email does not exist.']
            return Response(json.dumps([errors, form_fields]), status=404)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')
