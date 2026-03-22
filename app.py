import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pickle
import os

# ── Page Config ──────────────────────────────────────────────
st.set_page_config(
    page_title = "MoodMetric",
    page_icon  = "🎵",
    layout     = "wide",
    initial_sidebar_state = "expanded"
)

# ── Custom CSS ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: #0a0a0f;
    color: #e8e8f0;
}

.stApp {
    background: linear-gradient(
        135deg,
        #0a0a0f 0%,
        #0d0d1a 50%,
        #0a0f0d 100%
    );
}

/* ── Hide default streamlit elements ── */
#MainMenu, footer, header {visibility: hidden;}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg, #0d0d1a, #0a0a0f
    ) !important;
    border-right: 1px solid #1a1a2e;
}

[data-testid="stSidebar"] * {
    color: #e8e8f0 !important;
}

/* ── Hero Header ── */
.hero {
    text-align  : center;
    padding     : 3rem 0 2rem 0;
    position    : relative;
}

.hero-title {
    font-family : 'Syne', sans-serif;
    font-size   : 5rem;
    font-weight : 800;
    background  : linear-gradient(
        135deg, #00ff88, #00d4ff, #7c3aed
    );
    -webkit-background-clip : text;
    -webkit-text-fill-color : transparent;
    background-clip         : text;
    letter-spacing          : -2px;
    line-height             : 1;
    margin-bottom           : 0.5rem;
}

.hero-sub {
    font-family : 'Space Mono', monospace;
    font-size   : 0.85rem;
    color       : #4a4a6a;
    letter-spacing: 4px;
    text-transform: uppercase;
}

/* ── Metric Cards ── */
.metric-card {
    background    : linear-gradient(
        135deg,
        rgba(0,255,136,0.05),
        rgba(0,212,255,0.05)
    );
    border        : 1px solid rgba(0,255,136,0.15);
    border-radius : 16px;
    padding       : 1.5rem;
    text-align    : center;
    transition    : all 0.3s ease;
    position      : relative;
    overflow      : hidden;
}

.metric-card::before {
    content       : '';
    position      : absolute;
    top           : 0; left: 0;
    right         : 0; height: 2px;
    background    : linear-gradient(
        90deg, #00ff88, #00d4ff
    );
}

.metric-card:hover {
    border-color  : rgba(0,255,136,0.4);
    transform     : translateY(-2px);
}

.metric-value {
    font-family   : 'Syne', sans-serif;
    font-size     : 2.5rem;
    font-weight   : 800;
    color         : #00ff88;
    line-height   : 1;
}

.metric-label {
    font-family   : 'Space Mono', monospace;
    font-size     : 0.7rem;
    color         : #4a4a6a;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top    : 0.5rem;
}

/* ── Section Headers ── */
.section-header {
    font-family   : 'Syne', sans-serif;
    font-size     : 1.8rem;
    font-weight   : 800;
    color         : #e8e8f0;
    margin        : 2rem 0 1rem 0;
    display       : flex;
    align-items   : center;
    gap           : 0.75rem;
}

.section-header::after {
    content       : '';
    flex          : 1;
    height        : 1px;
    background    : linear-gradient(
        90deg,
        rgba(0,255,136,0.3),
        transparent
    );
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background    : rgba(255,255,255,0.02);
    border-radius : 12px;
    padding       : 4px;
    border        : 1px solid rgba(255,255,255,0.05);
    gap           : 4px;
}

.stTabs [data-baseweb="tab"] {
    background    : transparent;
    border-radius : 10px;
    color         : #4a4a6a;
    font-family   : 'Space Mono', monospace;
    font-size     : 0.75rem;
    letter-spacing: 1px;
    padding       : 0.6rem 1.2rem;
    border        : none;
    transition    : all 0.2s;
}

.stTabs [aria-selected="true"] {
    background    : linear-gradient(
        135deg,
        rgba(0,255,136,0.15),
        rgba(0,212,255,0.15)
    ) !important;
    color         : #00ff88 !important;
    border        : 1px solid rgba(0,255,136,0.3) !important;
}

/* ── Buttons ── */
.stButton > button {
    background    : linear-gradient(
        135deg, #00ff88, #00d4ff
    );
    color         : #0a0a0f;
    font-family   : 'Space Mono', monospace;
    font-weight   : 700;
    font-size     : 0.8rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    border        : none;
    border-radius : 10px;
    padding       : 0.75rem 2rem;
    transition    : all 0.3s;
    width         : 100%;
}

.stButton > button:hover {
    transform     : translateY(-2px);
    box-shadow    : 0 8px 25px rgba(0,255,136,0.3);
}

/* ── Sliders ── */
.stSlider [data-testid="stThumbValue"] {
    color         : #00ff88;
    font-family   : 'Space Mono', monospace;
}

/* ── Selectbox ── */
.stSelectbox [data-baseweb="select"] {
    background    : rgba(255,255,255,0.03);
    border        : 1px solid rgba(255,255,255,0.1);
    border-radius : 10px;
}

/* ── Dataframe ── */
.stDataFrame {
    border        : 1px solid rgba(0,255,136,0.1);
    border-radius : 12px;
    overflow      : hidden;
}

/* ── Song Card ── */
.song-card {
    background    : rgba(255,255,255,0.03);
    border        : 1px solid rgba(255,255,255,0.07);
    border-radius : 12px;
    padding       : 1rem 1.25rem;
    margin        : 0.4rem 0;
    display       : flex;
    justify-content: space-between;
    align-items   : center;
    transition    : all 0.2s;
}

.song-card:hover {
    border-color  : rgba(0,255,136,0.3);
    background    : rgba(0,255,136,0.05);
}

/* ── Insight Box ── */
.insight-box {
    background    : linear-gradient(
        135deg,
        rgba(124,58,237,0.1),
        rgba(0,212,255,0.1)
    );
    border        : 1px solid rgba(124,58,237,0.3);
    border-radius : 16px;
    padding       : 1.5rem;
    margin        : 1rem 0;
}

/* ── Prediction Result ── */
.pred-result {
    text-align    : center;
    padding       : 2rem;
    background    : linear-gradient(
        135deg,
        rgba(0,255,136,0.05),
        rgba(0,212,255,0.05)
    );
    border-radius : 20px;
    border        : 1px solid rgba(0,255,136,0.2);
}

.pred-number {
    font-family   : 'Syne', sans-serif;
    font-size     : 6rem;
    font-weight   : 800;
    background    : linear-gradient(
        135deg, #00ff88, #00d4ff
    );
    -webkit-background-clip : text;
    -webkit-text-fill-color : transparent;
    line-height   : 1;
}

/* ── Divider ── */
.custom-divider {
    height        : 1px;
    background    : linear-gradient(
        90deg,
        transparent,
        rgba(0,255,136,0.3),
        transparent
    );
    margin        : 2rem 0;
}
</style>
""", unsafe_allow_html=True)

# ── File Paths ───────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

# ── Load Data ────────────────────────────────────────────────
@st.cache_data
def load_data():
    path = os.path.join(DATA_DIR, 'merged_data.csv')
    df   = pd.read_csv(path)
    for col in ['productivity_score', 'focus_score',
                'avg_tempo', 'avg_energy',
                'avg_valence', 'avg_instrumentalness',
                'avg_danceability', 'avg_acousticness']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col],
                                     errors='coerce')
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

df         = load_data()
df_spotify = load_spotify()
model      = load_model()

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0'>
        <div style='font-size:3rem'>🎵</div>
        <div style='font-family:Syne,sans-serif;
                    font-size:1.5rem;
                    font-weight:800;
                    background:linear-gradient(135deg,#00ff88,#00d4ff);
                    -webkit-background-clip:text;
                    -webkit-text-fill-color:transparent;'>
            MoodMetric
        </div>
        <div style='font-family:Space Mono,monospace;
                    font-size:0.65rem;
                    color:#4a4a6a;
                    letter-spacing:3px;'>
            MUSIC × PRODUCTIVITY
        </div>
    </div>
    <hr style='border-color:rgba(255,255,255,0.05);'>
    """, unsafe_allow_html=True)

    st.markdown("#### 🎛️ Filters")
    task_filter = st.multiselect(
        "Task Types",
        options = df['task_type'].unique().tolist(),
        default = df['task_type'].unique().tolist()
    )

    st.markdown("<div class='custom-divider'></div>",
                unsafe_allow_html=True)

    # Stats in sidebar
    avg_prod  = df['productivity_score'].mean()
    avg_focus = df['focus_score'].mean()

    st.markdown(f"""
    <div style='font-family:Space Mono,monospace;
                font-size:0.75rem; color:#4a4a6a;
                letter-spacing:2px;
                text-transform:uppercase;
                margin-bottom:1rem;'>
        QUICK STATS
    </div>
    <div style='display:flex;
                flex-direction:column; gap:0.75rem;'>
        <div class='metric-card'>
            <div class='metric-value'>{len(df)}</div>
            <div class='metric-label'>Sessions</div>
        </div>
        <div class='metric-card'>
            <div class='metric-value'
                 style='color:#00d4ff;'>
                 {avg_prod:.1f}
            </div>
            <div class='metric-label'>Avg Productivity</div>
        </div>
        <div class='metric-card'>
            <div class='metric-value'
                 style='color:#7c3aed;'>
                 {avg_focus:.1f}
            </div>
            <div class='metric-label'>Avg Focus</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Filter Data ──────────────────────────────────────────────
df_filtered = df[df['task_type'].isin(task_filter)]

# ── Hero Section ─────────────────────────────────────────────
st.markdown("""
<div class='hero'>
    <div class='hero-title'>MoodMetric</div>
    <div class='hero-sub'>
        Discover what music makes you most productive
    </div>
</div>
""", unsafe_allow_html=True)

# ── Top Metrics ──────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
best_task = df_filtered.groupby('task_type')[
    'productivity_score'].mean().idxmax()
best_feature_idx = model.feature_importances_.argmax()
features_list    = ['Tempo', 'Energy', 'Valence',
                    'Instrumentalness',
                    'Danceability', 'Acousticness']
best_feature = features_list[best_feature_idx] \
               if best_feature_idx < len(features_list) \
               else "Energy"

for col, val, label, color in [
    (c1, len(df_filtered), "Sessions Logged",  "#00ff88"),
    (c2, f"{df_filtered['productivity_score'].mean():.1f}/10",
         "Avg Productivity", "#00d4ff"),
    (c3, f"{df_filtered['focus_score'].mean():.1f}/10",
         "Avg Focus Score",  "#7c3aed"),
    (c4, best_task.title(), "Best Task Type",  "#ff6b6b")
]:
    col.markdown(f"""
    <div class='metric-card'>
        <div class='metric-value'
             style='color:{color};
                    font-size:2rem;'>
             {val}
        </div>
        <div class='metric-label'>{label}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div class='custom-divider'></div>",
            unsafe_allow_html=True)

# ── Tabs ─────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊  Analysis",
    "🎵  Playlist",
    "🔮  Predict",
    "📋  Sessions"
])

# ════════════════════════════════════════
# TAB 1 — ANALYSIS
# ════════════════════════════════════════
with tab1:
    st.markdown("""
    <div class='section-header'>
        📊 Your Music × Productivity Profile
    </div>
    """, unsafe_allow_html=True)

    # Insight box
    top_corr_feature = "Energy"
    st.markdown(f"""
    <div class='insight-box'>
        <div style='font-family:Space Mono,monospace;
                    font-size:0.7rem; color:#7c3aed;
                    letter-spacing:2px;
                    text-transform:uppercase;
                    margin-bottom:0.5rem;'>
            🧠 KEY INSIGHT
        </div>
        <div style='font-family:Syne,sans-serif;
                    font-size:1.1rem; font-weight:600;'>
            Your most impactful audio feature is
            <span style='color:#00ff88;'>
                {best_feature}
            </span>
            — this correlates most strongly with
            your productivity score.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        fig = px.scatter(
            df_filtered,
            x         = 'avg_energy',
            y         = 'productivity_score',
            color     = 'task_type',
            size      = 'avg_tempo',
            trendline = 'ols',
            title     = 'Energy vs Productivity',
            labels    = {
                'avg_energy'        : 'Energy Level',
                'productivity_score': 'Productivity',
                'task_type'         : 'Task'
            },
            color_discrete_sequence = [
                '#00ff88','#00d4ff',
                '#7c3aed','#ff6b6b','#ffd93d'
            ]
        )
        fig.update_layout(
            plot_bgcolor  = 'rgba(0,0,0,0)',
            paper_bgcolor = 'rgba(0,0,0,0)',
            font_color    = '#e8e8f0',
            title_font    = dict(family='Syne',
                                  size=16),
            legend        = dict(
                bgcolor='rgba(255,255,255,0.03)',
                bordercolor='rgba(255,255,255,0.1)'
            )
        )
        fig.update_xaxes(
            gridcolor='rgba(255,255,255,0.05)',
            zerolinecolor='rgba(255,255,255,0.1)'
        )
        fig.update_yaxes(
            gridcolor='rgba(255,255,255,0.05)',
            zerolinecolor='rgba(255,255,255,0.1)'
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.scatter(
            df_filtered,
            x         = 'avg_valence',
            y         = 'productivity_score',
            color     = 'task_type',
            size      = 'avg_instrumentalness',
            trendline = 'ols',
            title     = 'Valence vs Productivity',
            labels    = {
                'avg_valence'       : 'Valence (Mood)',
                'productivity_score': 'Productivity',
                'task_type'         : 'Task'
            },
            color_discrete_sequence = [
                '#00ff88','#00d4ff',
                '#7c3aed','#ff6b6b','#ffd93d'
            ]
        )
        fig2.update_layout(
            plot_bgcolor  = 'rgba(0,0,0,0)',
            paper_bgcolor = 'rgba(0,0,0,0)',
            font_color    = '#e8e8f0',
            title_font    = dict(family='Syne', size=16)
        )
        fig2.update_xaxes(
            gridcolor='rgba(255,255,255,0.05)')
        fig2.update_yaxes(
            gridcolor='rgba(255,255,255,0.05)')
        st.plotly_chart(fig2, use_container_width=True)

    # Feature Importance
    st.markdown("""
    <div class='section-header'>
        🏆 Feature Importance
    </div>
    """, unsafe_allow_html=True)

    feat_names = ['Tempo', 'Energy', 'Valence',
                  'Instrumentalness',
                  'Danceability', 'Acousticness']
    importance_df = pd.DataFrame({
        'Feature'   : feat_names,
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=True)

    fig3 = px.bar(
        importance_df,
        x           = 'Importance',
        y           = 'Feature',
        orientation = 'h',
        title       = 'What affects your productivity most?',
        color       = 'Importance',
        color_continuous_scale = [
            '#1a1a2e', '#00d4ff', '#00ff88'
        ]
    )
    fig3.update_layout(
        plot_bgcolor  = 'rgba(0,0,0,0)',
        paper_bgcolor = 'rgba(0,0,0,0)',
        font_color    = '#e8e8f0',
        title_font    = dict(family='Syne', size=16),
        coloraxis_showscale = False
    )
    fig3.update_xaxes(
        gridcolor='rgba(255,255,255,0.05)')
    st.plotly_chart(fig3, use_container_width=True)

    # Task comparison
    st.markdown("""
    <div class='section-header'>
        📈 Productivity by Task
    </div>
    """, unsafe_allow_html=True)

    task_avg = df_filtered.groupby('task_type').agg(
        Productivity = ('productivity_score', 'mean'),
        Focus        = ('focus_score',        'mean'),
        Sessions     = ('productivity_score', 'count')
    ).reset_index()

    fig4 = px.bar(
        task_avg,
        x       = 'task_type',
        y       = ['Productivity', 'Focus'],
        barmode = 'group',
        title   = 'Avg Scores by Task Type',
        color_discrete_map = {
            'Productivity': '#00ff88',
            'Focus'       : '#7c3aed'
        }
    )
    fig4.update_layout(
        plot_bgcolor  = 'rgba(0,0,0,0)',
        paper_bgcolor = 'rgba(0,0,0,0)',
        font_color    = '#e8e8f0',
        title_font    = dict(family='Syne', size=16),
        yaxis_range   = [0, 10],
        legend        = dict(
            bgcolor='rgba(255,255,255,0.03)'
        )
    )
    fig4.update_xaxes(
        gridcolor='rgba(255,255,255,0.05)')
    fig4.update_yaxes(
        gridcolor='rgba(255,255,255,0.05)')
    st.plotly_chart(fig4, use_container_width=True)

# ════════════════════════════════════════
# TAB 2 — PLAYLIST
# ════════════════════════════════════════
with tab2:
    st.markdown("""
    <div class='section-header'>
        🎵 Generate Your Productivity Playlist
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        task = st.selectbox(
            "🎯 What are you working on?",
            ["coding", "reading",
             "writing", "design", "other"],
            key='playlist_task'
        )
        num_songs = st.slider(
            "🎶 How many songs?", 5, 25, 10)

    with col2:
        st.markdown("""
        <div class='insight-box' style='height:100%;'>
            <div style='font-family:Space Mono,monospace;
                        font-size:0.7rem; color:#00ff88;
                        letter-spacing:2px;
                        margin-bottom:0.75rem;'>
                IDEAL MUSIC PROFILE
            </div>
        """, unsafe_allow_html=True)

        profiles = {
            'coding' : {'Instrumentalness': '70-100%',
                        'Energy'          : '30-70%',
                        'Tempo'           : '80-120 BPM'},
            'reading': {'Instrumentalness': '60-100%',
                        'Energy'          : '10-50%',
                        'Tempo'           : '60-95 BPM'},
            'writing': {'Instrumentalness': '30-90%',
                        'Energy'          : '20-60%',
                        'Tempo'           : '70-110 BPM'},
            'design' : {'Instrumentalness': '30-80%',
                        'Energy'          : '40-80%',
                        'Tempo'           : '90-130 BPM'},
            'other'  : {'Instrumentalness': '30-90%',
                        'Energy'          : '30-70%',
                        'Tempo'           : '75-115 BPM'}
        }
        for k, v in profiles[task].items():
            st.markdown(f"""
            <div style='display:flex;
                        justify-content:space-between;
                        margin:0.4rem 0;
                        font-family:Space Mono,monospace;
                        font-size:0.75rem;'>
                <span style='color:#4a4a6a;'>{k}</span>
                <span style='color:#00d4ff;'>{v}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🎵 Generate Playlist"):
        ranges = {
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

        r    = ranges[task]
        mask = (
            df_spotify['instrumentalness'].between(
                *r['instrumentalness']) &
            df_spotify['energy'].between(
                *r['energy']) &
            df_spotify['tempo'].between(
                *r['tempo'])
        )
        playlist = df_spotify[mask][
            ['track_name', 'artists',
             'tempo', 'energy', 'valence']
        ].drop_duplicates(
            subset='track_name'
        ).head(num_songs)

        st.success(
            f"✅ {len(playlist)} songs found for {task}!")

        for idx, row in playlist.iterrows():
            energy_pct = int(row['energy'] * 100)
            valence_pct = int(row['valence'] * 100)
            st.markdown(f"""
            <div class='song-card'>
                <div>
                    <div style='font-family:Syne,sans-serif;
                                font-weight:600;
                                font-size:0.95rem;'>
                        {row['track_name']}
                    </div>
                    <div style='font-family:Space Mono,monospace;
                                font-size:0.7rem;
                                color:#4a4a6a;
                                margin-top:0.2rem;'>
                        {row['artists']}
                    </div>
                </div>
                <div style='display:flex; gap:1rem;
                            font-family:Space Mono,monospace;
                            font-size:0.7rem;'>
                    <div style='text-align:center;'>
                        <div style='color:#00ff88;
                                    font-size:1rem;
                                    font-weight:700;'>
                            {int(row['tempo'])}
                        </div>
                        <div style='color:#4a4a6a;'>BPM</div>
                    </div>
                    <div style='text-align:center;'>
                        <div style='color:#00d4ff;
                                    font-size:1rem;
                                    font-weight:700;'>
                            {energy_pct}%
                        </div>
                        <div style='color:#4a4a6a;'>
                            Energy
                        </div>
                    </div>
                    <div style='text-align:center;'>
                        <div style='color:#7c3aed;
                                    font-size:1rem;
                                    font-weight:700;'>
                            {valence_pct}%
                        </div>
                        <div style='color:#4a4a6a;'>Mood</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ════════════════════════════════════════
# TAB 3 — PREDICT
# ════════════════════════════════════════
with tab3:
    st.markdown("""
    <div class='section-header'>
        🔮 Predict Your Productivity
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style='color:#4a4a6a;
              font-family:Space Mono,monospace;
              font-size:0.8rem;'>
        Adjust the music features below and get your
        predicted productivity score instantly.
    </p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### 🎼 Music Features")
        tempo  = st.slider("⚡ Tempo (BPM)",
                            60, 200, 100)
        energy = st.slider("🔥 Energy",
                            0.0, 1.0, 0.5,
                            step=0.01)
        valence = st.slider("😊 Valence (Mood)",
                             0.0, 1.0, 0.5,
                             step=0.01)

    with col2:
        st.markdown("##### 🎸 More Features")
        instrumentalness = st.slider(
            "🎹 Instrumentalness",
            0.0, 1.0, 0.5, step=0.01)
        danceability = st.slider(
            "💃 Danceability",
            0.0, 1.0, 0.5, step=0.01)
        acousticness = st.slider(
            "🎻 Acousticness",
            0.0, 1.0, 0.5, step=0.01)

    if st.button("🔮 Predict My Productivity"):
        input_df = pd.DataFrame([{
            'avg_tempo'           : tempo,
            'avg_energy'          : energy,
            'avg_valence'         : valence,
            'avg_instrumentalness': instrumentalness,
            'avg_danceability'    : danceability,
            'avg_acousticness'    : acousticness
        }])

        pred = model.predict(input_df)[0]
        pred = round(min(max(pred, 1), 10), 1)

        if pred >= 7:
            emoji = "🟢"
            msg   = "High Productivity Zone!"
            color = "#00ff88"
        elif pred >= 5:
            emoji = "🟡"
            msg   = "Moderate Productivity"
            color = "#ffd93d"
        else:
            emoji = "🔴"
            msg   = "Low Productivity Zone"
            color = "#ff6b6b"

        st.markdown(f"""
        <div class='pred-result'>
            <div style='font-family:Space Mono,monospace;
                        font-size:0.75rem;
                        color:#4a4a6a;
                        letter-spacing:3px;
                        text-transform:uppercase;
                        margin-bottom:0.5rem;'>
                Predicted Score
            </div>
            <div class='pred-number'
                 style='background:linear-gradient(
                            135deg, {color}, #00d4ff);
                        -webkit-background-clip:text;
                        -webkit-text-fill-color:transparent;'>
                {pred}
            </div>
            <div style='font-family:Syne,sans-serif;
                        font-size:1.2rem;
                        font-weight:600;
                        color:{color};
                        margin-top:0.5rem;'>
                {emoji} {msg}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Gauge
        fig = go.Figure(go.Indicator(
            mode  = "gauge+number",
            value = pred,
            title = {'text'     : "Productivity Score",
                     'font'     : {'color': '#e8e8f0',
                                   'family': 'Syne'}},
            number = {'font': {'color'  : color,
                               'family' : 'Syne',
                               'size'   : 48}},
            gauge = {
                'axis' : {
                    'range'     : [0, 10],
                    'tickcolor' : '#4a4a6a',
                    'tickfont'  : {'color': '#4a4a6a'}
                },
                'bar'  : {'color': color,
                           'thickness': 0.25},
                'bgcolor' : 'rgba(0,0,0,0)',
                'steps': [
                    {'range': [0, 4],
                     'color': 'rgba(255,107,107,0.1)'},
                    {'range': [4, 7],
                     'color': 'rgba(255,217,61,0.1)'},
                    {'range': [7, 10],
                     'color': 'rgba(0,255,136,0.1)'}
                ],
                'threshold': {
                    'line' : {'color': color,
                               'width': 3},
                    'value': pred
                }
            }
        ))
        fig.update_layout(
            paper_bgcolor = 'rgba(0,0,0,0)',
            font_color    = '#e8e8f0',
            height        = 300
        )
        st.plotly_chart(fig, use_container_width=True)

# ════════════════════════════════════════
# TAB 4 — SESSIONS
# ════════════════════════════════════════
with tab4:
    st.markdown("""
    <div class='section-header'>
        📋 Session History
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 3])

    with col1:
        tasks    = ['All'] + \
                   df['task_type'].unique().tolist()
        selected = st.selectbox("Filter by Task",
                                 tasks)

    filtered = df if selected == 'All' else \
               df[df['task_type'] == selected]

    # Productivity over time
    fig = px.line(
        filtered.reset_index(),
        x       = filtered.reset_index().index,
        y       = 'productivity_score',
        color   = 'task_type',
        markers = True,
        title   = 'Productivity Over Time',
        labels  = {'x': 'Session', 
                   'productivity_score': 'Score'},
        color_discrete_sequence = [
            '#00ff88','#00d4ff',
            '#7c3aed','#ff6b6b','#ffd93d'
        ]
    )
    fig.update_layout(
        plot_bgcolor  = 'rgba(0,0,0,0)',
        paper_bgcolor = 'rgba(0,0,0,0)',
        font_color    = '#e8e8f0',
        title_font    = dict(family='Syne', size=16),
        yaxis_range   = [0, 10]
    )
    fig.update_xaxes(
        gridcolor='rgba(255,255,255,0.05)')
    fig.update_yaxes(
        gridcolor='rgba(255,255,255,0.05)')
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        filtered[[
            'date', 'task_type', 'song1',
            'avg_tempo', 'avg_energy',
            'avg_valence', 'productivity_score',
            'focus_score'
        ]].rename(columns={
            'avg_tempo'          : 'Tempo',
            'avg_energy'         : 'Energy',
            'avg_valence'        : 'Valence',
            'productivity_score' : 'Productivity',
            'focus_score'        : 'Focus',
            'task_type'          : 'Task',
            'song1'              : 'Song'
        }),
        use_container_width = True,
        hide_index          = True
    )

# ── Footer ───────────────────────────────────────────────────
st.markdown("""
<div class='custom-divider'></div>
<div style='text-align:center;
            font-family:Space Mono,monospace;
            font-size:0.7rem;
            color:#4a4a6a;
            letter-spacing:2px;
            padding:1rem 0 2rem 0;'>
    MOODMETRIC — MUSIC × PRODUCTIVITY ANALYTICS
</div>
""", unsafe_allow_html=True)