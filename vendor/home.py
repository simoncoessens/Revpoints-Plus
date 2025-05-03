import streamlit as st
import pandas as pd
from urllib.parse import quote_plus
from pathlib import Path
import base64

# -------- Paths to local assets -------- #
ASSETS_PATH = Path(__file__).parent / "assets"
CARD_FILE = ASSETS_PATH / "card.png"
LOGO_FILE = ASSETS_PATH / "revolut_logo.png"
PROFILE_FILE = ASSETS_PATH / "user.png"
CSV_FILE = Path(__file__).parent / "transactions.csv"

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
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="collapsed",
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

if "transactions" not in st.session_state:
    if CSV_FILE.exists():
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
        # Select relevant columns
        st.session_state.transactions = df[["date_str", "name", "amount"]].rename(
            columns={"date_str": "date"}
        )
    else:
        # Fallback seed data
        seed = [
            {"date": "2025-05-02", "name": "Amazon", "amount": -42.35},
            {"date": "2025-05-01", "name": "Apple Pay", "amount": -7.99},
            {"date": "2025-04-29", "name": "Salary", "amount": 2400.00},
        ]
        st.session_state.transactions = pd.DataFrame(seed * 6)

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
st.markdown("<div class='card'>", unsafe_allow_html=True)
if CARD_FILE.exists():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(str(CARD_FILE), width=260)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown(f"<h1 style='text-align:center'>€ {st.session_state.balance:,.2f}</h1>", unsafe_allow_html=True)

# ---------- RECENT ACTIVITY ---------- #
st.markdown("#### Recent activity")
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
    ("Home", "🏠", Path(__file__)),
    ("Explore", "🔍", Path(__file__).parent / "pages/2_Explore.py"),
    ("Cards", "💳", Path(__file__).parent / "pages/3_Cards.py"),
    ("Settings", "⚙️", Path(__file__).parent / "pages/4_Settings.py"),
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