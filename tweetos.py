import logging
import os

import time
from flask import Flask, request

from TweetAPI.TweeterAPI import TweeterAPI

app = Flask(__name__)

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

PORT = 5000
HOST = "127.0.0.1"  # ip externe de la machine


@app.route('/')
def hello_world():
    return 'Hello World!', 418


@app.route('/api/tweeter', methods=['GET'])
def tweet_webhook():
    Log.info("Incoming message : %s", request.args)
    crc_token = request.args['crc_token']
    res = tweeter.validateCallbackURL(crc_token)
    return res.__str__(), 200


@app.route('/api/tweeter', methods=['POST'])
def tweet_request():
    Log.info("Incomming POST request from tweeter : %s", request.args)
    x_tweeter_webhook_signature = request.args['x-tweeter-webhook-signature']


def run():
    Log.info("Start server at host http://%s:%i", HOST, PORT)  # Logging
    app.run(port=PORT, host=HOST)


if __name__ == '__main__':
    tweeter = TweeterAPI()
    run()
