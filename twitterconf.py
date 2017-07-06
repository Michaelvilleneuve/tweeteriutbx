import arithmo

class Twitterconf:
    def __init__(self):
        twitterdb = arithmo.get_twitter()
        if twitterdb['owner_id'] is not None:
            self.owner_id = twitterdb['owner_id']
        else:
            self.owner_id = ""

        if twitterdb['token_access'] is not None:
            self.token_access = twitterdb['token_access']
        else:
            self.token_access = ""

        if twitterdb['token_access_secret'] is not None:
            self.token_access_secret = twitterdb['token_access_secret']
        else:
            self.token_access_secret = ""

        if twitterdb['consumer_key'] is not None:
            self.consumer_key = twitterdb['consumer_key']
        else:
            self.consumer_key = ""

        if twitterdb['consumer_secret'] is not None:
            self.consumer_secret = twitterdb['consumer_secret']
        else:
            self.consumer_secret = ""

    def get_owner_id(self):
        return self.owner_id

    def set_owner_id(self, v):
        self.owner_id = v

    def get_token_access(self):
        return self.token_access

    def set_token_access(self, v):
        self.token_access = v

    def get_token_access_secret(self):
        return self.token_access_secret

    def set_token_access_secret(self, v):
        self.token_access_secret = v

    def get_consumer_key(self):
        return self.consumer_key

    def set_consumer_key(self, v):
        self.consumer_key = v

    def get_consumer_key_secret(self):
        return self.consumer_key_secret

    def set_consumer_key_secret(self, v):
        self.consumer_key_secret = v
