import streamlit as st
import json
import os

def show_alerts(location='main', max_alerts=3):
    """Show trend alerts in a more subtle, GitHub-like style."""
    
    # Try to load alerts from the alerts file
    alerts_file = '../trend_alerts.json'
    if not os.path.exists(alerts_file):
        alerts_file = 'trend_alerts.json'
    
    if not os.path.exists(alerts_file):
        return
    
    try:
        with open(alerts_file) as f:
            alerts = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return
    
    if not alerts:
        return
    
    # Sort alerts by priority and timestamp
    sorted_alerts = sorted(
        alerts,
        key=lambda x: (-x.get('priority', 0), x.get('timestamp', '')),
        reverse=True
    )[:max_alerts]
    
    # Display alerts in the specified location
    container = st.sidebar if location == 'sidebar' else st
    
    with container:
        if location == 'sidebar':
            st.markdown("##### 🔔 Recent Alerts")
        
        for alert in sorted_alerts:
            # Determine alert style based on priority
            if alert.get('priority', 0) >= 2:
                icon = "🔴"  # High priority
                color = "#d73a4a"  # GitHub red
            elif alert.get('priority', 0) == 1:
                icon = "🟡"  # Medium priority
                color = "#d4a72c"  # GitHub yellow
            else:
                icon = "🟢"  # Low priority
                color = "#238636"  # GitHub green
            
            # Format the alert message
            message = alert.get('message', '')
            details = alert.get('details', '')
            
            # Display the alert using custom HTML/CSS
            st.markdown(
                f"""
                <div style="
                    padding: 0.75rem;
                    margin-bottom: 0.5rem;
                    border: 1px solid {color}33;
                    border-radius: 6px;
                    background-color: {color}11;
                ">
                    <div style="
                        color: {color};
                        font-weight: 500;
                        margin-bottom: 0.25rem;
                    ">
                        {icon} {message}
                    </div>
                    <div style="
                        color: #57606a;
                        font-size: 0.875rem;
                    ">
                        {details}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            ) 