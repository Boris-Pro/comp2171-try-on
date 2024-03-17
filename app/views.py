import os
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, session, abort
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from app.models import UserProfile
from app.forms import LoginForm
from app.forms import RegisterForm
from werkzeug.security import check_password_hash
from app.helper import get_uploaded_images
from flask import send_from_directory

###
# Routing for your application.
###


@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")


@app.route('/register', methods=['GET', 'POST'])
def register():
    myform = RegisterForm()
    if request.method == 'POST':
    
        if myform.validate_on_submit():
            # Perform actions with form data, like sending an email
            # For example:
            # send_email(form.name.data, form.email.data, form.subject.data, form.message.data)
            first_name = myform.first_name.data
            last_name = myform.last_name.data
            user_name = myform.user_name.data
            email = myform.email.data
            password = myform.password.data
    
            flash('You have successfully filled out the form', 'success')
            new_user = UserProfile(first_name=first_name,
                                    last_name=last_name,
                                    user_name=user_name,
                                    email=email,
                                    password=password)
            
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('home'))
        flash_errors(myform)
    return render_template('register.html', form=myform)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user_name = form.user_name.data
        password = form.password.data

        #user = UserProfile.query.filter_by(username=username).first()
        user = db.session.execute(db.select(UserProfile).filter_by(user_name=user_name)).scalar()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('home'))  # Redirect to the upload route or any other route
        else:
            flash('Invalid username or password.', 'danger')

    return render_template("login.html", form=form)    


# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return db.session.execute(db.select(UserProfile).filter_by(id=id)).scalar()

###
# The functions below should be applicable to all Flask apps.
###

# Flash errors from the form if validation fails

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('home'))

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
