import os
import logging
from flask import Flask
#from flask_jwt import JWT
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
from flask_sqlalchemy import SQLAlchemy
from src import RouteInitialization
from flask_migrate import Migrate
from src.Commands.MigrateContent import generate_model_class, load_csv_data
# from sqlalchemy import create_engine, Column, String, MetaData

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()


# Access environment variables
flask_env = os.getenv("FLASK_DEBUG")
secret_key = os.getenv("SECRET_KEY")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

# Construct the DATABASE_URI using the environment variables
database_uri=f'postgresql://{db_user}:{db_password}@postgres:5432/{db_name}'
# Admin credentials
admin_name = os.getenv("ADMIN_NAME")
admin_email = os.getenv("ADMIN_EMAIL")
admin_username = os.getenv("ADMIN_USERNAME")
admin_password = os.getenv("ADMIN_PASSWORD")
admin_phone = os.getenv("ADMIN_PHONE")
is_admin = os.getenv("IS_ADMIN")

mail = Mail()

def initdb(flask_app, db):
    db.init_app(flask_app)
    with flask_app.app_context():
        db.create_all()  # Create database tables for our data models
        print("Working on content migration ...")
        csv_path = './Quantitative_data.csv'  # Replace with the path to your CSV file
        # dynamic_model = generate_model_class(csv_path)
        # dynamic_model.__tablename__ = 'membrane_proteins'  # Set a table name
        
        print("Done with database creation. Creating migrations...")
        db.create_all()  # Create database tables for our data models
        print("Done migrating relations.")
        
        # load_csv_data(dynamic_model, csv_path)
        print("Done with content migration.")
        
        return flask_app

def create_default_user(flask_app, db):
    with flask_app.app_context():
        print("setting up default admin-user ...")
        check_user = UserModel.query.filter_by(username="admin").first()

        if(not check_user):
            default_user = UserModel(
                name=admin_name, 
                email=admin_email,
                username=admin_username, 
                phone=admin_phone,
                is_admin=is_admin
            )
            default_user.hash_password(admin_password)
            db.session.add(default_user)
            db.session.commit()
            print("Done creating admin user.")
            return flask_app
    
def create_app():
    flask_app = Flask(__name__, static_folder="./dist/static")
    
    # Initialize Flask-SQLAlchemy
    # Configuring our database
    print("Connecting and Configuring our database...")
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Configure Flask app
    flask_app.config["ENV"] = flask_env
    flask_app.config["SECRET_KEY"] = secret_key
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    
    db = SQLAlchemy(flask_app)

    # set log config for application
    print("Configure logging to both console and file ...")
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
    '''
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
    '''

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
    
    # Initialize CORS with default options (allow all origins)
    print("CORS origin setup for MPVIS...")
    CORS(flask_app)

    initdb(flask_app, db)
    db.create_all()  # Create database tables for our data models
    # create_default_user(flask_app, db)
    
    

    """
        Route Implementation. Well structured
    """
    init_route = RouteInitialization()
    init_route.init_app(flask_app)

    #JWT(flask_app, authenticate, identity)  # /auth
    #SECRET_KEY = os.environ.get('SECRET_KEY') or 'this is a secret'
    #flask_app.config['SECRET_KEY'] = SECRET_KEY

    @flask_app.route('/')
    def index():
        return 'Welcome to MPvis Rest API Setup!'

    @flask_app.route('/task')
    def task():
        # Trigger the Celery task
        result = add.delay(4, 4)
        return jsonify({"task_id": result.id, "status": "Task has been submitted."})

    return flask_app

app = create_app()

if __name__ == "__main__":
    app.run()
