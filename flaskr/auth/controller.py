from flask import Blueprint, render_template, request, flash, redirect, url_for, Response
from flask_login import current_user, login_user, login_required, logout_user
from . import auth
from .forms import LoginForm, RegisterForm

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