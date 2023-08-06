import requests
from hitbtcapi.constants import *


class HitBtcClient:
    def __init__(self, apikey, apisecret):
        self.API_KEY = apikey
        self.API_SECRET = apisecret

    def api_get_query(self, endpoint):
        session = requests.session()
        session.auth = (self.API_KEY, self.API_SECRET)

        response = session.get(BASE_API_URL + API_VERSION + "/" + endpoint).json()

        return response

    def api_post_query(self, endpoint, params):
        session = requests.session()
        session.auth = (self.API_KEY, self.API_SECRET)

        response = session.post(BASE_API_URL + API_VERSION + "/" + endpoint, params).json()

        return response
