from flaskr import get_error_items, get_form_fields, mysql
from flaskr.models import Users
from flask import Blueprint, render_template, request, flash, redirect, url_for, Response
from flask_login import current_user, login_required
from . import jobs
import wtforms_json
import json
wtforms_json.init()


@jobs.route('/jobs')
def job_index():
    return render_template('jobs/job_index.html')
