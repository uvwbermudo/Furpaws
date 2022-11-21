from flask import Blueprint, render_template, request, flash, redirect, url_for, Response
from flask_login import current_user, login_user, login_required, logout_user
from . import home
import wtforms_json
import json
wtforms_json.init() 



@home.route('/home')
@login_required
def home_page():
    return render_template('home/home.html')

