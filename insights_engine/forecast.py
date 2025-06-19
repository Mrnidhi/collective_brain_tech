import pandas as pd
from prophet import Prophet
from collections import Counter
from datetime import timedelta

def forecast_tags(fetched_data_path='fetched_data.json', top_n=5, days_ahead=7):
    df = pd.read_json(fetched_data_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    all_tags = [tag for tags in df['tags'] for tag in tags]
    top_tags = [tag for tag, _ in Counter(all_tags).most_common(top_n)]
    forecasts = []
    for tag in top_tags:
        tag_df = df[df['tags'].apply(lambda tags: tag in tags)]
        daily = tag_df.groupby(tag_df['timestamp'].dt.date).size().reset_index(name='count')
        if len(daily) < 5:
            continue
        daily = daily.rename(columns={'timestamp': 'ds', 'count': 'y'})
        daily['ds'] = pd.to_datetime(daily['ds'])
        m = Prophet(daily_seasonality=True, yearly_seasonality=False, weekly_seasonality=True)
        m.fit(daily)
        future = m.make_future_dataframe(periods=days_ahead)
        forecast = m.predict(future)
        last_row = forecast.iloc[-1]
        prev_row = forecast.iloc[-days_ahead-1] if len(forecast) > days_ahead else forecast.iloc[-2]
        direction = 'increasing' if last_row['yhat'] > prev_row['yhat'] else 'decreasing'
        forecasts.append({
            'tag': tag,
            'forecasted_count': int(round(last_row['yhat'])),
            'trend_direction': direction
        })
    return forecasts

if __name__ == '__main__':
    forecasts = forecast_tags()
    import json
    with open('forecast_output.json', 'w') as f:
        json.dump(forecasts, f, indent=2)
    print(f"Forecasted {len(forecasts)} tags. Output written to forecast_output.json") 