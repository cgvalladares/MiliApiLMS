import jwt
from flask import request, jsonify
from functools import wraps
from config import JWT

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token=request.headers.get('token')
        if not token:
            return jsonify({'message':'token no recibido'}), 403
        try:
            data=jwt.decode(token,JWT.JWT_SECRET_KEY, algorithms=['HS256'])
            #print(f'token decode: {data}')
        except jwt.ExpiredSignatureError:
            return jsonify({'message':'token expirado'}),403
        except jwt.InvalidTokenError:
            return jsonify({'message':'token invalido'}), 403
        return func(*args, **kwargs)
    return decorated
