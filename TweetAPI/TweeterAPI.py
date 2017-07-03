import base64
import hmac
import hashlib

from TweetAPI import APP_CONSUMER_SECRET, RESOURCE_URL, APP_CONSUMER_KEY


class TweeterAPI:
    def __init__(self):
        pass

    def validateCallbackURL(self, crc_token):
        sha256_hash_digest = hmac.new(b'APP_CONSUMER_SECRET', msg=b'crc_token', digestmod=hashlib.sha256).digest()

        response = {
            'response_token': 'sha256=' + str(base64.b64encode(sha256_hash_digest), 'utf-8')
        }

        return response

    def registerWebhook(self):
        url = RESOURCE_URL + 'account_activity/webhooks.json'

    def __get_auth_token(self):
        bearer_token_credential = APP_CONSUMER_KEY + ':' + APP_CONSUMER_SECRET
        return str(base64.b64encode(bearer_token_credential), 'utf-8')
