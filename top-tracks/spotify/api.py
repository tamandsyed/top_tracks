import requests

from . import auth
from . import exceptions

BASE_URL = 'http://api.spotify.com/v1'

def top_tracks(artist, country_code):
    return _make_top_tracks_request_for_artist(
        _find_artist_id(artist),
        country_code
    )

def _find_artist_id(artist):
    response =  _make_artist_search_request(artist)
    result =  list(
        filter(
            lambda x: x['name'].lower() == artist.lower(),
            response['artists']['items']
        )
    )
    if result:
        return result[0]['id']

    raise exceptions.ArtistNotFound(f'unable to find artist with name {artist}')

def _make_top_tracks_request_for_artist(artist_id, country_code):
    access_token = auth.get_auth_token()['access_token']
    response = requests.get(
        _top_tracks_url(artist_id),
        headers={'Authorization': f'Bearer {access_token}'},
        params={'country': country_code}
    )
    return response.json()

def _make_artist_search_request(artist):
    access_token = auth.get_auth_token()['access_token']
    response = requests.get(
        _search_url(),
        params={
            'q': artist,
            'type': 'artist'
        },
        headers={'Authorization': f'Bearer {access_token}'},
    )
    return response.json()

def _search_url():
    return f'{BASE_URL}/search'

def _top_tracks_url(artist_id):
    return f'{BASE_URL}/artists/{artist_id}/top-tracks'
