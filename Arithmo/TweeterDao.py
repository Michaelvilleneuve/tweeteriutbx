import os
import time

import logging
import twitter
from twitter import TwitterError

log_level = os.environ.get("LOGLEVEL") or 'NOTSET'

# Create logger
Log = logging.getLogger('TweeterAPI')
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


class TweeterDAO:
    def __init__(self):
        self._api = None
        self.last_update = 0
        self.nb_followers = 0
        self._user = None

    def set_api(self, consumer_key, consumer_secret, access_token, access_token_secret, user_id):
        if self._api is None:
            api = twitter.Api(consumer_key=consumer_key,
                              consumer_secret=consumer_secret,
                              access_token_key=access_token,
                              access_token_secret=access_token_secret)
            self._api = api
            self.get_user(user_id)

    def get_followers_count(self):
        """
        Update count of followers for the user account
        """
        status = self._api.GetFollowerIDs()
        Log.debug("Nb followers : " + str(len(status)))
        self.nb_followers = len(status)

    def update_followers_count(self):
        now = time.time()
        if now - self.last_update >= 1000 * 60:
            # update nb followers
            self.get_followers_count()
            self.last_update = now

    def get_friends(self):
        """
        Return list of friends for the user account
        :return:
        """
        return self._api.GetFriends()

    def get_stream(self):
        return self._api.GetUserStream()

    def get_user(self, user_id):
        if self._user is None:
            self._user = self._api.GetUser(user_id)
            Log.debug(self._user)
        return self._user

    def send_message(self, message):
        try:
            self._api.PostUpdate(message)
        except TwitterError as e:
            Log.error(e)
