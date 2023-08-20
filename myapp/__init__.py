from flask import Flask, render_template
from flask_login import LoginManager
from dotenv import load_dotenv

from .extensions import db, migrate

def create_app():
    import os
    load_dotenv()
    DB_SERVER = os.getenv('DB_SERVER')
    SECRET_KEY = os.getenv('SECRET_KEY')
    MYENV = '' if os.getenv('DEV_ENV') == None else os.getenv('DEV_ENV')

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_SERVER
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = SECRET_KEY
    db.init_app(app)
    migrate.init_app(app, db)

    #import blueprints
    from .mainstuff import mainstuff
    from .userstuff import userspages
    from .picstuff import picstuff

    #register blueprints
    app.register_blueprint(mainstuff)
    app.register_blueprint(userspages)
    app.register_blueprint(picstuff, url_prefix='/pictures')

    from .models import Users, Settings

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'userspages.login'

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(str(user_id))
    
    @app.context_processor
    def inject_myenv():
        settings = Settings.query.first()
        SITENAME = settings.sitename if settings else "Untitled"
        SIGNUP = settings.signup if settings else "y"
        # SITENAME = "Westley"
        return dict(myenv=MYENV, sitename=SITENAME, signup=SIGNUP)
    
    # Invalid URL
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    
    # Internal Server Error
    @app.errorhandler(500)
    def page_not_found(e):
        return render_template("500.html"), 500
    
    return app