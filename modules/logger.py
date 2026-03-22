import csv
import os
import pandas as pd
from datetime import datetime

LOG_FILE     = 'data/productivity_log.csv'
SPOTIFY_FILE = 'data/spotify_data.csv'

def initialize_log():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'date', 'start_time', 'end_time',
                'task_type',
                'song1', 'song2', 'song3',
                'productivity_score',
                'focus_score', 'notes'
            ])
        print("✅ Log file created")

def search_song(df, query):
    results = df[df['track_name'].str.contains(
                 query, case=False, na=False)]
    return results[['track_name', 'artist',
                    'tempo', 'energy',
                    'valence', 'instrumentalness',
                    'danceability', 'acousticness']].head(5)

def pick_song(df, song_number):
    while True:
        query = input(f"\n  Search Song {song_number}"
                      f" (or Enter to skip): ")
        if not query:
            return None

        results = search_song(df, query)

        if len(results) == 0:
            print("  ❌ Not found. Try different name.")
            continue

        print(f"\n  Results:")
        for i, (_, row) in enumerate(results.iterrows()):
            print(f"  {i+1}. {row['track_name']}"
                  f" — {row['artist']}")

        choice = input("  Pick number (0 to search again): ")
        if choice == '0':
            continue

        try:
            chosen = results.iloc[int(choice)-1]
            # Return ONLY the song name string
            song_name = (f"{chosen['track_name']}"
                        f" - {chosen['artist']}")
            print(f"  ✅ Added: {song_name}")
            return song_name
        except:
            print("  Invalid. Try again.")

def log_session():
    initialize_log()
    df_spotify = pd.read_csv(SPOTIFY_FILE, encoding='utf-8')

    print("\n" + "="*45)
    print("      🎵 MOODMETRIC SESSION LOGGER")
    print("="*45)

    date = input("\nDate (YYYY-MM-DD) or Enter for today: ")
    if not date:
        date = datetime.now().strftime('%Y-%m-%d')

    start_time = input("Start time (HH:MM): ")
    end_time   = input("End time   (HH:MM): ")

    print("\nTask: coding/reading/writing/design/other")
    task_type  = input("Task type: ").lower()

    print("\n🎵 Enter up to 3 songs you listened to:")

    # Save only song name strings
    song1 = pick_song(df_spotify, 1) or ""
    song2 = pick_song(df_spotify, 2) or ""
    song3 = pick_song(df_spotify, 3) or ""

    print()
    prod_score = input("Productivity score (1-10): ")
    focus      = input("Focus level        (1-10): ")
    notes      = input("Notes (optional)         : ")

    with open(LOG_FILE, 'a', newline='',
              encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            date, start_time, end_time,
            task_type,
            song1, song2, song3,    # only song names saved here
            prod_score, focus, notes
        ])

    print(f"\n{'='*45}")
    print(f"✅ Session logged successfully!")
    print(f"   Date  : {date}")
    print(f"   Task  : {task_type}")
    print(f"   Song1 : {song1}")
    print(f"   Song2 : {song2}")
    print(f"   Song3 : {song3}")
    print(f"   Score : {prod_score}/10")
    print(f"{'='*45}")

def view_sessions():
    if not os.path.exists(LOG_FILE):
        print("No sessions logged yet!")
        return
    df = pd.read_csv(LOG_FILE, encoding='utf-8')
    print(f"\n📊 Total sessions: {len(df)}")
    print(f"Avg productivity : "
          f"{pd.to_numeric(df['productivity_score'], errors='coerce').mean():.1f}/10")
    print(f"Avg focus        : "
          f"{pd.to_numeric(df['focus_score'], errors='coerce').mean():.1f}/10")
    print("\nAll Sessions:")
    print(df[['date', 'task_type', 'song1',
              'productivity_score',
              'focus_score']].to_string(index=False))

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
            print("Goodbye! 🎵")
            break
        else:
            print("Enter 1, 2 or 3.")