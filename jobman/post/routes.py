from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from jobman.forms import JobForm, ApplyForm, Apply
from jobman.models import Jobs, Application
from jobman import db

posts = Blueprint('post', __name__)

@posts.route("/posted_jobs")
@login_required
def posted_jobs():
    jobs = Jobs.query.filter_by(job_applier=current_user)
    return render_template('show_jobs.html', jobs=jobs)
@posts.route("/")
@posts.route("/show_jobs")
def show_jobs():
    jobs = Jobs.query.all()
    if current_user.is_authenticated: # type: ignore
        return render_template('show_jobs.html', jobs=jobs)
    else:    return redirect(url_for('users.login'))


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def post_jobs():
    if current_user.is_authenticated: # type: ignore
        if current_user.usertype == 'Job Seeker': # type: ignore
            return redirect(url_for('users.show_jobs'))
    form = JobForm()
    if form.validate_on_submit():
        job = Jobs(title=form.title.data, 
                content=form.content.data,
                location=form.location.data,
                level=form.level.data,
                job_applier=current_user) # type: ignore
        db.session.add(job)
        db.session.commit()
        return redirect(url_for('users.posted_jobs'))
    return render_template('create_post.html', form=form)

@posts.route("/job/<int:post_id>")
def post(post_id): 
    post = Jobs.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
def update_post(post_id):
    post = Jobs.query.get_or_404(post_id)
    form = JobForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.location = form.location.data
        post.level = form.level.data
        db.session.commit()
        flash('Your post has been updated', 'success')
        return redirect(url_for('post.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.location.data = post.location
        form.level.data = post.level

    return render_template('create_post.html', post=post, form=form, legend='Update Post')

@posts.route("/post/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Jobs.query.get_or_404(post_id)
    if current_user.usertype == 'Job Seeker': # type: ignore
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('users.show_jobs'))

@posts.route("/post/<int:job_id>/apply", methods=['GET', 'POST'])
@login_required
def apply_post(job_id):
    # post = Post.query.get_or_404(post_id)
    form = ApplyForm()
    job = Jobs.query.filter_by(id=job_id).first()
    if form.validate_on_submit():
        apply = Application(name=form.name.data,
                            experience=form.experience.data,
                            cover_letter=form.content.data,
                            email=form.email.data,
                            contact=form.contact.data,
                            job_id=job_id,
                            user_id=current_user.id, # type: ignore
                            degree=form.degree.data
                            #   content=form.content.data
                            #   cv=form.cv.data.filename
                            #   application_submiter=current_user,
                            #   application_jober=job,
                            #   resume=form.resume.data.filename
                            ) # type: ignore
        # picture_file = save_picture(form.resume.data)
        db.session.add(apply)
        db.session.commit()
        return redirect(url_for('users.show_jobs'))
    return render_template('apply.html', form=form, legend='Apply Now')

@posts.route("/show_applications/<jobid>", methods=['GET', 'POST'])
@login_required
def show_applications(jobid):
    if current_user.usertype == 'Job Seeker': # type: ignore
        abort(403)
    form = Apply()
    applications = Application.query.filter_by(job_id=jobid).order_by(Application.degree, Application.experience.desc()).all()
    # applications = Application.query.all()
    job = Jobs.query.all()
    if form.validate_on_submit():
        print(form.status.data)
        # db.session.add(status)
        # db.session.commit()
    return render_template('show_applications.html',applications=applications , job=job , form=form)


@posts.route("/show_applications/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_app(post_id):
    post = Jobs.query.get_or_404(post_id)
    if current_user.usertype == 'Job Seeker': # type: ignore
        abort(403)
    
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('users.show_jobs'))

@posts.route("/applications/<id>/", methods=['GET', 'POST'])
def update_app(id):
    application = Application.query.get_or_404(id)
    form = ApplyForm()
    form2 = Apply()
    id=id
    # apply = Application(status=form2.status.data)
    if form2.validate_on_submit():
        print(form2.status.data)
        application.status = form2.status.data
        db.session.commit()
        flash('Application has been updated', 'success')
        # return redirect(url_for('/show_applications/<id>', post_id=post.id))
    
    elif request.method == 'GET':
        form.name.data = application.name
        form.email.data = application.email
        form.experience.data = application.experience
        form.degree.data = application.degree
        form2.status.data = application.status

    return render_template('application.html', application=application, id=id , form=form, form2=form2)