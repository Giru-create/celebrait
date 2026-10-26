# celebrait — GenAI-Powered Celebration & Event Planner

**celebrait** is a lightweight, responsive Streamlit web application powered by the Google Gemini API (`google-genai`). It transforms basic event details into a structured, personalized event-planning blueprint in seconds.

---

## 📌 Project Overview

- **The Problem:** Planning celebrations—such as weddings, birthdays, or community gatherings—is fragmented, stressful, and time-consuming. Organizers must balance themes, budgets, vendor bookings, schedules, and unexpected risks. Most people either hire expensive event planners or struggle manually with scattered spreadsheets, messy notes, and unverified online advice.
- **The Solution:** celebrait acts as an intelligent starting point. By processing validated user inputs through Google Gemini, it synthesizes a comprehensive, localized planning outline covering concepts, budget breakdowns, countdown timelines, vendor questions, schedules, precautions, and cost-saving tips in clean Markdown.
- **Target Users:**
  - **Individuals & Families:** Planning birthdays, anniversaries, and family reunions.
  - **Couples:** Organizing weddings on realistic budgets.
  - **Students & Campus Clubs:** Planning college fests, farewells, and society events.
  - **Community Organizers & Volunteers:** Coordinating local festivals, cultural celebrations, and neighborhood gatherings.
  - **Small Event Coordinators:** Requiring a rapid, structured starting outline for client consultations.

---

## 🚀 Project Status (Version 1)

Version 1 is fully implemented, tested, and deployed:

- **Implemented:** Streamlit UI, input validation, progressive response streaming, secure Gemini integration (`google-genai` with `gemini-3.5-flash-lite`), structured seven-section Markdown event plan, Markdown download (`event_plan.md`), verification disclaimer, safe error handling, and Streamlit Community Cloud deployment.
- **Tested:** Valid event generation across small/large budgets and guest counts, invalid-input validation, missing API key handling with setup guidance, Gemini error handling (authentication, quota, server, network), Markdown rendering, and download verification. (See [TESTING.md](TESTING.md)).
- **Deployed:** The application is live on Streamlit Community Cloud with `GEMINI_API_KEY` securely configured in Streamlit Secrets.

---

## ✨ How Core Features Solve the Planning Problem

| Core Feature | How It Solves the Problem |
| :--- | :--- |
| **Personalized Event Concepts** | Overcomes theme indecision by generating 3 tailored theme options and 1 customized event concept. |
| **Category-wise Budget Table** | Prevents budget overruns with a clean Markdown table distributing funds realistically across catering, venue, décor, and photography. |
| **Dynamic Planning Timeline** | Eliminates procrastination and panic by calculating actual days remaining and grouping milestones logically. |
| **Vendor Checklist & Inquiries** | Reduces vendor booking anxiety with category-specific vendor checklists and key questions to ask before hiring. |
| **Day-of-Event Schedule** | Prevents chaos and delays on celebration day with a practical hour-by-hour operational timeline. |
| **Risk Precautions & Checklist** | Identifies easily overlooked failure points (weather, power, parking, guest surges) and pairs them with practical precautions. |
| **Money-Saving Tips** | Prevents unnecessary debt with 5–7 actionable cost-cutting tips that maintain event quality. |
| **One-Click Markdown Download** | Ensures immediate plan portability so users can download `event_plan.md` to edit or share anywhere. |

---

## 🛠️ Tech Stack

- **Frontend / Framework:** Streamlit
- **Language:** Python 3.10+
- **AI SDK:** `google-genai` (Model: `gemini-3.5-flash-lite`)
- **Deployment:** Streamlit Community Cloud

---

## 💻 Setup & Local Installation

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

## ☁️ Deployment to Streamlit Community Cloud

1. Push this repository to a public GitHub repository.
2. Sign in to [share.streamlit.io](https://share.streamlit.io).
3. Click **New app**, select your repository, branch (`main`), and main file path (`app.py`).
4. In the app settings, navigate to **Secrets** and add:
   ```toml
   GEMINI_API_KEY = "your_actual_gemini_api_key"
   ```
5. Click **Deploy**.

---

## 🔒 Security & Privacy

- **Zero Hardcoded Credentials:** API keys are never stored in code, logs, terminal outputs, or git commits.
- **Protected Environment:** `.gitignore` excludes `.env`, `.streamlit/secrets.toml`, virtual environments, and private generated files.
- **Safe Error Categorization:** API errors are safely grouped into user-friendly notifications (authentication, quota, configuration, server, network) without leaking stack traces or raw response headers.

---

## ⚠️ Limitations

- **Planning Estimates Only:** All vendor names, rates, and availability generated by the model are AI estimates and must be independently verified locally.
- **No Direct Bookings / Payments:** celebrait provides planning guidance; it does not process financial transactions, contracts, or live vendor bookings.
- **Not a Replacement for On-Site Directors:** The app serves as an intelligent planning assistant, not an on-site event coordinator.

---

## 🔮 Future Scope (Beyond Version 1)

The following capabilities are reserved for future phases:
- Guest RSVP tracking and digital invitations.
- Live vendor pricing and verified directory integrations.
- Expense tracker with dynamic remaining-budget calculations.
- Direct PDF export option.
- Multilingual support, including Hindi and regional Indian languages.
- Interactive AI chat assistant for follow-up adjustments.