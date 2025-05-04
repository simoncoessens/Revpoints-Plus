import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
import streamlit as st
import json
from urllib.parse import quote_plus
import pandas as pd

# -------- Fixed width & UI shell constants -------- #
FIXED = 750   # px fixed app width
BAR_HEIGHT = 20  # px faux status bar height

# Notifications Page

st.set_page_config(
    page_title="Notifications",
    page_icon="🔔",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- INJECT GLOBAL CSS (fixed width, hide default elements) ---------- #
st.markdown(
    f"""
    <style>
      /* hide the sidebar panel, header, footer */
      #MainMenu, footer, header {{ visibility: hidden; }}
      html, body, [data-testid=\"stAppViewContainer\"] {{
          max-width:{FIXED}px;
          width:{FIXED}px !important;
          margin:0 auto;
          overflow-x:hidden;
      }}
      [data-testid=\"stAppViewContainer\"]>.main {{
          padding-top:{BAR_HEIGHT}px;
          padding-bottom:4rem;
      }}
      /* --- TOP STATUS BAR --- */
      .mobile-top {{
          position:fixed;
          top:0;
          left:0;
          width:100%;
          height:{BAR_HEIGHT}px;
          background:#1a1d23;
          border-bottom:1px solid #2e323b;
          z-index:100;
      }}
      /* --- BOTTOM NAV BAR --- */
      .mobile-nav {{
          position:fixed;
          bottom:0;
          left:0;
          width:100%;
          background:#1a1d23;
          border-top:1px solid #2e323b;
          display:flex;
          justify-content:space-around;
          padding:.5rem 0;
          z-index:100;
      }}
      .mobile-nav a {{
          color:#888;
          text-decoration:none;
          font-size:.9rem;
          display:flex;
          flex-direction:column;
          align-items:center;
      }}
      .mobile-nav a[selected]{{ color:#fff; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- TOP BLACK BAR ---------- #
st.markdown(f"<div class='mobile-top' style='height:{BAR_HEIGHT}px'></div>", unsafe_allow_html=True)

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

# ---------- BOTTOM NAVIGATION ---------- #
NAV = [
    ("Home", "🏠", "home.py"),
    ("Explore", "🔍", "pages/2_Explore.py"),
    ("Notifications", "🔔", "pages/3_Notifications.py"),
    ("Savings", "💰", "pages/6_savings.py"),
]

st.markdown('<div class="mobile-nav">', unsafe_allow_html=True)
cols = st.columns(len(NAV))
for (label, icon, page), col in zip(NAV, cols):
    with col:
        st.page_link(page=page, label=label, icon=icon, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------- CARD STYLES ---------- #
st.markdown(
    f"""
    <style>
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
