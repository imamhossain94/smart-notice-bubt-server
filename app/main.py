import os
import sys
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from fcm.fcm import prepareData
from notice.notice import notice

# Load .env file
from dotenv import load_dotenv

load_dotenv()

# Visit https://stackoverflow.com/questions/21214270/how-to-schedule-a-function-to-run-every-hour-on-flask
# to know more

# Code for local pc
# For Server
sys.path.insert(0, os.getcwd() + '/apis')


def do_something():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=prepareData, trigger="interval", seconds=20)
    scheduler.start()


class MyFlaskApp(Flask):
    def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
        if not self.debug or os.getenv('WERKZEUG_RUN_MAIN') == 'true':
            with self.app_context():
                do_something()
        super(MyFlaskApp, self).run(host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)


app = MyFlaskApp(__name__)
app.register_blueprint(notice)


@app.route('/')
def welcome():
    return '<h1 align="center">Successfully Running</h1>'

# Code fore heroku
# For Server
# sys.path.insert(0, os.getcwd() + '/apis')
#
# app = Flask(__name__)
#
# app.register_blueprint(notice)
#
#
# @app.route('/')
# def welcome():
#     return '<h1 align="center">Successfully Running</h1>'
