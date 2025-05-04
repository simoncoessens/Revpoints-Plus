import streamlit as st
from pathlib import Path
import json
from recommendation_engine import generate_recs

# ---------- Paths to local assets ----------
ASSETS_PATH  = Path(__file__).parent.parent / "assets"
LOGO_FILE    = ASSETS_PATH / "revolut_logo.png"
PROFILE_FILE = ASSETS_PATH / "user.png"

# ---------- TOP BLACK BAR ----------
BAR_HEIGHT = 20  # px
st.markdown(f"<div class='mobile-top' style='height:{BAR_HEIGHT}px'></div>", unsafe_allow_html=True)

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
        background: #fff;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 8px rgba(0,0,0,.10);
        border-radius: 1rem;
        width: 250px;
        color: #222;
        text-decoration: none;
        margin-bottom: 0.2rem;
    }}
    .offer img {{
        width: 100%;
        height: 140px;
        object-fit: cover;
        border-top-left-radius: 1rem;
        border-top-right-radius: 1rem;
    }}
    .offer .body {{ padding: .7rem 1rem; }}
    .offer .body div[style*='font-weight:700'] {{ color: #222; }}
    .offer .body div[style*='font-size:.8rem'] {{ color: #666; }}
    .badge {{
        position: absolute;
        top: 8px; left: 8px;
        background: #ff5b5b;
        padding: 2px 6px;
        border-radius: 6px;
        font-size: .7rem;
        font-weight: 600;
        color: #fff;
        box-shadow: 0 1px 4px rgba(0,0,0,.10);
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
] * 4

# ------------------ Dynamic recommendations ------------------ #

# We need to import the recommendation engine located one level up from
# this *consumer/pages* directory. Add that directory to sys.path so that
# `import recommendation_engine` resolves to Revpoints-Plus/recommendation_engine.py

RECS_PLACEHOLDER_IMG = "https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg"

# Load vendor details for lookup by vendor_id
VENDOR_JSON_PATH = Path(__file__).parent.parent.parent / "data" / "partner_vendors.json"
with open(VENDOR_JSON_PATH, "r", encoding="utf-8") as f:
    vendor_data = json.load(f)
vendor_lookup = {v["vendor_id"]: v for v in vendor_data}


panels = generate_recs()


# ---------- Render recommendations grouped by category ----------
for panel in panels:
    st.markdown(f"### {panel['category']}")
    st.markdown(f"<div style='color:#888;font-size:.95rem;margin-bottom:.5rem'>{panel['reason']}</div>", unsafe_allow_html=True)
    offers_html = ""
    for offer in panel["offers"]:
        v = vendor_lookup.get(offer["vendor_id"])
        if v:
            offer_type = v["offer_details"].get("offer_type", "").replace("_", " ").title()
            offer_desc = v["offer_details"].get("offer_description", "")
            img = RECS_PLACEHOLDER_IMG
            offers_html += f'''<a class='offer' href='#' style='display:inline-block;vertical-align:top;'>
                <span class='badge'>{offer_type}</span>
                <img src='{img}' alt='offer'>
                <div class='body'>
                    <div style='font-weight:700;margin:.1rem 0'>{v['vendor_name']}</div>
                    <div style='font-size:.8rem;color:#888;white-space:normal;word-break:break-word;'>{offer_desc}</div>
                </div>
            </a>'''
    st.markdown((
        f"<div class='h-scroll' style='overflow-x:auto;white-space:nowrap;padding-bottom:0.4rem;'>"
        f"<div style='display:flex;gap:0.9rem;'>"
        f"{offers_html}"
        f"</div></div>"
    ).strip(), unsafe_allow_html=True)

# ---------- Bottom navigation ----------
NAV = [
    ("Home",    "🏠", Path(__file__).parent.parent / "home.py"),
    ("Explore", "🔍",  Path(__file__)),
    ("Notifications",   "🔔", Path(__file__).parent.parent / "pages/3_Notifications.py"),
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
