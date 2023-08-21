from flask_login import current_user
import uuid
import os

from . import db

UPLOAD_FOLDER = 'myapp/static/uploads/'
# UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')

def new_id():
    return uuid.uuid4()

def delpicture(picture):
    os.remove(os.path.join(UPLOAD_FOLDER, current_user.id, picture.picture))
    db.session.delete(picture)
    db.session.commit()
    return True
