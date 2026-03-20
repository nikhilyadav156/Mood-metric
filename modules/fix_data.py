import pandas as pd
import os

LOG_FILE     = 'data/productivity_log.csv'
SPOTIFY_FILE = 'data/dataset.csv'

def fix_and_merge():
    print("Loading files...")
    df_log     = pd.read_csv(LOG_FILE,encoding='latin1')
    df_spotify = pd.read_csv(SPOTIFY_FILE,encoding='utf-8')

    print(f"Sessions loaded  : {len(df_log)}")
    print(f"Columns in log   : {df_log.columns.tolist()}")

    # Store audio features for each session
    rows = []

    for i, row in enumerate(df_log.itertuples()):
        print(f"\nProcessing session {i+1}/{len(df_log)}")

        session_features = []

        # Check each song column
        for song_col in ['song1', 'song2', 'song3']:
            song_val = getattr(row, song_col, None)

            # Skip empty songs
            if pd.isna(song_val) or str(song_val).strip() == '':
                continue

            # Extract song name before the dash
            try:
                song_name = str(song_val).split(' - ')[0].strip()
            except:
                continue

            # Search in spotify dataset
            matches = df_spotify[
                df_spotify['track_name'].str.contains(
                    song_name, case=False, na=False
                )
            ]

            if len(matches) > 0:
                song_features = matches.iloc[0]
                session_features.append({
                    'tempo'           : song_features['tempo'],
                    'energy'          : song_features['energy'],
                    'valence'         : song_features['valence'],
                    'instrumentalness': song_features['instrumentalness'],
                    'danceability'    : song_features['danceability'],
                    'acousticness'    : song_features['acousticness']
                })
                print(f"  ✅ Found: {song_name}")
            else:
                print(f"  ❌ Not found: {song_name}")

        # Calculate averages for this session
        if session_features:
            avg_tempo  = sum(s['tempo']
                         for s in session_features) / len(session_features)
            avg_energy = sum(s['energy']
                         for s in session_features) / len(session_features)
            avg_val    = sum(s['valence']
                         for s in session_features) / len(session_features)
            avg_inst   = sum(s['instrumentalness']
                         for s in session_features) / len(session_features)
            avg_dance  = sum(s['danceability']
                         for s in session_features) / len(session_features)
            avg_acoust = sum(s['acousticness']
                         for s in session_features) / len(session_features)
        else:
            avg_tempo  = avg_energy = avg_val   = 0
            avg_inst   = avg_dance  = avg_acoust = 0

        rows.append({
            'date'               : row.date,
            'start_time'         : row.start_time,
            'end_time'           : row.end_time,
            'task_type'          : row.task_type,
            'song1'              : row.song1,
            'avg_tempo'          : round(avg_tempo,  2),
            'avg_energy'         : round(avg_energy, 3),
            'avg_valence'        : round(avg_val,    3),
            'avg_instrumentalness': round(avg_inst,  3),
            'avg_danceability'   : round(avg_dance,  3),
            'avg_acousticness'   : round(avg_acoust, 3),
            'productivity_score' : row.productivity_score,
            'focus_score'        : row.focus_score
        })

    # Create final merged dataframe
    df_merged = pd.DataFrame(rows)

    # Save
    df_merged.to_csv('data/merged_data.csv', index=False)

    print(f"\n{'='*45}")
    print(f"✅ Merged data saved to data/merged_data.csv")
    print(f"Total sessions : {len(df_merged)}")
    print(f"\nSample:")
    print(df_merged[['date', 'task_type', 'avg_tempo',
                     'avg_energy', 'avg_valence',
                     'productivity_score']].head())

if __name__ == "__main__":
    fix_and_merge()