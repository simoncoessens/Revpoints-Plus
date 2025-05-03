from pathlib import Path
import base64
import streamlit as st
from openai import OpenAI
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

# ─── Page config (MUST be first Streamlit call) ───
st.set_page_config(
    page_title="Campaign Assistant",
    page_icon="📣",
    layout="wide",
)

# ─── Responsive viewport on mobile ───
st.markdown(
    '<meta name="viewport" content="width=device-width, initial-scale=1">',
    unsafe_allow_html=True,
)

# ─── CSS (fixed width, status bar, top nav, chat layout; hide sidebar) ───
FIXED, BAR_HEIGHT, NAV_HEIGHT, GAP = 600, 20, 64, 8
st.markdown(f"""
<style>
  /* Hide Streamlit chrome */
  #MainMenu, footer {{ visibility: hidden; }}

  /* Hide the default Streamlit sidebar */
  [data-testid="stSidebar"] {{ display: none !important; }}

  /* App body: fixed width & padding */
  html, body, [data-testid="stAppViewContainer"] {{
    max-width: {FIXED}px;
    width: {FIXED}px !important;
    margin: 0 auto;
    overflow-x: hidden;
  }}
  .main .block-container {{
    padding: 1rem;
    max-width: {FIXED}px;
  }}
  [data-testid="stAppViewContainer"] > .main {{
    padding-top: {BAR_HEIGHT}px;
    padding-bottom: {GAP}px;
  }}

  /* Fake status bar */
  .mobile-top {{
    position: fixed;
    top: 0; left: 0; right: 0;
    height: {BAR_HEIGHT}px;
    background: #1a1d23;
    border-bottom: 1px solid #2e323b;
    z-index: 100;
  }}

  /* Top nav */
  .mobile-nav {{
    position: fixed;
    top: {BAR_HEIGHT}px;
    left: 50%; transform: translateX(-50%);
    width: 100%; max-width: {FIXED}px; height: {NAV_HEIGHT}px;
    background: #1a1d23;
    border-bottom: 1px solid #2e323b;
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

  /* Chat input at bottom */
  div[data-testid="stChatInputContainer"] {{
    position: fixed;
    left: 50%; transform: translateX(-50%);
    width: 100%; max-width: {FIXED}px;
    bottom: {GAP}px !important;
  }}

  /* Scrollable chat area */
  #chatbox {{
    margin-top: {BAR_HEIGHT + NAV_HEIGHT + GAP}px;
    height: calc(100vh - {BAR_HEIGHT + NAV_HEIGHT + GAP}px);
    overflow-y: auto;
    padding-bottom: 1rem;
  }}
</style>
""", unsafe_allow_html=True)

# ─── Top status bar & header ───
st.markdown("<div class='mobile-top'></div>", unsafe_allow_html=True)
colL, colM, colR = st.columns([1, 6, 1])
with colL:
    logo_path = Path(__file__).parent / "assets" / "revolut_logo.png"
    if logo_path.exists():
        img = base64.b64encode(logo_path.read_bytes()).decode()
        st.markdown(f'<img src="data:image/png;base64,{img}" height="28">', unsafe_allow_html=True)
with colM:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center'>Campaign Assistant</h1>", unsafe_allow_html=True)
with colR:
    pic_path = Path(__file__).parent / "assets" / "user.png"
    if pic_path.exists():
        img = base64.b64encode(pic_path.read_bytes()).decode()
        st.markdown(f'<img src="data:image/png;base64,{img}" height="30">', unsafe_allow_html=True)
st.divider()

# ─── Top navigation bar ───
NAV = [
    ("Home",    "🏠",  "home.py"),
    ("Explore", "🔍", Path(__file__).parent / "2_agent.py"),
    ("Cards",   "💳", Path(__file__).parent / "3_Cards.py"),
    ("Settings","⚙️", Path(__file__).parent / "4_Settings.py"),
    ("Campaign","📣", Path(__file__)),
]
st.markdown('<div class="mobile-nav">', unsafe_allow_html=True)
for (label, icon, target), c in zip(NAV, st.columns(len(NAV))):
    with c:
        st.page_link(page=target, label=label, icon=icon, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ─── Helper to inline logos & avatars ───
def img_tag(path: Path, height: int) -> str:
    if not path.exists():
        return ""
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    data = base64.b64encode(path.read_bytes()).decode()
    return f'<img src="data:{mime};base64,{data}" height="{height}">'

# ─── Vision model loader ───
def _init_vision():
    proc = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    mdl  = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    return proc, mdl

load_vision = st.cache_resource(_init_vision)
processor, vision_model = load_vision()

# ─── Chat setup ───
SYSTEM_PROMPT = (
    "You are a seasoned digital marketing strategist helping vendors design data-driven campaigns. "
    "Start by asking clarifying questions if the goal is unclear. "
    "When enough context is available, propose a concise campaign plan including: objective, target audience, key channels, budget split, and a short creative concept. "
    "Use bullet points and keep answers under 200 words unless the user asks for more detail."
)
client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY")) if st.secrets.get("OPENAI_API_KEY") else None

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi there! 👋 I'm here to help you craft your next marketing campaign. What goal would you like to achieve?"}
    ]

# ─── Image uploader & caption injection ───
uploaded = st.file_uploader("📷 Upload an image for context", type=["png","jpg","jpeg"])
if uploaded:
    img = Image.open(uploaded)
    st.image(img, caption="You uploaded:", use_column_width=True)
    inputs = processor(images=img, return_tensors="pt")
    out    = vision_model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)
    with st.chat_message("user"):
        st.markdown(f"![uploaded] Caption: *{caption}*")
    st.session_state.messages.append({"role":"user","content":f"Here’s an image: {caption}"})

# ─── Chat container ───
st.markdown("<div id='chatbox'>", unsafe_allow_html=True)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
st.markdown("</div>", unsafe_allow_html=True)

# ─── User input & LLM call ───
if prompt := st.chat_input("Describe your campaign goal…"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role":"user","content":prompt})

    if client:
        convo = [{"role":"system","content":SYSTEM_PROMPT}] + st.session_state.messages
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo", temperature=0.7, messages=convo, stream=True
        )
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
    else:
        response = f"Echo: {prompt}"
        with st.chat_message("assistant"):
            st.markdown(response)

    st.session_state.messages.append({"role":"assistant","content":response})
