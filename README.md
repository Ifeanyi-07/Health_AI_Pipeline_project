# 🩸 Blood Work Analyzer

A Streamlit app that analyzes a blood report using Google's Gemini model. It runs a two-stage pipeline:

1. **Extraction** – reads the raw blood report and classifies each test value as `HIGH`, `LOW`, or `NORMAL` based on the reference ranges in the report.
2. **Health Summary & Diet Plan** – generates a simple 3-line health summary plus a practical Indian diet plan (foods to avoid / foods to eat more of) based on the extracted values.

> ⚠️ **Disclaimer:** This tool is for informational purposes only and is not a substitute for professional medical advice.

---

## Features

- Upload a `.txt` blood report or paste the text directly
- One-click analysis (extraction → summary → diet plan)
- Download the full result as a Markdown report
- API key entered locally in the sidebar (never hardcoded or committed)

---

## Requirements

- Python 3.9+
- A Google API key with access to Gemini ([Google AI Studio](https://aistudio.google.com/app/apikey))

---

## Setup

1. **Clone the repo and enter the project folder**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-folder>
   ```

2. **(Recommended) Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate   AND # on Windows: venv\Scripts\activate
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
   (Alternatively, skip this step and paste your key directly into the app's sidebar at runtime.)

---

## Running the app

```bash
streamlit run app.py
```

Streamlit will start a local server and open the app in your browser, usually at:

```
http://localhost:8501
```
But it differs atimes, depending on how many streamlit apps you are currently running.

---

## Usage

1. Open the app in your browser.
2. Enter your Gemini API key in the sidebar (if not already set via `.env`).
3. Upload a `.txt` blood report, or paste the report text into the **Paste text** tab.
4. Click **Run analysis**.
5. Review the extracted values and the generated health summary + diet plan.
6. Optionally, download the full report as a Markdown file.

---

## Security notes

- Your API key is **never hardcoded** in the source code.
- Add a `.gitignore` entry for `.env` before pushing to GitHub so your key is never committed:
  ```
  .env
  ```

---

## Project structure

```
.
├── app.py               # Streamlit application
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

---

