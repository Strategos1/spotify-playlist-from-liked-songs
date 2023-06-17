import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import dotenv_values

config = dotenv_values("c:\\Users\\Jara Doktor\\Downloads\\.env")


def create_new_playlist_from_liked_songs():
    # Set up Spotify API credentials
    client_id = config['client_id'] # <--- Change this to your client ID
    client_secret = config['client_secret'] # <--- Change this to your client secret
    redirect_uri = "http://localhost:8888/callback" # <--- Change this to your redirect URI. You can use http://localhost:8888/callback for testing purposes.
    scope = "playlist-modify-private user-library-read" # <--- Don't change this

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                   client_secret=client_secret,
                                                   redirect_uri=redirect_uri,
                                                   scope=scope))

    user = sp.current_user()
    user_id = user["id"]

    tracks = []
    offset = 0
    limit = 50 # This is maximum limit for the Spotify API. Don't change this.
    while True:
        liked_songs = sp.current_user_saved_tracks(limit=limit, offset=offset)
        if len(liked_songs["items"]) == 0:
            break
        tracks.extend([track["track"]["uri"] for track in liked_songs["items"]])
        offset += limit

    # Create a new playlist
    playlist_name = "Playlist name"  # <--- Change this to the name of your new playlist
    playlist_description = "Playlist description"  # <--- Change this to the description of your new playlist
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False, description=playlist_description)
    playlist_id = playlist["id"]

    track_chunks = [tracks[i:i+100] for i in range(0, len(tracks), 100)]
    for chunk in track_chunks:
        sp.playlist_add_items(playlist_id=playlist_id, items=chunk)

    print(f"New playlist '{playlist_name}' created with {len(tracks)} songs.")


# Call the function to create a new playlist from the "Liked Songs" playlist
create_new_playlist_from_liked_songs()