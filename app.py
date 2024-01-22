# fmt: off

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_cors import CORS
from hooks.jwt_callbacks import jwt
import os



load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 86400
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
CORS(app)
db = SQLAlchemy(app)
jwt.init_app(app)

from models.models import User

with app.app_context():
    db.create_all()

from routes import public_routes
from routes.private_routes import private_routes

app.register_blueprint(public_routes)
app.register_blueprint(private_routes)

@app.route('/')
def hello_world():
    return 'Hello, World!'