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
        self.twitter_api = tweeter_api
        self.arduino = arduino

    def get_user_stream(self):
        try:
            for line in self.twitter_api.get_stream():
                Log.info(line)
                if 'event' in line.keys():
                    Log.info("Incoming event" + line)
                    if line['event'] == 'follow':
                        Log.info("Incoming follow")
                        Log.debug(line['event']['follow'])
                        self.twitter_api.nb_followers = line['target']['followers_count']
                        self.arduino.send_followers_count(
                            '@' + self.twitter_api.get_user('1648488114').name + ' ' + str(
                                self.twitter_api.nb_followers))
                elif 'friends' in line.keys():
                    Log.info('Stream open')
                    time.sleep(1)
                    self.twitter_api.update_followers_count()
                    self.arduino.send_followers_count(
                        '@' + self.twitter_api.get_user('1648488114').name + ' ' + str(self.twitter_api.nb_followers))
        except Exception as e:
            Log.error(e)

    def run(self):
        Log.info("ArithmoThread up !!")
        self.get_user_stream()
