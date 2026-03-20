import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble        import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics         import r2_score, mean_absolute_error
import pickle
import os

MERGED_FILE = 'data/merged_data.csv'

def load_data():
    df = pd.read_csv(MERGED_FILE, encoding='utf-8')
    df['productivity_score'] = pd.to_numeric(
        df['productivity_score'], errors='coerce')
    df = df.dropna(subset=['productivity_score'])
    print(f"✅ Loaded {len(df)} sessions")
    return df

def train_model(df):
    print("\n🤖 Training ML Model...")

    features = ['avg_tempo', 'avg_energy',
                'avg_valence', 'avg_instrumentalness',
                'avg_danceability', 'avg_acousticness']

    X = df[features]
    y = df['productivity_score']

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train model
    model = RandomForestRegressor(
        n_estimators = 100,
        random_state = 42
    )
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    r2     = r2_score(y_test, y_pred)
    mae    = mean_absolute_error(y_test, y_pred)

    print(f"\n📊 Model Performance:")
    print(f"   R² Score : {r2:.2f}")
    print(f"   MAE      : {mae:.2f}")

    # Feature importance
    importance = pd.Series(
        model.feature_importances_,
        index = [f.replace('avg_', '').title()
                 for f in features]
    ).sort_values(ascending=True)

    print(f"\n🏆 Feature Importance:")
    for feat, val in importance.items():
        bar = "█" * int(val * 50)
        print(f"   {feat.ljust(20)}: {val:.3f} {bar}")

    # Plot feature importance
    plt.figure(figsize=(8, 5))
    importance.plot(kind='barh',
                    color='steelblue',
                    edgecolor='white')
    plt.title('Feature Importance for Productivity Prediction',
              fontsize=13)
    plt.xlabel('Importance Score')
    plt.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    plt.savefig('data/feature_importance.png', dpi=150)
    plt.show()
    print("✅ Saved feature_importance.png")

    # Save model
    with open('data/model.pkl', 'wb') as f:
        pickle.dump(model, f)
    print("✅ Model saved to data/model.pkl")

    return model, features

def predict_productivity(model, features,
                         tempo, energy, valence,
                         instrumentalness,
                         danceability, acousticness):
    input_data = pd.DataFrame([{
        'avg_tempo'           : tempo,
        'avg_energy'          : energy,
        'avg_valence'         : valence,
        'avg_instrumentalness': instrumentalness,
        'avg_danceability'    : danceability,
        'avg_acousticness'    : acousticness
    }])

    prediction = model.predict(input_data)[0]
    return round(prediction, 1)

def recommend_songs(df_spotify, task_type, model):
    print(f"\n🎵 Recommended songs for {task_type}:")

    # Define ideal audio profiles per task
    profiles = {
        'coding' : {'avg_instrumentalness': 0.7,
                    'avg_energy'          : 0.5,
                    'avg_tempo'           : 100},
        'reading': {'avg_instrumentalness': 0.8,
                    'avg_energy'          : 0.3,
                    'avg_tempo'           : 75},
        'writing': {'avg_instrumentalness': 0.6,
                    'avg_energy'          : 0.4,
                    'avg_tempo'           : 90},
        'design' : {'avg_instrumentalness': 0.5,
                    'avg_energy'          : 0.6,
                    'avg_tempo'           : 110},
        'other'  : {'avg_instrumentalness': 0.5,
                    'avg_energy'          : 0.5,
                    'avg_tempo'           : 95}
    }

    profile = profiles.get(task_type,
                           profiles['other'])

    # Filter songs matching profile
    mask = (
        (df_spotify['instrumentalness'] >=
         profile['avg_instrumentalness'] - 0.3) &
        (df_spotify['energy'] >=
         profile['avg_energy'] - 0.2) &
        (df_spotify['energy'] <=
         profile['avg_energy'] + 0.2) &
        (df_spotify['tempo'] >=
         profile['avg_tempo'] - 30) &
        (df_spotify['tempo'] <=
         profile['avg_tempo'] + 30)
    )

    recommended = df_spotify[mask][
        ['track_name', 'artists',
         'tempo', 'energy',
         'instrumentalness', 'valence']
    ].drop_duplicates(
        subset='track_name'
    ).head(10)

    print(recommended.to_string(index=False))
    return recommended

if __name__ == "__main__":
    # Load data
    df         = load_data()
    df_spotify = pd.read_csv('data/dataset.csv',
                              encoding='utf-8')

    # Train model
    model, features = train_model(df)

    # Test prediction
    print("\n🔮 Test Prediction:")
    print("   Input: instrumental music, low energy, 90 BPM")
    score = predict_productivity(
        model, features,
        tempo            = 90,
        energy           = 0.3,
        valence          = 0.4,
        instrumentalness = 0.8,
        danceability     = 0.4,
        acousticness     = 0.5
    )
    print(f"   Predicted Productivity: {score}/10")

    # Recommendations
    recommend_songs(df_spotify, 'coding', model)

    print("\n✅ Model training complete!")