"""
celebrait — GenAI-Powered Celebration & Event Planner
app.py — Main Streamlit application (Version 1: UI, validation, Gemini integration, structured output)

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
    page_icon="✨",
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


def inject_custom_styles():
    """
    Inject high-fashion 'Celebration Atelier' aesthetic with layered Obsidian-Noir,
    Champagne-Gold leaf (#DAB76E) accents, sculptural Fraunces & Italiana typography,
    subtle star-dusk geometric background, and staggered entry micro-animations.
    """
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..800;1,9..144,300..800&family=Italiana&family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400;1,500&display=swap');

        :root {
            --atelier-bg-canvas: #090B0E;
            --atelier-bg-surface: #11141D;
            --atelier-bg-card: rgba(18, 22, 32, 0.78);
            --atelier-bg-card-hover: rgba(26, 32, 46, 0.92);
            --atelier-gold: #DAB76E;
            --atelier-gold-bright: #F7E4B5;
            --atelier-gold-deep: #A4833E;
            --atelier-amber: #E07A5F;
            --atelier-border: rgba(218, 183, 110, 0.22);
            --atelier-border-hover: rgba(247, 228, 181, 0.55);
            --atelier-text-main: #F7F7F9;
            --atelier-text-muted: #9EABB8;
            --atelier-text-faint: #626D7A;
            --atelier-font-display: 'Fraunces', Georgia, serif;
            --atelier-font-accent: 'Italiana', Georgia, serif;
            --atelier-font-body: 'Plus Jakarta Sans', -apple-system, sans-serif;
        }

        /* Ambient canvas depth with layered celestial glows */
        .stApp {
            background-color: var(--atelier-bg-canvas);
            background-image: 
                radial-gradient(circle at 18% 10%, rgba(218, 183, 110, 0.08) 0%, transparent 42%),
                radial-gradient(circle at 82% 80%, rgba(224, 122, 95, 0.06) 0%, transparent 40%),
                radial-gradient(rgba(218, 183, 110, 0.12) 1px, transparent 1px);
            background-size: auto, auto, 32px 32px;
            color: var(--atelier-text-main);
            font-family: var(--atelier-font-body);
        }

        /* Page layout container */
        .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 3rem !important;
            max-width: 1060px;
        }

        /* Sidebar atmosphere & borders */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0C0F15 0%, #11151F 100%) !important;
            border-right: 1px solid var(--atelier-border) !important;
        }
        [data-testid="stSidebar"] > div:first-child {
            padding-top: 1.25rem !important;
            padding-bottom: 2rem !important;
        }

        /* Sculptural typography */
        h1, h2, h3, h4 {
            font-family: var(--atelier-font-display) !important;
            letter-spacing: -0.015em;
            color: var(--atelier-text-main);
        }

        /* Hero styling */
        .atelier-hero-wrap {
            margin-bottom: 1.5rem;
            animation: revealFadeUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) both;
        }
        .atelier-crest {
            display: inline-flex;
            align-items: center;
            gap: 7px;
            background: rgba(218, 183, 110, 0.08);
            border: 1px solid rgba(218, 183, 110, 0.28);
            border-radius: 999px;
            padding: 0.32rem 0.95rem;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            color: var(--atelier-gold-bright);
            margin-bottom: 0.65rem;
        }
        .atelier-crest-spark {
            color: var(--atelier-gold);
            font-size: 0.85rem;
        }
        .atelier-brand-title {
            font-family: var(--atelier-font-display) !important;
            font-size: 2.85rem !important;
            font-weight: 600 !important;
            line-height: 1.1 !important;
            margin: 0.2rem 0 0.4rem 0 !important;
            letter-spacing: -0.03em !important;
            background: linear-gradient(135deg, #FFFFFF 0%, #F7E4B5 45%, #DAB76E 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .atelier-tagline {
            font-family: var(--atelier-font-body);
            font-size: 1.05rem;
            font-weight: 400;
            color: var(--atelier-text-muted);
            margin: 0;
            max-width: 650px;
            line-height: 1.55;
        }

        /* Elegant gold-tinted dividers */
        hr {
            border: none !important;
            border-top: 1px solid var(--atelier-border) !important;
            margin: 1.25rem 0 !important;
        }

        /* Live Event Intelligence HUD */
        .atelier-hud {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: linear-gradient(135deg, rgba(18, 22, 33, 0.85) 0%, rgba(25, 31, 46, 0.85) 100%);
            border: 1px solid var(--atelier-border);
            border-radius: 12px;
            padding: 0.85rem 1.4rem;
            margin: 1.25rem 0;
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(14px);
            animation: revealFadeUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.1s both;
            flex-wrap: wrap;
            gap: 14px;
        }
        .hud-metric {
            display: flex;
            flex-direction: column;
        }
        .hud-label {
            font-size: 0.62rem;
            font-weight: 700;
            letter-spacing: 0.16em;
            color: var(--atelier-gold);
            text-transform: uppercase;
            margin-bottom: 0.18rem;
        }
        .hud-val {
            font-family: var(--atelier-font-display);
            font-size: 1.02rem;
            font-weight: 600;
            color: #FFFFFF;
            letter-spacing: -0.01em;
        }
        .hud-sep {
            width: 1px;
            height: 26px;
            background: rgba(218, 183, 110, 0.2);
        }

        /* Curation Seeds bar */
        .atelier-seeds-bar {
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 1.35rem;
            animation: revealFadeUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.18s both;
        }
        .seeds-title {
            font-size: 0.68rem;
            font-weight: 700;
            letter-spacing: 0.15em;
            color: rgba(218, 183, 110, 0.8);
            text-transform: uppercase;
            margin-right: 4px;
        }
        .seed-chip {
            font-size: 0.78rem;
            font-weight: 500;
            color: #E2E8F0;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(218, 183, 110, 0.18);
            border-radius: 999px;
            padding: 0.28rem 0.85rem;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
            user-select: none;
        }
        .seed-chip:hover {
            background: rgba(218, 183, 110, 0.14);
            border-color: var(--atelier-gold-bright);
            color: #FFFFFF;
            transform: translateY(-1.5px);
        }

        /* Atelier Dossier Folio Cards Grid */
        .atelier-cards-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin: 0.5rem 0 1.5rem 0;
        }
        @media (max-width: 960px) {
            .atelier-cards-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
        @media (max-width: 580px) {
            .atelier-cards-grid {
                grid-template-columns: 1fr;
            }
            .hud-sep {
                display: none;
            }
        }

        .atelier-card {
            background: linear-gradient(160deg, rgba(20, 25, 36, 0.85) 0%, rgba(13, 16, 23, 0.95) 100%);
            border: 1px solid var(--atelier-border);
            border-radius: 12px;
            padding: 1.35rem 1.15rem;
            position: relative;
            overflow: hidden;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
            backdrop-filter: blur(14px);
        }
        .atelier-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--atelier-gold), transparent);
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        .atelier-card:hover {
            transform: translateY(-5px);
            border-color: var(--atelier-border-hover);
            box-shadow: 0 16px 36px -8px rgba(0, 0, 0, 0.7), 0 0 24px rgba(218, 183, 110, 0.16);
            background: linear-gradient(160deg, rgba(26, 33, 48, 0.9) 0%, rgba(16, 20, 30, 0.98) 100%);
        }
        .atelier-card:hover::before {
            opacity: 1;
        }
        .card-num {
            font-family: var(--atelier-font-display);
            font-size: 1.85rem;
            font-weight: 300;
            color: rgba(218, 183, 110, 0.32);
            line-height: 1;
            margin-bottom: 0.65rem;
            transition: color 0.3s ease;
        }
        .atelier-card:hover .card-num {
            color: var(--atelier-gold-bright);
        }
        .card-micro-tag {
            font-size: 0.65rem;
            font-weight: 700;
            letter-spacing: 0.16em;
            color: var(--atelier-gold);
            text-transform: uppercase;
            margin-bottom: 0.4rem;
        }
        .card-heading {
            font-family: var(--atelier-font-display);
            font-size: 1.1rem;
            font-weight: 600;
            color: #FFFFFF;
            margin-bottom: 0.45rem;
            letter-spacing: -0.01em;
        }
        .card-body {
            font-size: 0.83rem;
            color: var(--atelier-text-muted);
            line-height: 1.55;
            margin: 0;
        }

        /* Staggered entry animation delays */
        .card-reveal-1 { animation: revealFadeUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.22s both; }
        .card-reveal-2 { animation: revealFadeUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.30s both; }
        .card-reveal-3 { animation: revealFadeUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.38s both; }
        .card-reveal-4 { animation: revealFadeUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.46s both; }

        /* Primary action buttons */
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #1E2535 0%, #111520 100%) !important;
            color: var(--atelier-gold-bright) !important;
            border: 1px solid var(--atelier-gold) !important;
            border-radius: 8px !important;
            font-family: var(--atelier-font-body) !important;
            font-weight: 600 !important;
            font-size: 0.96rem !important;
            letter-spacing: 0.02em !important;
            padding: 0.65rem 1.65rem !important;
            box-shadow: 0 4px 18px rgba(0, 0, 0, 0.4), 0 0 12px rgba(218, 183, 110, 0.15) !important;
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
        }
        .stButton > button[kind="primary"]:hover {
            background: linear-gradient(135deg, #283248 0%, #161C2A 100%) !important;
            border-color: var(--atelier-gold-bright) !important;
            color: #FFFFFF !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 26px rgba(0, 0, 0, 0.55), 0 0 22px rgba(218, 183, 110, 0.35) !important;
        }
        .stButton > button[kind="primary"]:active {
            transform: translateY(0px) !important;
        }

        /* Download button — refined studio aesthetic */
        .stDownloadButton > button {
            background: rgba(218, 183, 110, 0.08) !important;
            color: var(--atelier-gold-bright) !important;
            border: 1px solid var(--atelier-gold) !important;
            border-radius: 8px !important;
            font-family: var(--atelier-font-body) !important;
            font-weight: 600 !important;
            font-size: 0.92rem !important;
            padding: 0.6rem 1.4rem !important;
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
        }
        .stDownloadButton > button:hover {
            background: rgba(218, 183, 110, 0.2) !important;
            border-color: var(--atelier-gold-bright) !important;
            color: #FFFFFF !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35), 0 0 16px rgba(218, 183, 110, 0.25) !important;
        }

        /* Sidebar Inputs & High-Contrast Typography */
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
        [data-testid="stSidebar"] [data-testid="stWidgetLabel"] span {
            color: #E2E8F0 !important;
            font-weight: 500 !important;
        }
        [data-testid="stSidebar"] .stCaption,
        [data-testid="stSidebar"] small {
            color: var(--atelier-text-muted) !important;
        }
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] h4 {
            color: var(--atelier-gold-bright) !important;
        }

        [data-testid="stSidebar"] input,
        [data-testid="stSidebar"] textarea,
        [data-testid="stSidebar"] div[data-baseweb="select"] > div {
            background: rgba(14, 18, 26, 0.8) !important;
            border-color: rgba(218, 183, 110, 0.2) !important;
            color: var(--atelier-text-main) !important;
            border-radius: 7px !important;
        }
        [data-testid="stSidebar"] div[data-baseweb="select"] span,
        [data-testid="stSidebar"] div[data-baseweb="select"] div {
            color: #F7F7F9 !important;
        }
        [data-testid="stSidebar"] input:focus,
        [data-testid="stSidebar"] textarea:focus {
            border-color: var(--atelier-gold) !important;
            box-shadow: 0 0 0 1px var(--atelier-gold) !important;
        }

        /* BaseWeb Selectbox & Datepicker dropdown menus contrast */
        div[data-baseweb="popover"],
        ul[data-baseweb="menu"] {
            background-color: #121622 !important;
            border: 1px solid rgba(218, 183, 110, 0.3) !important;
        }
        ul[data-baseweb="menu"] li,
        ul[data-baseweb="menu"] li span {
            color: #F7F7F9 !important;
        }
        ul[data-baseweb="menu"] li:hover {
            background-color: rgba(218, 183, 110, 0.15) !important;
        }

        /* Sidebar crest */
        .sidebar-crest-wrap {
            display: flex;
            align-items: center;
            gap: 6px;
            margin-bottom: 0.4rem;
        }
        .crest-spark {
            color: var(--atelier-gold);
            font-size: 0.95rem;
        }
        .crest-title {
            font-family: var(--atelier-font-display);
            font-size: 0.92rem;
            font-weight: 600;
            letter-spacing: 0.12em;
            color: var(--atelier-gold-bright);
            text-transform: uppercase;
        }

        /* Markdown Plan Output typography & tables */
        .stMarkdown h2 {
            font-family: var(--atelier-font-display) !important;
            font-size: 1.6rem !important;
            font-weight: 600 !important;
            color: var(--atelier-gold-bright) !important;
            margin-top: 2rem !important;
            margin-bottom: 0.75rem !important;
            padding-bottom: 0.45rem !important;
            border-bottom: 1px solid var(--atelier-border) !important;
            letter-spacing: -0.015em !important;
        }
        .stMarkdown h3 {
            font-family: var(--atelier-font-display) !important;
            font-size: 1.22rem !important;
            color: #FFFFFF !important;
            margin-top: 1.35rem !important;
            margin-bottom: 0.5rem !important;
        }
        .stMarkdown p, .stMarkdown li {
            line-height: 1.7 !important;
            color: #E2E8F0 !important;
        }
        .stMarkdown li::marker {
            color: var(--atelier-gold) !important;
        }

        /* Markdown tables in generated event plan */
        .stMarkdown table {
            width: 100% !important;
            border-collapse: separate !important;
            border-spacing: 0 !important;
            margin: 1.25rem 0 !important;
            border-radius: 9px !important;
            overflow: hidden !important;
            border: 1px solid var(--atelier-border) !important;
            background: rgba(18, 22, 33, 0.65) !important;
        }
        .stMarkdown th {
            background: rgba(218, 183, 110, 0.12) !important;
            color: var(--atelier-gold-bright) !important;
            font-family: var(--atelier-font-body) !important;
            font-weight: 700 !important;
            font-size: 0.82rem !important;
            letter-spacing: 0.08em !important;
            text-transform: uppercase !important;
            padding: 0.8rem 1rem !important;
            border-bottom: 2px solid rgba(218, 183, 110, 0.3) !important;
            text-align: left !important;
        }
        .stMarkdown td {
            padding: 0.75rem 1rem !important;
            color: #E2E8F0 !important;
            font-size: 0.9rem !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.06) !important;
        }
        .stMarkdown tr:last-child td {
            border-bottom: none !important;
        }
        .stMarkdown tr:hover td {
            background: rgba(218, 183, 110, 0.04) !important;
        }

        /* Plan compiled status banner */
        .atelier-plan-banner {
            background: linear-gradient(135deg, rgba(218, 183, 110, 0.1) 0%, rgba(26, 32, 46, 0.8) 100%);
            border: 1px solid var(--atelier-border);
            border-radius: 10px;
            padding: 0.85rem 1.25rem;
            margin-bottom: 1.25rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 10px;
        }
        .banner-status {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .status-beacon {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #10B981;
            box-shadow: 0 0 10px #10B981;
            animation: beaconPulse 2s infinite;
        }
        .status-text {
            font-size: 0.76rem;
            font-weight: 700;
            letter-spacing: 0.14em;
            color: var(--atelier-gold-bright);
            text-transform: uppercase;
        }
        .banner-meta {
            font-size: 0.82rem;
            color: var(--atelier-text-muted);
        }

        /* Glassmorphic alerts with high text contrast */
        .stAlert {
            background: rgba(18, 22, 33, 0.92) !important;
            border: 1px solid var(--atelier-border) !important;
            border-radius: 10px !important;
            backdrop-filter: blur(10px) !important;
        }
        .stAlert p, .stAlert span, .stAlert div, .stAlert li {
            color: #F7F7F9 !important;
        }

        /* Keyframe animations */
        @keyframes revealFadeUp {
            from {
                opacity: 0;
                transform: translateY(18px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        @keyframes beaconPulse {
            0%, 100% {
                opacity: 1;
                transform: scale(1);
            }
            50% {
                opacity: 0.45;
                transform: scale(0.85);
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# 3. Sidebar event input form
# ---------------------------------------------------------------------------

def render_sidebar():
    """
    Render grouped event-detail inputs in the sidebar.
    Returns a dict of raw input values.
    """
    st.sidebar.markdown(
        """
        <div class="sidebar-crest-wrap">
            <span class="crest-spark">✦</span>
            <span class="crest-title">ATELIER SPECS</span>
            <span class="crest-spark">✦</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.header("Event Details")
    st.sidebar.caption("Define your celebration parameters below.")

    sidebar_generate_top = st.sidebar.button(
        "Generate Event Plan",
        type="primary",
        use_container_width=True,
        key="sidebar_generate_btn_top",
    )
    st.sidebar.divider()

    # Group 1: Event Basics
    st.sidebar.subheader("Event Basics")
    event_type = st.sidebar.selectbox(
        "Event type",
        options=EVENT_TYPES,
        help="Select the type of celebration you are planning.",
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

    st.sidebar.divider()

    # Group 2: Budget
    st.sidebar.subheader("Budget")
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
        help="Select the currency for your budget estimates.",
    )

    st.sidebar.divider()

    # Group 3: Location and preferences
    st.sidebar.subheader("Location & Preferences")
    city = st.sidebar.text_input(
        "City or region",
        placeholder="e.g. Mumbai, New Delhi, London",
        help="Enter the city or region to help ground vendor guidance.",
    )

    theme = st.sidebar.text_input(
        "Theme or vibe (optional)",
        placeholder="e.g. Garden party, Traditional, Modern minimalist",
        help="Describe desired ambiance, aesthetic, or visual style.",
    )

    requirements = st.sidebar.text_area(
        "Special requirements (optional)",
        placeholder=(
            "e.g. Vegetarian-only catering, outdoor venue, "
            "accessibility needs, kids activities"
        ),
        help="List any specific dietary, accessibility, or venue preferences.",
        height=68,
    )

    sidebar_generate_bottom = st.sidebar.button(
        "Generate Event Plan",
        type="primary",
        use_container_width=True,
        key="sidebar_generate_btn_bottom",
    )

    # Store button state in session_state for easy retrieval in main()
    st.session_state["_sidebar_generate"] = (
        sidebar_generate_top or sidebar_generate_bottom
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

# The model identifier used here is Google's fast, stable Flash-Lite model,
# optimized for ultra-low latency and high-throughput text generation.
GEMINI_MODEL = "gemini-3.5-flash-lite"


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
    Build a concise, direct, seven-section event-planning prompt.
    Optimized for low-latency generation without sacrificing any of the
    required event-planning sections or safety precautions.

    Args:
        event_data (dict): Validated event details from render_sidebar().

    Returns:
        str: The complete prompt string ready to send to Gemini.
    """
    days_until_event = (event_data["event_date"] - datetime.date.today()).days

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
        "Create a concise, practical event plan in Markdown for this celebration:\n\n"
        f"- Event type: {event_data['event_type']}\n"
        f"- Event date: {event_data['event_date'].strftime('%d %B %Y')} "
        f"({days_until_event} days from today)\n"
        f"- Expected guests: {event_data['guests']}\n"
        f"- Total budget: {event_data['currency']} {event_data['budget']:,.0f}\n"
        f"- City or region: {event_data['city']}\n"
        f"- {theme_line}\n"
        f"- {requirements_line}\n\n"
        "Provide EXACTLY these seven sections using these exact headings:\n\n"
        "## Event Concept\n"
        "Provide 3 brief theme ideas and 1 personalized signature concept (1-2 sentences each), "
        f"tailored to {event_data['city']} and {event_data['guests']} guests.\n\n"
        "## Budget Plan\n"
        "Provide a compact category-wise budget in a Markdown table with columns: "
        "Category | Estimated Cost | Notes.\n"
        f"Include 5-6 core categories. The total must not exceed {event_data['currency']} {event_data['budget']:,.0f}. "
        f"Use {event_data['currency']} consistently throughout.\n\n"
        "## Planning Timeline\n"
        f"Provide concise action milestones across 3-4 chronological phases based on {days_until_event} days remaining.\n\n"
        "## Vendor Checklist\n"
        f"List 4-5 key vendor categories for this event size in {event_data['city']}. "
        "For each category, include a brief booking note and 2 essential vetting questions.\n\n"
        "## Day-of-Event Schedule\n"
        f"Provide a practical, concise hour-by-hour schedule of key activities for the event day, "
        f"scaled for {event_data['guests']} guests.\n\n"
        "## Risk Checklist\n"
        f"Identify 3-4 likely operational or weather risks in {event_data['city']} and 1 practical precaution for each.\n\n"
        "## Money-Saving Tips\n"
        f"Provide 5 practical, specific tips to optimize spending without compromising experience, "
        f"tailored to {event_data['city']} and the budget.\n\n"
        "Important rules:\n"
        "- Treat all vendor names, prices, and availability as ESTIMATES only; none are guaranteed or verified.\n"
        "- Keep every section concise, clear, and actionable. Avoid filler text and conversational fluff.\n"
        "- Return clean Markdown only. Do not add any text before the first heading or after the last section."
    )

    return prompt


def stream_event_plan(event_data, api_key, max_retries=2):
    """
    Stream chunks of the generated event plan from Gemini using the google-genai SDK.
    Retries safely on transient server errors (5xx) with backoff before yielding chunks.

    Args:
        event_data (dict): Validated event details.
        api_key (str): The Gemini API key.
        max_retries (int): Maximum retry attempts for transient server errors.

    Yields:
        str: Text chunks as they arrive from Gemini.
    """
    prompt = build_event_prompt(event_data)
    client = genai.Client(api_key=api_key)

    last_error = None
    for attempt in range(max_retries + 1):
        has_yielded = False
        try:
            response_stream = client.models.generate_content_stream(
                model=GEMINI_MODEL,
                contents=prompt,
            )
            for chunk in response_stream:
                if chunk.text:
                    has_yielded = True
                    yield chunk.text
            return
        except errors.ServerError as err:
            last_error = err
            # Only retry if no content was yielded yet
            if not has_yielded and attempt < max_retries:
                time.sleep(1.0 * (attempt + 1))
            else:
                raise
        except Exception:
            raise

    if last_error:
        raise last_error


def generate_event_plan(event_data, api_key, max_retries=2):
    """
    Generate the complete event plan text (non-streaming).
    Accumulates streaming chunks to provide a reliable non-streaming interface.

    Args:
        event_data (dict): Validated event details.
        api_key (str): The Gemini API key.
        max_retries (int): Maximum retry attempts for transient server errors.

    Returns:
        str: The complete event plan text.
    """
    chunks = []
    for chunk in stream_event_plan(event_data, api_key, max_retries=max_retries):
        chunks.append(chunk)
    return "".join(chunks)


# ---------------------------------------------------------------------------
# 6. Main application area
# ---------------------------------------------------------------------------

def main():
    # ---- Custom styling ----------------------------------------------------
    inject_custom_styles()

    # ---- App header --------------------------------------------------------
    st.markdown(
        """
        <div class="atelier-hero-wrap">
            <div class="atelier-crest">
                <span class="atelier-crest-spark">✦</span>
                <span>GENAI CELEBRATION ATELIER</span>
                <span class="atelier-crest-spark">✦</span>
            </div>
            <h1 class="atelier-brand-title">celebrait</h1>
            <p class="atelier-tagline">
                Orchestrating bespoke celebrations with cinematic vision, fiscal rigor, and tailored local intelligence.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---- Sidebar form ------------------------------------------------------
    event_data = render_sidebar()
    sidebar_generate = st.session_state.get("_sidebar_generate", False)

    # Initialize plan state in session_state if not already present
    if "event_plan" not in st.session_state:
        st.session_state["event_plan"] = None

    has_plan = bool(st.session_state.get("event_plan"))

    # ---- Introductory Overview (shown only before generation) --------------
    main_generate = False
    if not has_plan:
        # Dynamic Live Intelligence calculations from sidebar inputs
        today = datetime.date.today()
        event_date = event_data.get("event_date", today + datetime.timedelta(days=30))
        days_until = max(0, (event_date - today).days)
        guests = max(1, int(event_data.get("guests", 50)))
        budget = float(event_data.get("budget", 50000))
        unit_spend = budget / guests if guests > 0 else 0
        raw_currency = str(event_data.get("currency", "INR (Rs.)"))
        currency_code = raw_currency.split()[0]
        city_display = event_data.get("city") or "Location Pending"

        # 1. Live Event Intelligence HUD Ribbon
        st.markdown(
            f"""
            <div class="atelier-hud">
                <div class="hud-metric">
                    <span class="hud-label">OCCASION</span>
                    <span class="hud-val">{event_data.get('event_type', 'Celebration')}</span>
                </div>
                <div class="hud-sep"></div>
                <div class="hud-metric">
                    <span class="hud-label">COUNTDOWN</span>
                    <span class="hud-val">{days_until} Days</span>
                </div>
                <div class="hud-sep"></div>
                <div class="hud-metric">
                    <span class="hud-label">SCALE</span>
                    <span class="hud-val">{guests:,} Guests</span>
                </div>
                <div class="hud-sep"></div>
                <div class="hud-metric">
                    <span class="hud-label">ALLOCATION / HEAD</span>
                    <span class="hud-val">{currency_code} {unit_spend:,.0f}</span>
                </div>
                <div class="hud-sep"></div>
                <div class="hud-metric">
                    <span class="hud-label">TERRITORY</span>
                    <span class="hud-val">{city_display}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # 2. Curation Inspiration Seeds
        st.markdown(
            """
            <div class="atelier-seeds-bar">
                <span class="seeds-title">CURATION SEEDS:</span>
                <span class="seed-chip">👑 Heritage Royal Palace</span>
                <span class="seed-chip">✨ Midnight Terrace Soirée</span>
                <span class="seed-chip">🌿 Bohemian Meadow Gathering</span>
                <span class="seed-chip">⚡ High-Voltage Milestone Gala</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # 3. Four Curated Atelier Dossier Cards (Staggered CSS reveal)
        st.markdown(
            """
            <div class="atelier-cards-grid">
                <div class="atelier-card card-reveal-1">
                    <div class="card-num">01</div>
                    <div class="card-micro-tag">CREATIVE DIRECTION</div>
                    <div class="card-heading">Bespoke Concept</div>
                    <p class="card-body">Tailored visual themes, signature motifs, and atmospheric narratives grounded in your occasion.</p>
                </div>
                <div class="atelier-card card-reveal-2">
                    <div class="card-num">02</div>
                    <div class="card-micro-tag">FISCAL ARCHITECTURE</div>
                    <div class="card-heading">Budget Allocation</div>
                    <p class="card-body">Category spend plan scaled precisely to your attendee count with non-negotiable budget caps.</p>
                </div>
                <div class="atelier-card card-reveal-3">
                    <div class="card-num">03</div>
                    <div class="card-micro-tag">SUPPLIER DOSSIER</div>
                    <div class="card-heading">Vendor Checklist</div>
                    <p class="card-body">Essential service categories, local booking recommendations, and incisive vetting questions.</p>
                </div>
                <div class="atelier-card card-reveal-4">
                    <div class="card-num">04</div>
                    <div class="card-micro-tag">OPERATIONAL RUN-OF-SHOW</div>
                    <div class="card-heading">Schedule & Risks</div>
                    <p class="card-body">Hour-by-hour choreography, local risk mitigation, and insider cost-saving maneuvers.</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div style='margin-top: 0.5rem;'></div>", unsafe_allow_html=True)
        main_generate = st.button(
            "Generate Event Plan",
            type="primary",
            use_container_width=False,
            key="main_generate_btn",
        )

    # ---- Button logic ------------------------------------------------------
    generate_clicked = sidebar_generate or main_generate

    if generate_clicked:
        is_valid, validation_errors = validate_event_data(event_data)

        if not is_valid:
            # Show all validation problems together with calm, helpful phrasing
            error_lines = "\n".join(f"- {e}" for e in validation_errors)
            st.warning(
                f"**Please complete the following details before generating your event plan:**\n\n"
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
                # Clear previous plan if any
                st.session_state["event_plan"] = None

                # Show clear, honest status indicator while streaming starts
                status_placeholder = st.empty()
                status_placeholder.markdown(
                    """
                    <div class="atelier-plan-banner">
                        <div class="banner-status">
                            <span class="status-beacon"></span>
                            <span class="status-text">GENERATING YOUR EVENT PLAN…</span>
                        </div>
                        <div class="banner-meta">Streaming your personalized celebration outline from Gemini in real time…</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                stream_placeholder = st.empty()
                plan_text = ""
                try:
                    with stream_placeholder.container():
                        plan_text = st.write_stream(stream_event_plan(event_data, api_key))

                    status_placeholder.empty()

                    if not plan_text or not plan_text.strip():
                        stream_placeholder.empty()
                        # Empty response — ask user to retry
                        st.warning(
                            "Gemini returned an empty response. "
                            "Please try again in a moment."
                        )
                    else:
                        st.session_state["event_plan"] = plan_text
                        st.rerun()

                except Exception as exc:
                    status_placeholder.empty()
                    stream_placeholder.empty()
                    # Categorise the error safely without exposing raw credentials,
                    # headers, or stack traces
                    user_message, terminal_category = handle_gemini_error(exc)
                    print(f"[celebrait] {terminal_category}")
                    st.error(user_message)

    # ---- Display generated plan (replaces intro overview after generation) ---
    if has_plan:
        plan_text = st.session_state["event_plan"]

        # Compiled dossier status banner
        city_tag = event_data.get("city") or "Local Region"
        budget_val = float(event_data.get("budget", 50000))
        currency_str = event_data.get("currency", "INR (Rs.)")
        guests_val = event_data.get("guests", 50)

        st.markdown(
            f"""
            <div class="atelier-plan-banner">
                <div class="banner-status">
                    <span class="status-beacon"></span>
                    <span class="status-text">EVENT DOSSIER COMPILED • GEMINI 3.5 FLASH-LITE</span>
                </div>
                <div class="banner-meta">
                    Cap: <strong>{currency_str} {budget_val:,.0f}</strong> &bull; Scaled for <strong>{guests_val} guests</strong> &bull; {city_tag}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Top row: clear heading and immediately visible Download button
        top_head_col, top_dl_col = st.columns([3, 1])
        with top_head_col:
            st.subheader("Your Event Plan")
        with top_dl_col:
            st.download_button(
                label="Download Event Plan",
                data=plan_text,
                file_name="event_plan.md",
                mime="text/markdown",
                help="Download your generated event plan as a Markdown (.md) file",
                key="download_plan_top_btn",
                use_container_width=True,
            )

        # Markdown plan output
        st.markdown(plan_text)
        st.divider()

        # Bottom row: inline verification disclaimer and secondary Download button
        disc_col, btm_dl_col = st.columns([3, 1])
        with disc_col:
            st.info(
                "celebrait provides AI-generated planning estimates. "
                "Vendor names, prices, availability, and local "
                "recommendations must be independently verified."
            )
        with btm_dl_col:
            st.download_button(
                label="Download Event Plan",
                data=plan_text,
                file_name="event_plan.md",
                mime="text/markdown",
                help="Download your generated event plan as a Markdown (.md) file",
                key="download_plan_bottom_btn",
                use_container_width=True,
            )

    # ---- Footer disclaimer -------------------------------------------------
    st.divider()
    show_disclaimer()


if __name__ == "__main__":
    main()
