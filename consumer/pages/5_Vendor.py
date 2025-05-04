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
VENDORS_FILE  = Path(__file__).parent.parent.parent / "data" / "partner_vendors.json"

# ---------- Bottom navigation definition ---------- #
NAV = [
    ("Home",     "🏠", "home.py"),
    ("Explore",  "🔍", "pages/2_Explore.py"),
    ("Notifications",    "🔔", "pages/3_Notifications.py"),
    ("Settings", "⚙️", "pages/4_Settings.py"),
]

# ---------- Fixed width & UI shell constants ---------- #
FIXED = 600   # px fixed app width
BAR_HEIGHT = 20  # px faux status bar height


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

# ---------- Streamlit page configuration ---------- #
st.set_page_config(
    page_title=vendor_name,
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
      /* hide the sidebar panel */
      section[data-testid="stSidebar"] {
        display: none;
      }
      /* hide the collapse/expand button in the header bar */
      [data-testid="collapsedControl"] {
        display: none;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Extract dynamic fields ---------- #
vendor_description  = vendor.get('vendor_description', '')
vendor_logo_file    = ASSETS_PATH / f"{vendor['vendor_id']}_logo.png"
vendor_website      = vendor.get('website', '')
vendor_page_url     = vendor.get('url', '')
vendor_image_url    = vendor.get('image_url', '')

# ---------- Read transaction data and compute metrics dynamically ---------- #
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
    page_icon="🔔",
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
    /* --- CARD STYLES --- */
    .card {{
        background: linear-gradient(145deg,#2a2d34,#343741);
        color: #fff;
        border-radius: 1.5rem;
        padding: 1.5rem;
        box-shadow: 0 10px 20px rgba(0,0,0,.3);
        margin-bottom:1rem;
    }}
    /* --- RECENT ACTIVITY SCROLLER --- */
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

# ---------- About (centered) ---------- #
about_html = (
    f"<div style='text-align:center;'>"
    f"  <h4 style='font-size:1.1rem;font-weight:600;margin:0 0 0.5rem;'>About</h4>"
    f"  <p style='font-size:0.97rem;line-height:1.5;margin:0 0 0.8rem;color:#222;'>{vendor_description}</p>"
)
if vendor.get("About"):
    about_html += (
        f"  <div style='font-size:0.95rem;line-height:1.6;color:#444;background:#f7f7fa;padding:0.7em 1em;border-radius:0.7em;margin:0 auto 0.8rem;display:inline-block;font-weight:500'>{vendor['About']}</div>"
    )
if vendor_website:
    about_html += f"  <p style='margin:0 0 0.4rem;'><a href='{vendor_website}' target='_blank'>Visit Website</a></p>"
if vendor_page_url:
    about_html += f"  <p style='margin:0;'><a href='{vendor_page_url}' target='_blank'>Order Now</a></p>"
about_html += "</div>"

st.markdown(about_html, unsafe_allow_html=True)

# ---------- Metrics ---------- #
col1, col2, col3 = st.columns(3)
with col2:
    st.markdown('<br></br>', unsafe_allow_html=True)
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
