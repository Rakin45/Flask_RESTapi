from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
import os

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()

basedir = os.path.abspath(os.path.dirname(__file__))


def create_app(database_uri=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='h7V4kCJ9ySec4tOQjoik2A',
        JWT_SECRET_KEY='dfc77058462ab931095114bb89816729'
    )
    if database_uri:
        app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(app.instance_path, 'water_quality.sqlite')
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    from webapp.routes import api_bp
    app.register_blueprint(api_bp)
    
    import logging

    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(filename='app.log', level=logging.INFO, format=log_format)
    
    @app.before_request
    def log_request_info():
        logging.info(f"Request: {request.method} {request.url} - IP: {request.remote_addr}")


    @app.cli.command('init-db')
    def init_db_command():
        db.create_all()
        print('Initialised the database.')

    return app
