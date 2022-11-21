from flask import Blueprint, render_template, request, flash, redirect, url_for, Response
from flask_login import current_user, login_user, login_required, logout_user
from . import profile
import wtforms_json
import json
wtforms_json.init() 



@profile.route('/profile')
@login_required
def profile_page():
    return render_template('profile/profile.html')
