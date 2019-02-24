import os

import requests

from . import exceptions

SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/api/token'

def get_auth_token():
    pass

def _get_client_credentials_from_env():
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    if client_id is None or client_secret is None:
        raise exceptions.SpotifyAuthError("missing client credentials")
    return client_id, client_secret

def _base64_encode_client_credentials():
    pass
