# celebrait — GenAI-Powered Celebration & Event Planner

**celebrait** is a lightweight, responsive Streamlit web application powered by the Google Gemini API (`google-genai`). It generates personalized event-planning outlines for weddings, birthdays, community gatherings, and celebrations in seconds.

---

## Project Status (Version 1)

Version 1 is fully implemented, tested, and deployed:

- **Implemented:** Streamlit UI, input validation, secure Gemini integration (`google-genai` with `gemini-3.8-flash`), structured seven-section Markdown event plan, Markdown download (`event_plan.md`), verification disclaimer, safe error handling, and Streamlit Community Cloud deployment.
- **Tested:** Valid event generation across small/large budgets and guest counts, invalid-input validation, missing API key handling with setup guidance, Gemini error handling (authentication, quota, server, network), Markdown rendering, and download verification.
- **Deployed:** The application is live on Streamlit Community Cloud with `GEMINI_API_KEY` securely configured in Streamlit Secrets.

---

## Features

- **Personalized Event Concepts:** 3 theme options and 1 customized event concept.
- **Category-wise Budget Plan:** Formatted in Markdown tables with clear estimates scaled to your guest count and currency.
- **Dynamic Planning Timeline:** Actionable task countdown grouped according to days remaining until the event.
- **Vendor Checklist & Inquiries:** Category-specific vendor recommendations and key questions to ask before booking.
- **Day-of-Event Schedule:** Hour-by-hour timeline designed for smooth event day coordination.
- **Risk Precautions & Checklist:** Identification of common regional/event risks and mitigation strategies.
- **Money-Saving Tips:** 5–7 practical ways to reduce expenses without compromising event quality.
- **One-Click Markdown Download:** Download your event plan as `event_plan.md`.

---

## Tech Stack

- **Framework:** Streamlit
- **Language:** Python 3.10+
- **AI SDK:** `google-genai` (Model: `gemini-3.8-flash`)
- **Deployment:** Streamlit Community Cloud

---

## Setup & Local Installation

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/celebrait.git
cd celebrait
```

### 2. Create and activate a virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure your Gemini API key
Get a free Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey).

You can configure your key using either an environment variable or a local Streamlit Secrets file:

**Option A — Environment Variable (Recommended for Local Dev):**
- **Windows (Command Prompt):**
  ```cmd
  set GEMINI_API_KEY=your_gemini_api_key_here
  ```
- **Windows (PowerShell):**
  ```powershell
  $env:GEMINI_API_KEY="your_gemini_api_key_here"
  ```
- **macOS / Linux:**
  ```bash
  export GEMINI_API_KEY="your_gemini_api_key_here"
  ```

**Option B — Local Streamlit Secrets (`.streamlit/secrets.toml`):**
Create `.streamlit/secrets.toml` in the project root:
```toml
GEMINI_API_KEY = "your_gemini_api_key_here"
```

> ⚠️ **Security Warning:** Never commit `.streamlit/secrets.toml`, `.env`, or hardcode API keys into code. These files are listed in `.gitignore` to prevent credential exposure.

### 5. Run the application
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

---

## Deployment to Streamlit Community Cloud

1. Push this repository to a public GitHub repository.
2. Sign in to [share.streamlit.io](https://share.streamlit.io).
3. Click **New app**, select your repository, branch (`main`), and main file path (`app.py`).
4. In the app settings, navigate to **Secrets** and add:
   ```toml
   GEMINI_API_KEY = "your_actual_gemini_api_key"
   ```
5. Click **Deploy**.

---

## Security & Privacy

- API keys are never hardcoded, logged, or committed to GitHub.
- Credentials and local secrets are excluded from Git via `.gitignore`.
- Streamlit Secrets and environment variables are used for secure key injection.

---

## Disclaimer

celebrait provides AI-generated planning estimates. Vendor names, pricing, availability, and local recommendations must be independently verified prior to booking or financial commitments.