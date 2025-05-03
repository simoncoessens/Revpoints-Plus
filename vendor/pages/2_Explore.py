import streamlit as st
from pathlib import Path

# ---------- Paths to local assets ----------
ASSETS_PATH  = Path(__file__).parent.parent / "assets"
LOGO_FILE    = ASSETS_PATH / "revolut_logo.png"
PROFILE_FILE = ASSETS_PATH / "user.png"

# ---------- TOP BLACK BAR ----------
BAR_HEIGHT = 20  # px
st.markdown(f"<div class='mobile-top' style='height:{BAR_HEIGHT}px'></div>", unsafe_allow_html=True)

# ---------- CSS ----------
st.markdown(
    f"""
    <style>
    /* hide Streamlit chrome */
    #MainMenu, footer, header {{ visibility: hidden; }}

    /* fixed top bar */
    .mobile-top {{
        position: fixed;
        top: 0; left: 0;
        width: 100%;
        height: {BAR_HEIGHT}px;
        background: #1a1d23;
        border-bottom: 1px solid #2e323b;
        z-index: 100;
    }}

    /* push content below the top bar */
    [data-testid="stAppViewContainer"] > .main {{
        max-width: 420px;
        margin: auto;
        padding: {BAR_HEIGHT + 16}px 0 4rem;
    }}

    h3 {{ margin: 1.4rem 0 .8rem 0; }}

    /* Scroll container */
    .h-scroll {{
        display: flex;
        overflow-x: auto;
        gap: .9rem;
        padding-bottom: .4rem;
        -ms-overflow-style: none;
        scrollbar-width: none;
    }}
    .h-scroll::-webkit-scrollbar {{ display: none; }}

    /* Horizontal vendor chip */
    .store {{
        flex: 0 0 auto;
        display: flex;
        align-items: center;
        gap: .55rem;
        background: #2a2d34;
        border-radius: 1.2rem;
        padding: .45rem .8rem;
        color: #fff;
        font-size: .8rem;
        box-shadow: 0 2px 6px rgba(0,0,0,.25);
    }}
    .store img {{
        width: 48px;
        height: 48px;
        border-radius: 50%;
        object-fit: cover;
    }}
    .store .label {{ font-weight: 600; line-height: 1.1; }}
    .store .pts {{ font-size: .7rem; color: #35d07f; white-space: nowrap; }}

    /* Offer card */
    .offer {{
        flex: 0 0 auto;
        position: relative;
        background: #2a2d34;
        border-radius: 1rem;
        width: 250px;
        color: #fff;
        text-decoration: none;
        box-shadow: 0 4px 10px rgba(0,0,0,.35);
    }}
    .offer img {{
        width: 100%;
        height: 140px;
        object-fit: cover;
        border-top-left-radius: 1rem;
        border-top-right-radius: 1rem;
    }}
    .offer .body {{ padding: .6rem .8rem; }}
    .badge {{
        position: absolute;
        top: 8px; left: 8px;
        background: #ff5b5b;
        padding: 2px 6px;
        border-radius: 6px;
        font-size: .7rem;
        font-weight: 600;
    }}

    /* Bottom navigation */
    .mobile-nav {{
        position: fixed;
        bottom: 0; left: 0;
        width: 100%;
        background: #1a1d23;
        border-top: 1px solid #2e323b;
        display: flex;
        justify-content: space-around;
        padding: .5rem 0;
        z-index: 100;
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

# ---------- Header ----------
header_l, _, header_r = st.columns([1, 6, 1])
with header_l:
    if LOGO_FILE.exists():
        st.image(str(LOGO_FILE), width=34)
with header_r:
    if PROFILE_FILE.exists():
        st.image(str(PROFILE_FILE), width=36)

# ---------- Data ----------
stores = [
    {"name":"Mercadona",        "logo":"https://upload.wikimedia.org/wikipedia/commons/5/5c/Mercadona.svg",                                           "points":"Earn 1×"},
    {"name":"La Boqueria",       "logo":"https://upload.wikimedia.org/wikipedia/commons/9/96/Barcelona_-_Mercat_de_Sant_Josep_%28la_Boqueria%29_-_Entrance.jpg", "points":"Earn 2×"},
    {"name":"Cervecería Moritz", "logo":"https://upload.wikimedia.org/wikipedia/commons/5/52/Entrada_F%C3%A0brica_Moritz.png",                               "points":"Earn 3×"},
    {"name":"Casa Batlló Shop",   "logo":"https://upload.wikimedia.org/wikipedia/commons/7/7f/Casa_Batll%C3%B3_%28shop%29.jpg",                              "points":"Earn 1×"},
    {"name":"El Corte Inglés",    "logo":"https://upload.wikimedia.org/wikipedia/commons/d/d1/Logo_El_Corte_Ingl%C3%A9s.svg",                                 "points":"Earn 1×"},
]

offers = [
    {"vendor":"Tickets Bar", "img":"https://images.pexels.com/photos/461198/pexels-photo-461198.jpeg", "subtitle":"Redeem 250 Pts for 20 € credit", "badge":"Top Offer"},
    {"vendor":"Bar Marsella", "img":"https://images.pexels.com/photos/261537/pexels-photo-261537.jpeg", "subtitle":"Redeem 120 Pts for 2 absinth shots", "badge":"Offer"},
]

recommendations = [
    {"vendor":"Honest Greens", "img":"https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg", "subtitle":"2× points today"},
    {"vendor":"La Fábrica",    "img":"https://yt3.googleusercontent.com/mNUiPrdKp1qVL2igzXa71f3D1Yn-Z7TaFzpBf1bVFmfDKPE_ssMA8vjG9tn-BIuWqmoSGa7eeQ=s900-c-k-c0x00ffffff-no-rj", "subtitle":"Happy-hour bonus"},
]

# ---------- Redeem offers ----------
st.markdown("### Redeem your points")
st.markdown("<div class='h-scroll'>", unsafe_allow_html=True)
for o in offers:
    st.markdown(
        f"""
        <a class='offer' href='#'>
            <span class='badge'>{o['badge']}</span>
            <img src='{o['img']}' alt='offer'>
            <div class='body'>
                <div style='font-weight:700;margin:.1rem 0'>{o['vendor']}</div>
                <div style='font-size:.8rem;color:#ccc'>{o['subtitle']}</div>
            </div>
        </a>
        """,
        unsafe_allow_html=True,
    )
st.markdown("</div>", unsafe_allow_html=True)

# ---------- Tailored picks ----------
st.markdown("### Tailored to your taste")
st.markdown("<div class='h-scroll'>", unsafe_allow_html=True)
for r in recommendations:
    st.markdown(
        f"""
        <a class='offer' href='#'>
            <span class='badge'>{r['subtitle']}</span>
            <img src='{r['img']}' alt='rec'>
            <div class='body'>
                <div style='font-weight:700;margin:.1rem 0'>{r['vendor']}</div>
            </div>
        </a>
        """,
        unsafe_allow_html=True,
    )
st.markdown("</div>", unsafe_allow_html=True)

# ---------- Bottom navigation ----------
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
st.markdown('</div>', unsafe_allow_html=True)
