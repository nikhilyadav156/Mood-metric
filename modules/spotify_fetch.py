import pandas as pd

def load_spotify_dataset():
    print("Loading Spotify dataset...")
    df = pd.read_csv('data/dataset.csv')

    print("Actual columns in your CSV:")
    print(df.columns.tolist())

    # Print first 2 rows
    print("\nFirst 2 rows:")
    print(df.head(2))

    # Keep only relevant columns
    df = df[['track_id', 'track_name', 'artists',
                 'tempo', 'energy', 'valence',
                 'danceability', 'acousticness',
                 'instrumentalness', 'loudness',
                 'speechiness', 'popularity']]

    # Clean column name
    df = df.rename(columns={'artists': 'artist'})
    df = df.dropna()

    print(f"✅ Loaded {len(df)} songs")
    return df

def search_song(df, song_name):
    # Search for a song by name
    results = df[df['track_name'].str.contains(
                 song_name, case=False, na=False)]
    return results[['track_name', 'artist', 'tempo',
                    'energy', 'valence',
                    'instrumentalness']].head(5)

if __name__ == "__main__":
    df = load_spotify_dataset()

    print("\nSample songs:")
    print(df[['track_name', 'artist',
              'tempo', 'energy', 'valence']].head(10))

    print("\nSearch test:")
    print(search_song(df, "Believer"))