# 🎵 MoodMetric — Music × Productivity Analyzer

> **Does the music you listen to actually make you more productive?**
> MoodMetric answers this question scientifically using your real Spotify data.

<br>

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Spotify](https://img.shields.io/badge/Spotify_API-1DB954?style=for-the-badge&logo=spotify&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

---

## 📌 Table of Contents

- [What is MoodMetric](#-what-is-moodmetric)
- [How It Works](#-how-it-works)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Usage](#-usage)
- [Screenshots](#-screenshots)
- [Dataset](#-dataset)
- [Results](#-results)
- [Authors](#-authors)
- [License](#-license)

---

## 🎯 What is MoodMetric

MoodMetric is a full end-to-end **personal data science project** that
analyzes the relationship between your Spotify listening habits and your
personal productivity. It collects real audio feature data from the
Spotify API, combines it with self-reported productivity scores from
your daily work sessions, and uses machine learning to uncover patterns
unique to **you**.

The project culminates in an interactive **Streamlit dashboard** with a
Spotify-inspired dark UI that lets you explore your music-productivity
patterns, generate personalized focus playlists, and predict your
productivity score for any music profile.

> Built as a **B.Tech 6th Semester Data Science Minor Project**

---

## ⚙️ How It Works

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│   Spotify API          Self-Reported Sessions           │
│   (Real tracks)   +    (productivity_log.csv)           │
│        ↓                        ↓                       │
│   Audio Features           Work Session Data            │
│   tempo, energy,           date, task type,             │
│   valence, etc.            score out of 10              │
│        ↓                        ↓                       │
│           ┌──────────────────────┐                      │
│           │   Data Merging       │                      │
│           │   (fix_data.py)      │                      │
│           └──────────┬───────────┘                      │
│                      ↓                                  │
│           ┌──────────────────────┐                      │
│           │  Correlation &       │                      │
│           │  Feature Analysis    │                      │
│           │  (analysis.py)       │                      │
│           └──────────┬───────────┘                      │
│                      ↓                                  │
│           ┌──────────────────────┐                      │
│           │  Random Forest       │                      │
│           │  ML Model            │                      │
│           │  (model.py)          │                      │
│           └──────────┬───────────┘                      │
│                      ↓                                  │
│           ┌──────────────────────┐                      │
│           │  Streamlit Dashboard │                      │
│           │  (app.py)            │                      │
│           └──────────────────────┘                      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎵 **Spotify Integration** | Fetches your real recently played and top tracks via Spotify Web API |
| 📝 **Session Logger** | CLI tool to log daily work sessions with productivity scores |
| 📊 **Correlation Analysis** | Scatter plots, heatmaps, and radar charts showing music-productivity patterns |
| 🤖 **ML Prediction** | Random Forest model predicts your productivity score from audio features |
| 🎯 **Feature Importance** | Identifies which audio feature impacts YOUR productivity the most |
| 🎧 **Playlist Generator** | Recommends songs from 114K dataset based on your task type |
| 🔮 **Real-time Prediction** | Adjust sliders and get instant productivity score prediction |
| 📈 **Session History** | Track and filter all your logged sessions with visual timeline |
| 🌙 **Spotify-inspired UI** | Dark theme dashboard with green accent colors |

---

## 🛠 Tech Stack

| Category | Technology | Purpose |
|---|---|---|
| **Language** | Python 3.11+ | Core programming |
| **API** | Spotify Web API + Spotipy | Fetch real listening data |
| **Data** | Pandas, NumPy | Data processing and merging |
| **ML** | Scikit-learn (Random Forest) | Productivity prediction model |
| **Visualization** | Plotly, Matplotlib, Seaborn | Interactive charts |
| **Dashboard** | Streamlit | Web application UI |
| **Dataset** | Kaggle Spotify Tracks (114K songs) | Audio feature lookup |
| **Auth** | python-dotenv | Secure API key management |

---

## 📁 Project Structure

```
MoodMetric/
│
├── app.py                      # Streamlit dashboard (main UI)
│
├── modules/
│   ├── spotify_fetch.py        # Fetch tracks from Spotify API
│   ├── logger.py               # CLI productivity session logger
│   ├── fix_data.py             # Merge Spotify + session data
│   ├── analysis.py             # EDA, correlation plots
│   └── model.py                # Train Random Forest model
│
├── data/
│   ├── dataset.csv             # Kaggle Spotify tracks (114K songs)
│   ├── productivity_log.csv    # Your logged work sessions
│   ├── spotify_data.csv        # Fetched Spotify tracks
│   ├── merged_data.csv         # Final merged dataset
│   └── model.pkl               # Saved trained model
│
├── .env                        # Spotify API keys (not committed)
├── .gitignore                  # Excludes .env, dataset, model
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or above
- A Spotify account (free or premium)
- A Spotify Developer account

### 1. Clone the Repository

```bash
git clone https://github.com/YourUsername/MoodMetric.git
cd MoodMetric
```

### 2. Create Virtual Environment

```bash
# Create
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Spotify API

```
1. Go to https://developer.spotify.com/dashboard
2. Create a new app → name it "MoodMetric"
3. Set Redirect URI → http://localhost:8080
4. Copy your Client ID and Client Secret
```

### 5. Configure Environment Variables

Create a `.env` file in the root folder:

```env
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
SPOTIFY_REDIRECT_URI=http://localhost:8080
```

### 6. Download the Dataset

```
1. Go to https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset
2. Download and extract
3. Rename the CSV file to dataset.csv
4. Place it inside the data/ folder
```

---

## 📖 Usage

### Step 1 — Fetch Your Spotify Data

```bash
python modules/spotify_fetch.py
```

A browser window will open. Log in to Spotify and allow access.
Your tracks will be saved to `data/spotify_data.csv`.

### Step 2 — Log Your Work Sessions Daily

```bash
python modules/logger.py
```

After every study or work session run this and fill in:
- Start and end time
- Task type (coding, reading, writing, etc.)
- Up to 3 songs you listened to
- Productivity score (1-10)
- Focus score (1-10)

> Collect at least **20 sessions** for meaningful analysis.

### Step 3 — Merge and Process Data

```bash
python modules/fix_data.py
```

### Step 4 — Run Analysis and Generate Graphs

```bash
python modules/analysis.py
```

### Step 5 — Train the ML Model

```bash
python modules/model.py
```

### Step 6 — Launch the Dashboard

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501` 🎉

---

## 📸 Screenshots

### Hero Dashboard
> Spotify-inspired dark UI with live stats and audio profile

### Analytics Tab
> Scatter plots, feature importance, radar chart, and tempo distribution

### Playlist Generator
> Task-based playlist with BPM, energy, mood, and type tags

### Predict Tab
> Adjust audio sliders → get instant productivity score with gauge

### History Tab
> Session timeline with color-coded productivity scores

---

## 📦 Dataset

| Dataset | Source | Size |
|---|---|---|
| Spotify Tracks Dataset | [Kaggle — maharshipandya](https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset) | 114,000 songs |
| Personal Session Logs | Self-collected via logger.py | 22+ sessions |
| Spotify Listening History | Spotify Web API | Real-time |

**Audio Features Used:**

| Feature | Range | Description |
|---|---|---|
| `tempo` | 0–250 BPM | Speed of the track |
| `energy` | 0.0–1.0 | Intensity and activity level |
| `valence` | 0.0–1.0 | Musical positivity |
| `danceability` | 0.0–1.0 | Suitability for dancing |
| `instrumentalness` | 0.0–1.0 | Absence of vocals |
| `acousticness` | 0.0–1.0 | Acoustic vs electronic |
| `loudness` | -60–0 dB | Overall loudness |
| `speechiness` | 0.0–1.0 | Spoken word presence |

---

## 📊 Results

```
Model           : Random Forest Regressor
Sessions Used   : 22
Features Used   : 6 audio features
Most Impactful  : Energy (highest feature importance)
```

> Note: Model accuracy improves significantly with more logged sessions.
> We recommend logging 50+ sessions for best results.

---

## 🔧 Requirements

```
streamlit
spotipy
pandas
numpy
matplotlib
seaborn
scikit-learn
plotly
python-dotenv
statsmodels
ipykernel
```

Generate `requirements.txt` with:

```bash
pip freeze > requirements.txt
```

---

## 👥 Authors

**Nikhil Yadav**
- 🎓 B.Tech CSE (Data Science) — 6th Semester
- 💼 [LinkedIn](https://linkedin.com/in/yourprofile)
- 🐙 [GitHub](https://github.com/yourusername)

**Adarsh Tiwari**
- 🎓 B.Tech CSE (Data Science) — 6th Semester
- 💼 [LinkedIn](https://linkedin.com/in/adarshtiwari)
- 🐙 [GitHub](https://github.com/adarshtiwari)

> Both authors independently built this project from scratch
> as part of their B.Tech 6th Semester Data Science Minor Project.

---

## 📄 License

This project is licensed under the MIT License.
See the [LICENSE](LICENSE) file for details.

```
MIT License — free to use, modify and distribute
with proper attribution.
```

---

## 🙏 Acknowledgements

- [Spotify for Developers](https://developer.spotify.com/) — for the Web API
- [Spotipy](https://spotipy.readthedocs.io/) — Python wrapper for Spotify API
- [Kaggle — maharshipandya](https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset) — Spotify Tracks Dataset
- [Streamlit](https://streamlit.io/) — for the amazing dashboard framework
- [Plotly](https://plotly.com/) — for interactive visualizations

---

<div align="center">
  <br>
  <strong>Built with ❤️ by Nikhil Yadav & Adarsh Tiwari</strong>
  <br>
  <em>B.Tech 6th Semester — Data Science Minor Project — 2026</em>
  <br><br>
  ⭐ Star this repo if you found it useful!
</div>
