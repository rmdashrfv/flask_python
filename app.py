import os
from flask import Flask, send_file, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config
from models import db, User, Post
from pprint import pprint
import platform

app = Flask(__name__, static_folder='public')
CORS(app, origins=['*'])
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)

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
    print(user)
    user.username = request.form['username']
    db.session.commit()
    return jsonify({})


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
    print(post.user)
    return {}


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=os.environ.get('PORT', 3000))