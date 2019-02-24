import os
import base64
from unittest.mock import MagicMock
from collections import namedtuple

import requests
import pytest

from spotify import auth
from spotify import exceptions


def test_get_auth_token(initialize_client_credentials, monkeypatch):
    Response = namedtuple('Response', ['status_code', 'json'])
    auth_json = {
        'access_token': 'access_token',
        'token_type': 'Bearer',
        'expires_in': '90',
        'scope': ""
    }

    monkeypatch.setattr(
        requests,
        'post',
        lambda url, headers, data: Response(status_code=200, json=lambda: auth_json)
    )

    response = auth.get_auth_token()

    assert response == auth_json

def test_get_client_credentials_from_env(initialize_client_credentials):
    """
    it retrieves client credentials from environment
    """
    expected_client_id = initialize_client_credentials[0]
    expected_client_secret = initialize_client_credentials[1]

    client_id, client_secret = auth._get_client_credentials_from_env()

    assert client_id == expected_client_id
    assert client_secret == expected_client_secret

def test_get_client_crendentials_from_env_raises_on_missing_client_id(initialize_client_secret_only):
    """
    it raises exception when spotify client_id not found in environment
    """
    with pytest.raises(exceptions.SpotifyAuthError) as excinfo:
         auth._get_client_credentials_from_env()

    assert str(excinfo.value) == 'missing client credentials'

def test_get_client_crendentials_from_env_raises_on_missing_client_secret(initialize_client_id_only):
    """
    it raises exception when spotify client secret  not found in environment
    """
    with pytest.raises(exceptions.SpotifyAuthError) as excinfo:
         auth._get_client_credentials_from_env()

    assert str(excinfo.value) == 'missing client credentials'

def test_client_credentials_base64_encoding(initialize_client_credentials):
    """
    it correctly base64 encodes client credentials
    """
    client_id, client_secret = initialize_client_credentials

    # TODO: Code Smell. Re implements function logic
    expected_encoded_value = base64.urlsafe_b64encode(f'{client_id}:{client_secret}'.encode())
    encoded = auth._base64_encode_client_credentials(client_id, client_secret)

    assert encoded == expected_encoded_value

def test_make_token_request_makes_correct_post_request(initialize_client_credentials, monkeypatch):
    """
    it makes post request with correct headers and request body
    """
    Response = namedtuple('Response', ['status_code', 'json'])
    mock_post_method = MagicMock(return_value=Response(status_code=200, json=lambda:None))
    monkeypatch.setattr(requests, 'post', mock_post_method)

    encoded_credentials = auth._base64_encode_client_credentials(*initialize_client_credentials)
    auth._make_token_request(encoded_credentials)

    mock_post_method.assert_called_once_with(
        auth.SPOTIFY_AUTH_URL,
        headers={'Authorization': 'Basic Y2xpZW50X2lkOmNsaWVudF9zZWNyZXQ='},
        data={'grant_type': 'client_credentials'}
    )

def test_make_token_request_handles_200_response(monkeypatch):
    """
    it correctly parses json response from a successful auth token request
    """
    Response = namedtuple('Response', ['status_code', 'json'])
    auth_json = {
        'access_token': 'access_token',
        'token_type': 'Bearer',
        'expires_in': '90',
        'scope': ""
    }

    monkeypatch.setattr(
        requests,
        'post',
        lambda url, headers, data: Response(status_code=200, json=lambda: auth_json)
    )

    response = auth._make_token_request(b'encoded_credentials')

    assert response == auth_json

def test_make_token_request_raises_on_non_200_responses(monkeypatch):
    """
    it raises SpotifyAuthError on non 200 responses with correct error message
    """
    Response = namedtuple('Response', ['status_code', 'json'])
    error_json = {
        'error': 'error_message'
    }

    monkeypatch.setattr(
        requests,
        'post',
        lambda url, headers, data: Response(status_code=401, json=lambda: error_json)
    )

    with pytest.raises(exceptions.SpotifyAuthError) as excinfo:
        auth._make_token_request(b'encoded_credentials')

    assert str(excinfo.value) == 'error_message'


@pytest.fixture()
def initialize_client_credentials():
    os.environ['SPOTIFY_CLIENT_ID'] = 'client_id'
    os.environ['SPOTIFY_CLIENT_SECRET'] = 'client_secret'

    yield os.environ['SPOTIFY_CLIENT_ID'], os.environ['SPOTIFY_CLIENT_SECRET']

    del  os.environ['SPOTIFY_CLIENT_ID']
    del  os.environ['SPOTIFY_CLIENT_SECRET']


@pytest.fixture()
def initialize_client_id_only():
    os.environ['SPOTIFY_CLIENT_ID'] = 'client_id'

    yield

    del  os.environ['SPOTIFY_CLIENT_ID']

@pytest.fixture()
def initialize_client_secret_only():
    os.environ['SPOTIFY_CLIENT_SECRET'] = 'client_secret'

    yield


    del  os.environ['SPOTIFY_CLIENT_SECRET']
