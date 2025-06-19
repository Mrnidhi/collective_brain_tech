# Trend Analysis Module

This module processes the collected data to identify patterns and trends in technology discussions. It uses various text analysis techniques to extract meaningful insights from the raw data.

## Main Components

### 1. Data Cleaning (`cleaner.py`)
Prepares text data for analysis:
- Removes special characters and formatting
- Normalizes text case and spacing
- Handles missing or invalid data
- Applies advanced text preprocessing

### 2. Information Extraction (`extractor.py`)
Extracts meaningful information from text:
- **TF-IDF Keywords**: Identifies important terms using statistical analysis
- **KeyBERT Keywords**: Uses machine learning to find relevant keywords
- **Named Entity Recognition**: Identifies people, organizations, and technologies using spaCy
- **Tag Analysis**: Processes platform-specific tags

### 3. Pattern Analysis (`analyzer.py`)
Ranks and analyzes extracted information:
- Ranks keywords by importance scores
- Counts entity occurrences
- Analyzes tag popularity
- Tracks repository mentions

### 4. Data Visualization (`visualizer.py`)
Creates visual representations:
- Generates bar charts for rankings
- Creates word clouds for keyword visualization
- Plots trend lines over time
- Saves charts as image files

### 5. Pipeline Runner (`run_trends.py`)
Coordinates the entire analysis process:
- Loads data from `fetched_data.json`
- Applies cleaning and extraction
- Performs ranking and analysis
- Generates visualizations
- Saves results to `trends.json`

## How to Use

1. Ensure you have collected data first:
   ```bash
   python run_fetch.py
   ```

2. Run the trend analysis:
   ```bash
   python trend_analysis/run_trends.py
   ```

## Analysis Process

1. **Data Loading**: Reads `fetched_data.json`
2. **Text Cleaning**: Applies advanced text preprocessing
3. **Keyword Extraction**: 
   - TF-IDF analysis for statistical keyword identification
   - KeyBERT for machine learning-based keyword extraction
4. **Entity Recognition**: Uses spaCy for named entity extraction
5. **Ranking**: Ranks keywords, entities, tags, and repositories
6. **Visualization**: Creates charts and word clouds
7. **Output**: Saves results to `trends.json`

## Output Format

The analysis produces structured results in `trends.json`:
```json
{
    "top_keywords": [
        ["python", 0.85],
        ["javascript", 0.72],
        ["react", 0.68]
    ],
    "top_entities": [
        ["GitHub", 45],
        ["Stack Overflow", 32],
        ["Python", 28]
    ],
    "top_tags": [
        ["python", 156],
        ["javascript", 134],
        ["react", 89]
    ],
    "top_repos": [
        ["user/repo1", 12],
        ["user/repo2", 8]
    ],
    "keybert_keywords": [
        ["machine learning", 0.92],
        ["web development", 0.88]
    ]
}
```

## Analysis Methods

### TF-IDF Analysis
- Statistical method for keyword extraction
- Identifies terms that are important in the context
- Provides numerical importance scores

### KeyBERT Analysis
- Machine learning-based keyword extraction
- Uses BERT embeddings for better understanding
- Identifies semantically relevant keywords

### Named Entity Recognition
- Uses spaCy library
- Identifies organizations, technologies, and other entities
- Provides entity type classification

### Trend Ranking
- Counts occurrences across platforms
- Calculates popularity scores
- Ranks items by frequency and importance

## Visualization Features

- **Bar Charts**: Show rankings and counts
- **Word Clouds**: Visualize keyword importance
- **Line Charts**: Track trends over time
- **Interactive Plots**: Generated with matplotlib

## Dependencies

- pandas (data manipulation)
- scikit-learn (TF-IDF analysis)
- keybert (keyword extraction)
- spacy (named entity recognition)
- matplotlib (visualization)
- wordcloud (word cloud generation)

## Customization

You can modify the analysis by:
- Adjusting the number of top keywords/entities
- Changing text cleaning parameters
- Modifying visualization styles
- Adding new analysis methods 