# Spotify_ETL_Pipeline
ETL process using Spotifys API. 

## Step 1: Extract Data
1. Data is extracted by using the Spotipy module. Documentation and source code cane be found here: https://github.com/plamere/spotipy.
2. This library simplifies the request made to Spotify's API, and allows for seamless use.
3. Each JSON response is loaded into a dataclass that is then added to a list.

## Step 2: Clean(Transform) the Data
1. Load the list of dataclass instances into a pandas dataframe.
2. The data from Spotify needs to be scrubbed, we filter the data so that the requested year is in the "release_date" column.

## Step 3: Load the Data:
1. Create a local SQLITE db file.
2. Write the scrubbed dataframe to the SQLITE DB.
