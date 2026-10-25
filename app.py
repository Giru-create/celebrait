"""
celebrait — GenAI-Powered Celebration & Event Planner
app.py — Main Streamlit application (Phase 1 & 2: UI and input validation)

Sections:
    1. Page configuration
    2. UI helpers
    3. Sidebar event input form
    4. Input validation
    5. Main application area
"""

import datetime
import streamlit as st


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
    if not event_data["event_type"]:
        errors.append("Event type: please select an event type.")

    # Event date — must be today or a future date
    if event_data["event_date"] < today:
        errors.append(
            f"Event date: the date must be today ({today.strftime('%d %B %Y')}) "
            "or a future date. Past dates are not accepted."
        )

    # Guests — must be a whole number of at least 1
    if not isinstance(event_data["guests"], int) or event_data["guests"] < 1:
        errors.append(
            "Number of guests: must be a whole number of at least 1."
        )

    # Budget — must be greater than zero
    if event_data["budget"] <= 0:
        errors.append(
            "Total budget: must be greater than 0. "
            "Please enter a realistic budget for your event."
        )

    # Currency — must be a valid, non-empty selection
    if not event_data["currency"]:
        errors.append("Currency: please select a currency.")

    # City or region — required, whitespace already stripped by render_sidebar
    if not event_data["city"]:
        errors.append(
            "City or region: this field is required. "
            "It helps generate locally relevant recommendations."
        )

    # Theme and special requirements are optional — no validation needed

    is_valid = len(errors) == 0
    return is_valid, errors


# ---------------------------------------------------------------------------
# 5. Main application area
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
            # Validation passed — Phase 3 will add Gemini API call here
            st.success(
                "Event details validated successfully. "
                "AI-powered event-plan generation will be added in the next phase."
            )

            # Show a summary of the validated inputs so the user can review them
            st.subheader("Your event at a glance")
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"**Event type:** {event_data['event_type']}")
                st.markdown(
                    f"**Event date:** "
                    f"{event_data['event_date'].strftime('%d %B %Y')}"
                )
                st.markdown(f"**Guests:** {event_data['guests']:,}")
                st.markdown(
                    f"**Budget:** {event_data['currency']} "
                    f"{event_data['budget']:,.0f}"
                )

            with col2:
                st.markdown(f"**City / Region:** {event_data['city']}")
                if event_data["theme"]:
                    st.markdown(f"**Theme:** {event_data['theme']}")
                if event_data["requirements"]:
                    st.markdown(
                        f"**Special requirements:** {event_data['requirements']}"
                    )

    # ---- Disclaimer --------------------------------------------------------
    st.divider()
    show_disclaimer()


if __name__ == "__main__":
    main()
