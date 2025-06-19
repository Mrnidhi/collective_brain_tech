# Insights Engine

This module provides advanced trend analysis capabilities including spike detection, forecasting, and alert generation. It uses historical data to identify significant changes and predict future trends.

## Components

### 1. Trend Monitor (`monitor.py`)
Detects significant changes in trends:
- Identifies sudden spikes in tag mentions
- Calculates growth rates and thresholds
- Monitors trend acceleration
- Detects unusual activity patterns

### 2. Forecasting System (`forecast.py`)
Predicts future trend behavior:
- Uses simple statistical forecasting
- Analyzes historical patterns
- Calculates trend predictions
- Provides confidence scores

### 3. Alert Generator (`alert.py`)
Creates and manages trend alerts:
- Generates spike detection alerts
- Creates forecast-based notifications
- Manages alert priorities and thresholds
- Handles alert formatting and storage

### 4. Data Storage (`trend_storage.py`)
Manages historical data persistence:
- SQLite database for trend storage
- Historical alert tracking
- Data lifecycle management
- Efficient data retrieval

### 5. Main Runner (`run_insights.py`)
Coordinates the entire insights process:
- Initializes the database
- Runs spike detection
- Executes forecasting
- Triggers alerts
- Saves outputs to JSON files

## How It Works

1. **Database Initialization**:
   ```python
   from insights_engine import trend_storage
   trend_storage.init_db()
   ```

2. **Spike Detection**:
   ```python
   from insights_engine import monitor
   spikes = monitor.detect_spikes()
   ```

3. **Forecasting**:
   ```python
   from insights_engine import forecast
   predictions = forecast.forecast_tags()
   ```

## Output Files

The engine generates several output files:

### spike_output.json
Contains detected trend spikes:
```json
[
    {
        "tag": "python",
        "detected_at": "2024-03-20T10:30:00Z",
        "growth_rate": 2.5,
        "threshold": 1.5,
        "confidence": 0.85
    }
]
```

### forecast_output.json
Contains trend forecasts:
```json
[
    {
        "tag": "react",
        "forecasted_count": 150,
        "confidence": 0.78,
        "timeframe": "next_week"
    }
]
```

### trend_alerts.json
Contains generated alerts:
```json
[
    {
        "alerted_at": "2024-03-20T10:30:00Z",
        "tag": "python",
        "type": "growth_spike",
        "details": "150% increase in mentions"
    }
]
```

### trends.db
SQLite database containing:
- Historical trend data
- Alert history
- Forecast records
- Spike events

## Features

### 1. Spike Detection
- Monitors tag mention frequency
- Calculates growth rates
- Identifies significant increases
- Provides confidence scores

### 2. Basic Forecasting
- Statistical trend prediction
- Historical pattern analysis
- Confidence interval calculation
- Time-based forecasting

### 3. Alert Management
- Automatic alert generation
- Priority-based alerting
- Historical alert tracking
- Alert persistence

### 4. Data Persistence
- SQLite database storage
- Efficient data retrieval
- Historical data maintenance
- Data backup capabilities

## Usage

Run the complete insights pipeline:
```bash
python insights_engine/run_insights.py
```

This will:
1. Initialize the database
2. Detect trend spikes
3. Generate forecasts
4. Create alerts
5. Save all outputs

## Configuration

The engine can be configured by modifying:
- Spike detection thresholds
- Forecasting parameters
- Alert generation rules
- Database settings

## Dependencies

- sqlite3 (database management)
- pandas (data analysis)
- json (data serialization)
- datetime (time handling)

## Integration

The insights engine integrates with:
- Trend analysis module (for input data)
- Dashboard (for alert display)
- Data collection pipeline (for historical data)

## Limitations

Current implementation includes:
- Basic statistical forecasting
- Simple spike detection
- Local SQLite storage
- JSON-based outputs

Future enhancements could include:
- Advanced machine learning models
- Real-time streaming analysis
- Cloud-based storage
- Advanced alerting systems 