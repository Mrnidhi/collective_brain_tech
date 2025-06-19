import json
from datetime import datetime
import os
import requests
import smtplib
from email.mime.text import MIMEText

def send_slack_alert(message, webhook_url):
    if not webhook_url:
        return
    payload = {"text": message}
    try:
        requests.post(webhook_url, json=payload, timeout=5)
    except Exception:
        pass

def send_telegram_alert(message, bot_token, chat_id):
    if not bot_token or not chat_id:
        return
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    try:
        requests.post(url, data=payload, timeout=5)
    except Exception:
        pass

def send_email_alert(message, to_email, from_email, smtp_server, smtp_port, smtp_user, smtp_pass):
    if not (to_email and from_email and smtp_server and smtp_user and smtp_pass):
        return
    msg = MIMEText(message)
    msg['Subject'] = 'Collective Brain Trend Alert'
    msg['From'] = from_email
    msg['To'] = to_email
    try:
        with smtplib.SMTP_SSL(smtp_server, int(smtp_port)) as server:
            server.login(smtp_user, smtp_pass)
            server.sendmail(from_email, [to_email], msg.as_string())
    except Exception:
        pass

def trigger_alerts(spike_path='spike_output.json', forecast_path='forecast_output.json', alert_path='trend_alerts.json'):
    alerts = []
    # Notification config from env
    slack_webhook = os.getenv('SLACK_WEBHOOK_URL')
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
    email_to = os.getenv('ALERT_EMAIL_TO')
    email_from = os.getenv('ALERT_EMAIL_FROM')
    smtp_server = os.getenv('ALERT_SMTP_SERVER')
    smtp_port = os.getenv('ALERT_SMTP_PORT', '465')
    smtp_user = os.getenv('ALERT_SMTP_USER')
    smtp_pass = os.getenv('ALERT_SMTP_PASS')
    # Spike-based alerts
    try:
        with open(spike_path) as f:
            spikes = json.load(f)
        for s in spikes:
            if s['growth_percent'] >= 150:
                alert = {
                    'type': 'growth_spike',
                    'tag': s['tag'],
                    'platform': s['platform'],
                    'growth_percent': s['growth_percent'],
                    'detected_at': s['detected_at'],
                    'alerted_at': datetime.utcnow().isoformat() + 'Z'
                }
                alerts.append(alert)
                msg = f"[Growth Spike] {s['tag']} on {s['platform']} (+{s['growth_percent']}%)"
                send_slack_alert(msg, slack_webhook)
                send_telegram_alert(msg, telegram_token, telegram_chat_id)
                send_email_alert(msg, email_to, email_from, smtp_server, smtp_port, smtp_user, smtp_pass)
    except Exception:
        pass
    # Forecast-based alerts
    try:
        with open(forecast_path) as f:
            forecasts = json.load(f)
        for fcast in forecasts:
            if fcast.get('trend_direction') == 'increasing':
                alert = {
                    'type': 'forecast_trend',
                    'tag': fcast['tag'],
                    'forecasted_count': fcast['forecasted_count'],
                    'trend_direction': fcast['trend_direction'],
                    'alerted_at': datetime.utcnow().isoformat() + 'Z'
                }
                alerts.append(alert)
                msg = f"[Forecast Trend] {fcast['tag']} trending up (forecast: {fcast['forecasted_count']})"
                send_slack_alert(msg, slack_webhook)
                send_telegram_alert(msg, telegram_token, telegram_chat_id)
                send_email_alert(msg, email_to, email_from, smtp_server, smtp_port, smtp_user, smtp_pass)
    except Exception:
        pass
    with open(alert_path, 'w') as f:
        json.dump(alerts, f, indent=2)
    return alerts

if __name__ == '__main__':
    alerts = trigger_alerts()
    print(f"Triggered {len(alerts)} alerts. Output written to trend_alerts.json") 