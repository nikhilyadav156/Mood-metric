import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pickle
import os

# ── Fix File Paths ───────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

# ── Load Data Functions ──────────────────────────────────────
@st.cache_data
def load_data():
    path = os.path.join(DATA_DIR, 'merged_data.csv')
    df   = pd.read_csv(path, encoding='utf-8')
    df['productivity_score'] = pd.to_numeric(
        df['productivity_score'], errors='coerce')
    df['focus_score'] = pd.to_numeric(
        df['focus_score'], errors='coerce')
    return df.dropna(subset=['productivity_score'])

@st.cache_data
def load_spotify():
    path = os.path.join(DATA_DIR, 'dataset.csv')
    return pd.read_csv(path, encoding='utf-8')

@st.cache_resource
def load_model():
    path = os.path.join(DATA_DIR, 'model.pkl')
    with open(path, 'rb') as f:
        return pickle.load(f)

# ── Actually Call the Functions ──────────────────────────────
df         = load_data()
df_spotify = load_spotify()
model      = load_model()

# ── Page Config ──────────────────────────────────────────────
st.set_page_config(
    page_title = "🎵 MoodMetric",
    page_icon  = "🎵",
    layout     = "wide"
)

# ── Header ───────────────────────────────────────────────────
st.title("🎵 MoodMetric")
st.markdown("#### *Discover what music makes you most productive*")
st.divider()

# ── Metrics Row ──────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sessions",
            len(df))
col2.metric("Avg Productivity",
            f"{df['productivity_score'].mean():.1f}/10")
col3.metric("Avg Focus",
            f"{df['focus_score'].mean():.1f}/10")
col4.metric("Best Task",
            df.groupby('task_type')[
            'productivity_score'].mean().idxmax().title())

st.divider()

# ── Tabs ─────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Analysis",
    "🎵 Recommendations",
    "🔮 Predict",
    "📋 Sessions"
])

# ════════════════════════════════════════════════════════════
# TAB 1 — ANALYSIS
# ════════════════════════════════════════════════════════════
with tab1:
    st.subheader("📊 How Music Affects Your Productivity")

    col1, col2 = st.columns(2)

    with col1:
        fig = px.scatter(
            df,
            x         = 'avg_energy',
            y         = 'productivity_score',
            color     = 'task_type',
            size      = 'avg_tempo',
            title     = 'Energy vs Productivity Score',
            labels    = {
                'avg_energy'        : 'Average Energy',
                'productivity_score': 'Productivity Score',
                'task_type'         : 'Task Type'
            },
            trendline = 'ols'
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.scatter(
            df,
            x         = 'avg_valence',
            y         = 'productivity_score',
            color     = 'task_type',
            title     = 'Valence (Happiness) vs Productivity',
            labels    = {
                'avg_valence'       : 'Average Valence',
                'productivity_score': 'Productivity Score'
            },
            trendline = 'ols'
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Productivity by Task Type
    st.subheader("📈 Productivity by Task Type")
    task_avg = df.groupby('task_type').agg(
        Productivity = ('productivity_score', 'mean'),
        Focus        = ('focus_score',        'mean')
    ).reset_index()

    fig3 = px.bar(
        task_avg,
        x       = 'task_type',
        y       = ['Productivity', 'Focus'],
        barmode = 'group',
        title   = 'Avg Productivity & Focus by Task',
        labels  = {'task_type': 'Task Type',
                   'value'    : 'Score (out of 10)'},
        color_discrete_map = {
            'Productivity': 'steelblue',
            'Focus'       : 'coral'
        }
    )
    fig3.update_layout(yaxis_range=[0, 10])
    st.plotly_chart(fig3, use_container_width=True)

    # Feature Importance
    st.subheader("🏆 Most Impactful Audio Features")
    features = ['avg_tempo', 'avg_energy', 'avg_valence',
                'avg_instrumentalness', 'avg_danceability',
                'avg_acousticness']

    importance_df = pd.DataFrame({
        'Feature'   : [f.replace('avg_', '').title()
                       for f in features],
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=True)

    fig4 = px.bar(
        importance_df,
        x           = 'Importance',
        y           = 'Feature',
        orientation = 'h',
        title       = 'Feature Importance for YOUR Productivity',
        color       = 'Importance',
        color_continuous_scale = 'Blues'
    )
    st.plotly_chart(fig4, use_container_width=True)

# ════════════════════════════════════════════════════════════
# TAB 2 — RECOMMENDATIONS
# ════════════════════════════════════════════════════════════
with tab2:
    st.subheader("🎵 Get Your Productivity Playlist")

    task      = st.selectbox(
        "What are you about to work on?",
        ["coding", "reading", "writing", "design", "other"]
    )
    num_songs = st.slider("Number of songs", 5, 20, 10)

    if st.button("🎵 Generate Playlist"):
        profiles = {
            'coding' : {'instrumentalness': (0.4, 1.0),
                        'energy'          : (0.3, 0.7),
                        'tempo'           : (80,  120)},
            'reading': {'instrumentalness': (0.6, 1.0),
                        'energy'          : (0.1, 0.5),
                        'tempo'           : (60,   95)},
            'writing': {'instrumentalness': (0.3, 0.9),
                        'energy'          : (0.2, 0.6),
                        'tempo'           : (70,  110)},
            'design' : {'instrumentalness': (0.3, 0.8),
                        'energy'          : (0.4, 0.8),
                        'tempo'           : (90,  130)},
            'other'  : {'instrumentalness': (0.3, 0.9),
                        'energy'          : (0.3, 0.7),
                        'tempo'           : (75,  115)}
        }

        p    = profiles[task]
        mask = (
            df_spotify['instrumentalness'].between(
                *p['instrumentalness']) &
            df_spotify['energy'].between(
                *p['energy']) &
            df_spotify['tempo'].between(
                *p['tempo'])
        )

        playlist = df_spotify[mask][
            ['track_name', 'artists', 'tempo',
             'energy', 'valence', 'instrumentalness']
        ].drop_duplicates(
            subset='track_name'
        ).head(num_songs)

        st.success(f"✅ Found {len(playlist)} songs"
                   f" for {task}!")
        st.dataframe(playlist, use_container_width=True)

# ════════════════════════════════════════════════════════════
# TAB 3 — PREDICT
# ════════════════════════════════════════════════════════════
with tab3:
    st.subheader("🔮 Predict Your Productivity Score")
    st.markdown("Adjust the sliders and predict your"
                " productivity:")

    col1, col2 = st.columns(2)

    with col1:
        tempo            = st.slider("Tempo (BPM)",
                                      60, 200, 100)
        energy           = st.slider("Energy",
                                      0.0, 1.0, 0.5)
        valence          = st.slider("Valence (Mood)",
                                      0.0, 1.0, 0.5)
    with col2:
        instrumentalness = st.slider("Instrumentalness",
                                      0.0, 1.0, 0.5)
        danceability     = st.slider("Danceability",
                                      0.0, 1.0, 0.5)
        acousticness     = st.slider("Acousticness",
                                      0.0, 1.0, 0.5)

    if st.button("🔮 Predict"):
        input_df = pd.DataFrame([{
            'avg_tempo'           : tempo,
            'avg_energy'          : energy,
            'avg_valence'         : valence,
            'avg_instrumentalness': instrumentalness,
            'avg_danceability'    : danceability,
            'avg_acousticness'    : acousticness
        }])

        prediction = model.predict(input_df)[0]
        prediction = round(min(max(prediction, 1), 10), 1)

        if prediction >= 7:
            color = "🟢"
        elif prediction >= 5:
            color = "🟡"
        else:
            color = "🔴"

        st.markdown(f"### {color} Predicted Productivity:"
                    f" **{prediction}/10**")

        fig = go.Figure(go.Indicator(
            mode  = "gauge+number",
            value = prediction,
            title = {'text': "Productivity Score"},
            gauge = {
                'axis' : {'range': [0, 10]},
                'bar'  : {'color': "steelblue"},
                'steps': [
                    {'range': [0, 4],  'color': '#ffcccc'},
                    {'range': [4, 7],  'color': '#fff3cc'},
                    {'range': [7, 10], 'color': '#ccffcc'}
                ]
            }
        ))
        st.plotly_chart(fig, use_container_width=True)

# ════════════════════════════════════════════════════════════
# TAB 4 — SESSIONS
# ════════════════════════════════════════════════════════════
with tab4:
    st.subheader("📋 All Logged Sessions")

    tasks    = ['All'] + df['task_type'].unique().tolist()
    selected = st.selectbox("Filter by Task", tasks)

    filtered = df if selected == 'All' else \
               df[df['task_type'] == selected]

    st.dataframe(filtered[[
        'date', 'task_type', 'song1',
        'avg_tempo', 'avg_energy',
        'avg_valence', 'productivity_score',
        'focus_score'
    ]], use_container_width=True)

    fig = px.line(
        filtered.reset_index(),
        x       = 'date',
        y       = 'productivity_score',
        title   = 'Your Productivity Over Time',
        markers = True,
        color   = 'task_type'
    )
    fig.update_layout(yaxis_range=[0, 10])
    st.plotly_chart(fig, use_container_width=True)