import streamlit as st
import json

def load_alerts(path='trend_alerts.json'):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return []

def show_alerts(location='sidebar'):
    alerts = load_alerts()
    if not alerts:
        if location == 'sidebar':
            st.sidebar.info('No active alerts.')
        else:
            st.info('No active alerts.')
        return
    alert_type_map = {
        'growth_spike': ('🔥', 'orange'),
        'forecast_trend': ('📈', 'blue'),
    }
    for alert in alerts:
        icon, color = alert_type_map.get(alert['type'], ('⚠️', 'gray'))
        msg = f"{icon} [{alert['type'].replace('_', ' ').title()}] <b>{alert['tag']}</b>"
        if 'platform' in alert:
            msg += f" ({alert['platform']})"
        if 'growth_percent' in alert:
            msg += f" <span style='color:orange'>+{alert['growth_percent']}%</span>"
        if location == 'sidebar':
            st.sidebar.markdown(msg, unsafe_allow_html=True)
        else:
            st.markdown(msg, unsafe_allow_html=True) 