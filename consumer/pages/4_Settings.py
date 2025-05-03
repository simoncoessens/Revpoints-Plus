import streamlit as st
import pandas as pd
from urllib.parse import quote_plus
from pathlib import Path
import base64

# -------- Paths to local assets -------- #
ASSETS_PATH = Path(__file__).parent / "assets"
LOGO_FILE = ASSETS_PATH / "revolut_logo.png"
PROFILE_FILE = ASSETS_PATH / "user.png"

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

#
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

# ---------- BOTTOM NAVIGATION ---------- #
NAV = [
    ("Home",    "🏠", Path(__file__).parent.parent / "home.py"),
    ("Explore", "🔍",  Path(__file__)),
    ("Cards",   "💳", Path(__file__).parent.parent / "pages/3_Cards.py"),
    ("Settings","⚙️", Path(__file__).parent.parent / "pages/4_Settings.py"),
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