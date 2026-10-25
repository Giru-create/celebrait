"""
celebrait — GenAI-Powered Celebration & Event Planner
app.py — Main Streamlit application (Phases 1-4: UI, validation, Gemini integration, structured output)

Sections:
    1. Page configuration
    2. UI helpers
    3. Sidebar event input form
    4. Input validation
    5. Gemini service
    6. Main application area
"""

import datetime
import os
import time

import streamlit as st
from google import genai
from google.genai import errors


# ---------------------------------------------------------------------------
# 1. Page configuration
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="celebrait — Event Planner",
    page_icon="🎉",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------------------------
# 2. UI helpers
# ---------------------------------------------------------------------------

DISCLAIMER = (
    "**Disclaimer:** celebrait provides AI-generated planning estimates. "
    "Vendor names, prices, availability, and local recommendations must be "
    "independently verified before making any bookings or commitments."
)

EVENT_TYPES = [
    "Wedding",
    "Birthday",
    "Anniversary",
    "College Event",
    "Community Event",
    "Family Gathering",
    "Corporate Event",
    "Religious / Cultural Celebration",
    "Other",
]

CURRENCIES = [
    "INR (Rs.)",
    "USD ($)",
    "EUR (€)",
    "GBP (£)",
    "AED",
    "CAD",
    "AUD",
]


def show_disclaimer():
    """Render the disclaimer in a visually distinct info box."""
    st.info(DISCLAIMER)


# ---------------------------------------------------------------------------
# 3. Sidebar event input form
# ---------------------------------------------------------------------------

def render_sidebar():
    """
    Render all event-detail inputs in the sidebar.
    Returns a dict of raw input values.
    """
    st.sidebar.title("Event Details")
    st.sidebar.caption(
        "Fill in the details below and click **Generate Event Plan** "
        "to create your personalised planning outline."
    )
    st.sidebar.divider()

    event_type = st.sidebar.selectbox(
        "Event type",
        options=EVENT_TYPES,
        help="Select the type of event you are planning.",
    )

    event_date = st.sidebar.date_input(
        "Event date",
        value=datetime.date.today() + datetime.timedelta(days=30),
        min_value=datetime.date.today(),
        help="Choose the date on which the event will take place.",
    )

    guests = st.sidebar.number_input(
        "Expected number of guests",
        min_value=1,
        value=50,
        step=1,
        help="Enter the approximate number of people attending.",
    )

    budget = st.sidebar.number_input(
        "Total budget",
        min_value=0,
        value=50000,
        step=500,
        help="Enter your total available budget for the event.",
    )

    currency = st.sidebar.selectbox(
        "Currency",
        options=CURRENCIES,
        help="Select the currency for your budget.",
    )

    city = st.sidebar.text_input(
        "City or region",
        placeholder="e.g. Mumbai, New Delhi, London",
        help="Enter the city or region where the event will be held.",
    )

    st.sidebar.divider()
    st.sidebar.caption("Optional details")

    theme = st.sidebar.text_input(
        "Theme or vibe (optional)",
        placeholder="e.g. Garden party, Traditional, Modern minimalist",
        help="Describe the overall look and feel you want for the event.",
    )

    requirements = st.sidebar.text_area(
        "Special requirements (optional)",
        placeholder=(
            "e.g. Vegetarian-only catering, outdoor venue, "
            "accessibility needs, kids activities"
        ),
        help="List any specific needs or preferences for the event.",
    )

    # Trim whitespace on free-text fields so validation is not fooled by spaces
    return {
        "event_type": event_type,
        "event_date": event_date,
        "guests": guests,
        "budget": budget,
        "currency": currency,
        "city": city.strip(),
        "theme": theme.strip(),
        "requirements": requirements.strip(),
    }


# ---------------------------------------------------------------------------
# 4. Input validation
# ---------------------------------------------------------------------------

def validate_event_data(event_data):
    """
    Validate every required field in event_data against the rules defined
    in ARCHITECTURE.md §4.2.

    Collects every failing rule into a list so the user can fix all
    problems in one pass rather than one at a time.

    Returns:
        (bool, list[str]): (is_valid, errors)
        errors is an empty list when all fields pass.
    """
    today = datetime.date.today()
    errors = []

    # Event type — must be a non-empty selection
    if not event_data.get("event_type") or not str(event_data.get("event_type")).strip():
        errors.append("Event type: please select an event type.")

    # Event date — must be today or a future date
    event_date = event_data.get("event_date")
    if not event_date or event_date < today:
        errors.append(
            f"Event date: the date must be today ({today.strftime('%d %B %Y')}) "
            "or a future date. Past dates are not accepted."
        )

    # Guests — must be a whole number of at least 1
    guests = event_data.get("guests")
    if not isinstance(guests, int) or guests < 1:
        errors.append(
            "Number of guests: must be a whole number of at least 1."
        )

    # Budget — must be greater than zero
    budget = event_data.get("budget")
    if budget is None or budget <= 0:
        errors.append(
            "Total budget: must be greater than 0. "
            "Please enter a realistic budget for your event."
        )

    # Currency — must be a valid, non-empty selection
    if not event_data.get("currency") or not str(event_data.get("currency")).strip():
        errors.append("Currency: please select a currency.")

    # City or region — required, whitespace already stripped by render_sidebar
    city = event_data.get("city")
    if not city or (isinstance(city, str) and not city.strip()):
        errors.append(
            "City or region: this field is required. "
            "It helps generate locally relevant recommendations."
        )

    # Theme and special requirements are optional — no validation needed

    is_valid = len(errors) == 0
    return is_valid, errors


# ---------------------------------------------------------------------------
# 5. Gemini service
# ---------------------------------------------------------------------------

# The model identifier used here is the current stable Gemini Flash model.
# Verified against Google Gemini API documentation.
GEMINI_MODEL = "gemini-3.8-flash"


def load_api_key():
    """
    Load GEMINI_API_KEY securely.

    Checks Streamlit Secrets first (for deployed apps on Streamlit Community
    Cloud), then falls back to the GEMINI_API_KEY environment variable for
    local development.

    Returns:
        str or None: The API key string, or None if not found or empty.
    """
    # 1. Try Streamlit Secrets (set via Streamlit Community Cloud dashboard or secrets.toml)
    try:
        key = st.secrets.get("GEMINI_API_KEY")
        if key and str(key).strip():
            return str(key).strip()
    except Exception:
        # st.secrets is not available in all environments — fall through
        pass

    # 2. Fall back to the environment variable for local development
    env_key = os.environ.get("GEMINI_API_KEY")
    if env_key and env_key.strip():
        return env_key.strip()

    return None


def handle_gemini_error(exc):
    """
    Categorise a Gemini exception into a safe user-facing message and a
    non-sensitive category for terminal logging.

    Never exposes the raw API key, headers, payload, or full stack trace.

    Args:
        exc (Exception): The exception caught during the Gemini API call.

    Returns:
        tuple[str, str]: (user_message, terminal_log_category)
    """
    err_str = str(exc).lower()
    msg_str = str(getattr(exc, "message", "")).lower()
    combined = f"{err_str} {msg_str}"
    code = getattr(exc, "code", None)

    # 1. Invalid, missing, or expired API key
    if (
        code in (401, 403)
        or any(
            token in combined
            for token in [
                "api key not valid",
                "api_key_invalid",
                "api key",
                "unauthenticated",
                "permission_denied",
                "forbidden",
            ]
        )
    ):
        return (
            "Gemini API key is invalid, missing, or expired. "
            "Please create or update your GEMINI_API_KEY in Streamlit Secrets "
            "or as an environment variable with a valid key from Google AI Studio "
            "(https://aistudio.google.com/apikey).",
            "Gemini client error",
        )

    # 2. Quota / rate limit exceeded
    if code == 429 or any(
        token in combined
        for token in [
            "resource_exhausted",
            "quota",
            "rate limit",
            "too many requests",
        ]
    ):
        return (
            "Gemini API quota or rate limit exceeded. "
            "Please wait a moment and retry later.",
            "Gemini client error",
        )

    # 3. Model or request-format issue
    if code == 404 or (
        isinstance(exc, errors.ClientError)
        and any(
            token in combined
            for token in [
                "not_found",
                "model",
                "invalid_argument",
                "bad request",
            ]
        )
    ):
        return (
            "The Gemini request could not be processed due to a model or "
            "request-format issue. The Gemini request configuration needs correction.",
            "Gemini client error",
        )

    # 4. Server error (5xx)
    if isinstance(exc, errors.ServerError) or (
        isinstance(code, int) and code >= 500
    ):
        return (
            "Gemini service is temporarily unavailable due to a server issue. "
            "Please retry later.",
            "Gemini server error",
        )

    # 5. Network / connection error
    if any(
        token in combined
        for token in [
            "connection",
            "timeout",
            "timed out",
            "network",
            "unreachable",
            "getaddrinfo",
        ]
    ):
        return (
            "Unable to reach the Gemini service. "
            "Please check your network connection and retry later.",
            "Gemini network error",
        )

    # 6. Fallback client or temporary error
    if isinstance(exc, errors.ClientError):
        return (
            "A Gemini client error occurred. "
            "Please verify your request configuration and retry later.",
            "Gemini client error",
        )

    return (
        "A temporary issue occurred while contacting Gemini. "
        "Please retry later.",
        "Gemini client error",
    )


def build_event_prompt(event_data):
    """
    Build the full structured seven-section event-planning prompt from
    validated event details.

    The prompt instructs Gemini to return a single, well-formatted Markdown
    document with exactly the sections listed in ARCHITECTURE.md §5.3.

    Args:
        event_data (dict): Validated event details from render_sidebar().

    Returns:
        str: The complete prompt string ready to send to Gemini.
    """
    # Calculate days until the event so the timeline section is realistic
    days_until_event = (event_data["event_date"] - datetime.date.today()).days

    # Include optional fields only when the user supplied them
    theme_line = (
        f"Theme or vibe: {event_data['theme']}"
        if event_data["theme"]
        else "Theme or vibe: not specified"
    )
    requirements_line = (
        f"Special requirements: {event_data['requirements']}"
        if event_data["requirements"]
        else "Special requirements: none"
    )

    prompt = (
        "You are an experienced, practical event-planning assistant.\n\n"
        "A user needs a complete event plan for the following event:\n\n"
        f"- Event type: {event_data['event_type']}\n"
        f"- Event date: {event_data['event_date'].strftime('%d %B %Y')} "
        f"({days_until_event} days from today)\n"
        f"- Expected guests: {event_data['guests']}\n"
        f"- Total budget: {event_data['currency']} {event_data['budget']:,.0f}\n"
        f"- City or region: {event_data['city']}\n"
        f"- {theme_line}\n"
        f"- {requirements_line}\n\n"
        "Please write a complete event plan in Markdown with EXACTLY these "
        "seven sections, using these exact headings:\n\n"
        "## Event Concept\n"
        "Provide three suitable theme ideas and one personalised event concept. "
        "Tailor ideas to the event type, city or region, guest count, and theme "
        "if one was provided.\n\n"
        "## Budget Plan\n"
        "Create a category-wise estimated budget in a Markdown table with "
        "columns: Category | Estimated Cost | Notes. "
        f"The total must not exceed {event_data['currency']} {event_data['budget']:,.0f}. "
        f"Use {event_data['currency']} consistently throughout. "
        "Scale spending categories sensibly for "
        f"{event_data['guests']} guests.\n\n"
        "## Planning Timeline\n"
        f"Group planning tasks based on {days_until_event} days remaining. "
        "Use time-based groups such as 'Immediately', 'Within the next 2 weeks', "
        "'1 month before', '1 week before', and 'Day before / Day of'. "
        "Adjust group labels to match the actual days available.\n\n"
        "## Vendor Checklist\n"
        "List the relevant vendor categories for this event type and size. "
        "For each category, include: a short booking note and two or three "
        "important questions to ask the vendor before booking. "
        f"Make recommendations practical for {event_data['city']}.\n\n"
        "## Day-of-Event Schedule\n"
        "Create a practical hour-by-hour schedule of key activities for the "
        "event day. Adjust timing and activities to suit the event type and "
        f"a guest count of {event_data['guests']}.\n\n"
        "## Risk Checklist\n"
        "Identify the most likely risks for this type of event in this city or "
        "region, and list one practical precaution for each risk.\n\n"
        "## Money-Saving Tips\n"
        "Provide five to seven practical, specific tips to reduce costs without "
        "reducing the quality or experience of the event. "
        "Tailor tips to the event type, city, and budget.\n\n"
        "Important rules:\n"
        "- Treat all vendor names, prices, and availability as ESTIMATES only. "
        "Do not claim any vendor is verified, bookable, or guaranteed.\n"
        "- Do not claim real-time availability for any service or product.\n"
        "- Avoid presenting any vendor as verified or bookable.\n"
        "- Make recommendations practical for the provided city or region, "
        "noting that all recommendations must be independently verified locally.\n"
        f"- Use {event_data['currency']} consistently for every monetary value.\n"
        "- Scale recommendations appropriately for the guest count and budget.\n"
        "- Use the event date to create a realistic planning timeline.\n"
        "- Incorporate the theme and special requirements when provided.\n"
        "- Return clean, readable Markdown only. "
        "Do not add any text before the first heading or after the last section."
    )

    return prompt


def generate_event_plan(event_data, api_key, max_retries=2):
    """
    Build the structured prompt and send it to the Gemini API.
    Retries safely on transient server errors (5xx) with backoff.

    Args:
        event_data (dict): Validated event details.
        api_key (str): The Gemini API key.
        max_retries (int): Maximum retry attempts for transient server errors.

    Returns:
        str or None: The Gemini response text, or None on failure.
    """
    prompt = build_event_prompt(event_data)
    client = genai.Client(api_key=api_key)

    last_error = None
    for attempt in range(max_retries + 1):
        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
            )
            return response.text
        except errors.ServerError as err:
            last_error = err
            if attempt < max_retries:
                time.sleep(1.0 * (attempt + 1))
            else:
                raise
        except Exception:
            raise

    if last_error:
        raise last_error


# ---------------------------------------------------------------------------
# 6. Main application area
# ---------------------------------------------------------------------------

def main():
    # ---- App header --------------------------------------------------------
    st.title("celebrait")
    st.caption(
        "GenAI-powered celebration and event planning assistant — "
        "create a personalised event-planning outline in seconds."
    )
    st.write(
        "Enter your event details in the sidebar on the left. "
        "celebrait will use those details to generate a structured outline "
        "covering your event concept, budget plan, planning timeline, "
        "vendor checklist, day-of-event schedule, risk checklist, "
        "and money-saving tips."
    )

    st.divider()

    # ---- Sidebar form ------------------------------------------------------
    event_data = render_sidebar()

    # ---- Generate button ---------------------------------------------------
    generate_clicked = st.button(
        "Generate Event Plan",
        type="primary",
        use_container_width=False,
    )

    # ---- Button logic ------------------------------------------------------
    if generate_clicked:
        is_valid, errors = validate_event_data(event_data)

        if not is_valid:
            # Show all validation problems together so the user can fix
            # everything in one pass
            error_lines = "\n".join(f"- {e}" for e in errors)
            st.warning(
                f"Please fix the following before generating your event plan:\n\n"
                f"{error_lines}"
            )
        else:
            # Validation passed — load the API key and call Gemini
            api_key = load_api_key()

            if not api_key:
                # Show setup guidance and stop — never crash or expose details
                st.error(
                    "Gemini API key not found.\n\n"
                    "**To run locally:** Set the environment variable before "
                    "starting Streamlit:\n"
                    "```\n"
                    "set GEMINI_API_KEY=your_key_here   # Windows\n"
                    "export GEMINI_API_KEY=your_key_here  # macOS / Linux\n"
                    "streamlit run app.py\n"
                    "```\n"
                    "**On Streamlit Community Cloud:** Add `GEMINI_API_KEY` "
                    "in the app's Secrets settings (Settings → Secrets).\n\n"
                    "Get a free key at https://aistudio.google.com/apikey"
                )
            else:
                # Call Gemini with a loading spinner
                with st.spinner("Generating your event planning outline…"):
                    try:
                        plan_text = generate_event_plan(event_data, api_key)

                        if not plan_text or not plan_text.strip():
                            # Empty response — ask user to retry
                            st.warning(
                                "Gemini returned an empty response. "
                                "Please try again in a moment."
                            )
                        else:
                            # Display the complete AI-generated event plan
                            st.subheader("Your event plan")
                            st.markdown(plan_text)

                            # Inline disclaimer below the plan
                            st.info(
                                "celebrait provides AI-generated planning estimates. "
                                "Vendor names, prices, availability, and local "
                                "recommendations must be independently verified."
                            )

                            # Download button — visible only after a successful plan
                            st.download_button(
                                label="Download Event Plan",
                                data=plan_text,
                                file_name="event_plan.md",
                                mime="text/markdown",
                            )

                    except Exception as exc:
                        # Categorise the error safely without exposing raw credentials,
                        # headers, or stack traces
                        user_message, terminal_category = handle_gemini_error(exc)
                        print(f"[celebrait] {terminal_category}")
                        st.error(user_message)

    # ---- Disclaimer --------------------------------------------------------
    st.divider()
    show_disclaimer()


if __name__ == "__main__":
    main()
