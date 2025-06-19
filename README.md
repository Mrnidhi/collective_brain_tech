# Collective Brain of Tech Students

## Overview
A real-time dashboard to analyze and visualize what students and developers are learning, using, and struggling with across GitHub, Stack Overflow, and Reddit.

---

## 📦 Project Structure
```
/project-root
├── dashboard/
│   └── app.py
├── trend_analysis/
├── fetch_sources/
├── .streamlit/
│   └── config.toml
├── .env.example      # (Do not upload actual API keys!)
├── requirements.txt
├── README.md
├── fetched_data.json (optional, as sample)
├── trends.json       (optional, as sample)
└── setup.sh          (optional for HuggingFace)
```

---

## 🚀 How to Run Locally
1. **Clone the repo**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up your .env file:**
   - Copy `.env.example` to `.env` and fill in your API keys.
4. **Fetch live data:**
   ```bash
   python run_fetch.py
   ```
5. **Generate trends:**
   ```bash
   python trend_analysis/run_trends.py
   ```
6. **Launch the dashboard:**
   ```bash
   streamlit run dashboard/app.py
   ```

---

## ☁️ Deploying to Streamlit Cloud
1. **Push this project to a public GitHub repo.**
2. **Go to [Streamlit Cloud](https://streamlit.io/cloud) and connect your repo.**
3. **Set the main file as:**
   ```
   dashboard/app.py
   ```
4. **Add your secrets (.env values) via Streamlit Cloud Secrets Manager.**
5. **[Optional] Add sample_data/fetched_data.json and trends.json for demo mode.**

---

## 🧪 Demo Mode (Optional)
- If no API keys are available, the app can use sample data from `sample_data/`.
- To try demo mode, copy files from `sample_data/` to the project root.

---

## 🤖 HuggingFace Spaces (Optional)
- Add a `setup.sh` if you need custom install steps.
- Set the app entry point to `dashboard/app.py`.

---

## 🔐 Secrets & API Keys
- **Never commit your real .env file!**
- Use `.env.example` as a template.
- For deployment, add secrets via the platform's secrets manager.

## Phase 1 – Real-time Data Ingestion

This project fetches, analyzes, and normalizes what students and developers are learning, using, and struggling with across GitHub, Stack Overflow, and Reddit.

### Features
- Fetches commit messages, repo names, and languages from GitHub Public Events API
- Fetches recent questions, tags, and scores from Stack Overflow
- Fetches post titles, upvotes, and timestamps from Reddit subreddits: r/learnprogramming, r/cscareerquestions, r/AskProgramming
- Normalizes all data into a unified format and stores it in a local JSON file

---

## 📁 File Structure
```
collective_brain/
│
├── fetch_sources/
│   ├── github_fetcher.py
│   ├── so_fetcher.py
│   ├── reddit_fetcher.py
│   └── utils.py
│
├── run_fetch.py        # main orchestrator
├── requirements.txt
├── .env                # (for Reddit API keys)
└── README.md
```

---

## ⚡ Setup Instructions

1. **Clone the repository**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up Reddit API keys:**
   - Create a `.env` file in the root directory:
     ```ini
     REDDIT_CLIENT_ID=your_id_here
     REDDIT_SECRET=your_secret_here
     ```
4. **Run the main script:**
   ```bash
   python run_fetch.py
   ```
   This will fetch and save data to `fetched_data.json`.

---

## 🧪 Example Output
```json
{
  "source": "github",
  "timestamp": "2025-06-19T14:22:10Z",
  "text": "fix: handle null pointer bug in parser",
  "tags": ["bug"],
  "meta": {
    "lang": "python",
    "repo": "user/repo",
    "url": "https://github.com/user/repo"
  }
}
```

---

## Next Steps
- Topic extraction and trending (Phase 2)
- Streamlit dashboard (Phase 3)
