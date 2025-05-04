import streamlit as st
import json
from pathlib import Path
from urllib.parse import quote_plus
import pandas as pd

# Notifications Page

st.set_page_config(
    page_title="Notifications",
    page_icon="🔔",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- TOP BLACK BAR ---------- #
BAR_HEIGHT = 20  # px
st.markdown(f"<div class='mobile-top' style='height:{BAR_HEIGHT}px'></div>", unsafe_allow_html=True)

# ---------- CSS ---------- #
st.markdown(
    f"""
<style>
#MainMenu, footer, header {{ visibility: hidden; }}
[data-testid="stAppViewContainer"] > .main {{
    max-width: 420px;
    margin: auto;
    padding: {BAR_HEIGHT + 16}px 0 4rem;
    padding-bottom: 4rem;
}}
.mobile-top {{
    position: fixed;
    top: 0; left: 0;
    width: 100%;
    background: #1a1d23;
    border-bottom: 1px solid #2e323b;
    z-index: 100;
}}
.notification-card {{
    border-radius: 1.2rem;
    padding: 1.1rem 1.3rem;
    margin-bottom: 1.1rem;
    box-shadow: 0 4px 16px rgba(0,0,0,.08);
    font-size: 1.08rem;
    font-family: 'Inter', sans-serif;
    cursor: pointer;
    transition: box-shadow 0.15s, transform 0.12s;
    border: 1px solid #e5e7eb;
    text-decoration: none;
    display: block;
}}
.notification-card.alt {{
    background: linear-gradient(90deg, #f7f7fa 60%, #e9f5f1 100%);
    color: #1a1d23;
}}
.notification-card.norm {{
    background: linear-gradient(90deg, #f0f4fa 60%, #f7f7fa 100%);
    color: #1a1d23;
}}
.notification-card:hover {{
    box-shadow: 0 8px 24px rgba(0,0,0,.13);
    transform: translateY(-2px) scale(1.01);
}}
.notification-text {{
    font-size: 1.08rem;
    font-weight: 500;
    line-height: 1.5;
    margin-bottom: 0;
    color: #1a1d23;
}}
</style>
""",
    unsafe_allow_html=True,
)

# ---------- HEADER ---------- #
st.markdown("<h2 style='text-align:center;margin-bottom:2.2rem'>Notifications</h2>", unsafe_allow_html=True)

# ---------- Live-updating notifications fragment ---------- #
@st.fragment(run_every="10s")
def notifications_fragment():
    json_path = Path(__file__).parent.parent.parent / "data" / "campaigns_approved.json"
    with open(json_path, "r", encoding="utf-8") as f:
        campaigns = json.load(f)
    for idx, campaign in enumerate(campaigns):
        notification = campaign.get("notification", "")
        vendor_name = campaign.get("vendor_name", "")
        vendor_name_encoded = quote_plus(vendor_name)
        # Use campaign timestamp if available, else today's date
        date = campaign.get("timestamp") or pd.Timestamp.now().strftime("%Y-%m-%d")
        vendor_page = f"/Vendor?vendor_name={vendor_name_encoded}&date={date}"
        card_class = "alt" if idx % 2 else "norm"
        st.markdown(
            f"""
            <a href='{vendor_page}' target='_self' style='text-decoration:none;color:inherit;' class='notification-card {card_class}'>
                <div class='notification-text'>{notification}</div>
            </a>
            """,
            unsafe_allow_html=True
        )

notifications_fragment()

# ---------- Bottom Navigation ---------- #
NAV = [
    ("Home", "🏠", Path(__file__).parent.parent / "home.py"),
    ("Explore", "🔍", Path(__file__).parent.parent / "pages/2_Explore.py"),
    ("Notifications", "🔔", Path(__file__)),
    ("Settings", "⚙️", Path(__file__).parent.parent / "pages/4_Settings.py"),
]

st.markdown('<div class="mobile-nav">', unsafe_allow_html=True)
cols = st.columns(len(NAV))
for (label, icon, target), col in zip(NAV, cols):
    with col:
        st.page_link(page=target, label=label, icon=icon, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)