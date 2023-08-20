from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required, logout_user, login_user
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from . import db
from .webforms import LoginForm, UserSignupForm, UserEditForm, PasswordResetForm
from .models import Users 
from .extras import new_id

userspages = Blueprint("userspages", __name__)


@userspages.route('/login', methods=['GET','POST'])
def login():
    login_error = "Invalid User or Password - Try Again"
    active_error = "Your account is not active, contact your admin."
    go_next = request.args.get('next')
    form=LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            flash(login_error)
            return render_template("login.html",
                           form=form)
        
        if not check_password_hash(user.password_hash, form.password.data):
            flash(login_error)
            return render_template("login.html",
                           form=form)

        if user.active == 'n':
            flash(active_error)
            return render_template("login.html",
                           form=form)

        if user.active == 'y':
            login_user(user)
            flash(f"Last Login - {user.last_login}")
            user.last_login = datetime.now()
            db.session.add(user)
            db.session.commit()
            if go_next:
                return redirect(go_next)
            return redirect(url_for('mainstuff.main'))
    # elif:
    #     flash(login_error)

    return render_template("login.html",
                           form=form)

@userspages.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('mainstuff.main'))

@userspages.route('/signup', methods=['GET','POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('mainstuff.main'))
    form=UserSignupForm()
    if form.validate_on_submit():
        email_exists = Users.query.filter_by(email=form.email.data).first()
        name = form.name.data
        email = form.email.data
        password = form.password_hash.data
        if email_exists:
            # logging.debug("new user - email is user")
            flash("That email in use, sign in instead?")
            return redirect(url_for("userspages.login"))
        else:
            # Hash the password!!!
            hashed_pw = generate_password_hash(password)
            useruuid = new_id()
            user = Users(id=useruuid, name=name, email=email, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
            # logging.info(f"new user - username: {username}")
            flash("User Added Successfully!")	
            return redirect(url_for('userspages.login'))
    elif request.method == 'POST':
        flash("passwords do not match")
    return render_template("useredit.html",
                           form=form,
                           editid='n')

@userspages.route('/profile')
@login_required
def userprofile():
    form = UserEditForm()
    return render_template("profile.html",
                    form=form)

@userspages.route('/edit/<uuid:id>', methods=['GET', 'POST'])
@login_required
def useredit(id):
    form = UserEditForm()
    user_to_update = Users.query.get_or_404(id)
    
    if request.method == 'POST':
        email = form.email.data
        user_to_update.email = form.email.data
        user_to_update.name = form.name.data
        email_exists = Users.query.filter_by(email=email).first() if current_user.email != email else False
        if email_exists:
            flash("That email address is already in user")
        else:
            db.session.add(user_to_update)
            db.session.commit()
            return redirect(url_for('userspages.userprofile'))
    form.name.default=user_to_update.name
    form.email.default=user_to_update.email
    form.process()
    return render_template("profileedit.html",
                    form=form,
                    editid=user_to_update.id)
    
@userspages.route('/pass/<uuid:id>', methods=['GET','POST'])
@login_required
def passuser(id):
    form = PasswordResetForm()
    user_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        if form.password_hash.data != form.password_hash2.data:
            flash('Passwords do not match')
        else:
            hashed_pw = generate_password_hash(form.password_hash.data)
            user_to_update.password_hash = hashed_pw
            db.session.add(user_to_update)
            db.session.commit()
            return redirect(url_for('userspages.userprofile'))
    return render_template("profilepwreset.html",
                    form=form)
    