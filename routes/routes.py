from flask import Blueprint, request, jsonify, g, current_app
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from sqlalchemy.exc import IntegrityError
from middleware.decorators import jwt_required_and_user_loaded
from werkzeug.security import generate_password_hash, check_password_hash
from models.models import User
from app import db, app
from datetime import datetime, timedelta

jwt = JWTManager(app)

routes = Blueprint('routes', __name__)


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_data):
    return jsonify({'message': 'O token expirou.', 'expired_at': datetime.fromtimestamp(
        jwt_data['exp']).strftime('%Y-%m-%d %H:%M:%S')}), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({'message': 'O token é inválido.'}), 422


@jwt.unauthorized_loader
def unauthorized_callback(error):
    return jsonify({'message': 'O token está faltando.'}), 403


@jwt.needs_fresh_token_loader
def needs_fresh_token_callback():
    return jsonify({'message': 'O token precisa ser atualizado.'}), 402


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({'message': 'O token foi revogado.'}), 410


@routes.route('/register', methods=['POST'])
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


@routes.route('/login', methods=['POST'])
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


@routes.route('/users', methods=['GET'])
@jwt_required_and_user_loaded
def get_all_users():
    users = User.query.all()
    output = []
    print(g.user)
    for user in users:
        user_data = {'nome': user.name, 'email': user.email}
        output.append(user_data)
    return jsonify({'users': output}), 200


@routes.route('/user/<id>', methods=['PUT'])
@jwt_required_and_user_loaded
def update_user(id):
    data = request.get_json()
    user = User.query.filter_by(id=id).first()
    if data['nome']:
        user.nome = data['nome']
    if data['senha']:
        hashed_password = generate_password_hash(
            data['senha'], method='pbkdf2:sha256')
        user.senha = hashed_password
    db.session.commit()
    return jsonify({'message': 'usuario atualizado'}), 202
