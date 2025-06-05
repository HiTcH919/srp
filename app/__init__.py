import os
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager # Added import
from datetime import datetime

# Initialize extensions globally but without an app
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager() # Added login_manager
login_manager.login_view = 'auth.login' # Route name for login page (blueprint_name.route_function_name)
login_manager.login_message_category = 'info' # Flash category for login_required message
login_manager.login_message = "الرجاء تسجيل الدخول للوصول إلى هذه الصفحة." # Custom message

basedir = os.path.abspath(os.path.dirname(__file__))

def create_app(config_name=None): # config_name can be used for different configs e.g. testing, production
    app = Flask(__name__)

    # Default configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a_very_secret_dev_key') # Use env var or default
    # Construct the path to the database directory relative to the project root
    # __file__ is app/__init__.py, so dirname(__file__) is app/
    # os.path.join(basedir, '..', 'database', 'app.db') goes up one level from app/ to project root, then into database/
    db_path = os.path.join(basedir, '..', 'database')
    if not os.path.exists(db_path):
        os.makedirs(db_path) # Ensure database directory exists
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(db_path, 'app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Configuration for file uploads
    # app.static_folder is typically 'app/static'
    upload_path = os.path.join(app.static_folder, 'uploads', 'service_documents')
    app.config['UPLOAD_FOLDER'] = upload_path
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB upload limit (optional)

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app) # Initialize login_manager with the app

    # Import and register blueprints
    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from .routes.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

    from .routes.service_orders import service_orders_bp
    app.register_blueprint(service_orders_bp, url_prefix='/service')

    # Import models here so they are known to Flask-SQLAlchemy and Flask-Migrate
    # These imports need to happen after db is initialized with app for models to correctly inherit db.Model
    # However, for flask db commands to work, models must be imported when app is created.
    # The current structure (db global, then init_app) should work.
    from .models.user import User
    from .models.service_order import ServiceOrder
    from .models.document import Document # Import Document model as well
    # Import other models if they are directly used or need to be registered early
    # For Flask-Migrate, it's generally good if all models are imported when the app context is built for CLI.
    # The imports in app/models/__init__.py also help ensure they are known.

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # If you had other blueprints:
    # from .routes.reports import reports_bp
    # app.register_blueprint(reports_bp, url_prefix='/reports')
    # from .routes.phonebook import phonebook_bp
    # app.register_blueprint(phonebook_bp, url_prefix='/phonebook')
    # from .routes.backup import backup_bp
    # app.register_blueprint(backup_bp, url_prefix='/backup')


    # Template filters and context processors
    @app.template_filter('datetimeformat')
    def datetimeformat_filter(value, format='%Y-%m-%d %H:%M'):
        if value is None:
            return ""
        if isinstance(value, str):
            try:
                value = datetime.fromisoformat(value)
            except ValueError:
                try:
                    value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    return value
        if isinstance(value, datetime):
            return value.strftime(format)
        return value

    @app.context_processor
    def inject_now_filter(): # Renamed to avoid conflict with any 'now' variable
        return {'now': datetime.utcnow()}

    # Basic routes
    @app.route('/')
    def index():
        return redirect(url_for('dashboard.home'))

    @app.route('/hello')
    def hello():
        return "Hello, World! App is running. Database should be at: " + app.config['SQLALCHEMY_DATABASE_URI'] + \
               "<br>Upload folder is: " + app.config['UPLOAD_FOLDER']

    # Create upload folder if it doesn't exist, after app config is set
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        try:
            os.makedirs(app.config['UPLOAD_FOLDER'])
            print(f"Created upload folder: {app.config['UPLOAD_FOLDER']}")
        except OSError as e:
            print(f"Error creating upload folder {app.config['UPLOAD_FOLDER']}: {e}")


    return app
