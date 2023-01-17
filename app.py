import os
from flask import Flask, send_file, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config
from models import db, User, Post
from pprint import pprint
from flask_socketio import SocketIO, emit
import platform
import jwt

SECRET_KEY = 'burntheboats'
app = Flask(__name__, static_folder='public')
CORS(app, origins=['*'])
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)
socketio = SocketIO(app, cors_allowed_origins='*')

def authenticated(func):
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'No authentication token provided'}), 401
        try:
            # decode the incoming JWT using our application's secret key
            decoded_user = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user = User.query.get(decoded_user['user_id'])
            if not current_user:
                return jsonify({'message': 'User token is invalid'}), 401
            return func(*args, current_user=current_user, **kwargs)
        except Exception as e:
            print(e)
            return jsonify({'error': e}), 500
    return wrapper

# In Rails, controller actions and routes are separate
# Here in Flask, they are put together

@app.get('/')
def home():
    return send_file('welcome.html')


@app.get('/example')
def example():
    return {'message': 'Your app is running Python'}


@app.get('/info')
def info():
    print(dir(platform))
    return {'machine': platform.node()}


@app.post('/users')
def users():
    data = request.form
    user = User(data['username'], data['email'], data['password'])
    print(data)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


@app.post('/login')
def login():
    data = request.form
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({'error': 'No user found'}), 404
    given_password = data['password']
    if user.password == given_password:
        # encode JWT as the token variable, signing it with our application's secret key
        # we store only what the token will need while identifying the users on any given request
        token = jwt.encode({'user_id': user.id}, SECRET_KEY, algorithm='HS256')
        return jsonify({'user': user.to_dict(), 'token': token})
    else:
        return jsonify({'error': 'Invalid email or password'}), 422


@app.get('/users/<int:id>')
def show(id):
    user = User.query.get(id)
    if user:
        return jsonify(user.to_dict())
    else:
        return {}, 404


# run user.to_dict() for every user in users
@app.get('/users')
def all_users():
    users = User.query.all()
    User.query.count()
    return jsonify([user.to_dict() for user in users])


@app.patch('/users/<int:id>')
def update_user(id):
    user = User.query.get_or_404(id)
    user.username = request.form['username'] # currently only updates the username. Add more as you see fit
    db.session.commit()
    return jsonify(user.to_dict())


# This is how we protect routes. Ideally you'd check to ensure that the current_user id
# is the same as the id of the user who owns the resources being deleted
@app.delete('/users/<int:id>')
@authenticated
def delete_user(id, current_user):
    user = User.query.get(id)
    if user:
        if user.id == current_user.id:
            db.session.delete(user)
            db.session.commit()
            return jsonify(user.to_dict())
        else:
            return jsonify({'error': 'You cannot access this resource'}), 401
    else:
        return {'error': 'No user found'}, 404    


@app.get('/posts/<int:id>')
def show_post(id):
    post = Post.query.get(id)
    return jsonify(post.to_dict())


@socketio.on('connect')
def connected():
    '''This function is an event listener that gets called when the client connects to the server'''
    print(f'Client {request.sid} has connected')
    emit('connect', {'data': f'id: {request.sid} is connected'})


@socketio.on('data')
def handle_message(data):
    '''This function runs whenever a client sends a socket message to be broadcast'''
    print(f'Message from Client {request.sid} : ', data)
    emit('data', {'data': 'data', 'id': request.sid}, broadcast=True)


@socketio.on("disconnect")
def disconnected():
    '''This function is an event listener that gets called when the client disconnects from the server'''
    print(f'Client {request.sid} has disconnected')
    emit('disconnect', f'Client {request.sid} has disconnected', broadcast=True)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=os.environ.get('PORT', 3000))