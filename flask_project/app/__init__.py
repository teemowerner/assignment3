from flask import Flask, jsonify
from app.extensions import db, migrate
from app.config import Config
from app.routes import auth, jobs, applications, bookmarks

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(jobs, url_prefix="/jobs")
    app.register_blueprint(applications, url_prefix="/applications")
    app.register_blueprint(bookmarks, url_prefix="/bookmarks")

    # 기본 페이지 정의
    @app.route("/")
    def index():
        return jsonify({"message": "Welcome to the Job API!"})

    return app
