from genericpath import exists
from unicodedata import category
from flask import Blueprint, redirect, render_template, request, flash, url_for
from flask_migrate import current
from . import db, admin
from flask_admin.contrib.sqla import ModelView
from .models import CourtStatus, User, Location, Court
from flask_login import current_user, login_required
#from website import app

views = Blueprint('views', __name__)

@views.route("/")
def home():
    locations = db.session.query(Location)
    for location in locations:
        print(location)
    #users = db.session.query(User, Profile).outerjoin(Profile, Profile.user_id == User.id)
    # for user in users:
    #     print(user)
    return render_template("index.html", title="Home", user=current_user, locations=locations)


@views.route("/add-location", methods=['GET', 'POST'])
@views.route("/add-location/", methods=['GET', 'POST'])
@login_required
def add_location():
    if request.method == "POST":
        location_name = request.form.get("location-name")
        street_address = request.form.get("street")
        city = request.form.get("city")
        state = request.form.get("state")
        zip_code = request.form.get("zip")
        
        #check if location name already exists
        location = Location.query.filter_by(address=street_address).first()
        if location:
            flash("Location at the specified street address already exists.", category="error")
            return render_template("add-location.html", user=current_user, title="Add Location")
        else:
            new_location = Location(name=location_name, address=street_address, city=city, state=state, zip_code=zip_code)
            db.session.add(new_location)
            db.session.commit()
            flash("Location added.", category="success")
            return redirect(url_for('views.home'))
    return render_template("add-location.html", title="Add Location", user=current_user)

@views.route("/add-court")
@views.route("/add-court/")
@login_required
def add_court():
    return render_template("add-court.html", title="Add Court", user=current_user)

@views.route("/report/<int:court_id>", methods=['POST'])
@views.route("/report/<int:court_id>/", methods=['POST'])
def report(court_id):
    # queries the specified court
    is_open = request.form.get("status")
    # if there is data sent, update the court's status
    if is_open:
        if is_open == "open":
            new_status = CourtStatus(is_open=True, court_id=court_id)
        # if in use, set is_open to false in new status
        elif is_open == "used":
            new_status = CourtStatus(is_open=False, court_id=court_id)
    


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Location, db.session))
admin.add_view(ModelView(Court, db.session))
admin.add_view(ModelView(CourtStatus, db.session))