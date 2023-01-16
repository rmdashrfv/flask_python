import os
from flask import Flask, send_file, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config
from models import db, User, Post
from pprint import pprint
from flask_socketio import SocketIO, emit
import platform

app = Flask(__name__, static_folder='public')
CORS(app, origins=['*'])
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)
socketio = SocketIO(app, cors_allowed_origins='*')

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


@app.delete('/users/<int:id>')
def delete_user(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify(user.to_dict())
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