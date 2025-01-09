import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from . import db, auth, index, about


def create_app(test_config=None):
    # Create and configure the application
    app = Flask(__name__, instance_relative_config=True, static_folder='static')
    app.config.from_mapping(
        SECRET_KEY='582e8456d1921eaaf7da85c6f2f2da7eb0bc017c8ea91e5728c2ee23e3579aac',
        DATABASE=os.path.join(app.instance_path, 'puzzleske.sqlite'),
        # Limit file upload size
        MAX_CONTENT_LENGTH=2000 * 2000,
        # Limit file extensions
        UPLOAD_EXTENSIONS={'.jpg', '.png', '.gif', '.jpeg'},
    )

    # File upload path
    UPLOAD_PATH = os.path.join(app.static_folder, 'uploads')  # type: ignore
    if not os.path.exists(UPLOAD_PATH):
        os.makedirs(UPLOAD_PATH)
    app.config['UPLOAD_PATH'] = UPLOAD_PATH

    if test_config is None:
        # load the instance config, if exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the passed test_config
        app.config.from_mapping(test_config)

    # Check if instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register db
    db.init_app(app)

    # Register links
    app.register_blueprint(auth.bp)
    app.register_blueprint(index.bp)
    app.register_blueprint(about.bp)

    # test function
    @app.route('/hello')
    def hello():
        return 'Hello World.'

    return app
