import streamlit as st
import pandas as pd
from urllib.parse import quote_plus
from pathlib import Path
import base64
import os

# -------- Paths to local assets -------- #
ASSETS_PATH = Path(__file__).parent / "assets"
CARD_FILE = ASSETS_PATH / "card.png"
LOGO_FILE = ASSETS_PATH / "revolut_logo.png"
PROFILE_FILE = ASSETS_PATH / "user.png"

CSV_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "final_data.csv")
# ---------- Helper to inline images as <img> tags ---------- #

def img_tag(path: Path, height: int) -> str:
    if not path.exists():
        return ""
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    data = base64.b64encode(path.read_bytes()).decode()
    return f'<img src="data:{mime};base64,{data}" height="{height}">'  # noqa: E501

# ---------- Page config ---------- #

st.set_page_config(
    page_title="Revolut Lite",
    page_icon="🔔",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------- CSS: FIXED‑WIDTH APP (600 px) & UI SHELL ---------- #
FIXED = 750  # px
BAR_HEIGHT = 20  # px for the faux status bar
st.markdown(
    f"""
    <style>
    #MainMenu, footer {{visibility:hidden;}}
    html, body, [data-testid=\"stAppViewContainer\"] {{
        max-width:{FIXED}px;width:{FIXED}px !important;margin:0 auto;overflow-x:hidden;
    }}
    .main .block-container {{padding-left:1rem;padding-right:1rem;max-width:{FIXED}px;}}
    [data-testid=\"stAppViewContainer\"]>.main {{padding-top:{BAR_HEIGHT}px;padding-bottom:4rem;}}
    .mobile-top {{position:fixed;top:0;left:0;right:0;height:{BAR_HEIGHT}px;background:#1a1d23;border-bottom:1px solid #2e323b;z-index:100;}}
    .mobile-nav {{position:fixed;bottom:0;left:0;right:0;width:{FIXED}px;margin:0 auto;background:#1a1d23;border-top:1px solid #2e323b;display:flex;justify-content:space-around;padding:.5rem 0;z-index:999;}}
    .mobile-nav a {{color:#888;text-decoration:none;font-size:.9rem;display:flex;flex-direction:column;align-items:center;}}
    .mobile-nav a[selected]{{color:#fff;}}
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------- TOP BLACK BAR ---------- #
BAR_HEIGHT = 20  # px
st.markdown(f"<div class='mobile-top' style='height:{BAR_HEIGHT}px'></div>", unsafe_allow_html=True)

# ---------- HEADER (logo + avatar) ---------- #
header_l, _, header_r = st.columns([1, 6, 1])
with header_l:
    st.markdown(img_tag(LOGO_FILE, 28), unsafe_allow_html=True)
with header_r:
    st.markdown(img_tag(PROFILE_FILE, 30), unsafe_allow_html=True)

# ---------- Session state ---------- #
if "balance" not in st.session_state:
    st.session_state.balance = 1824.57

N_INIT = 50

if os.path.exists(CSV_FILE):
    # Read transactions from CSV
    df = pd.read_csv(
        CSV_FILE,
        parse_dates=["timestamp"]
    )
    # Rename and format date
    df = df.rename(
        columns={
            "timestamp": "date",
            "merchant_name": "name",
        }
    )
    df["date_str"] = df["date"].dt.strftime("%Y-%m-%d")
    df = df[["date_str", "name", "amount"]].rename(columns={"date_str": "date"})
    # Sort by date descending
    df = df.sort_values("date", ascending=False).reset_index(drop=True)
    # Set up lastn in session state
    if "lastn" not in st.session_state:
        st.session_state.lastn = N_INIT
    n = st.session_state.lastn
    # Split into hidden (most recent n) and shown (the rest)
    if n > 0 and len(df) > n:
        hidden_df = df.iloc[:n].copy()
        shown_df = df.iloc[n:].copy()
    else:
        hidden_df = pd.DataFrame(columns=df.columns)
        shown_df = df.copy()
    st.session_state.transactions_hidden = hidden_df
    st.session_state.transactions_shown = shown_df
    # Set the transactions to display
    if n > 0 and len(df) > n:
        st.session_state.transactions = shown_df.copy()
    else:
        st.session_state.transactions = df.copy()

# ---------- CSS ---------- #

st.markdown(
    f"""
<style>
#MainMenu, footer, header {{visibility: hidden;}}

[data-testid="stAppViewContainer"] > .main {{
    max-width: 420px; margin: auto; padding: {BAR_HEIGHT + 16}px 0 4rem;
}}

.mobile-top {{
    position: fixed; top: 0; left: 0; width: 100%;
    background: #1a1d23; border-bottom: 1px solid #2e323b; z-index: 100;
}}

.card {{
    background: linear-gradient(145deg,#2a2d34,#343741); color: #fff;
    border-radius: 1.5rem; padding: 1.5rem;
    box-shadow: 0 10px 20px rgba(0,0,0,.3); margin-bottom:1rem;
}}

.recent-activity {{max-height: 300px; overflow-y: auto; padding-right: .5rem;}}
.recent-activity::-webkit-scrollbar {{width:6px;}}
.recent-activity::-webkit-scrollbar-thumb {{background:#343741; border-radius:3px;}}

.mobile-nav {{
    position: fixed; bottom: 0; left: 0; width: 100%; background: #1a1d23;
    border-top: 1px solid #2e323b; display: flex; justify-content: space-around;
    padding: .5rem 0; z-index: 100;
}}
.mobile-nav a {{color: #888; text-decoration: none; font-size: .9rem; display: flex; flex-direction: column; align-items: center;}}
.mobile-nav a[selected] {{color: #fff;}}
</style>
""",
    unsafe_allow_html=True,
)

# ---------- MAIN CARD ---------- #
st.markdown(f"""
<div style='display: flex; align-items: center; justify-content: center; gap: 1.5rem; margin-bottom: 1.5rem;'>
    <img src='data:image/png;base64,{base64.b64encode(CARD_FILE.read_bytes()).decode()}' width='90' style='display:block;'>
    <span style='font-size:2.2rem;font-weight:700;'>12,345 Points</span>
</div>
""", unsafe_allow_html=True)

# ---------- RECENT ACTIVITY ---------- #
st.markdown("#### Recent activity")
if st.session_state.lastn > 0 and not st.session_state.transactions_hidden.empty:
    if st.button(f"Show last {st.session_state.lastn} transactions"):
        st.session_state.lastn = 0
        # Show all transactions
        df = pd.concat([
            st.session_state.transactions_hidden,
            st.session_state.transactions_shown
        ], ignore_index=True)
        st.session_state.transactions = df.copy()
        st.rerun()

rows_html = ""
for _, row in (
    st.session_state.transactions.assign(
        date_fmt=lambda d: pd.to_datetime(d.date).dt.strftime("%d %b %Y")
    )
).iterrows():
    color = "#0f0" if row["amount"] > 0 else "#ff5b5b"
    query = (
        f"vendor_name={quote_plus(row['name'])}"
        f"&amount={row['amount']}"
        f"&date={row['date']}"
    )
    href = f"/Vendor?{query}"
    rows_html += (
        f"<a href='{href}' target='_self' style='text-decoration:none;color:inherit;'>"
        f"  <div style='display:flex;justify-content:space-between;padding:4px 0;'>"
        f"    <div><strong>{row['name']}</strong><br>"
        f"      <span style='font-size:0.8rem;color:#888'>{row['date_fmt']}</span>"
        f"    </div>"
        f"    <div style='text-align:right;color:{color};'>€ {row['amount']:,.2f}</div>"
        f"  </div>"
        f"</a>"
    )

st.markdown(f"<div class='recent-activity'>{rows_html}</div>", unsafe_allow_html=True)

# ---------- BOTTOM NAVIGATION ---------- #
NAV = [
    ("Home",    "🏠", Path(__file__).parent / "home.py"),
    ("Explore", "🔍",  Path(__file__).parent / "pages/2_Explore.py"),
    ("Notifications",   "🔔", Path(__file__).parent / "pages/3_Notifications.py"),
    ("Settings","⚙️", Path(__file__).parent / "pages/4_Settings.py"),
]

st.markdown('<div class="mobile-nav">', unsafe_allow_html=True)
cols = st.columns(len(NAV))
for (label, icon, target), col in zip(NAV, cols):
    with col:
        if target:
            st.page_link(page=target, label=label, icon=icon, use_container_width=True)
        else:
            st.markdown(f"<a selected>{icon}<br>{label}</a>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)