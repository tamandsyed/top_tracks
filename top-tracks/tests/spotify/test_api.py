import os
from collections import namedtuple
from unittest.mock import MagicMock
from http import HTTPStatus

import requests
import pytest


from spotify import api
from spotify import auth
from spotify import exceptions


Response = namedtuple('Response', ['status_code', 'json'])

def test_make_artist_search_request(monkeypatch):
    """
    it makes the correct get request
    """
    expected_response = Response(HTTPStatus.OK, lambda:{})
    mock_get_method = MagicMock(return_value=expected_response)
    monkeypatch.setattr(requests, 'get', mock_get_method)
    monkeypatch.setattr(auth, 'get_auth_token', lambda: {'access_token':'access_token'})

    artist = 'queen'
    response = api._make_artist_search_request(artist)

    mock_get_method.assert_called_once_with(
        api._search_url(),
        params={'q': artist, 'type': 'artist'},
        headers={'Authorization': 'Bearer access_token'}
    )

    assert response == expected_response.json()



def test_make_top_tracks_request_for_artist(monkeypatch):
    """
    it makes the correct get request
    """
    expected_response = Response(HTTPStatus.OK, lambda:{})
    mock_get_method = MagicMock(return_value=expected_response)
    monkeypatch.setattr(requests, 'get', mock_get_method)
    monkeypatch.setattr(auth, 'get_auth_token', lambda: {'access_token':'access_token'})

    artist_id = 'quee123'
    country_code = 'GB'
    response =  api._make_top_tracks_request_for_artist(artist_id, country_code)

    mock_get_method.assert_called_once_with(
        api._top_tracks_url(artist_id),
        params={'country': country_code},
        headers={'Authorization': 'Bearer access_token'}
    )

    assert response == expected_response.json()

def test_find_artist_id_raises(monkeypatch):
    """
    it raises if artist not found
    """
    search_result = {
        'artists': {
            'items': [{'name': 'queen', 'id': 'queen123'}]
        }
    }
    monkeypatch.setattr(api, '_make_artist_search_request', lambda artist: search_result)

    with pytest.raises(exceptions.ArtistNotFound) as excinfo:
        api._find_artist_id('bohemia')

    assert str(excinfo.value) == 'unable to find artist with name bohemia'

def test_find_artist_id(monkeypatch):
    """
    it returns artist id when artist found
    """
    search_result = {
        'artists': {
            'items': [{'name': 'queen', 'id': 'queen123'}]
        }
    }
    monkeypatch.setattr(api, '_make_artist_search_request', lambda artist: search_result)

    artist_id=api._find_artist_id('queen')

    assert artist_id == 'queen123'

