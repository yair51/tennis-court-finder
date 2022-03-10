from genericpath import exists
from unicodedata import category
from flask import Blueprint, redirect, render_template, request, flash, url_for, jsonify
from flask_migrate import current
from . import db, admin
from flask_admin.contrib.sqla import ModelView
from .models import CourtStatus, User, Location, Court, LocationStatus
from flask_login import current_user, login_required
from sqlalchemy import func
#from website import app

views = Blueprint('views', __name__)

@views.route("/")
def home():
    subquery = db.session.query(LocationStatus.location_id, LocationStatus.is_open, LocationStatus.time, Location.name, Location.address, Location.city, Location.state, Location.zip_code,
    func.rank().over(order_by=LocationStatus.time.desc(),
    partition_by=LocationStatus.location_id).label('rnk')).filter(Location.id == LocationStatus.location_id).subquery()
    # queries locations and takes the first locations
    locations = db.session.query(subquery).filter(
    subquery.c.rnk==1)
    #locations = db.session.query(Location)
    for location in locations:
        print(location.is_open)
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

@views.route("/report/<int:location_id>", methods=['GET', 'POST'])
@views.route("/report/<int:location_id>/", methods=['GET', 'POST'])
def report(location_id):
    # queries the specified court
    status = request.args.get("status")
    # if there is data sent, update the court's status
    if status:
        if status == "open":
            new_status = LocationStatus(is_open=True, location_id=location_id)
            db.session.add(new_status)
        # if in use, set is_open to false in new status
        elif status == "used":
            new_status = LocationStatus(is_open=False, location_id=location_id)
            db.session.add(new_status)
        db.session.commit()
        return redirect(url_for("views.home"))
    return render_template("report.html", title="Report", user=current_user)

@views.route('/logs/<int:id>')
@views.route('/logs/<int:id>/')
def logs(id):
    count = 0
    # count variable used for numbers on logs
    # queries location status table and shows only the current location based on the route
    logs = db.session.query(LocationStatus.time, LocationStatus.id, LocationStatus.is_open).filter(LocationStatus.location_id == id).order_by(LocationStatus.time.desc())
    for log in logs:
        count += 1
    return render_template("logs.html", user=current_user, title="Logs", logs=logs, count=count)

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Location, db.session))
admin.add_view(ModelView(Court, db.session))
admin.add_view(ModelView(CourtStatus, db.session))
admin.add_view(ModelView(LocationStatus, db.session))