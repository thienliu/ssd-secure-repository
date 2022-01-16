from flask import Flask, Blueprint
from flask_restful import Api
# from flask_migrate import Migrate

from config import config

def create_app(env):
    app = Flask(__name__)
    app.config.from_object(config[env])

    # migrate = Migrate()
    # migrate.init_app(app, db)

    api_bp = Blueprint('api', __name__)
    api = Api(api_bp)
    # api = Api(app)

    app.register_blueprint(api_bp, url_prefix="/api/v1")
    
    return app