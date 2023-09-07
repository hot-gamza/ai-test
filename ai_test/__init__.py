from flask import Flask
from .views import main_routes

def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(main_routes.bp)

    return app