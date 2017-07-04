import twitter


class TweeterDAO:
    def __init__(self):
        self._api = None

    def get_api(self, consumer_key, consumer_secret, access_token, access_token_secret):
        if self._api is None:
            api = twitter.Api(consumer_key=consumer_key,
                              consumer_secret=consumer_secret,
                              access_token_key=access_token,
                              access_token_secret=access_token_secret)
            self._api = api
        return self._api

    def followers_count(self):
        """
        Return count of followers for the user account
        :return: int
        """
        status = self._api.GetFollowerIDs()
        return len(status)

    def get_friends(self):
        """
        Return list of friends for the user account
        :return:
        """
        return self._api.GetFriends()
