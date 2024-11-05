from flask import Flask
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import logging

logging.basicConfig(level=logging.DEBUG)


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.debug = True
    
    app.config['SECRET_KEY'] = 'mysecret6660'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sneakpeek.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    Bootstrap(app)

    from .views import main_bp as main_blueprint
    app.register_blueprint(main_blueprint)

    @app.errorhandler(404) 
    # Inbuilt function (to Flask) which takes error as parameter
    def not_found(e): 
      return render_template("error.html", error=e)

    # Handles server errors (look-up 'HTTP response status codes')
    @app.errorhandler(500)
    def internal_error(e):
      return render_template("error.html", error=e)

    return app

def create_tables(app):
    app = create_app()
    with app.app_context():
        db.create_all()

