import os

import pytest

from spotify import auth
from spotify import exceptions

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
