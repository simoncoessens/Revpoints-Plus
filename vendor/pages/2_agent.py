import sys
import os
import json
import tempfile
import datetime
from pathlib import Path

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

# ─── MOBILE-FIRST + ANIMATION CSS ───
st.markdown("""
<style>
body, .main { margin:0; padding:0; width:100%; max-width:100vw; font-family:Arial,sans-serif; }
.main { display:flex; flex-direction:column; align-items:center; padding:0.5rem; }
.top-section, .campaign-section, .revision-section, .confirmation { width:100%; padding:1rem 0.5rem; box-sizing:border-box; }
.agent-card { border-left:4px solid #00aeff; background:#262730; color:#fff; border-radius:12px; padding:1rem; margin:1rem 0; }
.agent-card h3 { margin-top:0; color:#00aeff; }
textarea, input, button { width:100% !important; box-sizing:border-box; margin-top:0.5rem; font-size:1rem; }
button { padding:0.75rem; border:none; border-radius:8px; background:#00aeff; color:#fff; }
button:disabled { background:#555; }
.banner { width:100%; background:#0a342a; color:#fff; text-align:center; padding:0.75rem; border-radius:8px; animation:slideFade 3s ease-out forwards; margin-bottom:1rem; }
@keyframes slideFade { 0%{opacity:0;transform:translateY(-20px);}10%{opacity:1;transform:translateY(0);}90%{opacity:1;}100%{opacity:0;transform:translateY(-20px);} }
.footer { margin-top:2rem; padding:1rem; width:100%; text-align:center; background-color:#1a1d23; color:#aaa; font-size:0.9rem; }
.footer a { color:#00aeff; text-decoration:none; margin:0 0.5rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='main'>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align:center; font-size:1.6rem;'>Campaign Assistant</h1>", unsafe_allow_html=True)

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
        st.image(uploaded, use_column_width=True)
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

# ─── Footer ───
st.markdown("""
<div class="footer">
  <a href="home.py">Home</a>
  <a href="2_agent.py">Campaign</a>
  <a href="pages/3_Cards.py">Cards</a>
  <a href="pages/4_Settings.py">Settings</a>
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
