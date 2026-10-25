# celebrait — Testing Documentation & Manual Verification Log

This document records the comprehensive functional, validation, error-handling, output, security, and usability test results for **celebrait (Version 1)**.

---

## 1. Test Metadata

- **Test Date:** 25 October 2026
- **Test Environments:**
  1. **Local Environment:** Windows 11, Python 3.14, Streamlit 1.44+, `google-genai` SDK, launched via `streamlit run app.py`.
  2. **Cloud Environment:** Streamlit Community Cloud (Linux container, Python 3.11+, `GEMINI_API_KEY` injected via Streamlit Secrets).
- **Tester / Evaluator:** Antigravity Pair Programmer & Local Testing Suite
- **Overall Result:** 19 / 19 Tests Passed (100% Pass Rate)

---

## 2. Test Execution Log

| # | Test Case | Target Layer | Test Inputs / Scenario | Expected Result | Actual Result | Status |
| :-: | :--- | :--- | :--- | :--- | :--- | :-: |
| **1** | Wedding with ₹50,000 budget | Presentation / Application / AI | Type: Wedding, Date: +60 days, Guests: 80, Budget: 50,000, Currency: INR (Rs.), City: Delhi | Generates complete 7-section plan tailored to wedding, uses INR consistently, budget table scales to 80 guests. | All 7 sections generated; INR budget table matches 50,000 limit with sensible category allocations. | **PASS** |
| **2** | Birthday with 20 guests | Presentation / Application / AI | Type: Birthday, Date: +14 days, Guests: 20, Budget: 15,000, Currency: INR (Rs.), City: Pune | Generates small-scale, intimate birthday plan; budget and timeline scaled for 2 weeks remaining. | Intimate venue/catering recommendations; timeline starts immediately; budget scaled appropriately. | **PASS** |
| **3** | Community event with 200 guests | Presentation / Application / AI | Type: Community Event, Date: +90 days, Guests: 200, Budget: 200,000, Currency: INR (Rs.), City: Bengaluru | Generates large-scale event plan with crowd logistics, public safety, PA system, and permits. | Practical vendor & permits checklist; crowd management in risk checklist; budget scaled for 200 attendees. | **PASS** |
| **4** | Optional fields (Theme & Requirements) | Application / AI | Blank theme and requirements vs. Populated ("Royal Heritage", "Vegetarian catering") | Handles blank state gracefully ("not specified" / "none"); incorporates theme & diet when provided. | Verified prompt dynamically adapts without errors; AI recommendations reflect custom preferences. | **PASS** |
| **5** | Missing event type | Application (Validator) | `event_type = ""` | Stops before Gemini; shows clear validation warning to select an event type. | Warning displayed: "Event type: please select an event type."; Gemini not called. | **PASS** |
| **6** | Missing city or region | Application (Validator) | `city = ""` or whitespace only | Stops before Gemini; warns that city is required for local recommendations. | Warning displayed: "City or region: this field is required..."; Gemini not called. | **PASS** |
| **7** | Zero or negative budget | Application (Validator) | `budget = 0` and `budget = -500` | Stops before Gemini; warns that budget must be greater than zero. | Warning displayed: "Total budget: must be greater than 0..."; Gemini not called. | **PASS** |
| **8** | Invalid guest count | Application (Validator) | `guests = 0` or negative | Stops before Gemini; warns that guests must be at least 1. | Warning displayed: "Number of guests: must be a whole number of at least 1."; Gemini not called. | **PASS** |
| **9** | Past event date | Application (Validator) | `event_date = yesterday` | Stops before Gemini; warns that date must be today or in the future. | Warning displayed: "Event date: the date must be today... or a future date."; Gemini not called. | **PASS** |
| **10** | Missing currency | Application (Validator) | `currency = ""` | Stops before Gemini; warns that currency selection is required. | Warning displayed: "Currency: please select a currency."; Gemini not called. | **PASS** |
| **11** | Invalid inputs execution barrier | Application (Validator) | Any combination of invalid inputs | AI API call is completely blocked; zero API tokens or network requests consumed. | Validated in local test: `generate_event_plan` is never reached when `is_valid` is `False`. | **PASS** |
| **12** | Missing API key | AI Service / Security | Unset `GEMINI_API_KEY` and empty `st.secrets` | Shows setup instructions for Windows/macOS/Linux and Streamlit Secrets; does not crash. | Informative error box rendered with exact setup commands and Google AI Studio link; no crash. | **PASS** |
| **13** | Gemini API failure & credential safety | AI Service / Security | Pass malformed key or invalid request format | Shows user-friendly error category; zero credentials, headers, or stack traces exposed. | Safe message displayed: "Gemini API key is invalid..."; no token or raw traceback leaked in UI or terminal. | **PASS** |
| **14** | Empty Gemini response | Output / Presentation | Model returns empty string or whitespace | Warns user that response was empty and suggests retrying. | Warning rendered: "Gemini returned an empty response. Please try again in a moment." | **PASS** |
| **15** | Temporary Gemini server error (5xx) | AI Service Layer | Mock 503 Service Unavailable / ServerError | Retries up to 2 times with backoff, then renders polite retry-later notice. | Retry mechanism triggered twice; on repeated failure shows friendly server-busy message. | **PASS** |
| **16** | Markdown rendering | Output / Presentation | Successful AI Markdown response | Headings (h2), bullet lists, and category-wise budget table render with correct formatting. | Table formatted cleanly with columns `Category | Estimated Cost | Notes`; typography is consistent. | **PASS** |
| **17** | `event_plan.md` download | Output / Presentation | Click "Download Event Plan" button | Downloads valid UTF-8 Markdown file matching the displayed plan. | Button active only after generation; file downloads as `event_plan.md` with exact text. | **PASS** |
| **18** | Disclaimer visibility | Presentation Layer | Page load and post-generation view | Prominently informs user that vendor details, prices, and availability are planning estimates. | Displayed directly below generated plan and in the page footer box. | **PASS** |
| **19** | Mobile & desktop usability | Presentation / Accessibility | Browser resized to mobile viewport (375px) and desktop (1440px) | Sidebar collapses cleanly into mobile drawer; controls and tables remain readable without overflow. | Verified layout reflows smoothly; touch targets and buttons remain easily clickable. | **PASS** |

---

## 3. Summary of Verification Highlights

1. **Security Compliance:**
   - No API keys appear in source code, logs, terminal output, git diff, or error messages.
   - Credentials are read securely via `st.secrets` with fallback to `os.environ`.
2. **Reliability & Error Isolation:**
   - Strict input validation acts as a circuit breaker preventing unnecessary Gemini calls.
   - Granular error categorizer maps exceptions safely to 5 distinct categories (Authentication, Quota, Configuration, Server, Network).
   - Server errors (5xx) automatically retry with backoff before gracefully alerting the user.
3. **Accessibility:**
   - Clear labels, helper tooltips, and placeholders on every widget.
   - Validation warnings use explicit text labels and warning icons (`⚠️`) rather than color alone.
   - Buttons feature accessible labels and tooltips.
