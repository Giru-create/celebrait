# celebrait — Project Report

## 1. Project Title

**celebrait — GenAI-Powered Celebration & Event Planner**

## 2. Project Overview

celebrait is a GenAI-powered web application that helps users plan weddings, birthdays, community events, and other celebrations.

Users enter basic event details such as event type, date, number of guests, budget, city, theme, and special requirements. The application uses Google Gemini to generate a personalized event plan containing theme ideas, a budget breakdown, a planning timeline, a vendor checklist, a day-of-event schedule, risk precautions, and money-saving tips.

## 3. Problem Statement

Planning an event is difficult because users must manage many tasks at once: choosing a theme, estimating costs, booking vendors, preparing schedules, handling guests, and managing last-minute risks.

Most people either hire an expensive event planner or manage everything manually using notes, spreadsheets, and scattered online searches.

celebrait solves this by generating a structured, personalized event-planning assistant in seconds.

## 4. Objectives

- Build a simple Streamlit-based GenAI event planner.
- Generate personalized plans for weddings, birthdays, and community events.
- Create a practical budget breakdown based on the user’s total budget.
- Generate a countdown timeline based on the event date.
- Provide vendor categories, verification questions, and booking guidance.
- Generate a day-of-event schedule and risk checklist.
- Allow users to download the generated event plan.
- Keep the application free, lightweight, and deployable on Streamlit Community Cloud.

## 5. Target Users

- Individuals planning birthdays or family celebrations
- Couples planning weddings
- Community organizations planning local events
- Students and volunteers organizing college or society events
- Small event organizers who need a quick starting plan

## 6. Proposed Solution

celebrait converts user inputs into a detailed prompt and sends it to the Google Gemini API. The AI response is displayed as a structured Markdown event plan inside Streamlit.

The application does not replace professional event planners. Instead, it acts as an intelligent starting point that helps users organize their ideas, budget, timeline, and vendor requirements.

## 7. System Architecture

```text
User Inputs
     ↓
Streamlit UI
     ↓
Input Validation
     ↓
Prompt Builder
     ↓
Google Gemini API
     ↓
Structured Event Plan
     ↓
Streamlit Markdown Display
     ↓
Downloadable Event Plan
```

### Main components

| Component         | Purpose                                     |
| ----------------- | ------------------------------------------- |
| Streamlit UI      | Collects event details from the user        |
| Input validator   | Checks required fields and invalid values   |
| Prompt builder    | Converts user inputs into a clear AI prompt |
| Gemini API        | Generates the personalized event plan       |
| Markdown renderer | Displays the AI-generated plan clearly      |
| Download module   | Lets users save the generated plan          |

## 8. Features

### Version 1 features

- Event type selection
- Event date selection
- Guest count input
- Budget input with currency selection
- City or region input
- Theme or vibe input
- Special requirements input
- AI-generated event concepts
- Budget plan with estimated category-wise spending
- Planning timeline
- Vendor checklist
- Day-of-event schedule
- Risk checklist
- Money-saving tips
- Downloadable Markdown event plan

### How Core Features Solve the Planning Problem

| Feature | Problem Solved |
| :--- | :--- |
| **Personalized Event Concepts** | Resolves creative block, theme indecision, and lack of cohesive celebration styling. |
| **Category-wise Budget Table** | Eliminates guesswork and budget overruns by distributing total funds across essential categories. |
| **Dynamic Planning Timeline** | Solves task overload by calculating actual days remaining and grouping tasks into clear milestones. |
| **Vendor Checklist & Questions** | Reduces booking mistakes by identifying necessary vendor types and critical vetting questions. |
| **Day-of-Event Schedule** | Prevents day-of delays and confusion by establishing a structured hour-by-hour operational agenda. |
| **Risk Precautions & Checklist** | Proactively mitigates hidden failure points (e.g., weather shifts, power backup, parking, guest surges). |
| **Money-Saving Tips** | Prevents unnecessary debt or overspending with 5–7 actionable, quality-preserving cost cuts. |
| **Downloadable Markdown Plan** | Ensures immediate portability so users can share, store, or edit the plan in any notes or task tool. |

## 9. Technology Stack

| Layer              | Technology                                |
| ------------------ | ----------------------------------------- |
| Frontend           | Streamlit                                 |
| Backend logic      | Python                                    |
| Generative AI      | Google Gemini API                         |
| AI SDK             | `google-genai`                            |
| Version control    | Git and GitHub                            |
| Deployment         | Streamlit Community Cloud                 |
| Secrets management | Environment variables / Streamlit Secrets |

## 10. User Input Fields

| Field                | Description                                          |
| -------------------- | ---------------------------------------------------- |
| Event type           | Wedding, birthday, community event, etc.             |
| Event date           | Date of the planned event                            |
| Guests               | Expected number of attendees                         |
| Budget               | Total available budget                               |
| Currency             | INR, USD, etc.                                       |
| City or region       | Used for local planning context                      |
| Theme or vibe        | Traditional, modern, minimal, colorful, etc.         |
| Special requirements | Food preferences, accessibility, outdoor venue, etc. |

## 11. AI Prompt Strategy

The application uses one structured prompt to ensure consistent output.

The prompt instructs Gemini to return:

1. Event concept with three theme ideas
2. Budget plan in table format
3. Planning timeline grouped by time remaining
4. Vendor checklist with key questions
5. Day-of-event schedule
6. Risk checklist
7. Money-saving tips

The prompt also instructs the model to mark all prices and vendor information as estimates and avoid presenting unverified information as fact.

## 12. Implementation & Project Status

Version 1 is now fully implemented, tested, and deployed:

- **Implemented:**
  - Streamlit UI with responsive sidebar input form and clean main display
  - Robust client-side input validation
  - Secure Gemini API integration using the official `google-genai` SDK (`gemini-3.8-flash`)
  - Structured prompt building generating a complete seven-section Markdown event plan:
    1. Event Concept
    2. Budget Plan (Markdown table)
    3. Planning Timeline
    4. Vendor Checklist
    5. Day-of-Event Schedule
    6. Risk Checklist
    7. Money-Saving Tips
  - One-click Markdown plan download (`event_plan.md`)
  - Verification disclaimer visible below generated plan and in footer
  - Safe error categorization protecting credentials, raw headers, and stack traces
  - Transient server error (5xx) retry logic with backoff
  - Live deployment on Streamlit Community Cloud

- **Tested:**
  - Valid event generation (wedding with ₹50,000, birthday with 20 guests, community event with 200 guests)
  - Strict invalid-input validation (missing event type, missing city, zero/negative budget, invalid guest count, past date, missing currency)
  - Missing API key handling with setup guidance
  - Gemini error handling (authentication, model misconfiguration, quota, temporary server error, network)
  - Markdown rendering and table formatting
  - `event_plan.md` download matching displayed content

- **Deployed:**
  - The application is live on Streamlit Community Cloud with `GEMINI_API_KEY` configured securely in Streamlit Secrets.

## 13. File Structure

```text
celebrait/
├── AGENTS.md
├── PROJECT_REPORT.md
├── README.md
├── app.py
├── requirements.txt
└── .gitignore
```

## 14. Security and Privacy

- The Gemini API key must never be hardcoded.
- The API key must not be committed to GitHub.
- `.env` and `.streamlit/secrets.toml` must remain in `.gitignore`.
- The deployed app must use Streamlit Secrets or environment variables.
- User inputs are used only to generate the event plan.
- The application should not collect or store personal data in Version 1.

## 15. Testing Plan

| Test case                       | Expected result                          |
| ------------------------------- | ---------------------------------------- |
| Wedding with ₹50,000 budget     | Generates a relevant wedding plan        |
| Birthday with 20 guests         | Generates a smaller-scale birthday plan  |
| Community event with 200 guests | Generates a larger-scale community plan  |
| Missing city                    | Shows a warning and stops generation     |
| Zero budget                     | Shows a warning or handles it gracefully |
| Missing API key                 | Shows a clear setup error                |
| Download button                 | Downloads a Markdown event plan          |

## 16. Expected Output

The app should generate a Markdown event plan containing:

- Event concept
- Budget breakdown
- Planning timeline
- Vendor checklist
- Day-of-event schedule
- Risk checklist
- Money-saving tips

## 17. Limitations

- AI-generated vendor names, prices, and availability may be inaccurate.
- The app does not currently verify real-time vendor availability.
- The app does not currently process payments or manage bookings.
- Budget estimates depend on the quality of user inputs.
- The free Gemini API tier may have usage limits.

## 18. Future Scope

- Add guest RSVP tracking.
- Add an expense tracker with remaining-budget calculation.
- Add vendor comparison tables.
- Add regional recommendations for Uttarakhand.
- Add PDF export.
- Add multilingual support, including Hindi.
- Add image generation for décor and invitation ideas.
- Add a chat assistant for follow-up planning questions.

## 19. Expected Impact

celebrait can reduce the initial effort required to plan an event by giving users a clear, structured starting point. It can help users avoid missed tasks, understand budget categories, prepare vendor questions, and plan for common risks.

## 20. Conclusion

celebrait demonstrates how Generative AI can simplify real-life planning tasks. Using Streamlit and the Gemini API, the project provides a practical, accessible, and deployable event-planning assistant for individuals and communities.
