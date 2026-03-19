import csv
import os
import pandas as pd
from datetime import datetime

LOG_FILE     = 'data/productivity_log.csv'
SPOTIFY_FILE = 'data/dataset.csv'

# ── Create log file with headers ────────────────────────────
def initialize_log():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'date', 'start_time', 'end_time',
                'task_type',
                'song1', 'song2', 'song3',
                'avg_tempo', 'avg_energy',
                'avg_valence', 'avg_instrumentalness',
                'avg_danceability', 'avg_acousticness',
                'productivity_score',
                'focus_score', 'notes'
            ])
        print("✅ Log file created")

# ── Search song from dataset ─────────────────────────────────
def search_song(df, query):
    results = df[df['track_name'].str.contains(
                 query, case=False, na=False)]
    results = results[['track_name', 'artists',
                        'tempo', 'energy',
                        'valence',
                        'instrumentalness',
                        'danceability',
                        'acousticness']].head(5)
    return results

# ── Pick a song interactively ────────────────────────────────
def pick_song(df, song_number):
    while True:
        query = input(f"\n  Search Song {song_number} "
                      f"(or Enter to skip): ")
        if not query:
            return None

        results = search_song(df, query)

        if len(results) == 0:
            print("  ❌ No song found. Try different name.")
            continue

        print(f"\n  Results for '{query}':")
        for i, (_, row) in enumerate(results.iterrows()):
            print(f"  {i+1}. {row['track_name']}"
                  f" — {row['artists']}"
                  f" | Tempo:{row['tempo']:.0f}"
                  f" Energy:{row['energy']:.2f}"
                  f" Valence:{row['valence']:.2f}")

        choice = input("\n  Pick number (0 to search again): ")

        if choice == '0':
            continue

        try:
            chosen = results.iloc[int(choice)-1]
            print(f"  ✅ Added: {chosen['track_name']}"
                  f" — {chosen['artists']}")
            return chosen
        except:
            print("  Invalid choice. Try again.")

# ── Log a session ────────────────────────────────────────────
def log_session():
    initialize_log()
    df_spotify = pd.read_csv(SPOTIFY_FILE, encoding='latin1')

    print("\n" + "="*45)
    print("      🎵 MOODMETRIC SESSION LOGGER")
    print("="*45)

    # Date and time
    date = input("\nDate (YYYY-MM-DD) or Enter for today: ")
    if not date:
        date = datetime.now().strftime('%Y-%m-%d')

    start_time = input("Start time (HH:MM): ")
    end_time   = input("End time   (HH:MM): ")

    # Task type
    print("\nTask types: coding / reading / writing"
          " / design / other")
    task_type  = input("Task type: ").lower()

    # Songs
    print("\n🎵 Enter songs you listened to"
          " during this session (up to 3):")
    songs      = []
    song_data  = []

    for i in range(3):
        song = pick_song(df_spotify, i+1)
        if song is not None:
            songs.append(f"{song['track_name']}"
                         f" - {song['artists']}")
            song_data.append(song)
        else:
            break

    # Pad songs list
    while len(songs) < 3:
        songs.append("")

    # Calculate average audio features
    if song_data:
        avg_tempo   = sum(s['tempo']
                      for s in song_data) / len(song_data)
        avg_energy  = sum(s['energy']
                      for s in song_data) / len(song_data)
        avg_valence = sum(s['valence']
                      for s in song_data) / len(song_data)
        avg_inst    = sum(s['instrumentalness']
                      for s in song_data) / len(song_data)
        avg_dance   = sum(s['danceability']
                      for s in song_data) / len(song_data)
        avg_acoust  = sum(s['acousticness']
                      for s in song_data) / len(song_data)
    else:
        avg_tempo = avg_energy = avg_valence = 0
        avg_inst  = avg_dance  = avg_acoust  = 0

    # Scores
    print()
    prod_score = input("Productivity score (1-10): ")
    focus      = input("Focus level        (1-10): ")
    notes      = input("Notes (optional)         : ")

    # Save to CSV
    with open(LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            date, start_time, end_time,
            task_type,
            songs[0], songs[1], songs[2],
            round(avg_tempo,   2),
            round(avg_energy,  3),
            round(avg_valence, 3),
            round(avg_inst,    3),
            round(avg_dance,   3),
            round(avg_acoust,  3),
            prod_score, focus, notes
        ])

    print(f"\n{'='*45}")
    print(f"✅ Session logged!")
    print(f"   Date      : {date}")
    print(f"   Time      : {start_time} → {end_time}")
    print(f"   Task      : {task_type}")
    print(f"   Songs     : {len(song_data)} logged")
    print(f"   Avg Tempo : {avg_tempo:.0f} BPM")
    print(f"   Avg Energy: {avg_energy:.2f}")
    print(f"   Prod Score: {prod_score}/10")
    print(f"{'='*45}")

# ── View all sessions ────────────────────────────────────────
def view_sessions():
    if not os.path.exists(LOG_FILE):
        print("No sessions logged yet!")
        return
    df = pd.read_csv(LOG_FILE, encoding='latin1')
    print(f"\n📊 Total sessions logged: {len(df)}")
    print(f"Average productivity   : "
          f"{pd.to_numeric(df['productivity_score'], errors='coerce').mean():.1f}/10")
    print(f"Average focus          : "
          f"{pd.to_numeric(df['focus_score'], errors='coerce').mean():.1f}/10")
    print("\nAll Sessions:")
    print(df.to_string(index=False))

# ── Main menu ────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n🎵 Welcome to MoodMetric Logger")

    while True:
        print("\n1. Log new session")
        print("2. View all sessions")
        print("3. Exit")
        choice = input("\nChoice: ")

        if choice == '1':
            log_session()
        elif choice == '2':
            view_sessions()
        elif choice == '3':
            print("\nGoodbye! Keep logging! 🎵")
            break
        else:
            print("Invalid choice. Enter 1, 2 or 3.")