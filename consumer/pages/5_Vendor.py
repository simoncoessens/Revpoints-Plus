import streamlit as st
import pandas as pd
import json
from pathlib import Path
import base64
from urllib.parse import quote_plus

# -------- Paths to local assets -------- #
ASSETS_PATH   = Path(__file__).parent.parent / "assets"
LOGO_FILE     = ASSETS_PATH / "revolut_logo.png"
PROFILE_FILE  = ASSETS_PATH / "user.png"
VENDORS_FILE  = "final.json"

# ---------- Bottom navigation definition ---------- #
NAV = [
    ("Home",     "🏠", "home.py"),
    ("Explore",  "🔍", "pages/2_Explore.py"),
    ("Cards",    "💳", "pages/3_Cards.py"),
    ("Settings", "⚙️", "pages/4_Settings.py"),
]

# ---------- Fixed width & UI shell constants ---------- #
FIXED = 600   # px fixed app width
BAR_HEIGHT = 20  # px for the faux status bar at top and bottom

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
vendor_page_url     = vendor.get('url', '')
vendor_image_url    = vendor.get('image_url', '')

# Read transaction data and compute metrics dynamically
CSV_FILE = Path(__file__).parent.parent.parent / "data/final_data.csv"
if CSV_FILE.exists():
    df = pd.read_csv(CSV_FILE, parse_dates=["timestamp"])
    vendor_txns = df[df["merchant_name"] == vendor_name]
    total_spent = -vendor_txns["amount"].sum()
    visits = len(vendor_txns)
    transactions = vendor_txns.sort_values("timestamp", ascending=False).head(10).to_dict("records")
    if not vendor_txns.empty:
        last_row = vendor_txns.sort_values("timestamp", ascending=False).iloc[0]
        last_purchase = {"date": last_row["timestamp"], "amount": last_row["amount"]}
    else:
        last_purchase = {"date": pd.Timestamp.now(), "amount": 0}
else:
    total_spent = 0
    visits = 0
    transactions = []
    last_purchase = {"date": pd.Timestamp.now(), "amount": 0}

# ---------- Page config ---------- #
st.set_page_config(
    page_title=vendor_name,
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------- Inject CSS for fixed-width layout and UI shell ---------- #
st.markdown(
    f"""
    <style>
    #MainMenu, footer, header {{ visibility: hidden; }}
    html, body, [data-testid=\"stAppViewContainer\"] {{
        max-width:{FIXED}px;
        width:{FIXED}px !important;
        margin:0 auto;
        overflow-x:hidden;
    }}
    .main .block-container {{
        padding-left:1rem;
        padding-right:1rem;
        max-width:{FIXED}px;
    }}
    [data-testid=\"stAppViewContainer\"]>.main {{
        padding-top:{BAR_HEIGHT}px;
        padding-bottom:4rem;
    }}
    .mobile-top {{
        position:fixed;
        top:0; left:0; right:0;
        height:{BAR_HEIGHT}px;
        background:#1a1d23;
        border-bottom:1px solid #2e323b;
        z-index:100;
    }}
    .mobile-nav {{
        position:fixed;
        bottom:0; left:0; right:0;
        width:{FIXED}px;
        margin:0 auto;
        background:#1a1d23;
        border-top:1px solid #2e323b;
        display:flex;
        justify-content:space-around;
        padding:.5rem 0;
        z-index:999;
    }}
    .mobile-nav a {{
        color:#888;
        text-decoration:none;
        font-size:.9rem;
        display:flex;
        flex-direction:column;
        align-items:center;
    }}
    .mobile-nav a[selected] {{ color:#fff; }}
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
    </style>
    """, unsafe_allow_html=True
)

# ---------- TOP BLACK BAR ---------- #
st.markdown(
    f"<div class='mobile-top' style='height:{BAR_HEIGHT}px;'></div>",
    unsafe_allow_html=True
)

# ---------- HEADER (logo + avatar) ---------- #
header_l, _, header_r = st.columns([1, 6, 1])
with header_l:
    st.markdown(img_tag(LOGO_FILE, 28), unsafe_allow_html=True)
with header_r:
    st.markdown(img_tag(PROFILE_FILE, 30), unsafe_allow_html=True)

# ---------- Vendor Header (logo + name) ---------- #
st.markdown(
    f"<div style='display:flex; align-items:center; gap:1rem; justify-content:center; margin-bottom:1.2rem;'>"
    + img_tag(vendor_logo_file, 60)
    + f"<span style='margin:0;font-size:2.1rem;font-weight:800;letter-spacing:-1px;font-family:sans-serif'>{vendor_name}</span></div>",
    unsafe_allow_html=True
)

# ---------- Vendor Image ---------- #
if vendor_image_url:
    st.markdown(
        f"<div style='text-align:center; margin-bottom:1.5rem;'>"
        f"  <img src='{vendor_image_url}' "
        f"style='max-width:300px; width:100%; height:auto; border-radius:1rem; box-shadow:0 4px 12px rgba(0,0,0,0.15);'/></div>",
        unsafe_allow_html=True
    )

# ---------- Main Card (Last Purchase & About) ---------- #
st.markdown("<div style='margin-bottom:1.5rem'>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.markdown(
        f"<p style='font-size:0.98rem;line-height:1.5;color:#222;font-family:sans-serif'><strong>Date:</strong> {pd.to_datetime(last_purchase['date']).strftime('%d %b %Y')}<br>"
        f"<strong>Amount:</strong> € {last_purchase['amount']:,.2f}</p>",
        unsafe_allow_html=True
    )
with col2:
    about_text = vendor.get('About', '')
    st.markdown(
        f"<h4 style='font-size:1.08rem;font-weight:600;margin-bottom:0.3em'>About</h4>"
        f"<p style='font-size:0.98rem;line-height:1.5;color:#222;font-family:sans-serif;margin-bottom:0.5em'>{vendor_description}</p>"
        + (f"<div style='font-size:0.97rem;line-height:1.7;color:#444;background:#f7f7fa;padding:0.7em 1em;border-radius:0.7em;margin-bottom:0.5em;font-family:sans-serif;font-weight:500'>{about_text}</div>" if about_text else "")
        + (f"<p><a href='{vendor_website}' target='_blank'>Visit Website</a></p>" if vendor_website else "")
        + (f"<p><a href='{vendor_page_url}' target='_blank'>Order Now</a></p>" if vendor_page_url else ""),
        unsafe_allow_html=True
    )
st.markdown("</div>", unsafe_allow_html=True)

# ---------- Metrics ---------- #
st.markdown(
    f"<div class='metrics-container' style='display:flex; gap:1rem;'>"
    f"<div class='metric'><h5 style='font-size:1.05rem;font-weight:600;margin-bottom:0.2em'>€ {total_spent:,.2f}</h5><p style='font-size:0.92rem'>Total Spent</p></div>"
    f"<div class='metric'><h5 style='font-size:1.05rem;font-weight:600;margin-bottom:0.2em'>{visits}</h5><p style='font-size:0.92rem'>Visits</p></div>"
    f"</div>",
    unsafe_allow_html=True
)

# ---------- Recent Transactions ---------- #
st.markdown("#### Recent activity")
rows_html = ""
for t in transactions:
    date_fmt = pd.to_datetime(t['timestamp']).strftime("%d %b %Y")
    color = "#0f0" if t["amount"] > 0 else "#ff5b5b"
    rows_html += (
        f"  <div style='display:flex;justify-content:space-between;align-items:center;padding:8px 0;'>"
        f"    <span style='font-size:0.95rem;color:#888'>{date_fmt}</span>"
        f"    <span style='font-size:1.15rem;font-weight:600;color:{color};'>€ {t['amount']:,.2f}</span>"
        f"  </div>"
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
# Matches top bar, spans full viewport width
st.markdown(
    f"<div class='mobile-top' style='height:{BAR_HEIGHT}px; bottom:-{BAR_HEIGHT}px;'></div>",
    unsafe_allow_html=True
)
