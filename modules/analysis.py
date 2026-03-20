import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

LOG_FILE = 'data/productivity_log.csv'

def load_data():
    df = pd.read_csv(LOG_FILE, encoding='utf-8')
    df['productivity_score'] = pd.to_numeric(
        df['productivity_score'], errors='coerce')
    df['focus_score'] = pd.to_numeric(
        df['focus_score'], errors='coerce')

    # Convert audio features to numeric
    for col in ['avg_tempo','avg_energy','avg_valence',
                'avg_instrumentalness','avg_danceability',
                'avg_acousticness']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    df = df.dropna(subset=['productivity_score',
                            'focus_score'])
    print(f"✅ Loaded {len(df)} sessions")
    print(f"Columns: {df.columns.tolist()}")
    return df

def show_stats(df):
    print("\n" + "="*45)
    print("       📊 YOUR MOODMETRIC STATS")
    print("="*45)
    print(f"Total Sessions     : {len(df)}")
    print(f"Avg Productivity   : "
          f"{df['productivity_score'].mean():.1f}/10")
    print(f"Avg Focus          : "
          f"{df['focus_score'].mean():.1f}/10")

    if 'avg_tempo' in df.columns:
        print(f"Avg Tempo          : "
              f"{df['avg_tempo'].mean():.0f} BPM")
        print(f"Avg Energy         : "
              f"{df['avg_energy'].mean():.2f}")
        print(f"Avg Valence        : "
              f"{df['avg_valence'].mean():.2f}")

    print(f"Most common task   : "
          f"{df['task_type'].mode()[0]}")
    print(f"Best productivity  : "
          f"{df['productivity_score'].max()}/10")
    print(f"Worst productivity : "
          f"{df['productivity_score'].min()}/10")
    print("="*45)

def correlation_analysis(df):
    features = ['avg_tempo','avg_energy','avg_valence',
                'avg_instrumentalness','avg_danceability',
                'avg_acousticness']

    # Only use features that exist and have data
    available = [f for f in features
                 if f in df.columns
                 and df[f].notna().sum() > 2]

    if not available:
        print("⚠️ No audio features found for correlation!")
        return

    print(f"\n📊 Running Correlation Analysis "
          f"for {len(available)} features...")

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes      = axes.flatten()

    for i in range(6):
        if i < len(available):
            feature = available[i]
            x = df[feature].dropna()
            y = df.loc[x.index, 'productivity_score']

            axes[i].scatter(x, y, alpha=0.7,
                           color='steelblue', s=100)

            if len(x) > 1:
                z  = np.polyfit(x, y, 1)
                p  = np.poly1d(z)
                xs = np.linspace(x.min(), x.max(), 100)
                axes[i].plot(xs, p(xs),
                            "r--", alpha=0.8)

            corr = x.corr(y)
            label = feature.replace('avg_','').title()
            axes[i].set_xlabel(label, fontsize=11)
            axes[i].set_ylabel('Productivity', fontsize=11)
            axes[i].set_title(f'{label} (r={corr:.2f})',
                            fontsize=12,
                            fontweight='bold')
            axes[i].set_ylim(0, 11)
        else:
            axes[i].set_visible(False)

    plt.suptitle('Audio Features vs Productivity Score',
                fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('data/correlation_plots.png', dpi=150)
    plt.show()
    print("✅ Saved → data/correlation_plots.png")

def plot_heatmap(df):
    cols = ['avg_tempo','avg_energy','avg_valence',
            'avg_danceability','avg_instrumentalness',
            'avg_acousticness','productivity_score',
            'focus_score']

    available = [c for c in cols
                 if c in df.columns
                 and df[c].notna().sum() > 2]

    if len(available) < 2:
        print("⚠️ Not enough data for heatmap")
        return

    print("\n📊 Generating Heatmap...")
    plt.figure(figsize=(12, 9))
    sns.heatmap(df[available].corr(),
                annot=True, cmap='coolwarm',
                fmt='.2f', linewidths=0.5,
                center=0,
                annot_kws={'size': 10})
    plt.title('Feature Correlation Heatmap',
             fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('data/heatmap.png', dpi=150)
    plt.show()
    print("✅ Saved → data/heatmap.png")

def plot_by_task(df):
    print("\n📊 Productivity by Task Type...")

    # Clean task_type
    df['task_type'] = df['task_type'].astype(str).str.strip()
    task_avg = df.groupby('task_type')[
        'productivity_score'].mean().sort_values(
        ascending=False)

    print(f"Task types found: {task_avg.index.tolist()}")

    plt.figure(figsize=(10, 6))
    colors = ['steelblue','coral','mediumseagreen',
              'mediumpurple','sandybrown']

    bars = plt.bar(task_avg.index,
                   task_avg.values,
                   color=colors[:len(task_avg)],
                   width=0.5)

    for bar, val in zip(bars, task_avg.values):
        plt.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + 0.15,
                f'{val:.1f}', ha='center',
                fontsize=12, fontweight='bold')

    plt.title('Average Productivity by Task Type',
             fontsize=14, fontweight='bold')
    plt.xlabel('Task Type', fontsize=12)
    plt.ylabel('Avg Productivity Score', fontsize=12)
    plt.ylim(0, 12)
    plt.xticks(fontsize=11)
    plt.tight_layout()
    plt.savefig('data/task_productivity.png', dpi=150)
    plt.show()
    print("✅ Saved → data/task_productivity.png")

def plot_over_time(df):
    print("\n📊 Productivity Over Time...")
    plt.figure(figsize=(12, 5))
    plt.plot(range(len(df)),
             df['productivity_score'],
             marker='o', color='steelblue',
             linewidth=2, markersize=8)
    plt.fill_between(range(len(df)),
                    df['productivity_score'],
                    alpha=0.2, color='steelblue')

    avg = df['productivity_score'].mean()
    plt.axhline(y=avg, color='red',
               linestyle='--', alpha=0.7,
               label=f'Average: {avg:.1f}')

    plt.title('Your Productivity Over Time',
             fontsize=14, fontweight='bold')
    plt.xlabel('Session Number', fontsize=12)
    plt.ylabel('Productivity Score', fontsize=12)
    plt.legend(fontsize=11)
    plt.ylim(0, 11)
    plt.tight_layout()
    plt.savefig('data/productivity_over_time.png', dpi=150)
    plt.show()
    print("✅ Saved → data/productivity_over_time.png")

if __name__ == "__main__":
    df = load_data()
    show_stats(df)
    correlation_analysis(df)
    plot_heatmap(df)
    plot_by_task(df)
    plot_over_time(df)
    print("\n🎉 All analysis complete!")