A simple command line application to request the top tracks for an artist in a region from the Spotify API

# Requirements
Python 3.6 or greater

# Setup
Create a spotify developer account and request a `spotify client id` and `spotify client secret`. Once you have the client id and secret,
set their values to the `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET` environment variables respectively.

Install the package requirements - ideally in a virtual environment - by executing `pip3 install -r requirements.txt`

# Running the App
`python3 top_tracks.py [artist_name] [region]`


