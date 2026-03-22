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

# ── CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Figtree:wght@300;400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Figtree', sans-serif !important;
    background : #121212 !important;
    color      : #FFFFFF !important;
}
.stApp { background: #121212 !important; }
#MainMenu, footer, header { visibility: hidden; }

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #121212; }
::-webkit-scrollbar-thumb { background: #333; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #1DB954; }

[data-testid="stSidebar"] {
    background: #000000 !important;
    border-right: none !important;
}
[data-testid="stSidebar"] * {
    color: #B3B3B3 !important;
    font-family: 'Figtree', sans-serif !important;
}
[data-testid="stSidebar"] label {
    color: #FFFFFF !important;
    font-weight: 600 !important;
}
[data-testid="stSidebar"] [data-baseweb="tag"] {
    background: #1DB954 !important;
    color: #000 !important;
}
.block-container {
    padding-top: 0 !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    max-width: none !important;
}
.stTabs [data-baseweb="tab-list"] {
    background: transparent;
    border-bottom: 1px solid #282828;
    gap: 0; padding: 0;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #B3B3B3 !important;
    font-family: 'Figtree', sans-serif !important;
    font-size: 0.8rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    padding: 1rem 1.5rem !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    border-radius: 0 !important;
}
.stTabs [data-baseweb="tab"]:hover { color: #FFFFFF !important; }
.stTabs [aria-selected="true"] {
    background: transparent !important;
    color: #FFFFFF !important;
    border-bottom: 2px solid #1DB954 !important;
}
.stButton > button {
    background: #1DB954 !important;
    color: #000000 !important;
    font-family: 'Figtree', sans-serif !important;
    font-weight: 800 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 500px !important;
    padding: 0.7rem 2rem !important;
    width: auto !important;
}
.stButton > button:hover {
    background: #1ed760 !important;
    transform: scale(1.03) !important;
}
.stSelectbox > div > div,
.stMultiSelect > div > div {
    background: #282828 !important;
    border: 1px solid #3E3E3E !important;
    border-radius: 6px !important;
    color: #FFFFFF !important;
}
.stSelectbox label, .stMultiSelect label, .stSlider label {
    color: #FFFFFF !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
}
</style>
""", unsafe_allow_html=True)

# ── Paths ────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

# ── Colors ───────────────────────────────────────────────────
G  = '#1DB954'
B  = '#4C9EEB'
P  = '#A78BFA'
A  = '#FCD34D'
C  = '#FF6B6B'
T  = '#2DD4BF'
PALETTE = [G, B, P, A, C, T]

# ── Chart theme ───────────────────────────────────────────────
# KEY FIX: legend moved to BOTTOM (y=-0.25) so it never
# overlaps the title (which sits at the top).
# Margins: t=50 for title, b=90 for bottom legend.
def sp(fig, h=400, show_legend=True):
    fig.update_layout(
        plot_bgcolor  = '#1a1a1a',
        paper_bgcolor = '#181818',
        font          = dict(family='Figtree', color='#B3B3B3', size=11),
        title_font    = dict(family='Figtree', color='#FFFFFF', size=14),
        height        = h,
        # t=50 gives title room; b=90 gives bottom legend room
        margin        = dict(t=50, b=90, l=50, r=20),
        showlegend    = show_legend,
        legend        = dict(
            bgcolor        = 'rgba(0,0,0,0)',
            bordercolor    = 'rgba(0,0,0,0)',
            font           = dict(color='#B3B3B3', size=11, family='Figtree'),
            orientation    = 'h',       # horizontal row
            yanchor        = 'top',     # anchor relative to y
            y              = -0.22,     # below the chart
            xanchor        = 'center',
            x              = 0.5        # centred
        )
    )
    fig.update_xaxes(
        gridcolor  = '#282828', linecolor = '#282828',
        tickfont   = dict(color='#B3B3B3', size=10, family='Figtree'),
        title_font = dict(color='#B3B3B3', size=11, family='Figtree')
    )
    fig.update_yaxes(
        gridcolor  = '#282828', linecolor = '#282828',
        tickfont   = dict(color='#B3B3B3', size=10, family='Figtree'),
        title_font = dict(color='#B3B3B3', size=11, family='Figtree')
    )
    return fig

# Variant for bar charts with many x-axis labels — extra bottom space
def sp_bar(fig, h=400):
    fig = sp(fig, h=h)
    fig.update_layout(
        margin = dict(t=50, b=120, l=50, r=20),
        xaxis  = dict(tickangle=-35)   # angled labels = no cut-off
    )
    return fig

# Variant for charts with no legend needed
def sp_nolegend(fig, h=400):
    return sp(fig, h=h, show_legend=False)

# ── Data ─────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv(os.path.join(DATA_DIR, 'merged_data.csv'))
    for c in ['productivity_score','focus_score','avg_tempo',
              'avg_energy','avg_valence','avg_instrumentalness',
              'avg_danceability','avg_acousticness']:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce')
    return df.dropna(subset=['productivity_score'])

@st.cache_data
def load_spotify():
    return pd.read_csv(
        os.path.join(DATA_DIR, 'dataset.csv'), encoding='utf-8')

@st.cache_resource
def load_model():
    with open(os.path.join(DATA_DIR, 'model.pkl'), 'rb') as f:
        return pickle.load(f)

df         = load_data()
df_spotify = load_spotify()
model      = load_model()

avg_prod   = df['productivity_score'].mean()
avg_focus  = df['focus_score'].mean()
total_sess = len(df)
best_task  = df.groupby('task_type')['productivity_score'].mean().idxmax()
avg_tempo  = df['avg_tempo'].mean()
avg_energy = df['avg_energy'].mean()

feat_names = ['Tempo','Energy','Valence',
              'Instrumentalness','Danceability','Acousticness']
feat_cols  = ['avg_tempo','avg_energy','avg_valence',
              'avg_instrumentalness','avg_danceability','avg_acousticness']
best_fi    = int(model.feature_importances_.argmax())
best_feat  = feat_names[best_fi] if best_fi < 6 else "Energy"

# ════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### 🎵 MoodMetric")
    st.markdown("---")

    task_filter = st.multiselect(
        "FILTERS — Task Types",
        options = df['task_type'].unique().tolist(),
        default = df['task_type'].unique().tolist()
    )

    st.markdown("---")
    st.markdown("**Avg Audio Profile**")

    for label, val, mx, clr in [
        ("Energy",       df['avg_energy'].mean(),          1, G),
        ("Valence",      df['avg_valence'].mean(),          1, B),
        ("Instrumental", df['avg_instrumentalness'].mean(), 1, P),
        ("Danceability", df['avg_danceability'].mean(),     1, A),
    ]:
        pct = min(int((val / mx) * 100), 100)
        st.markdown(
            f"<div style='margin-bottom:10px;'>"
            f"<div style='display:flex;justify-content:space-between;"
            f"font-size:0.75rem;color:#B3B3B3;margin-bottom:3px;'>"
            f"<span>{label}</span>"
            f"<span style='color:{clr};font-weight:700;'>{pct}%</span>"
            f"</div>"
            f"<div style='background:#282828;border-radius:4px;height:3px;'>"
            f"<div style='width:{pct}%;height:3px;background:{clr};"
            f"border-radius:4px;'></div></div></div>",
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.markdown("**Quick Stats**")
    for lbl, val, clr in [
        ("Sessions",        str(total_sess),      G),
        ("Avg Productivity",f"{avg_prod:.1f}/10",  B),
        ("Avg Focus",       f"{avg_focus:.1f}/10", P),
        ("Best Task",       best_task.title(),     A),
    ]:
        st.markdown(
            f"<div style='display:flex;justify-content:space-between;"
            f"padding:5px 0;border-bottom:1px solid #1e1e1e;'>"
            f"<span style='font-size:0.78rem;color:#B3B3B3;'>{lbl}</span>"
            f"<span style='font-size:0.78rem;font-weight:700;"
            f"color:{clr};'>{val}</span></div>",
            unsafe_allow_html=True
        )

# ── Filtered data ────────────────────────────────────────────
dff = df[df['task_type'].isin(task_filter)]

# ════════════════════════════════════════════════════════════
# HERO
# ════════════════════════════════════════════════════════════
st.markdown(
    "<div style='background:linear-gradient("
    "180deg,#1a5c35 0%,#0f3320 45%,#121212 100%);"
    "padding:3rem 2.5rem 2.5rem;"
    "margin:-1rem -2rem 1.5rem;"
    "position:relative;overflow:hidden;'>"
    "<div style='position:absolute;top:-50px;right:-30px;"
    "width:320px;height:320px;"
    "background:radial-gradient(circle,rgba(29,185,84,0.1) 0%,"
    "transparent 65%);pointer-events:none;'></div>"
    "<div style='font-size:0.68rem;font-weight:700;"
    "letter-spacing:0.18em;text-transform:uppercase;"
    "color:#1DB954;margin-bottom:0.6rem;'>"
    "&#9679; Verified Analytics</div>"
    "<div style='font-size:3.8rem;font-weight:900;color:#FFFFFF;"
    "line-height:1;letter-spacing:-2px;margin-bottom:1rem;'>"
    "MoodMetric</div>"
    f"<div style='display:flex;align-items:center;gap:1.2rem;"
    f"flex-wrap:wrap;margin-bottom:1.25rem;'>"
    f"<span style='font-size:0.88rem;color:#B3B3B3;'>"
    f"&#127911; <strong style='color:#fff;'>{total_sess}</strong> sessions</span>"
    f"<span style='color:#535353;'>&#9679;</span>"
    f"<span style='font-size:0.88rem;color:#B3B3B3;'>"
    f"&#9889; <strong style='color:#fff;'>{avg_prod:.1f}/10</strong> avg productivity</span>"
    f"<span style='color:#535353;'>&#9679;</span>"
    f"<span style='font-size:0.88rem;color:#B3B3B3;'>"
    f"&#127942; Best at <strong style='color:#fff;'>{best_task.title()}</strong></span>"
    f"<span style='color:#535353;'>&#9679;</span>"
    f"<span style='font-size:0.88rem;color:#B3B3B3;'>"
    f"&#9835; <strong style='color:#fff;'>{avg_tempo:.0f} BPM</strong> avg</span>"
    f"</div>"
    f"<span style='display:inline-block;background:rgba(29,185,84,0.15);"
    f"border:1px solid rgba(29,185,84,0.3);color:#1DB954;"
    f"border-radius:500px;padding:4px 14px;font-size:0.78rem;"
    f"font-weight:600;margin:3px;'>&#127919; {best_feat}</span>"
    f"<span style='display:inline-block;background:rgba(76,158,235,0.12);"
    f"border:1px solid rgba(76,158,235,0.25);color:#4C9EEB;"
    f"border-radius:500px;padding:4px 14px;font-size:0.78rem;"
    f"font-weight:600;margin:3px;'>"
    f"&#9889; {int(avg_energy*100)}% Energy</span>"
    f"<span style='display:inline-block;background:rgba(167,139,250,0.12);"
    f"border:1px solid rgba(167,139,250,0.25);color:#A78BFA;"
    f"border-radius:500px;padding:4px 14px;font-size:0.78rem;"
    f"font-weight:600;margin:3px;'>&#127942; {best_task.title()}</span>"
    f"<span style='display:inline-block;background:rgba(252,211,77,0.12);"
    f"border:1px solid rgba(252,211,77,0.25);color:#FCD34D;"
    f"border-radius:500px;padding:4px 14px;font-size:0.78rem;"
    f"font-weight:600;margin:3px;'>&#128202; {total_sess} Sessions</span>"
    "</div>",
    unsafe_allow_html=True
)

# ── Stat cards ───────────────────────────────────────────────
def stat_card(icon, value, label, sub, clr, bg):
    return (
        f"<div style='background:#181818;border:1px solid #282828;"
        f"border-radius:10px;padding:1.3rem;position:relative;"
        f"overflow:hidden;height:100%;'>"
        f"<div style='position:absolute;top:0;left:0;right:0;"
        f"height:2px;background:linear-gradient(90deg,{clr},transparent);'></div>"
        f"<div style='width:36px;height:36px;border-radius:8px;"
        f"background:{bg};display:flex;align-items:center;"
        f"justify-content:center;font-size:1rem;margin-bottom:0.8rem;'>{icon}</div>"
        f"<div style='font-size:1.9rem;font-weight:800;color:{clr};"
        f"line-height:1;margin-bottom:0.25rem;'>{value}</div>"
        f"<div style='font-size:0.8rem;color:#B3B3B3;font-weight:500;'>{label}</div>"
        f"<div style='font-size:0.7rem;color:#535353;margin-top:0.25rem;'>{sub}</div>"
        f"</div>"
    )

sc1, sc2, sc3, sc4 = st.columns(4)
sc1.markdown(stat_card("🎧", str(total_sess),   "Sessions Logged",  "All time",          G, "rgba(29,185,84,0.12)"),  unsafe_allow_html=True)
sc2.markdown(stat_card("⚡", f"{avg_prod:.1f}", "Avg Productivity", "Out of 10",         B, "rgba(76,158,235,0.12)"), unsafe_allow_html=True)
sc3.markdown(stat_card("🎯", f"{avg_focus:.1f}","Avg Focus Score",  "Out of 10",         P, "rgba(167,139,250,0.12)"),unsafe_allow_html=True)
sc4.markdown(stat_card("🏆", best_task.title(), "Best Task Type",   "Highest avg score", A, "rgba(252,211,77,0.12)"), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# TABS
# ════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4 = st.tabs([
    "Analytics", "Your Playlist", "Predict", "History"
])

# ════════════════════════════════════════════════════════════
# TAB 1 — ANALYTICS
# ════════════════════════════════════════════════════════════
with tab1:

    corr_e = dff['avg_energy'].corr(dff['productivity_score'])
    corr_v = dff['avg_valence'].corr(dff['productivity_score'])
    dir_e  = "positively" if corr_e > 0 else "negatively"

    st.markdown(
        f"<div style='background:#181818;border-left:3px solid #1DB954;"
        f"border-radius:0 8px 8px 0;padding:1.1rem 1.4rem;margin-bottom:1.5rem;'>"
        f"<div style='font-size:0.62rem;font-weight:700;letter-spacing:0.14em;"
        f"text-transform:uppercase;color:#1DB954;margin-bottom:0.35rem;'>Key Insight</div>"
        f"<div style='font-size:0.9rem;color:#E0E0E0;line-height:1.65;'>"
        f"Your productivity is most influenced by "
        f"<strong style='color:#1DB954;'>{best_feat}</strong>. "
        f"Energy {dir_e} correlates "
        f"(<strong style='color:#fff;'>r = {corr_e:.2f}</strong>), "
        f"valence shows <strong style='color:#fff;'>r = {corr_v:.2f}</strong>. "
        f"You perform best during "
        f"<strong style='color:#1DB954;'>{best_task.title()}</strong> sessions."
        f"</div></div>",
        unsafe_allow_html=True
    )

    # ── Charts 1 & 2: Scatter ────────────────────────────────
    st.markdown(
        "<div style='font-size:1.15rem;font-weight:700;color:#FFFFFF;"
        "margin-bottom:0.75rem;'>Energy &amp; Valence vs Productivity</div>",
        unsafe_allow_html=True
    )

    cc1, cc2 = st.columns(2)

    with cc1:
        fig1 = px.scatter(
            dff,
            x         = 'avg_energy',
            y         = 'productivity_score',
            color     = 'task_type',
            size      = 'avg_tempo',
            size_max  = 15,
            trendline = 'ols',
            title     = 'Energy vs Productivity',
            labels    = {
                'avg_energy'        : 'Energy',
                'productivity_score': 'Productivity',
                'task_type'         : 'Task',
                'avg_tempo'         : 'Tempo'
            },
            color_discrete_sequence = PALETTE,
            opacity   = 0.85
        )
        for trace in fig1.data:
            if hasattr(trace, 'mode') and trace.mode and 'markers' in trace.mode:
                trace.marker.line = dict(width=0)
        st.plotly_chart(sp(fig1, h=420), use_container_width=True)

    with cc2:
        fig2 = px.scatter(
            dff,
            x         = 'avg_valence',
            y         = 'productivity_score',
            color     = 'task_type',
            size      = 'avg_instrumentalness',
            size_max  = 15,
            trendline = 'ols',
            title     = 'Valence vs Productivity',
            labels    = {
                'avg_valence'       : 'Valence (Mood)',
                'productivity_score': 'Productivity',
                'task_type'         : 'Task'
            },
            color_discrete_sequence = PALETTE,
            opacity   = 0.85
        )
        for trace in fig2.data:
            if hasattr(trace, 'mode') and trace.mode and 'markers' in trace.mode:
                trace.marker.line = dict(width=0)
        st.plotly_chart(sp(fig2, h=420), use_container_width=True)

    # ── Chart 3: Feature Importance ──────────────────────────
    st.markdown(
        "<div style='font-size:1.15rem;font-weight:700;color:#FFFFFF;"
        "margin:0.5rem 0 0.75rem;'>Feature Impact on Your Productivity</div>",
        unsafe_allow_html=True
    )

    imp_df = pd.DataFrame({
        'Feature'   : feat_names,
        'Importance': model.feature_importances_.tolist()
    }).sort_values('Importance', ascending=True)

    fig3 = px.bar(
        imp_df,
        x           = 'Importance',
        y           = 'Feature',
        orientation = 'h',
        title       = 'What drives your productivity most?',
        color       = 'Feature',
        color_discrete_sequence = PALETTE,
        labels      = {'Importance':'Impact Score', 'Feature':''}
    )
    fig3.update_traces(marker_line_width=0)
    fig3.update_layout(showlegend=False)
    # No legend needed here — labels are on y-axis
    st.plotly_chart(sp_nolegend(fig3, h=340), use_container_width=True)

    # ── Charts 4 & 5: Task bar + Tempo histogram ─────────────
    cc3, cc4 = st.columns(2)

    with cc3:
        st.markdown(
            "<div style='font-size:1.15rem;font-weight:700;color:#FFFFFF;"
            "margin:0.5rem 0 0.75rem;'>Score by Task Type</div>",
            unsafe_allow_html=True
        )
        task_avg = dff.groupby('task_type').agg(
            Productivity = ('productivity_score','mean'),
            Focus        = ('focus_score','mean')
        ).reset_index()

        fig4 = go.Figure()
        fig4.add_trace(go.Bar(
            name              = 'Productivity',
            x                 = task_avg['task_type'],
            y                 = task_avg['Productivity'],
            marker_color      = G,
            marker_line_width = 0,
            hovertemplate     = '<b>%{x}</b><br>Productivity: %{y:.1f}<extra></extra>'
        ))
        fig4.add_trace(go.Bar(
            name              = 'Focus',
            x                 = task_avg['task_type'],
            y                 = task_avg['Focus'],
            marker_color      = B,
            marker_line_width = 0,
            hovertemplate     = '<b>%{x}</b><br>Focus: %{y:.1f}<extra></extra>'
        ))
        fig4.update_layout(
            barmode    = 'group',
            title      = 'Avg Scores by Task',
            yaxis_range= [0, 10]
        )
        # sp_bar: angled x labels + extra bottom margin for legend+labels
        st.plotly_chart(sp_bar(fig4, h=400), use_container_width=True)

    with cc4:
        st.markdown(
            "<div style='font-size:1.15rem;font-weight:700;color:#FFFFFF;"
            "margin:0.5rem 0 0.75rem;'>Tempo Distribution</div>",
            unsafe_allow_html=True
        )
        dff2          = dff.copy()
        dff2['Level'] = dff2['productivity_score'].apply(
            lambda x: 'High (7+)' if x >= 7 else 'Low (<7)')

        fig5 = px.histogram(
            dff2,
            x       = 'avg_tempo',
            color   = 'Level',
            nbins   = 14,
            barmode = 'overlay',
            opacity = 0.82,
            title   = 'Tempo: High vs Low Productivity',
            labels  = {'avg_tempo':'Tempo (BPM)'},
            color_discrete_map = {'High (7+)': G, 'Low (<7)': C}
        )
        fig5.update_traces(marker_line_width=0)
        st.plotly_chart(sp(fig5, h=400), use_container_width=True)

    # ── Chart 6: Radar ───────────────────────────────────────
    st.markdown(
        "<div style='font-size:1.15rem;font-weight:700;color:#FFFFFF;"
        "margin:0.5rem 0 0.75rem;'>Audio Fingerprint by Task Type</div>",
        unsafe_allow_html=True
    )

    radar_cols = ['avg_energy','avg_valence',
                  'avg_danceability','avg_acousticness',
                  'avg_instrumentalness']
    radar_labs = ['Energy','Valence',
                  'Danceability','Acousticness','Instrumentalness']

    clr_map = {
        'coding' : (G,  29,  185, 84),
        'reading': (B,  76,  158, 235),
        'writing': (P,  167, 139, 250),
        'design' : (A,  252, 211, 77),
        'other'  : (C,  255, 107, 107),
    }

    fig6 = go.Figure()
    for i, (task_name, grp) in enumerate(dff.groupby('task_type')):
        vals = [grp[c].mean() for c in radar_cols]
        vals.append(vals[0])
        labs = radar_labs + [radar_labs[0]]

        if task_name in clr_map:
            hex_c, rr, gg, bb = clr_map[task_name]
        else:
            hex_c = PALETTE[i % len(PALETTE)]
            rr = int(hex_c[1:3], 16)
            gg = int(hex_c[3:5], 16)
            bb = int(hex_c[5:7], 16)

        fig6.add_trace(go.Scatterpolar(
            r         = vals,
            theta     = labs,
            fill      = 'toself',
            name      = task_name.title(),
            line      = dict(color=hex_c, width=2),
            fillcolor = f'rgba({rr},{gg},{bb},0.1)'
        ))

    fig6.update_layout(
        plot_bgcolor  = '#1a1a1a',
        paper_bgcolor = '#181818',
        height        = 460,
        title         = dict(
            text      = 'Audio features per task type',
            font      = dict(color='#FFFFFF', size=14, family='Figtree'),
            y         = 0.97,
            x         = 0.5,
            xanchor   = 'center'
        ),
        margin        = dict(t=60, b=20, l=60, r=60),
        polar         = dict(
            bgcolor     = '#1a1a1a',
            radialaxis  = dict(
                visible   = True,
                range     = [0, 1],
                gridcolor = '#2a2a2a',
                linecolor = '#2a2a2a',
                tickfont  = dict(color='#535353', size=9, family='Figtree'),
                tickmode  = 'linear',
                tick0     = 0,
                dtick     = 0.25
            ),
            angularaxis = dict(
                gridcolor = '#2a2a2a',
                linecolor = '#2a2a2a',
                tickfont  = dict(color='#B3B3B3', size=11, family='Figtree')
            )
        ),
        legend = dict(
            font    = dict(color='#B3B3B3', size=11, family='Figtree'),
            bgcolor = 'rgba(0,0,0,0)',
            orientation = 'h',
            yanchor     = 'top',
            y           = -0.05,
            xanchor     = 'center',
            x           = 0.5
        )
    )
    st.plotly_chart(fig6, use_container_width=True)

# ════════════════════════════════════════════════════════════
# TAB 2 — PLAYLIST
# ════════════════════════════════════════════════════════════
with tab2:
    st.markdown(
        "<div style='font-size:1.4rem;font-weight:700;color:#FFFFFF;"
        "margin-bottom:1.25rem;'>Build Your Focus Playlist</div>",
        unsafe_allow_html=True
    )

    pc1, pc2, pc3 = st.columns([2, 1, 1])
    with pc1:
        task = st.selectbox("Activity",
            ["coding","reading","writing","design","other"])
    with pc2:
        num_songs = st.slider("Songs", 5, 30, 15)
    with pc3:
        st.markdown("<br>", unsafe_allow_html=True)
        gen_btn = st.button("Generate Playlist")

    profiles = {
        'coding' : [('Instrumental','70-100%',G),('Energy','30-70%',B),('Tempo','80-120 BPM',P)],
        'reading': [('Instrumental','60-100%',G),('Energy','10-50%',B),('Tempo','60-95 BPM',P)],
        'writing': [('Instrumental','30-90%',G),('Energy','20-60%',B),('Tempo','70-110 BPM',P)],
        'design' : [('Instrumental','30-80%',G),('Energy','40-80%',B),('Tempo','90-130 BPM',P)],
        'other'  : [('Instrumental','30-90%',G),('Energy','30-70%',B),('Tempo','75-115 BPM',P)],
    }
    chips = []
    for k, v, clr in profiles[task]:
        rr = int(clr[1:3], 16); gg = int(clr[3:5], 16); bb = int(clr[5:7], 16)
        chips.append(
            f"<span style='display:inline-block;"
            f"background:rgba({rr},{gg},{bb},0.12);"
            f"border:1px solid rgba({rr},{gg},{bb},0.3);"
            f"color:{clr};border-radius:500px;"
            f"padding:4px 12px;font-size:0.78rem;"
            f"font-weight:600;margin:3px;'>{k}: {v}</span>"
        )
    st.markdown(
        "<div style='margin:0.75rem 0 1.5rem;'>" + "".join(chips) + "</div>",
        unsafe_allow_html=True
    )

    if gen_btn:
        rngs = {
            'coding' : {'instrumentalness':(0.4,1.0),'energy':(0.3,0.7),'tempo':(80,120)},
            'reading': {'instrumentalness':(0.6,1.0),'energy':(0.1,0.5),'tempo':(60,95)},
            'writing': {'instrumentalness':(0.3,0.9),'energy':(0.2,0.6),'tempo':(70,110)},
            'design' : {'instrumentalness':(0.3,0.8),'energy':(0.4,0.8),'tempo':(90,130)},
            'other'  : {'instrumentalness':(0.3,0.9),'energy':(0.3,0.7),'tempo':(75,115)},
        }
        r    = rngs[task]
        mask = (
            df_spotify['instrumentalness'].between(*r['instrumentalness']) &
            df_spotify['energy'].between(*r['energy']) &
            df_spotify['tempo'].between(*r['tempo'])
        )
        pl = df_spotify[mask][
            ['track_name','artists','tempo','energy','valence','instrumentalness']
        ].drop_duplicates(subset='track_name').head(num_songs)

        st.markdown(
            f"<div style='display:flex;align-items:flex-end;gap:1.25rem;"
            f"padding:1.5rem 0 1rem;border-bottom:1px solid #282828;"
            f"margin-bottom:0.5rem;'>"
            f"<div style='width:82px;height:82px;"
            f"background:linear-gradient(135deg,#1DB954,#0d6e32);"
            f"border-radius:6px;display:flex;align-items:center;"
            f"justify-content:center;font-size:2rem;flex-shrink:0;'>"
            f"&#127925;</div>"
            f"<div>"
            f"<div style='font-size:0.62rem;font-weight:700;"
            f"letter-spacing:0.14em;text-transform:uppercase;"
            f"color:#B3B3B3;margin-bottom:0.2rem;'>Playlist</div>"
            f"<div style='font-size:1.8rem;font-weight:800;"
            f"color:#FFFFFF;line-height:1.1;margin-bottom:0.3rem;'>"
            f"Focus: {task.title()}</div>"
            f"<div style='font-size:0.82rem;color:#B3B3B3;'>"
            f"MoodMetric &nbsp;&middot;&nbsp; {len(pl)} songs</div>"
            f"</div></div>",
            unsafe_allow_html=True
        )

        st.markdown(
            "<div style='display:grid;"
            "grid-template-columns:28px 1fr 72px 90px 70px 100px;"
            "gap:8px;padding:5px 10px;"
            "font-size:0.62rem;font-weight:700;"
            "letter-spacing:0.12em;text-transform:uppercase;"
            "color:#B3B3B3;border-bottom:1px solid #282828;"
            "margin-bottom:3px;'>"
            "<span>#</span><span>Title</span>"
            "<span style='text-align:center;'>BPM</span>"
            "<span style='text-align:center;'>Energy</span>"
            "<span style='text-align:center;'>Mood</span>"
            "<span style='text-align:center;'>Type</span>"
            "</div>",
            unsafe_allow_html=True
        )

        for idx, (_, row) in enumerate(pl.iterrows(), 1):
            e   = float(row['energy'])
            v   = float(row['valence'])
            ins = float(row['instrumentalness'])
            bpm = int(row['tempo'])

            if e < 0.4:
                e_bg, e_cl, e_txt = 'rgba(29,185,84,0.15)',  G, f"{int(e*100)}% Low"
            elif e < 0.7:
                e_bg, e_cl, e_txt = 'rgba(76,158,235,0.15)', B, f"{int(e*100)}% Mid"
            else:
                e_bg, e_cl, e_txt = 'rgba(252,211,77,0.15)', A, f"{int(e*100)}% High"

            if v < 0.4:
                v_bg, v_cl, v_txt = 'rgba(167,139,250,0.15)', P, f"{int(v*100)}%"
            elif v < 0.7:
                v_bg, v_cl, v_txt = 'rgba(76,158,235,0.15)',  B, f"{int(v*100)}%"
            else:
                v_bg, v_cl, v_txt = 'rgba(252,211,77,0.15)',  A, f"{int(v*100)}%"

            if ins > 0.6:
                t_bg, t_cl, t_txt = 'rgba(29,185,84,0.15)',   G, 'Instrumental'
            else:
                t_bg, t_cl, t_txt = 'rgba(167,139,250,0.15)', P, 'Vocal'

            def pk(bg, cl, txt):
                return (f"<span style='background:{bg};color:{cl};"
                        f"border-radius:500px;padding:3px 8px;"
                        f"font-size:0.7rem;font-weight:600;"
                        f"white-space:nowrap;'>{txt}</span>")

            st.markdown(
                f"<div style='display:grid;"
                f"grid-template-columns:28px 1fr 72px 90px 70px 100px;"
                f"gap:8px;align-items:center;padding:7px 10px;"
                f"border-radius:5px;margin:1px 0;'>"
                f"<span style='font-size:0.82rem;color:#B3B3B3;text-align:center;'>{idx}</span>"
                f"<div style='overflow:hidden;'>"
                f"<div style='font-size:0.88rem;font-weight:600;color:#FFFFFF;"
                f"white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>"
                f"{str(row['track_name'])[:34]}</div>"
                f"<div style='font-size:0.73rem;color:#B3B3B3;margin-top:1px;"
                f"white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>"
                f"{str(row['artists'])[:24]}</div></div>"
                f"<div style='text-align:center;'>"
                f"<span style='background:#282828;color:#FFFFFF;border-radius:500px;"
                f"padding:3px 8px;font-size:0.7rem;font-weight:500;'>{bpm}</span></div>"
                f"<div style='text-align:center;'>{pk(e_bg,e_cl,e_txt)}</div>"
                f"<div style='text-align:center;'>{pk(v_bg,v_cl,v_txt)}</div>"
                f"<div style='text-align:center;'>{pk(t_bg,t_cl,t_txt)}</div>"
                f"</div>",
                unsafe_allow_html=True
            )

# ════════════════════════════════════════════════════════════
# TAB 3 — PREDICT
# ════════════════════════════════════════════════════════════
with tab3:
    st.markdown(
        "<div style='font-size:1.4rem;font-weight:700;color:#FFFFFF;"
        "margin-bottom:0.5rem;'>Predict Your Productivity Score</div>"
        "<p style='font-size:0.88rem;color:#B3B3B3;line-height:1.65;"
        "margin-bottom:2rem;'>Set the audio features of music you plan "
        "to listen to. The model predicts your productivity score based "
        "on your personal session history.</p>",
        unsafe_allow_html=True
    )

    ps1, ps2, ps3 = st.columns(3)
    with ps1:
        st.markdown(
            f"<div style='font-size:0.7rem;font-weight:700;"
            f"letter-spacing:0.14em;text-transform:uppercase;"
            f"color:{G};margin-bottom:0.5rem;'>Rhythm</div>",
            unsafe_allow_html=True)
        tempo   = st.slider("Tempo (BPM)",   60, 200, 100)
        energy  = st.slider("Energy",        0.0, 1.0, 0.5, step=0.01)

    with ps2:
        st.markdown(
            f"<div style='font-size:0.7rem;font-weight:700;"
            f"letter-spacing:0.14em;text-transform:uppercase;"
            f"color:{B};margin-bottom:0.5rem;'>Mood</div>",
            unsafe_allow_html=True)
        valence          = st.slider("Valence",          0.0, 1.0, 0.5, step=0.01)
        instrumentalness = st.slider("Instrumentalness", 0.0, 1.0, 0.5, step=0.01)

    with ps3:
        st.markdown(
            f"<div style='font-size:0.7rem;font-weight:700;"
            f"letter-spacing:0.14em;text-transform:uppercase;"
            f"color:{P};margin-bottom:0.5rem;'>Texture</div>",
            unsafe_allow_html=True)
        danceability = st.slider("Danceability", 0.0, 1.0, 0.5, step=0.01)
        acousticness = st.slider("Acousticness", 0.0, 1.0, 0.5, step=0.01)

    st.markdown("<br>", unsafe_allow_html=True)
    bc, _ = st.columns([1, 4])
    with bc:
        pred_btn = st.button("Predict Score")

    if pred_btn:
        inp  = pd.DataFrame([{
            'avg_tempo'           : tempo,
            'avg_energy'          : energy,
            'avg_valence'         : valence,
            'avg_instrumentalness': instrumentalness,
            'avg_danceability'    : danceability,
            'avg_acousticness'    : acousticness
        }])
        pred = float(model.predict(inp)[0])
        pred = round(min(max(pred, 1), 10), 1)

        if pred >= 7:
            sc = G; ico = '✅'; stat = 'High Productivity Zone'
            desc = 'Great. This profile aligns with your best sessions.'
        elif pred >= 5:
            sc = A; ico = '⚡'; stat = 'Moderate Productivity'
            desc = 'Decent focus expected. Try raising instrumentalness.'
        else:
            sc = C; ico = '⚠️'; stat = 'Low Productivity Zone'
            desc = 'This may distract. Try calmer, instrumental tracks.'

        rc, gc = st.columns(2)

        with rc:
            st.markdown(
                f"<div style='background:#181818;border:1px solid #282828;"
                f"border-radius:12px;padding:2.5rem 2rem;text-align:center;'>"
                f"<div style='font-size:0.65rem;font-weight:700;"
                f"letter-spacing:0.16em;text-transform:uppercase;"
                f"color:#535353;margin-bottom:0.75rem;'>Predicted Score</div>"
                f"<div style='font-size:6rem;font-weight:900;line-height:1;"
                f"letter-spacing:-3px;color:{sc};'>{pred}</div>"
                f"<div style='font-size:1.1rem;color:#535353;margin-bottom:1.25rem;'>/ 10</div>"
                f"<hr style='border:none;border-top:1px solid #282828;margin:0 0 1rem;'>"
                f"<div style='font-size:1rem;font-weight:700;color:{sc};"
                f"margin-bottom:0.4rem;'>{ico} {stat}</div>"
                f"<div style='font-size:0.84rem;color:#B3B3B3;line-height:1.6;'>{desc}</div>"
                f"</div>",
                unsafe_allow_html=True
            )

        with gc:
            gauge = go.Figure(go.Indicator(
                mode   = "gauge+number",
                value  = pred,
                title  = {'text':'Score',
                          'font':{'color':'#B3B3B3','family':'Figtree','size':13}},
                number = {'font':{'color':sc,'family':'Figtree','size':52},
                          'suffix':'/10'},
                gauge  = {
                    'axis': {'range':[0,10],
                             'tickfont':{'color':'#535353','family':'Figtree'}},
                    'bar' : {'color':sc,'thickness':0.2},
                    'bgcolor'    : 'rgba(0,0,0,0)',
                    'bordercolor': 'rgba(0,0,0,0)',
                    'steps': [
                        {'range':[0,4],  'color':'rgba(255,107,107,0.08)'},
                        {'range':[4,7],  'color':'rgba(252,211,77,0.08)'},
                        {'range':[7,10], 'color':'rgba(29,185,84,0.08)'}
                    ],
                    'threshold': {'line':{'color':sc,'width':2},'value':pred}
                }
            ))
            gauge.update_layout(
                paper_bgcolor = '#181818',
                height        = 310,
                margin        = dict(t=50, b=20, l=30, r=30),
                font          = dict(family='Figtree', color='#B3B3B3')
            )
            st.plotly_chart(gauge, use_container_width=True)

        st.markdown(
            "<div style='font-size:1.1rem;font-weight:700;color:#FFFFFF;"
            "margin:1.5rem 0 0.75rem;'>Your Input Audio Profile</div>",
            unsafe_allow_html=True
        )
        for bname, bval, bclr in [
            ('Tempo',           tempo / 200,   G),
            ('Energy',          energy,        B),
            ('Valence',         valence,       P),
            ('Instrumentalness',instrumentalness, A),
            ('Danceability',    danceability,  T),
            ('Acousticness',    acousticness,  C),
        ]:
            pct = int(bval * 100)
            st.markdown(
                f"<div style='display:flex;align-items:center;gap:12px;margin:7px 0;'>"
                f"<span style='font-size:0.8rem;color:#B3B3B3;min-width:115px;"
                f"text-align:right;font-weight:500;'>{bname}</span>"
                f"<div style='flex:1;background:#282828;border-radius:4px;height:4px;'>"
                f"<div style='width:{pct}%;height:4px;background:{bclr};"
                f"border-radius:4px;'></div></div>"
                f"<span style='font-size:0.78rem;color:{bclr};min-width:34px;"
                f"text-align:right;font-weight:700;'>{pct}%</span></div>",
                unsafe_allow_html=True
            )

# ════════════════════════════════════════════════════════════
# TAB 4 — HISTORY
# ════════════════════════════════════════════════════════════
with tab4:
    hc1, hc2 = st.columns(2)
    with hc1:
        tasks    = ['All'] + df['task_type'].unique().tolist()
        selected = st.selectbox("Filter by Task", tasks)
    with hc2:
        min_sc = st.slider("Min Productivity Score", 1, 10, 1)

    flt = df.copy()
    if selected != 'All':
        flt = flt[flt['task_type'] == selected]
    flt = flt[flt['productivity_score'] >= min_sc]

    m1, m2, m3, m4 = st.columns(4)
    for col, val, lbl, clr in [
        (m1, str(len(flt)),                             "Sessions",        G),
        (m2, f"{flt['productivity_score'].mean():.1f}", "Avg Productivity", B),
        (m3, f"{flt['focus_score'].mean():.1f}",        "Avg Focus",       P),
        (m4, f"{flt['avg_tempo'].mean():.0f} BPM",      "Avg Tempo",       A),
    ]:
        col.markdown(
            f"<div style='background:#181818;border:1px solid #282828;"
            f"border-radius:8px;padding:1rem 1.1rem;'>"
            f"<div style='font-size:1.55rem;font-weight:800;color:{clr};"
            f"line-height:1;margin-bottom:0.2rem;'>{val}</div>"
            f"<div style='font-size:0.78rem;color:#B3B3B3;'>{lbl}</div>"
            f"</div>",
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        "<div style='font-size:1.15rem;font-weight:700;color:#FFFFFF;"
        "margin-bottom:0.75rem;'>Productivity &amp; Focus Over Time</div>",
        unsafe_allow_html=True
    )

    fig7 = go.Figure()
    idx_list = list(range(len(flt)))
    fig7.add_trace(go.Scatter(
        x    = idx_list,
        y    = flt['productivity_score'].values.tolist(),
        name = 'Productivity',
        mode = 'lines+markers',
        line = dict(color=G, width=2.5),
        marker = dict(color=G, size=7, line=dict(color='#121212', width=1.5)),
        hovertemplate = 'Session %{x}<br>Productivity: %{y:.1f}<extra></extra>'
    ))
    fig7.add_trace(go.Scatter(
        x    = idx_list,
        y    = flt['focus_score'].values.tolist(),
        name = 'Focus',
        mode = 'lines+markers',
        line = dict(color=B, width=2.5, dash='dot'),
        marker = dict(color=B, size=7, line=dict(color='#121212', width=1.5)),
        hovertemplate = 'Session %{x}<br>Focus: %{y:.1f}<extra></extra>'
    ))
    fig7.update_layout(title='Session performance over time', yaxis_range=[0, 10])
    st.plotly_chart(sp(fig7), use_container_width=True)

    st.markdown(
        "<div style='font-size:1.15rem;font-weight:700;color:#FFFFFF;"
        "margin:0.5rem 0 0.75rem;'>All Sessions</div>"
        "<div style='display:grid;"
        "grid-template-columns:26px 1fr 80px 80px 80px 70px;"
        "gap:8px;padding:5px 10px;"
        "font-size:0.62rem;font-weight:700;"
        "letter-spacing:0.12em;text-transform:uppercase;"
        "color:#B3B3B3;border-bottom:1px solid #282828;margin-bottom:3px;'>"
        "<span>#</span><span>Song &middot; Task</span>"
        "<span style='text-align:center;'>Tempo</span>"
        "<span style='text-align:center;'>Energy</span>"
        "<span style='text-align:center;'>Score</span>"
        "<span style='text-align:center;'>Focus</span>"
        "</div>",
        unsafe_allow_html=True
    )

    for i, (_, row) in enumerate(flt.head(25).iterrows(), 1):
        prod  = float(row['productivity_score'])
        focus = float(row['focus_score'])
        bpm   = float(row['avg_tempo'])
        eng   = float(row['avg_energy'])
        song  = str(row.get('song1', '—'))
        if pd.isna(row.get('song1')):
            song = '—'
        tsk = row['task_type'].title()
        dt  = str(row['date'])[:10]

        s_clr = G if prod >= 7 else A if prod >= 5 else C
        e_clr = G if eng < 0.4 else B if eng < 0.7 else A

        def mpill(clr, txt):
            rr = int(clr[1:3], 16); gg = int(clr[3:5], 16); bb = int(clr[5:7], 16)
            return (f"<span style='background:rgba({rr},{gg},{bb},0.14);color:{clr};"
                    f"border-radius:500px;padding:3px 8px;font-size:0.7rem;"
                    f"font-weight:600;white-space:nowrap;'>{txt}</span>")

        st.markdown(
            f"<div style='display:grid;"
            f"grid-template-columns:26px 1fr 80px 80px 80px 70px;"
            f"gap:8px;align-items:center;padding:7px 10px;"
            f"border-radius:5px;margin:1px 0;'>"
            f"<span style='font-size:0.8rem;color:#B3B3B3;text-align:center;'>{i}</span>"
            f"<div style='overflow:hidden;'>"
            f"<div style='font-size:0.87rem;font-weight:600;color:#FFFFFF;"
            f"white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>{song[:38]}</div>"
            f"<div style='font-size:0.73rem;color:#B3B3B3;margin-top:1px;'>"
            f"{tsk} &middot; {dt}</div></div>"
            f"<div style='text-align:center;'>"
            f"<span style='background:#282828;color:#FFFFFF;border-radius:500px;"
            f"padding:3px 8px;font-size:0.7rem;font-weight:500;'>{bpm:.0f}</span></div>"
            f"<div style='text-align:center;'>{mpill(e_clr, f'{int(eng*100)}%')}</div>"
            f"<div style='text-align:center;font-size:0.92rem;font-weight:700;"
            f"color:{s_clr};'>{prod:.0f}/10</div>"
            f"<div style='text-align:center;font-size:0.87rem;color:#B3B3B3;'>"
            f"{focus:.0f}/10</div></div>",
            unsafe_allow_html=True
        )

# ── Footer ───────────────────────────────────────────────────
st.markdown(
    "<div style='border-top:1px solid #282828;margin-top:2rem;"
    "display:flex;justify-content:space-between;align-items:center;"
    "padding:1rem 0 2rem;'>"
    "<div style='font-size:0.8rem;color:#535353;'>"
    "<span style='color:#1DB954;font-weight:700;'>MoodMetric</span>"
    " &nbsp;&middot;&nbsp; Music &times; Productivity Analytics</div>"
    "<div style='font-size:0.72rem;color:#333;'>"
    "Streamlit &nbsp;&middot;&nbsp; Spotify API"
    " &nbsp;&middot;&nbsp; scikit-learn</div></div>",
    unsafe_allow_html=True
)