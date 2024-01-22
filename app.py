# fmt: off

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_cors import CORS
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 86400
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
CORS(app)
db = SQLAlchemy(app)

from models.models import User

with app.app_context():
    db.create_all()

from routes.routes import routes as routes_blueprint
app.register_blueprint(routes_blueprint)

@app.route('/')
def hello_world():
    return 'Hello, World!'