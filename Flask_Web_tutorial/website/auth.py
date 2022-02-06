from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
"""
    import
    something called
    current user, which is
    going to represent or
    hold the current user.
    Now, this is the reason
    why we needed to in our
    'models.py'
    file, have this 'UserMixin' so that we can
    use this current user
    object here to access
    all of the information
    about the currently
    logged in user.
"""

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email= request.form.get('email')
        password= request.form.get('password')

        user= User.query.filter_by(email=email).first() # query returns that row as object
        if user:
            if check_password_hash(user.password, password): # user.email gives 'email'
                flash('Logged in successfully !', category='success')

                login_user(user, remember=True)
                """
                This is going to
                log in the user. Last
                thing we'll say,
                remember equals true.
                Now what this does is
                this remembers the fact
                that this user is
                logged in, uh, until
                the user, I guess,
                clears their browsing
                history or their
                session. Uh, this is
                going to store in the
                flask session. So after
                you restart the flask
                web server, this will
                no longer be true.
                So they don't need to
                log in every single
                time they go on the
                website.
                """
                return redirect(url_for('views.home'))
            else:
                flash('Password or Username is incorrect, Please try again', category='error')
        else:
            flash('Password or Username is incorrect, Please try again', category='error')


    return render_template("login.html", user= current_user)

@auth.route('/logout')
@login_required # We can only access this function iff we are logged in 
def logout():
    logout_user()
    return redirect((url_for('auth.login'))) #redirects to login page

@auth.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        email= request.form.get('email')
        firstname= request.form.get('firstname')
        password1= request.form.get('password1')
        password2= request.form.get('password2')

        user= User.query.filter_by(email=email).first()

        if user:
            flash("Bro, this email is already used ", category='error')
        elif len(email)<4:
            flash("Invalid email", category='error')
        elif len(firstname)<1:
            flash("Invalid name", category='error')
        elif len(password1)<7:
            flash("Password should be of minimum 7 characters", category='error')
        elif password1 != password2:
            flash("Passwords do not match", category='error')
        else:
            new_user = User(email=email, first_name=firstname, password= generate_password_hash(password1, method='sha256'))
            """
            This 'User' is the 'User'
            that we defined in the
            models.py. So what I need to
            do now is
            to import that. So say
            from .models import User (at the top)
            """
            db.session.add(new_user) # adds the user object to database
            db.session.commit()
            flash("Successfully signedup ", category='success')
            return redirect(url_for('views.home')) # redirects to the home function inside views.py
            # url_for('/') also works

    return render_template("signup.html", user= current_user)