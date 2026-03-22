import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import re
import os

CLIENT_ID     = "9bc0caa1c1f448fb9eb1d5c8e997bcc2"
CLIENT_SECRET = "314a7abf0e204bd79959fc19b8c5556a"
REDIRECT_URI  = "http://127.0.0.1:8080"

def authenticate():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id     = CLIENT_ID,
        client_secret = CLIENT_SECRET,
        redirect_uri  = REDIRECT_URI,
        scope         = " ".join([
            "user-read-recently-played",
            "user-top-read"
        ])
    ))
    print(f"✅ Logged in as: "
          f"{sp.current_user()['display_name']}")
    return sp

def fetch_recent_tracks(sp, limit=50):
    print("\nFetching recently played tracks...")
    results = sp.current_user_recently_played(limit=limit)
    tracks  = []
    for item in results['items']:
        track = item['track']
        tracks.append({
            'track_name' : track['name'],
            'artist'     : track['artists'][0]['name'],
            'played_at'  : item['played_at'],
            'source'     : 'recent'
        })
    df = pd.DataFrame(tracks)
    print(f"✅ Fetched {len(df)} recently played tracks")
    return df

def fetch_top_tracks(sp):
    print("\nFetching top tracks...")
    tracks      = []
    time_ranges = ['short_term',
                   'medium_term',
                   'long_term']
    for time_range in time_ranges:
        results = sp.current_user_top_tracks(
            limit      = 50,
            time_range = time_range
        )
        for item in results['items']:
            tracks.append({
                'track_name' : item['name'],
                'artist'     : item['artists'][0]['name'],
                'played_at'  : None,
                'source'     : f'top_{time_range}'
            })
    df = pd.DataFrame(tracks).drop_duplicates(
                                subset='track_name')
    print(f"✅ Fetched {len(df)} unique top tracks")
    return df

def match_audio_features(df_tracks, df_kaggle):
    print("\nMatching audio features from dataset...")
    matched   = []
    not_found = 0

    for _, row in df_tracks.iterrows():
        track_name = str(row['track_name'])

        # Exact match
        results = df_kaggle[
            df_kaggle['track_name'].str.lower() ==
            track_name.lower()
        ]

        # Partial match
        if len(results) == 0:
            try:
                safe_name = re.escape(track_name[:15])
                results   = df_kaggle[
                    df_kaggle['track_name'].str.contains(
                        safe_name,
                        case=False,
                        na=False,
                        regex=True
                    )
                ]
            except:
                results = pd.DataFrame()

        if len(results) > 0:
            best = results.iloc[0]
            matched.append({
                'track_name'      : track_name,
                'artist'          : row['artist'],
                'played_at'       : row['played_at'],
                'source'          : row['source'],
                'tempo'           : best['tempo'],
                'energy'          : best['energy'],
                'valence'         : best['valence'],
                'danceability'    : best['danceability'],
                'acousticness'    : best['acousticness'],
                'instrumentalness': best['instrumentalness'],
                'loudness'        : best['loudness'],
                'speechiness'     : best['speechiness']
            })
        else:
            not_found += 1

    df_matched = pd.DataFrame(matched)
    print(f"✅ Matched  : {len(df_matched)} tracks")
    print(f"❌ Not found: {not_found} tracks")
    return df_matched

if __name__ == "__main__":
    sp        = authenticate()
    df_recent = fetch_recent_tracks(sp)
    df_top    = fetch_top_tracks(sp)

    df_tracks = pd.concat(
        [df_recent, df_top], ignore_index=True
    ).drop_duplicates(subset='track_name')

    print(f"\n📊 Total unique tracks: {len(df_tracks)}")

    df_kaggle = pd.read_csv('data/dataset.csv',
                             encoding='utf-8')
    print(f"✅ Kaggle dataset: {len(df_kaggle)} songs")

    df_final = match_audio_features(df_tracks, df_kaggle)

    df_final.to_csv('data/spotify_data.csv', index=False)

    print(f"\n{'='*45}")
    print(f"✅ Saved to data/spotify_data.csv")
    print(f"Total tracks  : {len(df_final)}")
    print(f"\n🎵 Sample:")
    print(df_final[['track_name', 'artist',
                    'tempo', 'energy',
                    'valence', 'source']].head(10))