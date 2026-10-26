# celebrait — System Architecture

This document defines the official architecture for **celebrait**.

Both OpenCode and Antigravity must follow this architecture when creating, modifying, or reviewing project code.

## 1. Architecture Style

celebrait uses a simple **layered monolithic architecture**.

It is a single Streamlit application with clearly separated responsibilities:

1. Presentation layer — Streamlit UI
2. Application layer — validation and prompt building
3. AI service layer — Google Gemini API integration
4. Output layer — Markdown rendering and file download

Do not convert the project into a microservices architecture, add a backend server, or introduce a database unless the user explicitly requests it.

## 2. High-Level Architecture

```text
+----------------------+
|        User          |
+----------------------+
          |
          | Event details
          v
+----------------------+
|     Streamlit UI     |
|  Presentation Layer  |
+----------------------+
          |
          | Raw inputs
          v
+----------------------+
|    Input Validator   |
|   Application Layer  |
+----------------------+
          |
          | Validated data
          v
+----------------------+
|     Prompt Builder   |
|   Application Layer  |
+----------------------+
          |
          | Structured prompt
          v
+----------------------+
|     Gemini Service   |
|       AI Layer       |
+----------------------+
          |
          | Markdown response
          v
+----------------------+
|    Output Renderer   |
|     Output Layer     |
+----------------------+
          |
          | Event plan
          v
+----------------------+
|  User sees/downloads |
|       the plan       |
+----------------------+
```

## 3. Project Structure

The project must follow this structure:

```text
celebrait/
├── .streamlit/
│   └── config.toml
├── AGENTS.md
├── ARCHITECTURE.md
├── PROJECT_REPORT.md
├── README.md
├── TESTING.md
├── app.py
├── requirements.txt
└── .gitignore
```

### Version 1 file responsibilities

| File                | Responsibility                                                                               |
| ------------------- | -------------------------------------------------------------------------------------------- |
| `app.py`            | Main Streamlit application, UI, validation, prompt creation, Gemini call, and output display |
| `requirements.txt`  | Python dependencies                                                                          |
| `README.md`         | Project documentation and setup instructions                                                 |
| `AGENTS.md`         | Rules for OpenCode and Antigravity                                                           |
| `ARCHITECTURE.md`   | Official system architecture                                                                 |
| `PROJECT_REPORT.md` | Project goals, features, testing, and future scope                                           |
| `.gitignore`        | Prevents secrets and unnecessary files from being committed                                  |

For Version 1, all application logic may remain in `app.py`.

If the file becomes too large, split it only into these modules:

```text
celebrait/
├── app.py
├── utils/
│   ├── validator.py
│   ├── prompt_builder.py
│   └── gemini_service.py
```

Do not create extra modules unless they are genuinely needed.

## 4. Component Architecture

### 4.1 Presentation Layer

**Technology:** Streamlit  
**Main file:** `app.py`

Responsibilities:

- Display the app title and description.
- Collect event details in the sidebar.
- Provide a primary “Generate event plan” button.
- Display validation messages.
- Display the generated event plan using `st.markdown()`.
- Provide a Markdown download button.
- Show loading feedback while Gemini is generating the plan.

Allowed Streamlit components:

- `st.title()`
- `st.caption()`
- `st.sidebar`
- `st.selectbox()`
- `st.date_input()`
- `st.number_input()`
- `st.text_input()`
- `st.text_area()`
- `st.button()`
- `st.spinner()`
- `st.markdown()`
- `st.download_button()`
- `st.error()`
- `st.warning()`

The UI must remain clean, mobile-friendly, and beginner-friendly.

### 4.2 Application Layer

**Responsibility:** Validate inputs and prepare the AI request.

This layer must contain:

- Input validation
- Budget and guest-count checks
- Date validation
- Prompt construction
- Error handling before calling Gemini

#### Validation rules

| Input                | Rule                   |
| -------------------- | ---------------------- |
| Event type           | Must be selected       |
| Event date           | Must be today or later |
| Guests               | Must be at least 1     |
| Budget               | Must be greater than 0 |
| City or region       | Required               |
| Theme                | Optional               |
| Special requirements | Optional               |

If validation fails, the app must stop and show a clear Streamlit warning.

### 4.3 AI Service Layer

**Technology:** Google Gemini API  
**Python package:** `google-genai`

Responsibilities:

- Read `GEMINI_API_KEY` from the environment.
- Create the Gemini client.
- Send the structured prompt to Gemini.
- Receive the Markdown response.
- Return the response text to the presentation layer.
- Handle API errors gracefully.

Security rules:

- Never hardcode the API key.
- Never print, log, display, or commit the API key.
- Never store the API key in the repository.
- Use Streamlit Secrets or environment variables in deployment.

### 4.4 Output Layer

**Responsibility:** Convert the Gemini response into a user-friendly result.

Responsibilities:

- Render the Gemini Markdown response.
- Display budget tables, timelines, and checklists properly.
- Provide a download button for `event_plan.md`.
- Show a disclaimer that costs and vendor details are estimates.

## 5. Data Flow

### 5.1 Input data

```text
event_type
event_date
guests
budget
currency
city
theme
requirements
```

### 5.2 Internal data object

The application should collect these values into a single dictionary:

```python
event_data = {
    "event_type": event_type,
    "event_date": event_date,
    "guests": guests,
    "budget": budget,
    "currency": currency,
    "city": city,
    "theme": theme,
    "requirements": requirements,
}
```

### 5.3 Output data

Gemini must return Markdown text containing:

1. Event Concept
2. Budget Plan
3. Planning Timeline
4. Vendor Checklist
5. Day-of-Event Schedule
6. Risk Checklist
7. Money-Saving Tips

The app must display this Markdown directly and allow the user to download it.

## 6. Prompt Flow

```text
User inputs
   ↓
Validation
   ↓
Prompt template
   ↓
Final Gemini prompt
   ↓
Gemini API
   ↓
Markdown event plan
```

The prompt must always include:

- Event type
- Event date and calculated days countdown
- Expected number of guests
- Total budget and specified currency
- City or region
- Optional theme or vibe
- Optional special requirements

## 7. Version 1 Architecture & Deployment Status

Version 1 is implemented, tested, and deployed in accordance with this specification:

- **Layer 1 (Presentation):** Streamlit UI (`app.py`), sidebar form, input validation error summaries, Markdown output rendering, disclaimer callout, and `event_plan.md` download button.
- **Layer 2 (Application):** Input validator (`validate_event_data`) enforcing required fields and boundaries; prompt builder (`build_event_prompt`) assembling the structured seven-section prompt.
- **Layer 3 (AI Service):** Google Gemini API integration via `google-genai` using model `gemini-3.5-flash-lite` with progressive response streaming (`stream_event_plan`), secure key loading (`load_api_key`) prioritizing Streamlit Secrets with environment variable fallback, safe exception mapping (`handle_gemini_error`), and transient error retry logic.
- **Layer 4 (Output):** Direct Streamlit Markdown rendering and one-click file download.
- **Deployment:** Live on Streamlit Community Cloud with `GEMINI_API_KEY` configured in Streamlit Secrets.
