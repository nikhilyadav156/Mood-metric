import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

LOG_FILE = 'data/productivity_log.csv'

# ── Load Data ────────────────────────────────────────────────
def load_data():
    df = pd.read_csv(LOG_FILE, encoding='latin1')

    # Print columns so we can verify
    print("Columns found:", df.columns.tolist())

    df['productivity_score'] = pd.to_numeric(
        df['productivity_score'], errors='coerce')
    df['focus_score'] = pd.to_numeric(
        df['focus_score'], errors='coerce')
    df = df.dropna(subset=['productivity_score',
                            'focus_score'])
    print(f"✅ Loaded {len(df)} sessions")
    return df
# ── Basic Stats ──────────────────────────────────────────────
def show_stats(df):
    print("\n" + "="*45)
    print("       📊 YOUR MOODMETRIC STATS")
    print("="*45)
    print(f"Total Sessions     : {len(df)}")
    print(f"Avg Productivity   : "
          f"{df['productivity_score'].mean():.1f}/10")
    print(f"Avg Focus          : "
          f"{df['focus_score'].mean():.1f}/10")

    # Safely check columns before accessing
    tempo_col = [c for c in df.columns if 'tempo' in c.lower()]
    energy_col = [c for c in df.columns if 'energy' in c.lower()]
    valence_col = [c for c in df.columns if 'valence' in c.lower()]

    if tempo_col:
        df[tempo_col[0]] = pd.to_numeric(
            df[tempo_col[0]], errors='coerce')
        print(f"Avg Tempo          : "
              f"{df[tempo_col[0]].mean():.0f} BPM")

    if energy_col:
        df[energy_col[0]] = pd.to_numeric(
            df[energy_col[0]], errors='coerce')
        print(f"Avg Energy         : "
              f"{df[energy_col[0]].mean():.2f}")

    if valence_col:
        df[valence_col[0]] = pd.to_numeric(
            df[valence_col[0]], errors='coerce')
        print(f"Avg Valence        : "
              f"{df[valence_col[0]].mean():.2f}")

    print(f"Most common task   : "
          f"{df['task_type'].mode()[0]}")
    print(f"Best productivity  : "
          f"{df['productivity_score'].max()}/10")
    print(f"Worst productivity : "
          f"{df['productivity_score'].min()}/10")
    print("="*45)

# ── Correlation Analysis ─────────────────────────────────────
def correlation_analysis(df):
    print("\n📊 Running Correlation Analysis...")

    features = ['avg_tempo', 'avg_energy', 'avg_valence',
                'avg_instrumentalness', 'avg_danceability',
                'avg_acousticness']

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes      = axes.flatten()

    for i, feature in enumerate(features):
        if feature in df.columns:
            x = pd.to_numeric(df[feature], errors='coerce')
            y = df['productivity_score']

            axes[i].scatter(x, y, alpha=0.6,
                           color='steelblue', s=80)

            # Trend line
            mask = ~(np.isnan(x) | np.isnan(y))
            if mask.sum() > 1:
                z = np.polyfit(x[mask], y[mask], 1)
                p = np.poly1d(z)
                xs = np.linspace(x.min(), x.max(), 100)
                axes[i].plot(xs, p(xs), "r--", alpha=0.8)

            corr = x.corr(y)
            axes[i].set_xlabel(feature.replace('avg_', ''))
            axes[i].set_ylabel('Productivity Score')
            axes[i].set_title(
                f'{feature.replace("avg_", "").title()}'
                f' (r = {corr:.2f})')

    plt.suptitle('Audio Features vs Productivity Score',
                 fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('data/correlation_plots.png', dpi=150)
    plt.show()
    print("✅ Saved → data/correlation_plots.png")

# ── Heatmap ──────────────────────────────────────────────────
def plot_heatmap(df):
    print("\n📊 Generating Heatmap...")

    cols = ['avg_tempo', 'avg_energy', 'avg_valence',
            'avg_danceability', 'avg_instrumentalness',
            'avg_acousticness', 'productivity_score',
            'focus_score']

    # Convert to numeric
    for col in cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    available = [c for c in cols if c in df.columns]
    plt.figure(figsize=(10, 8))
    sns.heatmap(df[available].corr(),
                annot    = True,
                cmap     = 'coolwarm',
                fmt      = '.2f',
                linewidths = 0.5,
                center   = 0)
    plt.title('Feature Correlation Heatmap',
              fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('data/heatmap.png', dpi=150)
    plt.show()
    print("✅ Saved → data/heatmap.png")

# ── Productivity by Task Type ────────────────────────────────
def plot_by_task(df):
    print("\n📊 Productivity by Task Type...")

    plt.figure(figsize=(10, 6))
    task_avg = df.groupby('task_type')[
        'productivity_score'].mean().sort_values(
        ascending=False)

    colors = ['steelblue', 'coral', 'mediumseagreen',
              'mediumpurple', 'sandybrown']
    bars   = plt.bar(task_avg.index, task_avg.values,
                     color=colors[:len(task_avg)])

    # Add value labels on bars
    for bar, val in zip(bars, task_avg.values):
        plt.text(bar.get_x() + bar.get_width()/2,
                 bar.get_height() + 0.1,
                 f'{val:.1f}', ha='center',
                 fontweight='bold')

    plt.title('Average Productivity by Task Type',
              fontsize=14, fontweight='bold')
    plt.xlabel('Task Type')
    plt.ylabel('Average Productivity Score')
    plt.ylim(0, 11)
    plt.tight_layout()
    plt.savefig('data/task_productivity.png', dpi=150)
    plt.show()
    print("✅ Saved → data/task_productivity.png")

# ── Productivity Over Time ───────────────────────────────────
def plot_over_time(df):
    print("\n📊 Productivity Over Time...")

    plt.figure(figsize=(12, 5))
    plt.plot(range(len(df)),
             df['productivity_score'],
             marker='o', color='steelblue',
             linewidth=2, markersize=6)
    plt.fill_between(range(len(df)),
                     df['productivity_score'],
                     alpha=0.2, color='steelblue')

    # Average line
    avg = df['productivity_score'].mean()
    plt.axhline(y=avg, color='red',
                linestyle='--', alpha=0.7,
                label=f'Average: {avg:.1f}')

    plt.title('Your Productivity Over Time',
              fontsize=14, fontweight='bold')
    plt.xlabel('Session Number')
    plt.ylabel('Productivity Score')
    plt.legend()
    plt.ylim(0, 11)
    plt.tight_layout()
    plt.savefig('data/productivity_over_time.png', dpi=150)
    plt.show()
    print("✅ Saved → data/productivity_over_time.png")

# ── Run All ──────────────────────────────────────────────────
if __name__ == "__main__":
    df = load_data()
    show_stats(df)
    correlation_analysis(df)
    plot_heatmap(df)
    plot_by_task(df)
    plot_over_time(df)

    print("\n✅ All analysis complete!")
    print("📁 Check data/ folder for saved graphs")