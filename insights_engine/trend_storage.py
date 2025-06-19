import sqlite3
from datetime import datetime

def get_db(db_path='trends.db'):
    conn = sqlite3.connect(db_path)
    return conn

def init_db(db_path='trends.db'):
    conn = get_db(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS trends (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        tag TEXT,
        value REAL,
        type TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        tag TEXT,
        alert_type TEXT,
        details TEXT
    )''')
    conn.commit()
    conn.close()

def store_trend(trend, db_path='trends.db'):
    conn = get_db(db_path)
    c = conn.cursor()
    c.execute('INSERT INTO trends (timestamp, tag, value, type) VALUES (?, ?, ?, ?)',
              (trend.get('timestamp', datetime.utcnow().isoformat()), trend['tag'], trend['value'], trend.get('type', 'unknown')))
    conn.commit()
    conn.close()

def store_alert(alert, db_path='trends.db'):
    conn = get_db(db_path)
    c = conn.cursor()
    c.execute('INSERT INTO alerts (timestamp, tag, alert_type, details) VALUES (?, ?, ?, ?)',
              (alert.get('alerted_at', datetime.utcnow().isoformat()), alert['tag'], alert['type'], str(alert)))
    conn.commit()
    conn.close()

def get_trends(tag=None, since=None, until=None, db_path='trends.db'):
    conn = get_db(db_path)
    c = conn.cursor()
    query = 'SELECT timestamp, tag, value, type FROM trends WHERE 1=1'
    params = []
    if tag:
        query += ' AND tag=?'
        params.append(tag)
    if since:
        query += ' AND timestamp>=?'
        params.append(since)
    if until:
        query += ' AND timestamp<=?'
        params.append(until)
    c.execute(query, params)
    rows = c.fetchall()
    conn.close()
    return rows

def get_alerts(since=None, until=None, db_path='trends.db'):
    conn = get_db(db_path)
    c = conn.cursor()
    query = 'SELECT timestamp, tag, alert_type, details FROM alerts WHERE 1=1'
    params = []
    if since:
        query += ' AND timestamp>=?'
        params.append(since)
    if until:
        query += ' AND timestamp<=?'
        params.append(until)
    c.execute(query, params)
    rows = c.fetchall()
    conn.close()
    return rows

if __name__ == '__main__':
    init_db()
    print('Initialized trends.db') 