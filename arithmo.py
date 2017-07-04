import logging
import os
import time

from flask import Flask, request, render_template, session, flash, redirect, url_for

from utils import TweeterDAO

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


@app.route('/api/utils', methods=['GET'])
def tweet_webhook():
    Log.info("Incoming message : %s", request.args)
    return 'Hello', 200


@app.route('/api/utils', methods=['POST'])
def tweet_request():
    Log.info("Incoming POST request from utils : %s", request.args)


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
    Log.info("Create Twitter api instance")
    tweeter_api = TweeterDAO()
    api = tweeter_api.get_api('8G9uQK2sjZDkU2BG58dvOShQU', 'nG4nq29rQdsNfu9Cxpe5q1j9RjjIpWHDnWOStN9Be21zS48C7n',
                              '1648488114-gFdXDFyIrQIFTfXRKY5xX59pAFjPY9iCTxFWeyo',
                              'UDud8JyFUqpN06xJAgOcCyTBwpTZsgSfA7C7V47oBnICK')
    try:
        users = tweeter_api.get_friends()
        print([u.screen_name for u in users])
        Log.debug(users.__str__())
        nb_followers = tweeter_api.followers_count()
        Log.debug(nb_followers)
    except Exception as e:
        Log.error(e.__str__())

    app.run(port=PORT, host=HOST)


if __name__ == '__main__':
    run()
