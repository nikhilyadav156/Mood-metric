import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pickle
import os

# ── Page Config ──────────────────────────────────────────────
st.set_page_config(
    page_title            = "MoodMetric",
    page_icon             = "🎵",
    layout                = "wide",
    initial_sidebar_state = "expanded"
)

# ── Spotify-Inspired CSS ─────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Figtree:wght@300;400;500;600;700;800&display=swap');

* { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family : 'Figtree', sans-serif;
    background  : #121212;
    color       : #FFFFFF;
}

.stApp { background: #121212; }

#MainMenu, footer, header { visibility: hidden; }

::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: #121212; }
::-webkit-scrollbar-thumb {
    background: #535353; border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: #1DB954;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background  : #000000 !important;
    border-right: none !important;
    min-width   : 240px !important;
}
[data-testid="stSidebar"] > div { padding: 0 !important; }
[data-testid="stSidebar"] * { color: #B3B3B3 !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #FFFFFF !important; }
[data-testid="stSidebar"] .stMultiSelect span {
    background: #1DB954 !important;
    color     : #000000 !important;
}

/* TABS */
.stTabs [data-baseweb="tab-list"] {
    background   : transparent;
    border-bottom: 1px solid #282828;
    gap          : 0;
    padding      : 0;
}
.stTabs [data-baseweb="tab"] {
    background    : transparent;
    color         : #B3B3B3;
    font-family   : 'Figtree', sans-serif;
    font-size     : 0.875rem;
    font-weight   : 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding       : 1rem 1.5rem;
    border        : none;
    border-bottom : 2px solid transparent;
    border-radius : 0;
    transition    : all 0.2s;
}
.stTabs [data-baseweb="tab"]:hover { color: #FFFFFF; }
.stTabs [aria-selected="true"] {
    background    : transparent !important;
    color         : #FFFFFF !important;
    border-bottom : 2px solid #1DB954 !important;
}

/* BUTTONS */
.stButton > button {
    background    : #1DB954;
    color         : #000000;
    font-family   : 'Figtree', sans-serif;
    font-weight   : 700;
    font-size     : 0.875rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    border        : none;
    border-radius : 500px;
    padding       : 0.875rem 2rem;
    transition    : all 0.2s;
    min-width     : 160px;
}
.stButton > button:hover {
    background: #1ed760;
    transform : scale(1.04);
}

/* SELECT / MULTISELECT */
.stSelectbox [data-baseweb="select"] > div,
.stMultiSelect [data-baseweb="select"] > div {
    background    : #282828 !important;
    border        : 1px solid #333 !important;
    border-radius : 4px !important;
    color         : #FFFFFF !important;
}

/* CUSTOM COMPONENTS */
.now-playing {
    background    : linear-gradient(135deg,#1a6b38 0%,#121212 100%);
    border-radius : 12px;
    padding       : 2.5rem 3rem;
    margin-bottom : 2rem;
    position      : relative;
    overflow      : hidden;
}
.now-playing::before {
    content       : '';
    position      : absolute;
    top:-50%; right:-10%;
    width         : 400px;
    height        : 400px;
    background    : radial-gradient(circle,rgba(29,185,84,0.15) 0%,transparent 70%);
    pointer-events: none;
}
.now-playing-label {
    font-size     : 0.7rem;
    font-weight   : 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color         : #1DB954;
    margin-bottom : 0.5rem;
}
.now-playing-title {
    font-size     : 3.5rem;
    font-weight   : 800;
    color         : #FFFFFF;
    line-height   : 1.05;
    letter-spacing: -1px;
    margin-bottom : 0.75rem;
}
.now-playing-sub {
    font-size: 1rem;
    color    : #B3B3B3;
}

.stat-card {
    background   : #181818;
    border-radius: 8px;
    padding      : 1.5rem;
    transition   : background 0.2s;
    height       : 100%;
}
.stat-card:hover { background: #282828; }
.stat-card-icon  { font-size: 2rem; margin-bottom: 1rem; }
.stat-card-value {
    font-size    : 2rem;
    font-weight  : 800;
    color        : #FFFFFF;
    line-height  : 1;
    margin-bottom: 0.35rem;
}
.stat-card-label {
    font-size: 0.8rem;
    color    : #B3B3B3;
}
.stat-card-badge {
    display       : inline-block;
    background    : #1DB954;
    color         : #000000;
    font-size     : 0.65rem;
    font-weight   : 700;
    letter-spacing: 0.05em;
    padding       : 2px 8px;
    border-radius : 500px;
    margin-top    : 0.5rem;
    text-transform: uppercase;
}

.track-row {
    display        : flex;
    align-items    : center;
    padding        : 0.5rem 1rem;
    border-radius  : 4px;
    transition     : background 0.15s;
    margin         : 2px 0;
    gap            : 1rem;
}
.track-row:hover  { background: #282828; }
.track-number {
    font-size  : 0.9rem;
    color      : #B3B3B3;
    min-width  : 20px;
    text-align : center;
}
.track-info   { flex: 1; }
.track-name   {
    font-size  : 0.95rem;
    font-weight: 500;
    color      : #FFFFFF;
}
.track-artist {
    font-size : 0.8rem;
    color     : #B3B3B3;
    margin-top: 2px;
}
.track-pill {
    background   : #282828;
    border-radius: 500px;
    padding      : 3px 10px;
    font-size    : 0.75rem;
    color        : #B3B3B3;
    font-weight  : 500;
}
.track-pill-green {
    background: rgba(29,185,84,0.15);
    color     : #1DB954;
}

.sp-section {
    display        : flex;
    justify-content: space-between;
    align-items    : baseline;
    margin         : 2rem 0 1rem 0;
}
.sp-section-title {
    font-size     : 1.5rem;
    font-weight   : 700;
    color         : #FFFFFF;
    letter-spacing: -0.3px;
}

.insight-card {
    background   : #181818;
    border-radius: 8px;
    padding      : 1.5rem;
    border-left  : 3px solid #1DB954;
    margin       : 1rem 0;
}
.insight-tag {
    font-size     : 0.65rem;
    font-weight   : 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color         : #1DB954;
    margin-bottom : 0.5rem;
}
.insight-text {
    font-size  : 0.95rem;
    color      : #FFFFFF;
    line-height: 1.6;
}

.pred-card {
    background   : #181818;
    border-radius: 12px;
    padding      : 3rem 2rem;
    text-align   : center;
}
.pred-score {
    font-size     : 8rem;
    font-weight   : 800;
    line-height   : 1;
    color         : #1DB954;
    letter-spacing: -4px;
}
.pred-label {
    font-size     : 0.75rem;
    font-weight   : 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color         : #B3B3B3;
    margin-top    : 0.5rem;
}

.sp-bar-wrap  { margin: 0.5rem 0; }
.sp-bar-label {
    display        : flex;
    justify-content: space-between;
    margin-bottom  : 5px;
    font-size      : 0.8rem;
    color          : #B3B3B3;
}
.sp-bar-bg {
    background   : #282828;
    border-radius: 500px;
    height       : 4px;
    width        : 100%;
    overflow     : hidden;
}
.sp-bar-fill {
    height       : 4px;
    border-radius: 500px;
    background   : #1DB954;
}

.sp-divider {
    border    : none;
    border-top: 1px solid #282828;
    margin    : 1.5rem 0;
}

.genre-tag {
    display      : inline-block;
    background   : #282828;
    border-radius: 4px;
    padding      : 0.4rem 0.85rem;
    font-size    : 0.8rem;
    font-weight  : 500;
    color        : #FFFFFF;
    margin       : 3px;
    transition   : background 0.15s;
}
.genre-tag:hover      { background: #3E3E3E; }
.genre-tag-active {
    background: rgba(29,185,84,0.2);
    color     : #1DB954;
}
</style>
""", unsafe_allow_html=True)

# ── File Paths ───────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

SP_COLORS = ['#1DB954','#1ed760','#169e47',
             '#0d6e32','#53d683']

def sp_fig(fig, height=380):
    fig.update_layout(
        plot_bgcolor  = 'rgba(0,0,0,0)',
        paper_bgcolor = 'rgba(24,24,24,1)',
        font_color    = '#B3B3B3',
        font_family   = 'Figtree',
        title_font    = dict(size=15, color='#FFFFFF',
                              family='Figtree'),
        height        = height,
        margin        = dict(t=50,b=40,l=40,r=20),
        legend        = dict(
            bgcolor = 'rgba(0,0,0,0)',
            font    = dict(color='#B3B3B3', size=12)
        )
    )
    fig.update_xaxes(
        gridcolor='#282828', linecolor='#282828',
        tickcolor='#535353',
        tickfont=dict(color='#B3B3B3', size=11)
    )
    fig.update_yaxes(
        gridcolor='#282828', linecolor='#282828',
        tickcolor='#535353',
        tickfont=dict(color='#B3B3B3', size=11)
    )
    return fig

# ── Load Data ────────────────────────────────────────────────
@st.cache_data
def load_data():
    path = os.path.join(DATA_DIR, 'merged_data.csv')
    df   = pd.read_csv(path)
    for col in ['productivity_score','focus_score',
                'avg_tempo','avg_energy','avg_valence',
                'avg_instrumentalness',
                'avg_danceability','avg_acousticness']:
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

avg_prod   = df['productivity_score'].mean()
avg_focus  = df['focus_score'].mean()
best_task  = df.groupby('task_type')[
    'productivity_score'].mean().idxmax()
total_sess = len(df)

feat_names = ['Tempo','Energy','Valence',
              'Instrumentalness',
              'Danceability','Acousticness']
best_feat_i = model.feature_importances_.argmax()
best_feat   = feat_names[best_feat_i] \
              if best_feat_i < len(feat_names) \
              else "Energy"

# ── SIDEBAR ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:1.5rem 1.5rem 0.5rem;'>
        <div style='display:flex;align-items:center;
                    gap:0.6rem;margin-bottom:2rem;'>
            <div style='width:36px;height:36px;
                        background:#1DB954;border-radius:50%;
                        display:flex;align-items:center;
                        justify-content:center;
                        font-size:1.1rem;'>🎵</div>
            <span style='font-family:Figtree,sans-serif;
                          font-size:1.3rem;font-weight:800;
                          color:#FFFFFF !important;
                          letter-spacing:-0.5px;'>
                MoodMetric
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    task_filter = st.multiselect(
        "Filter by Task",
        options = df['task_type'].unique().tolist(),
        default = df['task_type'].unique().tolist()
    )

    st.markdown("<hr class='sp-divider'>",
                unsafe_allow_html=True)

    st.markdown("""
    <div style='padding:0 1rem;'>
        <div style='font-size:0.65rem;font-weight:700;
                    letter-spacing:0.12em;
                    text-transform:uppercase;
                    color:#B3B3B3 !important;
                    margin-bottom:1rem;'>
            Avg Audio Profile
        </div>
    </div>
    """, unsafe_allow_html=True)

    feat_cols   = ['avg_tempo','avg_energy',
                   'avg_valence','avg_instrumentalness']
    feat_labels = ['Tempo','Energy',
                   'Valence','Instrumental']
    feat_maxes  = [200,1,1,1]

    for fcol,flabel,fmax in zip(
            feat_cols,feat_labels,feat_maxes):
        val = df[fcol].mean()
        pct = min(int((val/fmax)*100),100)
        disp = f"{val:.0f}" if fmax==200 \
               else f"{pct}%"
        st.markdown(f"""
        <div class='sp-bar-wrap'
             style='padding:0 1rem;'>
            <div class='sp-bar-label'>
                <span>{flabel}</span>
                <span>{disp}</span>
            </div>
            <div class='sp-bar-bg'>
                <div class='sp-bar-fill'
                     style='width:{pct}%;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

# ── Filter ───────────────────────────────────────────────────
dff = df[df['task_type'].isin(task_filter)]

# ── Hero ─────────────────────────────────────────────────────
st.markdown(f"""
<div class='now-playing'>
    <div class='now-playing-label'>🎵 Now Analyzing</div>
    <div class='now-playing-title'>MoodMetric</div>
    <div class='now-playing-sub'>
        {total_sess} sessions tracked &nbsp;·&nbsp;
        {avg_prod:.1f}/10 avg productivity &nbsp;·&nbsp;
        Best at <strong style='color:#fff;'>
        {best_task.title()}</strong>
    </div>
    <br>
    <span class='genre-tag genre-tag-active'>
        🎯 {best_feat}
    </span>
    <span class='genre-tag'>🏆 {best_task.title()}</span>
    <span class='genre-tag'>📊 {total_sess} Sessions</span>
    <span class='genre-tag'>
        ⚡ {df['avg_tempo'].mean():.0f} BPM avg
    </span>
</div>
""", unsafe_allow_html=True)

# ── Stat Cards ───────────────────────────────────────────────
c1,c2,c3,c4 = st.columns(4)
for col,icon,val,label,badge in [
    (c1,"🎧",str(total_sess),
     "Sessions Logged","Active"),
    (c2,"⚡",f"{avg_prod:.1f}",
     "Avg Productivity","out of 10"),
    (c3,"🎯",f"{avg_focus:.1f}",
     "Avg Focus Score","out of 10"),
    (c4,"🏆",best_task.title(),
     "Best Task Type","Top performer"),
]:
    col.markdown(f"""
    <div class='stat-card'>
        <div class='stat-card-icon'>{icon}</div>
        <div class='stat-card-value'>{val}</div>
        <div class='stat-card-label'>{label}</div>
        <div class='stat-card-badge'>{badge}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Tabs ─────────────────────────────────────────────────────
tab1,tab2,tab3,tab4 = st.tabs([
    "Analytics","Your Playlist","Predict","History"
])

# ════════════════════════════════════════════════════════════
# TAB 1 — ANALYTICS
# ════════════════════════════════════════════════════════════
with tab1:
    corr_e = dff['avg_energy'].corr(
        dff['productivity_score'])
    corr_d = "positively" if corr_e > 0 \
             else "negatively"

    st.markdown(f"""
    <div class='insight-card'>
        <div class='insight-tag'>🧠 Insight</div>
        <div class='insight-text'>
            Your productivity is most influenced by
            <strong style='color:#1DB954;'>{best_feat}
            </strong>. Higher energy music {corr_d}
            correlates with your productivity
            (r = {corr_e:.2f}). You perform best during
            <strong style='color:#1DB954;'>
            {best_task.title()}</strong> sessions.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1,col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class='sp-section'>
            <span class='sp-section-title'>
                Energy vs Productivity
            </span>
        </div>""", unsafe_allow_html=True)
        fig = px.scatter(dff,
            x='avg_energy', y='productivity_score',
            color='task_type', size='avg_tempo',
            trendline='ols',
            labels={'avg_energy':'Energy',
                    'productivity_score':'Productivity',
                    'task_type':'Task'},
            color_discrete_sequence=SP_COLORS)
        fig.update_traces(
            marker=dict(line=dict(width=0)))
        st.plotly_chart(sp_fig(fig),
                        use_container_width=True)

    with col2:
        st.markdown("""
        <div class='sp-section'>
            <span class='sp-section-title'>
                Valence vs Productivity
            </span>
        </div>""", unsafe_allow_html=True)
        fig2 = px.scatter(dff,
            x='avg_valence', y='productivity_score',
            color='task_type',
            size='avg_instrumentalness',
            trendline='ols',
            labels={'avg_valence':'Valence (Mood)',
                    'productivity_score':'Productivity',
                    'task_type':'Task'},
            color_discrete_sequence=SP_COLORS)
        st.plotly_chart(sp_fig(fig2),
                        use_container_width=True)

    st.markdown("""
    <div class='sp-section'>
        <span class='sp-section-title'>
            What Drives Your Productivity
        </span>
    </div>""", unsafe_allow_html=True)

    imp_df = pd.DataFrame({
        'Feature'   : feat_names,
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=True)

    fig3 = px.bar(imp_df,
        x='Importance', y='Feature',
        orientation='h', color='Importance',
        color_continuous_scale=[
            '#0d6e32','#1DB954','#1ed760'],
        labels={'Importance':'Impact Score'})
    fig3.update_layout(coloraxis_showscale=False,
                       showlegend=False)
    fig3.update_traces(marker_line_width=0)
    st.plotly_chart(sp_fig(fig3, height=320),
                    use_container_width=True)

    col3,col4 = st.columns(2)

    with col3:
        st.markdown("""
        <div class='sp-section'>
            <span class='sp-section-title'>
                Score by Task Type
            </span>
        </div>""", unsafe_allow_html=True)
        task_avg = dff.groupby('task_type').agg(
            Productivity=('productivity_score','mean'),
            Focus=('focus_score','mean')
        ).reset_index()
        fig4 = px.bar(task_avg,
            x='task_type',
            y=['Productivity','Focus'],
            barmode='group',
            labels={'task_type':'Task',
                    'value':'Score'},
            color_discrete_map={
                'Productivity':'#1DB954',
                'Focus':'#535353'})
        fig4.update_layout(yaxis_range=[0,10])
        fig4.update_traces(marker_line_width=0)
        st.plotly_chart(sp_fig(fig4, height=320),
                        use_container_width=True)

    with col4:
        st.markdown("""
        <div class='sp-section'>
            <span class='sp-section-title'>
                Tempo Distribution
            </span>
        </div>""", unsafe_allow_html=True)
        dff2 = dff.copy()
        dff2['productive'] = (
            dff2['productivity_score'] >= 7)
        fig5 = px.histogram(dff2,
            x='avg_tempo', color='productive',
            nbins=12, barmode='overlay',
            opacity=0.85,
            labels={'avg_tempo':'Tempo (BPM)',
                    'productive':'High Productivity'},
            color_discrete_map={
                True:'#1DB954', False:'#535353'})
        fig5.update_traces(marker_line_width=0)
        st.plotly_chart(sp_fig(fig5, height=320),
                        use_container_width=True)

# ════════════════════════════════════════════════════════════
# TAB 2 — PLAYLIST
# ════════════════════════════════════════════════════════════
with tab2:
    st.markdown("""
    <div class='sp-section'>
        <span class='sp-section-title'>
            🎵 Build Your Focus Playlist
        </span>
    </div>""", unsafe_allow_html=True)

    col1,col2,col3 = st.columns([1.5,1,1])
    with col1:
        task = st.selectbox("Select Activity",
            ["coding","reading","writing",
             "design","other"])
    with col2:
        num_songs = st.slider(
            "Number of songs", 5, 30, 15)
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        generate = st.button("▶  Generate Playlist")

    profiles_info = {
        'coding' :[('Instrumentalness','70-100%'),
                   ('Energy','30-70%'),
                   ('Tempo','80-120 BPM')],
        'reading':[('Instrumentalness','60-100%'),
                   ('Energy','10-50%'),
                   ('Tempo','60-95 BPM')],
        'writing':[('Instrumentalness','30-90%'),
                   ('Energy','20-60%'),
                   ('Tempo','70-110 BPM')],
        'design' :[('Instrumentalness','30-80%'),
                   ('Energy','40-80%'),
                   ('Tempo','90-130 BPM')],
        'other'  :[('Instrumentalness','30-90%'),
                   ('Energy','30-70%'),
                   ('Tempo','75-115 BPM')]
    }

    pills = " ".join([
        f"<span class='genre-tag'>{k}: "
        f"<strong style='color:#1DB954;'>{v}"
        f"</strong></span>"
        for k,v in profiles_info[task]
    ])
    st.markdown(
        f"<div style='margin:0.5rem 0 1.5rem;'>"
        f"{pills}</div>",
        unsafe_allow_html=True)

    if generate:
        ranges = {
            'coding' :{'instrumentalness':(0.4,1.0),
                       'energy':(0.3,0.7),
                       'tempo':(80,120)},
            'reading':{'instrumentalness':(0.6,1.0),
                       'energy':(0.1,0.5),
                       'tempo':(60,95)},
            'writing':{'instrumentalness':(0.3,0.9),
                       'energy':(0.2,0.6),
                       'tempo':(70,110)},
            'design' :{'instrumentalness':(0.3,0.8),
                       'energy':(0.4,0.8),
                       'tempo':(90,130)},
            'other'  :{'instrumentalness':(0.3,0.9),
                       'energy':(0.3,0.7),
                       'tempo':(75,115)}
        }
        r    = ranges[task]
        mask = (
            df_spotify['instrumentalness'].between(
                *r['instrumentalness']) &
            df_spotify['energy'].between(
                *r['energy']) &
            df_spotify['tempo'].between(*r['tempo'])
        )
        playlist = df_spotify[mask][
            ['track_name','artists',
             'tempo','energy','valence',
             'instrumentalness']
        ].drop_duplicates(
            subset='track_name'
        ).head(num_songs)

        st.markdown(f"""
        <div style='display:flex;align-items:center;
                    gap:1rem;margin:1.5rem 0 0.5rem;'>
            <div style='width:80px;height:80px;
                        background:linear-gradient(
                            135deg,#1DB954,#169e47);
                        border-radius:4px;
                        display:flex;align-items:center;
                        justify-content:center;
                        font-size:2rem;flex-shrink:0;'>
                🎵
            </div>
            <div>
                <div style='font-size:0.65rem;
                            font-weight:700;
                            letter-spacing:0.12em;
                            text-transform:uppercase;
                            color:#B3B3B3;'>
                    Playlist
                </div>
                <div style='font-size:1.8rem;
                            font-weight:800;
                            color:#FFFFFF;
                            line-height:1.1;'>
                    Focus: {task.title()}
                </div>
                <div style='font-size:0.85rem;
                            color:#B3B3B3;
                            margin-top:4px;'>
                    {len(playlist)} songs curated
                    by MoodMetric
                </div>
            </div>
        </div>
        <hr class='sp-divider'>
        <div style='display:flex;padding:0 1rem 0.5rem;
                    font-size:0.65rem;font-weight:700;
                    letter-spacing:0.1em;
                    text-transform:uppercase;
                    color:#B3B3B3;
                    border-bottom:1px solid #282828;
                    margin-bottom:0.5rem;'>
            <span style='min-width:30px;'>#</span>
            <span style='flex:1;'>Title</span>
            <span style='width:80px;
                         text-align:center;'>BPM</span>
            <span style='width:80px;
                         text-align:center;'>Energy</span>
            <span style='width:80px;
                         text-align:center;'>Mood</span>
        </div>
        """, unsafe_allow_html=True)

        for i,(_, row) in enumerate(
                playlist.iterrows(), 1):
            e_pct = int(row['energy']  * 100)
            v_pct = int(row['valence'] * 100)
            e_cls = "track-pill-green" \
                    if e_pct < 70 else ""
            st.markdown(f"""
            <div class='track-row'>
                <span class='track-number'>{i}</span>
                <div class='track-info'>
                    <div class='track-name'>
                        {row['track_name']}
                    </div>
                    <div class='track-artist'>
                        {row['artists']}
                    </div>
                </div>
                <div style='width:80px;
                            text-align:center;'>
                    <span class='track-pill'>
                        {int(row['tempo'])} BPM
                    </span>
                </div>
                <div style='width:80px;
                            text-align:center;'>
                    <span class='track-pill {e_cls}'>
                        {e_pct}%
                    </span>
                </div>
                <div style='width:80px;
                            text-align:center;'>
                    <span class='track-pill'>
                        {v_pct}%
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# TAB 3 — PREDICT
# ════════════════════════════════════════════════════════════
with tab3:
    st.markdown("""
    <div class='sp-section'>
        <span class='sp-section-title'>
            🔮 Predict Your Productivity Score
        </span>
    </div>
    <p style='font-size:0.9rem;color:#B3B3B3;
              margin-bottom:2rem;'>
        Adjust audio feature sliders to match the music
        you plan to listen to and get your predicted
        productivity score instantly.
    </p>""", unsafe_allow_html=True)

    col1,col2,col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style='font-size:0.65rem;font-weight:700;
                    letter-spacing:0.12em;
                    text-transform:uppercase;
                    color:#B3B3B3;margin-bottom:1rem;'>
            Rhythm
        </div>""", unsafe_allow_html=True)
        tempo  = st.slider("Tempo (BPM)",
                            60,200,100)
        energy = st.slider("Energy",
                            0.0,1.0,0.5,step=0.01)

    with col2:
        st.markdown("""
        <div style='font-size:0.65rem;font-weight:700;
                    letter-spacing:0.12em;
                    text-transform:uppercase;
                    color:#B3B3B3;margin-bottom:1rem;'>
            Mood
        </div>""", unsafe_allow_html=True)
        valence          = st.slider("Valence",
                                      0.0,1.0,0.5,
                                      step=0.01)
        instrumentalness = st.slider(
            "Instrumentalness",0.0,1.0,0.5,step=0.01)

    with col3:
        st.markdown("""
        <div style='font-size:0.65rem;font-weight:700;
                    letter-spacing:0.12em;
                    text-transform:uppercase;
                    color:#B3B3B3;margin-bottom:1rem;'>
            Texture
        </div>""", unsafe_allow_html=True)
        danceability = st.slider("Danceability",
                                  0.0,1.0,0.5,
                                  step=0.01)
        acousticness = st.slider("Acousticness",
                                  0.0,1.0,0.5,
                                  step=0.01)

    st.markdown("<br>", unsafe_allow_html=True)
    col_btn,_ = st.columns([1,3])
    with col_btn:
        predict_btn = st.button(
            "▶  Predict Score")

    if predict_btn:
        inp  = pd.DataFrame([{
            'avg_tempo'           : tempo,
            'avg_energy'          : energy,
            'avg_valence'         : valence,
            'avg_instrumentalness': instrumentalness,
            'avg_danceability'    : danceability,
            'avg_acousticness'    : acousticness
        }])
        pred = model.predict(inp)[0]
        pred = round(min(max(pred,1),10),1)

        if pred >= 7:
            sc = '#1DB954'
            status = '✅ High Productivity Zone!'
            desc   = ('This music profile is great '
                      'for your focus sessions!')
        elif pred >= 5:
            sc = '#ffa500'
            status = '⚠️  Moderate Productivity'
            desc   = ('Decent focus expected. Try '
                      'increasing instrumentalness.')
        else:
            sc = '#e8450a'
            status = '❌ Low Productivity Zone'
            desc   = ('This music may distract you. '
                      'Try calmer instrumental tracks.')

        res_col,gauge_col = st.columns([1,1])

        with res_col:
            st.markdown(f"""
            <div class='pred-card'>
                <div style='font-size:0.65rem;
                            font-weight:700;
                            letter-spacing:0.15em;
                            text-transform:uppercase;
                            color:#B3B3B3;
                            margin-bottom:0.5rem;'>
                    Predicted Score
                </div>
                <div class='pred-score'
                     style='color:{sc};'>{pred}</div>
                <div class='pred-label'>out of 10</div>
                <hr class='sp-divider'>
                <div style='font-size:1rem;
                            font-weight:700;
                            color:{sc};
                            margin-bottom:0.4rem;'>
                    {status}
                </div>
                <div style='font-size:0.85rem;
                            color:#B3B3B3;'>
                    {desc}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with gauge_col:
            gauge = go.Figure(go.Indicator(
                mode  = "gauge+number",
                value = pred,
                title = {'text':'Score',
                         'font':{'color':'#B3B3B3',
                                  'family':'Figtree',
                                  'size':14}},
                number = {'font':{'color':sc,
                                   'family':'Figtree',
                                   'size':56},
                          'suffix':'/10'},
                gauge = {
                    'axis':{
                        'range':[0,10],
                        'tickcolor':'#535353',
                        'tickfont':{'color':'#535353'}
                    },
                    'bar':{'color':sc,'thickness':0.2},
                    'bgcolor':'rgba(0,0,0,0)',
                    'bordercolor':'rgba(0,0,0,0)',
                    'steps':[
                        {'range':[0,4],
                         'color':'#1a0a00'},
                        {'range':[4,7],
                         'color':'#1a1000'},
                        {'range':[7,10],
                         'color':'#001a08'}
                    ],
                    'threshold':{
                        'line':{'color':sc,'width':3},
                        'value':pred
                    }
                }
            ))
            gauge.update_layout(
                paper_bgcolor = '#181818',
                height        = 320,
                margin        = dict(
                    t=60,b=20,l=30,r=30)
            )
            st.plotly_chart(gauge,
                            use_container_width=True)

        st.markdown("""
        <div class='sp-section'>
            <span class='sp-section-title'>
                Input Breakdown
            </span>
        </div>""", unsafe_allow_html=True)

        feat_vals = [tempo/200,energy,valence,
                     instrumentalness,
                     danceability,acousticness]
        feat_labs = ['Tempo','Energy','Valence',
                     'Instrumental',
                     'Danceability','Acousticness']
        for lab,val in zip(feat_labs,feat_vals):
            pct = int(val*100)
            st.markdown(f"""
            <div class='sp-bar-wrap'>
                <div class='sp-bar-label'>
                    <span>{lab}</span>
                    <span>{pct}%</span>
                </div>
                <div class='sp-bar-bg'>
                    <div class='sp-bar-fill'
                         style='width:{pct}%;'>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# TAB 4 — HISTORY
# ════════════════════════════════════════════════════════════
with tab4:
    st.markdown("""
    <div class='sp-section'>
        <span class='sp-section-title'>
            📋 Session History
        </span>
    </div>""", unsafe_allow_html=True)

    col1,col2 = st.columns([1,1])
    with col1:
        tasks    = ['All'] + \
                   df['task_type'].unique().tolist()
        selected = st.selectbox(
            "Filter by Task", tasks)
    with col2:
        min_score = st.slider(
            "Min Productivity Score",1,10,1)

    filtered = df.copy()
    if selected != 'All':
        filtered = filtered[
            filtered['task_type'] == selected]
    filtered = filtered[
        filtered['productivity_score'] >= min_score]

    mc1,mc2,mc3,mc4 = st.columns(4)
    for col,val,lab in [
        (mc1, len(filtered),        "Sessions"),
        (mc2, f"{filtered['productivity_score'].mean():.1f}",
              "Avg Productivity"),
        (mc3, f"{filtered['focus_score'].mean():.1f}",
              "Avg Focus"),
        (mc4, f"{filtered['avg_tempo'].mean():.0f} BPM",
              "Avg Tempo"),
    ]:
        col.markdown(f"""
        <div class='stat-card'>
            <div class='stat-card-value'
                 style='font-size:1.5rem;'>
                {val}
            </div>
            <div class='stat-card-label'>{lab}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    fig6 = px.line(
        filtered.reset_index(),
        x       = filtered.reset_index().index,
        y       = ['productivity_score','focus_score'],
        markers = True,
        title   = 'Productivity & Focus Over Time',
        labels  = {'value':'Score','x':'Session #',
                   'variable':'Metric'},
        color_discrete_map = {
            'productivity_score':'#1DB954',
            'focus_score':'#535353'
        }
    )
    fig6.update_layout(yaxis_range=[0,10])
    st.plotly_chart(sp_fig(fig6),
                    use_container_width=True)

    st.markdown("""
    <div style='display:flex;padding:0 1rem 0.5rem;
                font-size:0.65rem;font-weight:700;
                letter-spacing:0.1em;
                text-transform:uppercase;
                color:#B3B3B3;
                border-bottom:1px solid #282828;
                margin:1rem 0 0.5rem;'>
        <span style='min-width:30px;'>#</span>
        <span style='flex:1;'>Song / Task</span>
        <span style='width:100px;text-align:center;'>
            Tempo</span>
        <span style='width:100px;text-align:center;'>
            Energy</span>
        <span style='width:100px;text-align:center;'>
            Productivity</span>
        <span style='width:80px;text-align:center;'>
            Focus</span>
    </div>
    """, unsafe_allow_html=True)

    for i,(_, row) in enumerate(
            filtered.head(20).iterrows(), 1):
        prod  = row['productivity_score']
        focus = row['focus_score']
        p_col = '#1DB954' if prod >= 7 \
                else '#B3B3B3'
        song  = str(row.get('song1','-'))
        if pd.isna(row.get('song1')):
            song = '-'
        st.markdown(f"""
        <div class='track-row'>
            <span class='track-number'>{i}</span>
            <div class='track-info'>
                <div class='track-name'
                     style='font-size:0.9rem;'>
                    {song[:45]}
                </div>
                <div class='track-artist'>
                    {row['task_type'].title()}
                    &nbsp;·&nbsp; {row['date']}
                </div>
            </div>
            <div style='width:100px;text-align:center;'>
                <span class='track-pill'>
                    {row['avg_tempo']:.0f} BPM
                </span>
            </div>
            <div style='width:100px;text-align:center;'>
                <span class='track-pill'>
                    {int(row['avg_energy']*100)}%
                </span>
            </div>
            <div style='width:100px;text-align:center;
                        font-size:1rem;font-weight:700;
                        color:{p_col};'>
                {prod:.0f}/10
            </div>
            <div style='width:80px;text-align:center;
                        font-size:0.9rem;color:#B3B3B3;'>
                {focus:.0f}/10
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── Footer ───────────────────────────────────────────────────
st.markdown("""
<hr class='sp-divider'>
<div style='display:flex;justify-content:space-between;
            align-items:center;padding:1rem 0 2rem;'>
    <div style='font-size:0.8rem;color:#B3B3B3;'>
        <span style='color:#1DB954;font-weight:700;'>
            MoodMetric
        </span>
        &nbsp;·&nbsp; Music × Productivity Analytics
    </div>
    <div style='font-size:0.75rem;color:#535353;'>
        Built with Streamlit &nbsp;·&nbsp;
        Powered by Spotify API
    </div>
</div>
""", unsafe_allow_html=True)