import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dataclasses import dataclass
import sqlite3


@dataclass
class Album:
    album_name: str = ""
    artist_name: str = ""
    release_date: str = ""
    number_of_songs: str = ""


"""
Link: https://developer.spotify.com/dashboard/
Go to link and login/create account
Create new App
Note Client ID
Click dropdown menu to get Client Secret 
"""

YEAR: str = "2001"  # Year for the top albums that you want to get
Num_OF_REQUESTS_FROM_API: int = 750  # total (pre-filtered) number of results that you want to get from the API
BATCH_SIZE: int = 50  # Number of results that will come back per request. NOTE: Spotify has a limit of 50 results / request
DB_NAME: str = "Top Albums"  # Name of SQLITE DB that will store the results
TABLE_NAME: str = "Year: 2001"  # Name of the table that results will be saved to
CLIENT_ID = ""  # Your Client ID
CLIENT_SECRET = ""  # Your secret key

albums = []

client_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)

sp_access = spotipy.Spotify(
    client_credentials_manager=client_manager
)
counter = 0
while counter <= Num_OF_REQUESTS_FROM_API:
    albums_from_2001 = sp_access.search(q=f"year: {YEAR}", type='album', limit=BATCH_SIZE, offset=counter)
    for i in albums_from_2001['albums']['items']:
        album_object = Album()
        album_object.artist_name = i['artists'][0]['name']
        album_object.album_name = i['name']
        album_object.release_date = i['release_date']
        album_object.number_of_songs = i['total_tracks']
        albums.append(album_object)
    counter += 50

df = pd.DataFrame(albums)
df['release_date'] = pd.to_datetime(df['release_date'], infer_datetime_format=True)
filtered_df = df.loc[df['release_date'].dt.year == int(YEAR)]
filtered_df = filtered_df.reset_index(drop=True)

cxn = sqlite3.connect(DB_NAME)
filtered_df.to_sql(TABLE_NAME, con=cxn, if_exists="replace")
