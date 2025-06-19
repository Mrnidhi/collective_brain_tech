# Collective Brain of Tech Students

Welcome to the Collective Brain of Tech Students project! This innovative platform analyzes and presents technology trends by gathering data from three major platforms: GitHub, Stack Overflow, and Reddit.

## Project Overview

Our project serves as a comprehensive trend analysis tool that helps students and educators stay updated with the latest developments in technology. By collecting and analyzing data from popular tech platforms, we provide valuable insights into emerging technologies, programming languages, and developer discussions.

## Key Features

1. **Multi-Platform Data Collection**
   - GitHub: Track commit messages and repository activity
   - Stack Overflow: Monitor recent questions and tags
   - Reddit: Analyze discussions from programming subreddits

2. **Advanced Analysis Tools**
   - Text cleaning and preprocessing
   - Keyword extraction using TF-IDF and KeyBERT
   - Named Entity Recognition (NER) with spaCy
   - Trend ranking and visualization

3. **Interactive Dashboard**
   - Platform-specific data visualization
   - Search functionality across all data
   - Real-time data refresh
   - Interactive charts and word clouds

4. **Insights Engine**
   - Trend spike detection
   - Basic forecasting capabilities
   - Alert system for significant changes
   - SQLite storage for historical data

## Project Structure

```
project/
├── fetch_sources/       # Data collection scripts
│   ├── github_fetcher.py
│   ├── so_fetcher.py
│   ├── reddit_fetcher.py
│   └── utils.py
├── trend_analysis/     # Trend processing pipeline
│   ├── cleaner.py
│   ├── extractor.py
│   ├── analyzer.py
│   ├── visualizer.py
│   └── run_trends.py
├── dashboard/          # Streamlit web interface
│   ├── app.py
│   └── components/
│       ├── charts.py
│       ├── filters.py
│       ├── load_data.py
│       └── alerts.py
├── insights_engine/    # Trend detection and forecasting
│   ├── monitor.py
│   ├── forecast.py
│   ├── alert.py
│   ├── trend_storage.py
│   └── run_insights.py
└── data files/        # Generated outputs
    ├── fetched_data.json
    ├── trends.json
    ├── trends.db
    └── various output files
```

## Setup Instructions

1. **Environment Setup**
   ```bash
   # Create a virtual environment
   python -m venv venv
   
   # Activate the environment
   # For Windows:
   venv\Scripts\activate
   # For macOS/Linux:
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Configuration**
   - Create a `.env` file with your Reddit API credentials:
     ```
     REDDIT_CLIENT_ID=your_client_id
     REDDIT_SECRET=your_client_secret
     ```

3. **Running the Application**
   ```bash
   # Fetch data from all platforms
   python run_fetch.py
   
   # Analyze trends
   python trend_analysis/run_trends.py
   
   # Run insights engine (optional)
   python insights_engine/run_insights.py
   
   # Start the dashboard
   cd dashboard
   streamlit run app.py
   ```

## Data Collection

The system collects data from:
- **GitHub**: Public events API for commit messages and repository activity
- **Stack Overflow**: Recent questions with tags and scores
- **Reddit**: Posts from r/learnprogramming, r/AskProgramming, and r/cscareerquestions

## Analysis Features

- **Text Processing**: Advanced cleaning and normalization
- **Keyword Extraction**: TF-IDF and KeyBERT-based keyword identification
- **Entity Recognition**: Named entity extraction using spaCy
- **Trend Ranking**: Statistical ranking of keywords, tags, and entities
- **Visualization**: Bar charts, word clouds, and line charts

## Dashboard Features

- **Multi-platform View**: Separate tabs for each data source
- **Search Functionality**: Search across all collected data
- **Interactive Charts**: Clickable visualizations
- **Real-time Updates**: Auto-refresh every 5 minutes
- **Data Filtering**: Filter by platform, date, and other criteria

## Output Files

- `fetched_data.json`: Raw collected data
- `trends.json`: Analyzed trends and rankings
- `trends.db`: SQLite database for historical data
- `spike_output.json`: Detected trend spikes
- `forecast_output.json`: Trend forecasts
- `trend_alerts.json`: Generated alerts

## Dependencies

- streamlit (dashboard)
- pandas (data processing)
- matplotlib (visualization)
- wordcloud (word clouds)
- scikit-learn (TF-IDF analysis)
- spacy (named entity recognition)
- keybert (keyword extraction)
- requests (API calls)
- python-dotenv (environment variables)

## Contributing

We welcome contributions! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## Contact

For questions or suggestions, please open an issue in the GitHub repository.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
