from flask import Blueprint, render_template, request, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
#from website import app
from .models import User, Location, Court
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route("/sign-up", methods=['GET', 'POST'])
@auth.route("/sign-up/", methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        pass1 = request.form.get("password1")
        pass2 = request.form.get("password2")
        auth_code = request.form.get("auth")
        ##print(auth_code)
        # grad_year = int(request.form.get("grad-year"))
        # interests = request.form.get("interests")
        # skills = request.form.get("skills")
        # create new users

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(fname) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif pass1 != pass2:
            flash('Passwords don\'t match.', category='error')
        elif len(pass1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        # fix the auth code!!!
        elif auth_code != "123":
            flash('Invalid authentication code. Please contact the developer for access.', category='error')
        else:
            new_user = User(email=email, first_name=fname, last_name=lname, password=generate_password_hash(
                pass1, method='sha256'))
            # adds the new profile
            db.session.add(new_user)
            db.session.commit()
            # logs in user before creating new profile with current user's id
            login_user(new_user, remember=True)
            #new_profile = Profile(graduation_year=grad_year, interests=interests, skills=skills, user_id=current_user.id)
            #db.session.add(new_profile)
            #db.session.commit()
            flash("Account Created!", category="success")
            return redirect(url_for("views.home"))
    return render_template("sign-up.html", title="Sign Up", user=current_user)

# @auth.route("/login", methods=['GET', 'POST'])
# @auth.route("login/", methods=['GET', 'POST'])
# def login():
#     return render_template("login.html", title="Login")

@auth.route('/login', methods=['GET', 'POST'])
@auth.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user, title="Login")


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))