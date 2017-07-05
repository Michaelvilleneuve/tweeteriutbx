import threading

import time

update = True


class UpdateThread(threading.Thread):
    def __init__(self, threadId, name, tweeter_api, arduino):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.name = name
        self.twitter_api = tweeter_api
        self.arduino = arduino

    def run(self):
        while update:
            now = time.time()
            if now - self.twitter_api.last_update >= 60000:
                self.twitter_api.update_followers_count()
                self.arduino.send_followers_count(
                    '@' + self.twitter_api.get_user('1648488114').name + str(self.twitter_api.nb_followers))
