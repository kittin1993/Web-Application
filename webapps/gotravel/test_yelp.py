from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import io,json

with io.open('config_secret.json') as cred:
    creds = json.load(cred)
    auth = Oauth1Authenticator(**creds)
    client = Client(auth)

params1 = {
    'term': 'hotel',
    'lang': 'fr',
    'limit': 3,
    'sort': 2,
}

params2 = {
    'term': 'restaurant',
    'lang': 'fr',
    'limit': 3,
    'sort': 2,
}


def get_hotel(location):
	response = client.search(location, **params1)
	return response.businesses

def get_restaurant(location):
	response = client.search(location, **params2)
	return response.businesses