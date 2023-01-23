import uuid
from flask import request, jsonify
from functools import wraps
from config import Config
from models import User
from datetime import datetime, timedelta
import jwt

def create_access_token(user_id):
    now = datetime.now()
    return jwt.encode(
        {
            'sub': user_id,
            'iat': int(round(now.timestamp())),
            'exp': round((now + timedelta(hours=1)).timestamp()),
            'jti': str(uuid.uuid4()),
            'uid': ''
        },
        Config.SECRET_KEY, algorithm='HS256'
    )

def authenticate(func):
    '''
    Require user authentication to access a decorated endpoint via access tokens. Also gives the function access to the
    currently authenticated user (object) by passing the `current_user` argument into the endpoint function, which is useful
    for easy authorization checks.
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'No authentication token provided'}), 401
        try:
            # decode the incoming JWT using our application's secret key
            decoded_data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            if not decoded_data['exp']:
                return jsonify({'error': 'Invalid token. Missing token expiry'}), 401
            current_user = User.query.get(decoded_data['sub'])
            if not current_user:
                return jsonify({'error': 'User token is invalid'}), 401
            return func(*args, current_user=current_user, **kwargs)
        except Exception as e:
            print(e)
            return jsonify({'error': str(e)}), 500
    return wrapper


def generate_uid():
    '''Create an anonymous unique ID to attach to access tokens'''
    pass