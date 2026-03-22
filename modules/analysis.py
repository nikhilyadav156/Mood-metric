import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

MERGED_FILE = 'data/merged_data.csv'

# ── Load Data ────────────────────────────────────────────────
def load_data():
    df = pd.read_csv(MERGED_FILE)

    numeric_cols = ['avg_tempo', 'avg_energy',
                    'avg_valence', 'avg_instrumentalness',
                    'avg_danceability', 'avg_acousticness',
                    'productivity_score', 'focus_score']

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col],
                                     errors='coerce')

    df = df.dropna(subset=['productivity_score'])
    print(f"✅ Loaded {len(df)} sessions")
    return df

# ── Plot 1: Scatter Plots ────────────────────────────────────
def plot_scatter(df):
    print("\nGenerating Scatter Plots...")

    features = ['avg_tempo',    'avg_energy',
                'avg_valence',  'avg_instrumentalness',
                'avg_danceability', 'avg_acousticness']

    features  = [f for f in features
                 if f in df.columns]
    df_clean  = df[features +
                   ['productivity_score']].dropna()

    print(f"Rows for scatter: {len(df_clean)}")

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes      = axes.flatten()

    for i, feature in enumerate(features):
        x = df_clean[feature].values.astype(float)
        y = df_clean['productivity_score'].values.astype(float)

        axes[i].scatter(x, y,
                        color      = 'steelblue',
                        edgecolors = 'white',
                        alpha      = 0.8,
                        s          = 100,
                        zorder     = 3)

        # Trend line
        if len(set(x)) > 1:
            z        = np.polyfit(x, y, 1)
            p        = np.poly1d(z)
            x_line   = np.linspace(x.min(), x.max(), 100)
            axes[i].plot(x_line, p(x_line),
                         'r--', linewidth=2,
                         alpha=0.8, zorder=2)

        corr  = np.corrcoef(x, y)[0, 1]
        label = feature.replace('avg_', '').title()

        axes[i].set_xlabel(label,      fontsize=11)
        axes[i].set_ylabel('Productivity', fontsize=11)
        axes[i].set_title(f'{label} (r={corr:.2f})',
                           fontsize=12)
        axes[i].set_ylim(0, 11)
        axes[i].grid(True, alpha=0.3)

    plt.suptitle('Audio Features vs Productivity Score',
                 fontsize=16)
    plt.tight_layout()
    plt.savefig('data/correlation_plots.png',
                dpi=150, bbox_inches='tight')
    plt.show()
    print("✅ Saved correlation_plots.png")

# ── Plot 2: Heatmap ──────────────────────────────────────────
def plot_heatmap(df):
    print("\nGenerating Heatmap...")

    cols     = ['avg_tempo', 'avg_energy',
                'avg_valence', 'avg_danceability',
                'avg_acousticness',
                'avg_instrumentalness',
                'productivity_score', 'focus_score']
    cols     = [c for c in cols if c in df.columns]
    df_clean = df[cols].dropna()
    df_clean = df_clean.loc[
                :, df_clean.nunique() > 1]

    plt.figure(figsize=(10, 7))
    sns.heatmap(df_clean.corr(),
                annot      = True,
                cmap       = 'coolwarm',
                fmt        = '.2f',
                center     = 0,
                linewidths = 0.5)
    plt.title('Feature Correlation Heatmap',
               fontsize=14)
    plt.tight_layout()
    plt.savefig('data/heatmap.png', dpi=150)
    plt.show()
    print("✅ Saved heatmap.png")

# ── Plot 3: By Task Type ─────────────────────────────────────
def plot_by_task(df):
    print("\nGenerating Task Analysis...")

    task_avg = df.groupby('task_type').agg(
        Productivity = ('productivity_score', 'mean'),
        Focus        = ('focus_score',        'mean')
    ).reset_index()

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].bar(task_avg['task_type'],
                task_avg['Productivity'],
                color='steelblue')
    axes[0].set_title('Avg Productivity by Task')
    axes[0].set_ylim(0, 10)
    axes[0].grid(True, alpha=0.3, axis='y')
    for i, v in enumerate(task_avg['Productivity']):
        axes[0].text(i, v+0.1, f'{v:.1f}',
                     ha='center', fontsize=11)

    axes[1].bar(task_avg['task_type'],
                task_avg['Focus'],
                color='coral')
    axes[1].set_title('Avg Focus by Task')
    axes[1].set_ylim(0, 10)
    axes[1].grid(True, alpha=0.3, axis='y')
    for i, v in enumerate(task_avg['Focus']):
        axes[1].text(i, v+0.1, f'{v:.1f}',
                     ha='center', fontsize=11)

    plt.suptitle('Productivity & Focus by Task Type',
                  fontsize=14)
    plt.tight_layout()
    plt.savefig('data/task_analysis.png', dpi=150)
    plt.show()
    print("✅ Saved task_analysis.png")

# ── Plot 4: High vs Low Productivity ────────────────────────
def plot_high_vs_low(df):
    print("\nGenerating High vs Low Analysis...")

    df['productive'] = df['productivity_score'] >= 7
    features         = ['avg_tempo', 'avg_energy',
                        'avg_valence',
                        'avg_instrumentalness']

    fig, axes = plt.subplots(1, 4, figsize=(16, 5))

    for i, feature in enumerate(features):
        high = df[df['productive'] == True][feature]
        low  = df[df['productive'] == False][feature]
        axes[i].boxplot([high, low],
                         labels=['High\n(≥7)',
                                 'Low\n(<7)'])
        axes[i].set_title(
            feature.replace('avg_', '').title())
        axes[i].grid(True, alpha=0.3)

    plt.suptitle(
        'Audio Profile: High vs Low Productivity',
        fontsize=14)
    plt.tight_layout()
    plt.savefig('data/high_vs_low.png', dpi=150)
    plt.show()
    print("✅ Saved high_vs_low.png")

# ── Print Insights ───────────────────────────────────────────
def print_insights(df):
    print("\n" + "="*50)
    print("       🎵 MOODMETRIC INSIGHTS")
    print("="*50)

    features = ['avg_tempo', 'avg_energy',
                'avg_valence', 'avg_instrumentalness',
                'avg_danceability', 'avg_acousticness']

    correlations = {}
    print("\n📊 Correlation with Productivity:")
    for f in features:
        if f in df.columns:
            corr           = df[f].corr(
                             df['productivity_score'])
            correlations[f] = corr
            bar            = "█" * int(abs(corr) * 20)
            sign           = "+" if corr > 0 else "-"
            print(f"  {f.replace('avg_','').ljust(20)}"
                  f": {sign}{abs(corr):.2f} {bar}")

    if correlations:
        best = max(correlations,
                   key=lambda x: abs(correlations[x]))
        print(f"\n🏆 Most Impactful: "
              f"{best.replace('avg_','').upper()}")

    print(f"\n📈 Your Stats:")
    print(f"   Avg Productivity : "
          f"{df['productivity_score'].mean():.1f}/10")
    print(f"   Avg Focus        : "
          f"{df['focus_score'].mean():.1f}/10")
    print(f"   Best Task        : "
          f"{df.groupby('task_type')['productivity_score'].mean().idxmax()}")
    print(f"   Total Sessions   : {len(df)}")
    print("="*50)

# ── Main ─────────────────────────────────────────────────────
if __name__ == "__main__":
    df = load_data()
    print_insights(df)
    plot_scatter(df)
    plot_heatmap(df)
    plot_by_task(df)
    plot_high_vs_low(df)
    print("\n✅ All analysis complete!")