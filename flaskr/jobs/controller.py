from flaskr import get_error_items, get_form_fields, mysql
from flaskr.models import Users, Jobs, CreateJobs, ApplyJobs, WorksOn, Reviews, FreelancerDetails, JobRequests
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
        working_on = WorksOn.query_filter(freelancer=current_user.tag)
        applied_to = ApplyJobs.query_filter(freelancer=current_user.tag, application_status='Sent')
        return render_template('jobs/job_index.html', available_jobs=available_jobs, working_on=working_on, applied_to=applied_to)

@jobs.route('/jobs/rating/<job_id>')
@login_required
def get_stars(job_id):
    return render_template('jobs/macros/stars.html', job_id=job_id)

@jobs.route('/jobs/job-posting', methods=['GET'])
@login_required
def job_home():
    if current_user.account_type == 'pet_owner':
        jobs_created = CreateJobs.query_filter(pet_owner=current_user.tag)
        jobs_posted = list(filter(lambda job: job.job_status == 'Waiting', jobs_created))
        ongoing_jobs = list(filter(lambda job: job.job_status == 'Ongoing', jobs_created))
        requests =  list(filter(lambda job: job.job_status == 'Requested', jobs_created))
        jobs_requested = []
        for job in requests:
            req = JobRequests.query_filter(reference_job=job.job_details.job_id)
            if req:
                req = req[0]
            else:
                continue
            jobs_requested.append(req)
        jobs_posted = jobs_posted+jobs_requested
        all_jobs = jobs_posted + ongoing_jobs
        return render_template('jobs/jobs_job_home.html', jobs_posted=jobs_posted, ongoing_jobs=ongoing_jobs, all_jobs_PE=all_jobs)
    else:
        applied_to = ApplyJobs.query_filter(freelancer=current_user.tag, application_status='Sent')
        working_on = WorksOn.query_filter(freelancer=current_user.tag) 
        working_on = list(filter(lambda job: job.job_details.job_status == 'Ongoing', working_on))
        requests = JobRequests.query_filter(freelancer_tag=current_user.tag)
        job_requests = list(filter(lambda req: req.request_status == 'Requested', requests))
        all_jobs = working_on + applied_to
        return render_template('jobs/jobs_job_home.html', applied_to=applied_to, working_on=working_on, all_jobs=all_jobs, job_requests=job_requests)

@jobs.route('/jobs/pet-owner/hire', methods=['POST'])
@login_required
def PE_hire_freelancer():
    cursor = mysql.connection.cursor()
    today = datetime.datetime.now()
    form = request.form
    print(form)
    applicant = Users.query_get(form['applicant_tag'])
    job_id = form['job_id']
    try:
        Jobs.update_status(job_id=job_id, new_status='Ongoing')
        Jobs.update_accept(job_id=job_id, accepted_datetime=today)
        ApplyJobs.set_hired(job_id=job_id, freelancer_tag=applicant.tag)
        new_work = WorksOn(freelancer_tag=applicant.tag, job_id=job_id)
        new_work.add()
        mysql.connection.commit()
        flash('Successfully hired!', category='success')
    except:
        flash('An error has occured, try again.', category='error')
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
    except Exception as e:
        flash('An error has occured.', category='error')
        print(e)
    return redirect(url_for('jobs.job_index'))

@jobs.route('/jobs/pet-owner/cancel-job', methods=['POST'])
@login_required
def PE_cancel_job():
    job_id=request.form['job_id']
    job = Jobs.query_get(job_id)
    worker = job.worker_details
    try:
        Jobs.update_status(job_id=job_id, new_status='Cancelled')
        ApplyJobs.update_application_status(job_id=job_id, status='Cancelled', freelancer_tag=worker.tag)
        mysql.connection.commit()
        flash("Job cancelled successfully", category='success')
    except Exception as e:
        flash("An error has occured", category='error')
        print(e)
    return redirect('/jobs')

@jobs.route('/jobs/pet-owner/complete-job', methods=['POST'])
@login_required
def PE_complete_job():
    job_id = request.form['job_id']
    review = request.form['review']
    job = Jobs.query_get(job_id=job_id)
    if 'rating' in request.form.keys():
        rating = request.form['rating']
        stars = Reviews.get_rating_list(freelancer=job.worker_details.tag)
        stars = [ int(stars[0]) for stars in stars]
        if stars:
            star_length = len(stars) + 1
            star_sum = sum(stars) + int(rating)
            new_average = star_sum/star_length
        else:
            new_average = rating
    else:
        rating='None'
    try:
        FreelancerDetails.update_average(freelancer=job.worker_details.tag, new_average=new_average)
        Jobs.update_status(job_id=job_id, new_status='Complete')
        ApplyJobs.set_application_status(job_id=job_id, freelancer_tag=job.worker_details.tag, new_status='Finished')
        review = Reviews(message=review, stars=rating, reference_job=job_id, reviewer_tag=current_user.tag, reviewee_tag=job.worker_details.tag)
        review.add()
        mysql.connection.commit()
        print(review, rating, job_id, current_user.tag, job.worker_details.tag)
        flash("Job completed successfully", category='success')
    except Exception as e:
        flash("An error has occured", category='error')
        print(e)
    return redirect('/jobs')    

@jobs.route('/jobs/pet-owner/freelancers')
@login_required
def PE_freelancers():
    freelancers = Users.query_all(account_type='freelancer')
    for freelancer in freelancers:
        print(freelancer.freelancing_details)
    return render_template('jobs/freelancer_list.html',freelancers=freelancers )

@jobs.route('/jobs/pet-owner/freelancers/<freelancer_tag>')
@login_required
def PE_freelancer_single(freelancer_tag):
    freelancer = Users.query_get(tag=freelancer_tag)
    return render_template('jobs/freelancer_single.html', freelancer=freelancer)

@jobs.route('/jobs/pet-owner/request-job/<freelancer_tag>', methods=['POST','GET'])
@login_required
def PE_request_job(freelancer_tag):
    cursor = mysql.connection.cursor()
    form = request.form
    if request.method == 'GET':
        freelancer = Users.query_get(freelancer_tag)
        return render_template('jobs/request_job_form.html', freelancer=freelancer)
    if request.method == 'POST':
        freelancer = freelancer_tag
        today = datetime.datetime.now()
        job_schedule = form['job_schedule']
        new_job = Jobs()
        new_job.job_status = 'Requested'
        new_job.job_type = form['job_type']
        new_job.job_rate = form['job_rate']
        new_job.job_description = form['job_description']
        new_job.job_schedule = job_schedule
        new_job.date_posted = today
        try:
            cursor.execute("START TRANSACTION")
            new_job.add()
            cursor.execute("SELECT LAST_INSERT_ID()")
            job_id = cursor.fetchone()[0]
            new_request = JobRequests(freelancer_tag=freelancer, pet_owner_tag=current_user.tag, reference_job=job_id, request_status='Requested')
            new_request.add()
            mysql.connection.commit()
            flash('Succesfully requested job', category='success')
        except Exception as e:
            flash('An error has occured.', category='error')
            print(e)

        return redirect('/jobs')


@jobs.route('/jobs/pet-owner/history')
@login_required
def PE_history():
    jobs_created = CreateJobs.query_filter(pet_owner=current_user.tag, order_by='date_posted', order='DESC')
    return render_template('jobs/PE_history.html', jobs_created=jobs_created)


# FREELANCER SIDE

@jobs.route('/jobs/freelancer/reject-request', methods=['POST'])
@login_required
def FL_reject_request():
    req_id = request.form['req_id']
    req_id = int(req_id)
    req = JobRequests.query_get(id=req_id)
    try:
        JobRequests.update_status(req_id=req_id, new_status='Rejected')
        Jobs.update_status(job_id=req.reference_job, new_status='Rejected')
        mysql.connection.commit()
        flash('Successfully Rejected the Job!', category='success')
    except Exception as e:
        flash('There was a problem. Try again.', category='error')
        print(e)
    return redirect('/jobs')


@jobs.route('/jobs/freelancer/accept-request', methods=['POST'])
@login_required
def FL_accept_request():
    req_id = request.form['req_id']
    req_id = int(req_id)
    req = JobRequests.query_get(id=req_id)
    today = datetime.datetime.now()
    try:
        JobRequests.update_status(req_id=req_id, new_status='Accepted')
        apply = ApplyJobs(freelancer_tag=current_user.tag, job_id=req.reference_job, date_applied=today, job_status='Ongoing', application_status='Hired')
        apply.add()
        mysql.connection.commit()
        Jobs.update_status(job_id=req.reference_job, new_status='Ongoing')
        Jobs.update_accept(accepted_datetime=today,job_id=req.reference_job)
        new_work = WorksOn(freelancer_tag=current_user.tag, job_id=req.reference_job)
        new_work.add()
        mysql.connection.commit()
        flash('Successfully Accepted Job!', category='success')
    except Exception as e:
        flash('There was a problem. Try again.', category='error')
        print(e)
    return redirect('/jobs')

@jobs.route('/jobs/freelancer/reviews')
@login_required
def FL_reviews():
    reviews = Reviews.query_filter(freelancer=current_user.tag)
    return render_template("/jobs/FL_reviews.html", reviews=reviews)

@jobs.route('/jobs/freelancer/reviews/<review_id>')
@login_required
def FL_reviews_single(review_id):
    review = Reviews.query_get(review_id)
    return render_template("/jobs/FL_review_modal_content.html", review=review)

@jobs.route('/jobs/freelancer/history')
@login_required
def FL_history():
    jobs_applied = ApplyJobs.query_filter(freelancer=current_user.tag, order_by='date_applied', order='DESC')
    return render_template('jobs/FL_history.html', jobs_applied=jobs_applied)

@jobs.route('/jobs/freelancer/update-bio', methods=['POST'])
@login_required
def FL_update_bio():
    new_bio = request.form['FL_bio']
    if not new_bio:
        new_bio = ' '
    FreelancerDetails.update_bio(freelancer=current_user.tag, new_bio=new_bio)
    mysql.connection.commit()
    return redirect('/jobs')

@jobs.route('jobs/freelancer/cancel-ongoing', methods=['POST'])
@login_required
def FL_cancel_ongoing():
    works_on = request.form['job_id']
    works_on = WorksOn.query_get(works_on)
    job = Jobs.query_get(works_on.job_id)
    job_id = job.job_id
    try:
        ApplyJobs.update_application_status(job_id=job_id, freelancer_tag=current_user.tag, status='Cancelled')
        Jobs.update_status(job_id=job_id, new_status='Cancelled')
        print(job_id, current_user.tag)
        mysql.connection.commit()
        flash('Cancelled Successfully', category='success')
    except Exception as e:
        flash('An error has occured', category='error')
        print(e)
    return redirect('/jobs')

@jobs.route('jobs/freelancer/cancel-application', methods=['POST'])
@login_required
def FL_cancel_application():
    job_id = request.form['job_id']
    try:
        print(job_id, current_user.tag)
        ApplyJobs.update_application_status(job_id=job_id, freelancer_tag=current_user.tag, status='Cancelled')
        mysql.connection.commit()
        flash('Cancelled Successfully', category='success')
    except Exception as e:
        flash('An error has occured', category='error')
        print(e)
    return redirect('/jobs')

@jobs.route('/jobs/freelancer/job-search')
@login_required
def FL_job_search():
    available_jobs = Jobs.query_filter(job_status='Waiting')
    applied_jobs = ApplyJobs.query_filter(freelancer=current_user.tag, application_status='Sent')
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
    job_status = job.job_status
    application_status = 'Sent'
    new_application = ApplyJobs(freelancer_tag=freelancer_tag, job_id=job_id, job_status=job_status, application_status=application_status, date_applied=today)
    try:
        new_application.add()
        mysql.connection.commit()
        flash('Successfully sent application!', category='success')
    except Exception as e:
        flash('An error has occured.', category='error')
        print(e)

    return redirect('/jobs')
