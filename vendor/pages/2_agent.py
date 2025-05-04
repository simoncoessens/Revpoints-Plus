import sys
import os
import json
import tempfile
import datetime
from pathlib import Path
import base64

import streamlit as st
from PIL import Image

# ─── Constants & ensure storage exists ───
APPROVED_DIR = Path("data")
APPROVED_FILE = APPROVED_DIR / "campaigns_approved.json"
APPROVED_DIR.mkdir(parents=True, exist_ok=True)
if not APPROVED_FILE.exists():
    # initialize as empty list
    APPROVED_FILE.write_text("[]")

# Insert parent folder so modules are found
sys.path.insert(0, str(Path(__file__).parent.parent))

# --- Import campaign generation components ---
try: 
    from campaign_agent import CampaignGenerationAgent, CampaignFormat, logger
    from human_in_loop import HumanInLoopManager, MAX_REVISIONS
    AGENT_AVAILABLE = True
except ImportError as e:
    
    st.error(f"Failed to import campaign modules: {e}", icon="🚨")
    AGENT_AVAILABLE = False
    class CampaignGenerationAgent: pass
    class HumanInLoopManager: pass
    class CampaignFormat: pass
    MAX_REVISIONS = 5
    logger = None

# ─── Page config ───
st.set_page_config(
    page_title="Campaign Assistant",
    page_icon="📣",
    layout="centered",
)
st.markdown('<meta name="viewport" content="width=device-width, initial-scale=1">', unsafe_allow_html=True)

# ---------- Paths to local assets ---------- #
BASE_DIR     = Path(__file__).parent.parent
ASSETS_PATH  = BASE_DIR / "assets"
REVOLUT_LOGO = ASSETS_PATH / "revolut_logo.png"
PROFILE_PIC  = ASSETS_PATH / "user.png"

# ---------- Bottom navigation definition ---------- #
NAV = [
    ("Home",     "🏠",  "home.py"),
    ("Create",    "🔍",  "pages/2_agent.py"),
]

# ---------- Helper to inline images ---------- #
def img_tag(path: Path, height: int) -> str:
    if not path.exists():
        return ""
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    data = base64.b64encode(path.read_bytes()).decode()
    return f'<img src="data:{mime};base64,{data}" height="{height}">'

# ---------- CSS: hide sidebar, center content & UI shell ---------- #
FIXED      = 600  # px
BAR_HEIGHT = 20   # px for the faux status bar

st.markdown(
    f"""
    <style>
    #MainMenu, footer {{visibility:hidden;}}
    [data-testid="stSidebar"] {{display:none !important;}}
    html, body, [data-testid="stAppViewContainer"] {{
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
    [data-testid="stAppViewContainer"] > .main {{
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
    .mobile-nav a[selected] {{color:#fff;}}
    button, .stButton > button {{
        text-align: center !important;
        display: block !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }}
    .stButton > button > div, .stButton > button > span {{
        text-align: center !important;
        width: 100% !important;
        justify-content: center !important;
        display: flex !important;
        align-items: center !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- TOP BLACK BAR ---------- #
st.markdown("<div class='mobile-top'></div>", unsafe_allow_html=True)

# ---------- HEADER ---------- #
header_l, header_mid, header_r = st.columns([1, 6, 1])
with header_l:
    st.markdown(img_tag(REVOLUT_LOGO, 28), unsafe_allow_html=True)
with header_mid:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center'>Make Your Own Campaign ✨</h1>", unsafe_allow_html=True)
with header_r:
    st.markdown(img_tag(PROFILE_PIC, 30), unsafe_allow_html=True)

# ─── Load tools & session defaults ───
@st.cache_resource
def load_tools():
    if not AGENT_AVAILABLE:
        return None, None
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if not api_key:
        st.error("Missing GOOGLE_API_KEY", icon="🔑")
        return None, None
    agent = CampaignGenerationAgent(api_key=api_key)
    mgr = HumanInLoopManager(agent)
    return agent, mgr

agent, hitl = load_tools()
for k, v in {
    "state": "idle",
    "catalog": None,
    "current": None,
    "just_refined": False
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─── Upload & Generate ───
st.markdown("<div class='top-section'>", unsafe_allow_html=True)
uploaded = st.file_uploader("Upload Catalog (PNG/JPG/PDF)", type=["png","jpg","jpeg","pdf"])
if uploaded:
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded.name).suffix)
    tmp.write(uploaded.getvalue()); tmp.close()
    st.session_state.catalog = tmp.name
    st.success(f"Uploaded {uploaded.name}")
    if uploaded.type.startswith("image/"):
        st.image(uploaded, use_container_width=True)
gen_disabled = not (st.session_state.catalog and agent)
if st.button("✨ Generate Campaign", disabled=gen_disabled):
    with st.spinner("Generating…"):
        camp = agent.generate_campaign(st.session_state.catalog)
    if camp:
        st.session_state.current = camp
        st.session_state.state = "feedback"
        st.session_state.just_refined = False
    else:
        st.error("Generation failed.")
st.markdown("</div>", unsafe_allow_html=True)

# ─── Show current campaign card ───
if st.session_state.current:
    c = st.session_state.current
    vendor = getattr(c, "vendor_name", "Unknown Vendor")
    st.markdown("<div class='campaign-section'>", unsafe_allow_html=True)
    st.markdown(f"""
      <div class="agent-card">
        <h3>Campaign for {vendor}</h3>
        <p><strong>Category:</strong> {getattr(c,'category','N/A')}</p>
        <p><strong>Slogan:</strong> {getattr(c,'campaign_slogan','N/A')}</p>
        <p><strong>Notification:</strong> {getattr(c,'notification','N/A')}</p>
        <p><strong>Message:</strong> {getattr(c,'campaign_message','N/A')}</p>
        <p><strong>Promotions:</strong></p>
        <ul>{"".join(f"<li>{p}</li>" for p in getattr(c,'promotions',[]))}</ul>
        <p><small>ID: {getattr(c,'campaign_id','N/A')} | {datetime.datetime.now():%Y-%m-%d %H:%M:%S}</small></p>
      </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ─── Revision & Animation Banner ───
if st.session_state.state == "feedback":
    st.markdown("<div class='revision-section'>", unsafe_allow_html=True)
    fb = st.text_area("Revision feedback:", height=80)
    if st.button("🛠️ Refine Campaign", disabled=not fb.strip()):
        with st.spinner("Refining…"):
            revised = hitl.revise_campaign(st.session_state.current, fb)
        if revised:
            st.session_state.current = revised
            st.session_state.just_refined = True
            st.session_state.state = "revised"
            st.rerun()
        else:
            st.error("Refinement failed.")
    st.markdown("</div>", unsafe_allow_html=True)

if st.session_state.just_refined:
    st.markdown("<div class='banner'>✅ Campaign has been refined!</div>", unsafe_allow_html=True)
    st.session_state.just_refined = False

# ─── Confirm & Append to single JSON ───
if st.session_state.state in ["revised","feedback"]:
    if st.button("✅ Confirm & Save"):
        c = st.session_state.current
        # build dict
        entry = {
            "campaign_id": getattr(c,"campaign_id",None),
            "vendor_name": getattr(c,"vendor_name",None),
            "category": getattr(c,"category",None),
            "campaign_slogan": getattr(c,"campaign_slogan",None),
            "notification": getattr(c,"notification",None),
            "campaign_message": getattr(c,"campaign_message",None),
            "promotions": getattr(c,"promotions",[]),
            "timestamp": datetime.datetime.now().isoformat()
        }
        # load existing, append, write back
        data = json.loads(APPROVED_FILE.read_text())
        data.append(entry)
        APPROVED_FILE.write_text(json.dumps(data, indent=2))
        st.balloons()
        st.session_state.state = "done"

# ─── Final Confirmation ───
if st.session_state.state == "done":
    vendor = getattr(st.session_state.current, "vendor_name", "Your campaign")
    st.markdown(f"<div class='confirmation'>🎉 <strong>{vendor} is now live on Revolut Explore! 🚀</strong></div>", unsafe_allow_html=True)

# ---------- Bottom Navigation ---------- #
st.markdown('<div class="mobile-nav">', unsafe_allow_html=True)
cols = st.columns(len(NAV))
for (label, icon, target), col in zip(NAV, cols):
    with col:
        st.page_link(page=target, label=label, icon=icon, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
