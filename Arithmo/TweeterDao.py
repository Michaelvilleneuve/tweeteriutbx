import time
import twitter


class TweeterDAO:
    def __init__(self):
        self._api = None
        self.last_update = 0
        self.nb_followers = 0

    def set_api(self, consumer_key, consumer_secret, access_token, access_token_secret):
        if self._api is None:
            api = twitter.Api(consumer_key=consumer_key,
                              consumer_secret=consumer_secret,
                              access_token_key=access_token,
                              access_token_secret=access_token_secret)
            self._api = api

    def get_followers_count(self):
        """
        Update count of followers for the user account
        """
        status = self._api.GetFollowerIDs()
        self.nb_followers = len(status)

    def update_followers_count(self):
            now = time.time()
            if now - self.last_update >= 2000 * 60:
                # update nb followers
                self.get_followers_count()
                self.last_update = now
            else:
                self.nb_followers += 1

    def get_friends(self):
        """
        Return list of friends for the user account
        :return:
        """
        return self._api.GetFriends()

    def get_stream(self):
        return self._api.GetUserStream()
