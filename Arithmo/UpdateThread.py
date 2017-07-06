import os
import threading

import time

import logging

update = True

log_level = os.environ.get("LOGLEVEL") or 'NOTSET'

# Create logger
Log = logging.getLogger('UpdateThread')
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


class UpdateThread(threading.Thread):
    def __init__(self, threadId, name, tweeter_api, arduino):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.name = name
        self.twitter_api = tweeter_api
        self.arduino = arduino

    def run(self):
        Log.debug("UpdateStream up")
        while update:
            now = time.time()
            do_update = now - self.twitter_api.last_update >= 60
            if do_update:
                try:
                    Log.info("Followers count updated !")
                    Log.debug(self.twitter_api.last_update)
                    self.twitter_api.update_followers_count()
                    self.arduino.send_followers_count(
                        '@' + self.twitter_api.get_user('1648488114').name + ' ' + str(self.twitter_api.nb_followers))
                except Exception as e:
                    Log.warning(e)
