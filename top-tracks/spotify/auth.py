import os
import base64
import http

import requests

from . import exceptions

SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/api/token'

def get_auth_token():
    client_id, client_secret = _get_client_credentials_from_env()
    return _make_token_request(
        _base64_encode_client_credentials(client_id, client_secret)
    )

def _get_client_credentials_from_env():
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    if client_id is None or client_secret is None:
        raise exceptions.SpotifyAuthError("missing client credentials")
    return client_id, client_secret

def _base64_encode_client_credentials(client_id, client_secret):
    return base64.urlsafe_b64encode(f'{client_id}:{client_secret}'.encode())

def _make_token_request(encoded_credentials):
    response = requests.post(
        SPOTIFY_AUTH_URL,
        headers={'Authorization': f'Basic {encoded_credentials.decode()}'},
        data={'grant_type': 'client_credentials'}
    )
    if response.status_code == http.HTTPStatus.OK:
        return response.json()
    else:
        raise exceptions.SpotifyAuthError(response.json()['error'])




