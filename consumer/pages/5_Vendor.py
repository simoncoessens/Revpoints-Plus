import streamlit as st
import pandas as pd
import json
from pathlib import Path
import base64
from urllib.parse import quote_plus

# -------- Paths to local assets -------- #
ASSETS_PATH   = Path(__file__).parent / "assets"
LOGO_FILE     = ASSETS_PATH / "revolut_logo.png"
PROFILE_FILE  = ASSETS_PATH / "user.png"
VENDORS_FILE  = "vendors.json"

# ---------- Bottom navigation definition ---------- #
NAV = [
    ("Home",     "🏠", Path(__file__).parent.parent / "home.py"),
    ("Explore",  "🔍", Path(__file__)),
    ("Cards",    "💳", Path(__file__).parent.parent / "pages/3_Cards.py"),
    ("Settings", "⚙️", Path(__file__).parent.parent / "pages/4_Settings.py"),
]

# ---------- Helper to inline images as <img> tags ---------- #
def img_tag(path: Path, height: int) -> str:
    if not path.exists():
        return ""
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    data = base64.b64encode(path.read_bytes()).decode()
    return f'<img src="data:{mime};base64,{data}" height="{height}">'

# ---------- Load vendor data ---------- #
with open(VENDORS_FILE, 'r', encoding='utf-8') as f:
    vendors = json.load(f)

# ---------- Get vendor_name from URL query params ---------- #
names = st.query_params.get_all("vendor_name")  # returns a list
vendor_name = names[0] if names else None

# ---------- Lookup vendor ---------- #
vendor = next((v for v in vendors if v["vendor_name"] == vendor_name), None)
if not vendor:
    st.error(
        f"Vendor '{vendor_name}' not found." if vendor_name else "No vendor_name provided in the URL."
    )
    st.stop()

# ---------- Extract dynamic fields ---------- #
vendor_description  = vendor.get('vendor_description', '')
vendor_logo_file    = ASSETS_PATH / f"{vendor['vendor_id']}_logo.png"
vendor_website      = vendor.get('website', '')
last_purchase       = vendor.get('last_purchase', {'date': pd.Timestamp.now(), 'amount': 0})
metrics             = vendor.get('metrics', {'total_spent': 0, 'visits': 0})
transactions        = vendor.get('recent_transactions', [])

# ---------- Page config ---------- #
st.set_page_config(
    page_title=vendor_name,
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------- TOP BLACK BAR ---------- #
BAR_HEIGHT = 20  # px
st.markdown(
    f"<div class='mobile-top' style='height:{BAR_HEIGHT}px'></div>",
    unsafe_allow_html=True
)

# ---------- CSS ---------- #
st.markdown(
    f"""
<style>
#MainMenu, footer, header {{ visibility: hidden; }}

[data-testid="stAppViewContainer"] > .main {{
    max-width: 420px;
    margin: auto;
    padding: {BAR_HEIGHT + 16}px 0 4rem;
    /* leave room at bottom for fixed nav */
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

.card {{
    background: linear-gradient(145deg,#2a2d34,#343741);
    color: #fff;
    border-radius: 1.5rem;
    padding: 1.5rem;
    box-shadow: 0 10px 20px rgba(0,0,0,.3);
    margin-bottom:1rem;
}}

.recent-activity {{
    max-height: 300px;
    overflow-y: auto;
    padding-right: .5rem;
}}
.recent-activity::-webkit-scrollbar {{ width:6px; }}
.recent-activity::-webkit-scrollbar-thumb {{
    background:#343741;
    border-radius:3px;
}}

/* Fixed Bottom Navigation */
.mobile-nav {{
    position: fixed;
    bottom: 0; left: 0;
    width: 100%;
    background: #1a1d23;
    border-top: 1px solid #2e323b;
    display: flex;
    justify-content: space-around;
    padding: .5rem 0;
    z-index: 999;
}}
.mobile-nav a {{
    color: #888;
    text-decoration: none;
    font-size: .9rem;
    display: flex;
    flex-direction: column;
    align-items: center;
}}
.mobile-nav a[selected] {{ color: #fff; }}
</style>
""",
    unsafe_allow_html=True,
)

# ---------- HEADER (logo + avatar) ---------- #
header_l, _, header_r = st.columns([1, 6, 1])
with header_l:
    st.markdown(img_tag(LOGO_FILE, 28), unsafe_allow_html=True)
with header_r:
    st.markdown(img_tag(PROFILE_FILE, 30), unsafe_allow_html=True)

# ---------- Vendor Header ---------- #
st.markdown(
    f"<div style='display:flex; align-items:center; gap:1rem;'>"
    + img_tag(vendor_logo_file, 60)
    + f"<h1>{vendor_name}</h1></div>",
    unsafe_allow_html=True
)

# ---------- Main Card (Last Purchase & About) ---------- #
st.markdown("<div class='card page-card'>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.markdown(
        f"<h3>Last Purchase</h3>"
        f"<p><strong>Date:</strong> {pd.to_datetime(last_purchase['date']).strftime('%d %b %Y')}<br>"
        f"<strong>Amount:</strong> € {last_purchase['amount']:,.2f}</p>",
        unsafe_allow_html=True
    )
with col2:
    st.markdown(
        f"<h3>About</h3><p>{vendor_description}</p>"
        + (f"<p><a href='{vendor_website}' target='_blank'>Visit Website</a></p>" if vendor_website else ""),
        unsafe_allow_html=True
    )
st.markdown("</div>", unsafe_allow_html=True)

# ---------- Metrics ---------- #
st.markdown(
    f"<div class='metrics-container' style='display:flex; gap:1rem;'>"
    f"<div class='metric'><h2>€ {metrics['total_spent']:,.2f}</h2><p>Total Spent</p></div>"
    f"<div class='metric'><h2>{metrics['visits']}</h2><p>Visits</p></div>"
    f"</div>",
    unsafe_allow_html=True
)

# ---------- Recent Transactions ---------- #
st.markdown("#### Recent Transactions")
rows_html = ""
for t in transactions:
    date = pd.to_datetime(t['date']).strftime('%d %b %Y')
    amt = t['amount']
    color = "#0f0" if amt > 0 else "#ff5b5b"
    rows_html += (
        f"<div style='display:flex;justify-content:space-between;padding:4px 0;'>"
        f"<strong>{date}</strong><span style='color:{color}'>€ {amt:,.2f}</span></div>"
    )
st.markdown(f"<div class='recent-activity'>{rows_html}</div>", unsafe_allow_html=True)

# ---------- Bottom Navigation ---------- #
st.markdown('<div class="mobile-nav">', unsafe_allow_html=True)
cols = st.columns(len(NAV))
for (label, icon, target), col in zip(NAV, cols):
    with col:
        st.page_link(page=target, label=label, icon=icon, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------- BOTTOM BLACK BAR ---------- #
st.markdown(
    f"<div class='mobile-top' style='height:{BAR_HEIGHT}px; bottom:-{BAR_HEIGHT}px;'></div>",
    unsafe_allow_html=True
)
