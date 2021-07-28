import os
import sys

from flask import Flask
from notice.notice import notice

# For Server
sys.path.insert(0, os.getcwd() + '/apis')

app = Flask(__name__)

app.register_blueprint(notice)


@app.route('/')
def welcome():
    return '<h1 align="center">Successfully Running</h1>'

