import requests
from hitbtcapi.constants import *


class HitBtcClient:
    def __init__(self, apikey, apisecret):
        self.API_KEY = apikey
        self.API_SECRET = apisecret

        self.session = requests.session()
        self.session.auth = (self.API_KEY, self.API_SECRET)

    def api_get_query(self, endpoint):
        response = self.session.get(BASE_API_URL + API_VERSION + "/" + endpoint).json()
        return response

    def api_post_query(self, endpoint, params):
        response = self.session.post(BASE_API_URL + API_VERSION + "/" + endpoint, params).json()
        return response
