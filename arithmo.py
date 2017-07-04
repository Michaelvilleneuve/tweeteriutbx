import logging
import os

import time

import sqlite3
import twitter
from flask import Flask, request, render_template, session, flash, redirect, url_for

HOST = '127.0.0.1'
PORT = 5000  # change to 80 in prod with sudo run

app = Flask(__name__)
app.config.from_object(__name__)  # Load config from this file.

app.config.update(dict(
    DATABASE=os.path.join(app.root_path + '/db', 'arithmo.sqlite'),
    SECRET_KEY='Asup3rScr37$#keYt0h4%rdtoF1nD'
))

log_level = os.environ.get("LOGLEVEL") or 'NOTSET'

# Create logger
Log = logging.getLogger('Tweetos')
Log.setLevel(log_level)

console_handler = logging.StreamHandler()
console_handler.setLevel(log_level)

file_handler = logging.FileHandler(
    os.path.dirname(os.path.abspath(__file__)) + '/logs/' + time.strftime("%d_%m_%Y") + '_tweetos-app.log')
file_handler.setLevel(log_level)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers
Log.addHandler(console_handler)
Log.addHandler(file_handler)


@app.route('/')
def hello_world():
    return render_template('welcome.html')


@app.route('/api/tweeter', methods=['GET'])
def tweet_webhook():
    Log.info("Incoming message : %s", request.args)
    return 'Hello', 200


@app.route('/api/tweeter', methods=['POST'])
def tweet_request():
    Log.info("Incoming POST request from tweeter : %s", request.args)


@app.route('/login', methods=['GET', 'POST'])
def login():
    pass


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


def run():
    Log.info("Start server at host http://%s:%i", HOST, PORT)
    app.run(port=PORT, host=HOST)
    Log.info("Create Twitter api instance")
    # api = twitter.Api(consumer_key='plop')


if __name__ == '__main__':
    run()
