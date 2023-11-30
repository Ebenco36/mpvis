import os
import logging
from flask import Flask
from flask_jwt import JWT
from SchedulerConfig import SConfig
from src.User.model import UserModel
from logging.handlers import RotatingFileHandler
from src.utils.security import authenticate, identity
from src.models.basemodel import db
from flask_mail import Mail
from celery import Celery
from src.middlewares.auth_middleware import token_required
from flask_apscheduler import APScheduler
from src.Jobs.MPStructJobs import MPSTRUCT
from src.Jobs.PDBJobs import PDBJOBS
from apscheduler.triggers.cron import CronTrigger
from flask_cors import CORS
from src import RouteInitialization

mail = Mail()
def initdb(flask_app):
    db.init_app(flask_app)
    with flask_app.app_context():
        print("We are here!")
        db.create_all()  # Create database tables for our data models
        return flask_app

def create_default_user(flask_app):
    with flask_app.app_context():
        check_user = UserModel.query.filter_by(username="admin").first()

        if(not check_user):
            default_user = UserModel(
                name='admin', 
                email='admin@example.com',
                username='admin', 
                phone='923928392832',
                is_admin=1
            )
            default_user.hash_password("password")
            db.session.add(default_user)
            print(default_user)
            db.session.commit()
            return flask_app
    
def create_app():
    flask_app = Flask(__name__, static_folder="./dist/static")

    # set log config for application
    # Configure logging to both console and file
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler = RotatingFileHandler('MPvisApp.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(formatter)
    flask_app.logger.addHandler(file_handler)

    # Configure logging
    logging.basicConfig(level=logging.INFO)  # Set the desired log level

    flask_app.config.from_object(SConfig())
    scheduler = APScheduler()
    # scheduler.api_enabled = True
    scheduler.init_app(flask_app)

    """
        Job Implementations
    """
    trigger = CronTrigger(
        year="*", month="*", day="15", hour="*", minute="*", second="*"
    )
    # interval example
    @scheduler.task(id='do_job_1', trigger=trigger)
    def mpstruct_job():
        mpstruct = MPSTRUCT()
        mpstruct.load_data().parse_data()
        print("Work is on going MPSTRUCT...")


    trigger_pdb = CronTrigger(
        year="*", month="*", day="15", hour="2", minute="*", second="*"
    )
    # interval example
    @scheduler.task(id='do_job_1', trigger=trigger_pdb)
    def pdb_job():
        pdb = PDBJOBS()
        pdb.load_data().parse_data()
        print("Work is on going PDB...")


    scheduler.start()

    # celery for jobs
    # Configure Celery
    # flask_app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
    # celery = Celery(flask_app.name, broker=flask_app.config['CELERY_BROKER_URL'])
    # # Define the background task
    # @celery.task
    # def background_task(arg1, arg2):
    #     # Perform background job here
    #     result = arg1 + arg2
    #     return result

    # @flask_app.route('/task')
    # def task1():
    #     # Trigger the background task
    #     result = background_task.delay(10, 20)
    #     return f"Background task started with task ID: {result.id}"

    # This is the configuration for the email server.
    flask_app.config["MAIL_SERVER"] = "smtp.gmail.com"
    flask_app.config["MAIL_PORT"] = 465
    flask_app.config["MAIL_USERNAME"] = os.environ.get("EMAIL_HOST_USER")
    flask_app.config["MAIL_PASSWORD"] = os.environ.get("EMAIL_HOST_PASSWORD")
    flask_app.config["MAIL_USE_TLS"] = False
    flask_app.config["MAIL_USE_SSL"] = True

    mail = Mail(flask_app)
    flask_app.config.from_pyfile('config.py')

    """
        Route Implementation. Well structured
    """
    init_route = RouteInitialization()
    init_route.init_app(flask_app)

    JWT(flask_app, authenticate, identity)  # /auth
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this is a secret'
    flask_app.config['SECRET_KEY'] = SECRET_KEY

    @flask_app.route('/')
    def index():
        return 'Welcome to MPvis Rest API Setup!'


    # Initialize CORS with default options (allow all origins)
    CORS(flask_app)

    initdb(flask_app)
    create_default_user(flask_app)

    return flask_app

app = create_app()

if __name__ == "__main__":
    app.run()
