import pandas as pd
from datetime import datetime
from collections import defaultdict

def detect_spikes(fetched_data_path='fetched_data.json', min_growth=2.0):
    df = pd.read_json(fetched_data_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['week'] = df['timestamp'].dt.to_period('W').apply(lambda r: r.start_time)
    spikes = []
    # Analyze tags and repos
    for platform in df['source'].unique():
        df_p = df[df['source'] == platform]
        # Tags
        tag_counts = defaultdict(list)
        for week, group in df_p.groupby('week'):
            tags = group['tags'].explode()
            for tag, count in tags.value_counts().items():
                tag_counts[tag].append((week, count))
        for tag, week_counts in tag_counts.items():
            week_counts = sorted(week_counts)
            for i in range(3, len(week_counts)):
                prev_counts = [c for _, c in week_counts[i-3:i]]
                prev_avg = sum(prev_counts) / 3 if prev_counts else 0
                curr_week, curr_count = week_counts[i]
                if prev_avg > 0 and curr_count / prev_avg >= min_growth:
                    spikes.append({
                        'tag': tag,
                        'growth_percent': round(100 * (curr_count - prev_avg) / prev_avg, 1),
                        'platform': platform.title() if platform != 'github' else 'GitHub',
                        'detected_at': curr_week.strftime('%Y-%m-%dT%H:%M:%S')
                    })
        # Repos (GitHub only)
        if platform == 'github':
            repo_counts = defaultdict(list)
            for week, group in df_p.groupby('week'):
                repos = group['meta'].apply(lambda m: m.get('repo', None))
                for repo, count in repos.value_counts().items():
                    repo_counts[repo].append((week, count))
            for repo, week_counts in repo_counts.items():
                week_counts = sorted(week_counts)
                for i in range(3, len(week_counts)):
                    prev_counts = [c for _, c in week_counts[i-3:i]]
                    prev_avg = sum(prev_counts) / 3 if prev_counts else 0
                    curr_week, curr_count = week_counts[i]
                    if prev_avg > 0 and curr_count / prev_avg >= min_growth:
                        spikes.append({
                            'tag': repo,
                            'growth_percent': round(100 * (curr_count - prev_avg) / prev_avg, 1),
                            'platform': 'GitHub',
                            'detected_at': curr_week.strftime('%Y-%m-%dT%H:%M:%S')
                        })
    return spikes

if __name__ == '__main__':
    spikes = detect_spikes()
    import json
    with open('spike_output.json', 'w') as f:
        json.dump(spikes, f, indent=2)
    print(f"Detected {len(spikes)} spikes. Output written to spike_output.json") 