from flask import g, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from functools import wraps
from models import User


def jwt_required_and_user_loaded(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user = User.query.filter_by(email=get_jwt_identity()['email']).first()
        if not user:
            return jsonify({'message': 'Usuário não encontrado.'}), 404
        user_dict = user.__dict__.copy()
        user_dict.pop('senha', None)
        user_dict.pop('_sa_instance_state', None)
        g.user = user_dict
        return fn(*args, **kwargs)
    return wrapper
