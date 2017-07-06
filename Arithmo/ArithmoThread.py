import os
import threading

import logging

import time

exitFlag = 0

log_level = os.environ.get("LOGLEVEL") or 'NOTSET'

# Create logger
Log = logging.getLogger('ArithmoThread')
Log.setLevel(log_level)

console_handler = logging.StreamHandler()
console_handler.setLevel(log_level)

file_handler = logging.FileHandler(
    os.path.dirname(os.path.abspath(__file__)) + '/../logs/' + time.strftime("%d_%m_%Y") + '_tweetos-app.log')
file_handler.setLevel(log_level)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers
Log.addHandler(console_handler)
Log.addHandler(file_handler)


class ArithmoThread(threading.Thread):
    def __init__(self, threadId, name, tweeter_api, arduino):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.name = name
        self.tweeter_api = tweeter_api
        self.arduino = arduino

    def get_user_stream(self):
        for line in self.tweeter_api.get_stream():
            Log.info(line)
            if 'target' in line.keys():
                Log.info(line['target']['followers_count'])
                self.tweeter_api.nb_followers = line['target']['followers_count']
                self.arduino.send_followers_count(self.tweeter_api.nb_followers)

    def run(self):
        self.get_user_stream()