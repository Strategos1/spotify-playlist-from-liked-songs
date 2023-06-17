import spotipy
from spotipy.oauth2 import SpotifyOAuth

def create_new_playlist_from_liked_songs():
    # Set up Spotify API credentials
    client_id = "8873d590ad17422bb28fe09dec41482a"
    client_secret = "9dac31b19a234988ac706ec029166c70"
    redirect_uri = "http://localhost:8888/callback"
    scope = "playlist-modify-private user-library-read"

    # Create a Spotify API client
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                   client_secret=client_secret,
                                                   redirect_uri=redirect_uri,
                                                   scope=scope))

    # Get user information
    user = sp.current_user()
    user_id = user["id"]

    # Get all tracks from the "Liked Songs" playlist
    tracks = []
    offset = 0
    limit = 50  # Maximum limit per request
    while True:
        liked_songs = sp.current_user_saved_tracks(limit=limit, offset=offset)
        if len(liked_songs["items"]) == 0:
            break
        tracks.extend([track["track"]["uri"] for track in liked_songs["items"]])
        offset += limit

    # Create a new playlist
    playlist_name = "Put new name for your playlisy"
    playlist_description = "This playlist was created from Liked Songs."
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False, description=playlist_description)
    playlist_id = playlist["id"]

    # Add tracks to the new playlist with pagination
    track_chunks = [tracks[i:i+100] for i in range(0, len(tracks), 100)]
    for chunk in track_chunks:
        sp.playlist_add_items(playlist_id=playlist_id, items=chunk)

    print(f"New playlist '{playlist_name}' created with {len(tracks)} songs.")

# Call the function to create a new playlist from the "Liked Songs" playlist
create_new_playlist_from_liked_songs()