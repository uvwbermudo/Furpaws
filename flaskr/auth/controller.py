from flask import Blueprint, render_template, request, flash, redirect, url_for, Response
from flask_login import current_user, login_user, login_required, logout_user
from . import auth
import wtforms_json
from .forms import LoginForm, RegisterForm
import json
wtforms_json.init()
from flaskr.models import Users
from flaskr import db
from flaskr import get_error_items, get_form_fields
from sqlalchemy import exc
from werkzeug.security import generate_password_hash, check_password_hash

@auth.route('/')
def index():
    return render_template('auth/landing.html')


@auth.route('/login')
def login():
    form = LoginForm()
    return render_template('auth/login.html', form=form)

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
    password2 = request.json['password2']
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
                email = email,
                tag = tag,
                password = generate_password_hash(password, method='sha256'),
                account_type = account_type,
                last_name = last_name,
                first_name = first_name,
                city = city,
                zipcode = zipcode,
                country = country,
                state = state
                )
            db.session.add(new_user)
            db.session.commit()

            return Response(json.dumps(['SUCCESS']), status=200)
        else:
            errors = get_error_items(form)
            if check or check_email:
                if check:
                    errors['tag'] = ['User tag is already taken.']
                if check_email:
                    errors['email'] = ['Email is already being used.']
        return Response(json.dumps([errors, form_fields]), status=422)
        
        
        