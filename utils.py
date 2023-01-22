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
            'user_id': user_id,
            'iat': int(round(now.timestamp())),
            'expires_at': (now + timedelta(hours=1)).isoformat()
        },
        Config.SECRET_KEY, algorithm='HS256'
    )

def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'No authentication token provided'}), 401
        try:
            # decode the incoming JWT using our application's secret key
            decoded_user = jwt.decode(
                token, Config.SECRET_KEY, algorithms=['HS256'])
            current_user = User.query.get(decoded_user['user_id'])
            if not current_user:
                return jsonify({'message': 'User token is invalid'}), 401
            return func(*args, current_user=current_user, **kwargs)
        except Exception as e:
            print(e)
            return jsonify({'error': str(e)}), 500
    return wrapper