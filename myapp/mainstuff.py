from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user
from werkzeug.security import generate_password_hash

from . import db
from .extras import new_id
from .models import Pictures, Settings, Users
from .webforms import SetupForm

mainstuff = Blueprint("mainstuff", __name__)

@mainstuff.route('/')
def main():
    settings = Settings.query.first()
    if not settings:
        return redirect(url_for("mainstuff.setup"))
    pictures = Pictures.query.order_by(Pictures.date_added.desc())
    return render_template("pictures.html",
                           pictures=pictures)

@mainstuff.route("/setup", methods=['GET','POST'])
def setup():
    form = SetupForm()
    if form.validate_on_submit():
        password = form.password_hash.data
        hashed_pw = generate_password_hash(password)
        useruuid = new_id()
        user = Users(id=useruuid, name=form.name.data, email=form.email.data, password_hash=hashed_pw, admin='y')
        db.session.add(user)
        # db.session.commit()
        settings = Settings(sitename=form.sitename.data, signup=form.signup.data)
        db.session.add(settings)
        db.session.commit()
        # logging.info(f"new user - username: {username}")
        flash("Site Setup Successfully!")	
        return redirect(url_for('mainstuff.main'))
    else:
        flash("Passwords do not match")
    settings = Settings.query.first()
    if not settings:
        
        return render_template("setupnew.html",
                               form=form)