import json
from insights_engine.monitor import detect_spikes
from insights_engine.forecast import forecast_tags
from insights_engine.alert import trigger_alerts
from insights_engine.trend_storage import init_db, store_trend, store_alert
from datetime import datetime

def main():
    print('Initializing database...')
    init_db()

    print('Running spike detection...')
    spikes = detect_spikes()
    with open('spike_output.json', 'w') as f:
        json.dump(spikes, f, indent=2)
    print(f"Detected {len(spikes)} spikes.")
    for s in spikes:
        store_alert({
            'alerted_at': s['detected_at'],
            'tag': s['tag'],
            'type': 'growth_spike',
            'details': str(s)
        })

    print('Running forecasting...')
    forecasts = forecast_tags()
    with open('forecast_output.json', 'w') as f:
        json.dump(forecasts, f, indent=2)
    print(f"Forecasted {len(forecasts)} tags.")
    for fcast in forecasts:
        store_trend({
            'timestamp': datetime.utcnow().isoformat(),
            'tag': fcast['tag'],
            'value': fcast['forecasted_count'],
            'type': 'forecast'
        })

    print('Running alerting...')
    alerts = trigger_alerts()
    for alert in alerts:
        store_alert(alert)
    print(f"Triggered {len(alerts)} alerts.")

    print('\n✅ Insights Engine Complete!')
    print('  - spike_output.json (spike events)')
    print('  - forecast_output.json (tag forecasts)')
    print('  - trend_alerts.json (alerts)')
    print('  - trends.db (historical trends & alerts)')

if __name__ == '__main__':
    main() 