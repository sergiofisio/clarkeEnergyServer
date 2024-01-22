from flask import Blueprint, request, jsonify, g
from werkzeug.security import generate_password_hash
from models.models import User
from app import db
from middleware.decorators import jwt_required_and_user_loaded

private_routes = Blueprint('private_routes', __name__)


@private_routes.route('/users', methods=['GET'])
@jwt_required_and_user_loaded
def get_all_users():
    users = User.query.all()
    output = []
    print(g.user)
    for user in users:
        user_data = {'nome': user.nome, 'email': user.email}
        output.append(user_data)
    return jsonify({'users': output}), 200


@private_routes.route('/user/<id>', methods=['PUT'])
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
