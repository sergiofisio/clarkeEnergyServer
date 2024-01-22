from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from models.models import User
from app import db
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta

public_routes = Blueprint('public_routes', __name__)


@public_routes.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        required_fields = ['nome', 'email', 'senha']
        for field in required_fields:
            if field not in data:
                raise ValueError(f'{field} é obrigatóriorio')
            if not data[field]:
                raise ValueError(f'{field} não pode ser vazio')
        hashed_password = generate_password_hash(
            data['senha'], method='pbkdf2:sha256')
        data.pop('senha', None)
        new_user = User(**data, senha=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'usuário criado com sucesso'}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'usuário ja existe'}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@public_routes.route('/login', methods=['POST'])
def login_user():
    try:
        data = request.get_json()
        required_fields = ['email', 'senha']
        for field in required_fields:
            if field not in data:
                raise ValueError(f'{field} é obrigatóriorio')
            if not data[field]:
                raise ValueError(f'{field} não pode ser vazio')
        user = User.query.filter_by(email=data['email']).first()
        if not user or not check_password_hash(user.senha, data['senha']):
            return jsonify({'message': 'Invalid username or password'})
        expires_delta = timedelta(
            seconds=current_app.config['JWT_ACCESS_TOKEN_EXPIRES'])
        expiration_time = datetime.now() + expires_delta
        access_token = create_access_token(identity={'email': user.email})
        user_info = vars(user)
        user_info.pop('senha', None)
        user_info.pop('_sa_instance_state', None)
        return jsonify({'token': access_token, 'expires_at': expiration_time.isoformat(), 'user': user_info}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
