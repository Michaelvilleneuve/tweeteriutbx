import logging
import os
import time

from flask import Flask, request, render_template, session, flash, redirect, url_for

from Arduino import Arduino
from Arithmo import TweeterDAO
from Arithmo import ArithmoThread
from Arithmo import UpdateThread

USER_STREAM_THREAD = "UserStream"
UPDATE_THREAD = "UpdateThread"

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
    Log.info("Create Twitter api instance")
    twitter_api = TweeterDAO()
    twitter_api.set_api('8G9uQK2sjZDkU2BG58dvOShQU', 'nG4nq29rQdsNfu9Cxpe5q1j9RjjIpWHDnWOStN9Be21zS48C7n',
                        '1648488114-gFdXDFyIrQIFTfXRKY5xX59pAFjPY9iCTxFWeyo',
                        'UDud8JyFUqpN06xJAgOcCyTBwpTZsgSfA7C7V47oBnICK',
                        '1648488114')
    try:
        arduino = Arduino()
        stream_user_thread = ArithmoThread(1, USER_STREAM_THREAD, twitter_api, arduino)
        stream_user_thread.start()
        update_thread = UpdateThread(2, UPDATE_THREAD, twitter_api, arduino)
        update_thread.start()
    except Exception as e:
        Log.error(e.__str__())
    time.sleep(0.5)
    twitter_api.send_message(
        "Hi, I'm @Projet_Arithmo. Now on air this " + time.strftime("%a the %d %d %Y at %H:%M:%S") + ";) Welcome to " +
        twitter_api.get_user('1648488114').name)

    Log.info("Start server at host http://%s:%i", HOST, PORT)
    app.run(port=PORT, host=HOST)

    @app.teardown_appcontext
    def stop():
        # Stop userStream connexion
        stream_user_thread.name.exit()
        update_thread.name.exit()


if __name__ == '__main__':
    run()
