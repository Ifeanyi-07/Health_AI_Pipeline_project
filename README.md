# 🩸 Blood Work Analyzer

A Streamlit app that analyzes a blood report using Google's Gemini model. It runs a two-stage pipeline:

1. **Extraction** – reads the raw blood report and classifies each test value as `HIGH`, `LOW`, or `NORMAL` based on the reference ranges in the report.
2. **Health Summary & Diet Plan** – generates a simple 3-line health summary plus a practical Indian diet plan (foods to avoid / foods to eat more of) based on the extracted values.

**🔗 Live app:** https://healthaianalysisapp-production.up.railway.app/

> ⚠️ **Disclaimer:** This tool is for informational purposes only and is not a substitute for professional medical advice.

---

## Features

- Upload a `.txt` blood report or paste the text directly
- One-click analysis (extraction → summary → diet plan)
- Download the full result as a Markdown report
- API key is read only from the server environment — never shown, editable, or shared in the UI

---

## Requirements

- Python 3.9+
- A Google API key with access to Gemini ([Google AI Studio](https://aistudio.google.com/app/apikey))

---

## Local setup

1. **Clone the repo and enter the project folder**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-folder>
   ```

2. **(Recommended) Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate   AND  on Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your API key**

   Create a `.env` file in the project root:
   ```
   GOOGLE_API_KEY=your_key_here
   ```

5. **Run the app**
   ```bash
   streamlit run app.py
   ```
   Opens in your browser, usually at `http://localhost:8501`.

---

## Usage

1. Open the app.
2. Upload a `.txt` blood report, or paste the report text into the **Paste text** tab.
3. Click **Run analysis**.
4. Review the extracted values and the generated health summary + diet plan.
5. Optionally, download the full report as a Markdown file.

---

## Deployment (Railway)

This app is deployed on [Railway](https://railway.app). To deploy your own copy:

1. Push `app.py`, `requirements.txt`, and `Procfile` to a GitHub repo (leave the exploratory `.ipynb` notebook out — it's not needed to run the app, and notebook outputs can accidentally leak sensitive values).
2. On Railway: **New Project → Deploy from GitHub repo** and select the repo.
3. In the project's **Variables** tab, add `GOOGLE_API_KEY` with your real key. This is the only place the key lives — it's read from the environment, never entered or displayed anywhere in the app itself.
4. Once the deploy is **Active**, go to **Settings → Networking → Generate Domain** to get a public URL.

The `Procfile` tells Railway how to start a Streamlit app correctly:
```
web: streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true
```
The `$PORT` binding matters — Railway assigns a random port at runtime, and Streamlit needs to listen on it rather than the default `8501`.

---

## Project structure

```
.
├── app.py               # Streamlit application
├── requirements.txt      # Python dependencies
├── Procfile               # Railway start command
├── .gitignore             # Keeps .env and other local files out of git
└── README.md              # This file
```

---

## Security notes

- The API key is **never hardcoded** and **never entered through the UI** — it's read exclusively from the `GOOGLE_API_KEY` environment variable (`.env` locally, a Railway variable in production).
- `.gitignore` excludes `.env` so the key can never be accidentally committed.
- If forking or sharing this repo, set your own `GOOGLE_API_KEY` in your own environment — don't hardcode it into `app.py`.

---