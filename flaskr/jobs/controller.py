from flaskr import get_error_items, get_form_fields, mysql
from flaskr.models import Users, Jobs, CreateJobs, ApplyJobs, WorksOn
from flask import Blueprint, render_template, request, flash, redirect, url_for, Response
from flask_login import current_user, login_required
from . import jobs
import wtforms_json
import json
wtforms_json.init()
import datetime


@jobs.route('/jobs', methods=['GET'])
@login_required
def job_index():
    if current_user.account_type == 'pet_owner':
        jobs_posted = CreateJobs.query_filter(pet_owner=current_user.tag)
        return render_template('jobs/job_index.html', jobs_posted=jobs_posted)
    else:
        available_jobs = Jobs.query_filter(job_status='Waiting')
        return render_template('jobs/job_index.html', available_jobs=available_jobs)

@jobs.route('/jobs/job-posting', methods=['GET'])
@login_required
def job_home():
    if current_user.account_type == 'pet_owner':
        jobs_created = CreateJobs.query_filter(pet_owner=current_user.tag)
        jobs_posted = list(filter(lambda job: job.job_status == 'Waiting', jobs_created))
        ongoing_jobs = list(filter(lambda job: job.job_status == 'Ongoing', jobs_created))
        return render_template('jobs/jobs_job_home.html', jobs_posted=jobs_posted, ongoing_jobs=ongoing_jobs)
    else:
        applied_to = ApplyJobs.query_filter(freelancer=current_user.tag, application_status='Sent')
        working_on = WorksOn.query_filter(freelancer=current_user.tag)

        return render_template('jobs/jobs_job_home.html', applied_to=applied_to, working_on=working_on)

@jobs.route('/jobs/pet-owner/hire', methods=['POST'])
@login_required
def PE_hire_freelancer():
    cursor = mysql.connection.cursor()
    today = datetime.datetime.now()
    form = request.form
    applicant = Users.query_get(form['applicant_tag'])
    job_id = form['job_id']
    Jobs.update_status(job_id=job_id, new_status='Ongoing')
    Jobs.update_accept(job_id=job_id, accepted_datetime=today)
    ApplyJobs.set_hired(job_id=job_id, freelancer_tag=applicant.tag)
    new_work = WorksOn(freelancer_tag=applicant.tag, job_id=job_id)
    new_work.add()
    flash('Successfully hired', category='success')
    mysql.connection.commit()
    return redirect('/jobs')


@jobs.route('/jobs/pet-owner/create-jobs', methods=['POST'])
@login_required

def PE_create_job():
    form = request.form
    today = datetime.datetime.now()
    job_schedule = form['job_schedule']
    new_job = Jobs()
    new_job.job_status = 'Waiting'
    new_job.job_type = form['job_type']
    new_job.job_rate = form['job_rate']
    new_job.job_description = form['job_description']
    new_job.job_schedule = job_schedule
    new_job.date_posted = today
    try:
        new_job.add()
        mysql.connection.commit()
        flash('Succesfully posted job', category='success')
    except:
        flash('An error has occured.', category='error')
    return redirect(url_for('jobs.job_index'))


@jobs.route('/jobs/pet-owner/freelancers')
@login_required
def PE_freelancers():
    return "<h1> TEST2</h1>"

@jobs.route('/jobs/reviews')
@login_required
def PE_reviews():
    return "<h1> TEST3</h1>"

@jobs.route('/jobs/history')
@login_required
def PE_history():
    return "<h1> TEST4</h1>"


# FREELANCER SIDE

@jobs.route('/jobs/freelancer/job-search')
@login_required
def FL_job_search():
    available_jobs = Jobs.query_filter(job_status='Waiting')
    applied_jobs = ApplyJobs.query_filter(freelancer=current_user.tag)
    applied_jobs = [job.job_id for job in applied_jobs]
    filtered_available_jobs = list(filter(lambda job: job.job_id not in applied_jobs, available_jobs))

    return render_template('jobs/jobs_FR_job_search.html', available_jobs=filtered_available_jobs)


@jobs.route('/jobs/freelancer/apply-job', methods=['POST'])
@login_required
def FL_apply_job():
    today = datetime.datetime.now()
    job_id = request.form['job_id'] 
    cursor = mysql.connection.cursor()
    job = Jobs.query_get(job_id)
    freelancer_tag = current_user.tag
    job_id = job_id
    job_status = job.job_status
    application_status = 'Sent'
    new_application = ApplyJobs(freelancer_tag=freelancer_tag, job_id=job_id, job_status=job_status, application_status=application_status, date_applied=today)
    try:
        new_application.add()
        mysql.connection.commit()
        flash('Successfully sent application!', category='success')
    except:
        flash('An error has occured.', category='error')
        return redirect('/jobs')

    return redirect('/jobs')
