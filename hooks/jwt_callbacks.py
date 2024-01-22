from flask import jsonify
from flask_jwt_extended import JWTManager
from datetime import datetime

jwt = JWTManager()


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
