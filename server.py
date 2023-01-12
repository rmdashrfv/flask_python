import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Your Python API is running!"


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=os.environ.get('PORT', 3000))