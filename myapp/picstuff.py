from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from datetime import date
import pathlib
import os

from . import db
from .extras import new_id, UPLOAD_FOLDER
from .models import Pictures, Settings, Users
from .webforms import PictureUploadForm

picstuff = Blueprint("picstuff", __name__)

@picstuff.route('/<uuid:id>')
@login_required
def viewpic(id):
    picture = Pictures.query.get_or_404(id)
    return render_template("picture.html",
                           picture=picture)

@picstuff.route('/add', methods=['GET','POST'])
@login_required
def picupload():
    form=PictureUploadForm()
    if request.method == 'POST':
        if 'picture' not in request.files:
            return redirect(url_for("mainstuff.main"))

        picture = request.files['picture']
        picture_filename = secure_filename(picture.filename)
        picture_uuid = new_id()
        today = str(date.today())
        picture_name = str(picture_uuid) + "_" + picture_filename
        picture_save = request.files['picture']
        pathlib.Path(UPLOAD_FOLDER, today).mkdir(exist_ok=True)
        picture_save.save(os.path.join(UPLOAD_FOLDER, today, picture_name))
        new_item = Pictures(id=picture_uuid, desc=form.desc.data, name=picture_name, folder=today, userid=current_user.id)
        db.session.add(new_item)
        db.session.commit()            
        return redirect(url_for("mainstuff.main",  _anchor=new_item.id))
    return render_template("pictureupload.html",
                           form=form)