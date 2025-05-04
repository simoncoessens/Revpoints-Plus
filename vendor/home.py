import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import base64
import plotly.express as px
import altair as alt
from datetime import datetime

# ---------- Page config (must be first Streamlit call) ---------- #
st.set_page_config(
    page_title="Bar de la FIB Dashboard",
    page_icon="☕",
    layout="wide",
)

# Inject mobile viewport meta tag
st.markdown(
    '<meta name="viewport" content="width=device-width, initial-scale=1">',
    unsafe_allow_html=True,
)

# ---------- Paths to local assets ---------- #
BASE_DIR     = Path(__file__).parent
SALES_FILE   = BASE_DIR / "sales.csv"
ASSETS_PATH  = BASE_DIR / "assets"
VENDOR_LOGO  = ASSETS_PATH / "vendor_logo.png"
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
    /* hide main menu & footer */
    #MainMenu, footer {{visibility:hidden;}}

    /* hide Streamlit sidebar */
    [data-testid="stSidebar"] {{display:none !important;}}

    /* center the app container */
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

    /* faux status bar */
    .mobile-top {{
        position:fixed;
        top:0; left:0; right:0;
        height:{BAR_HEIGHT}px;
        background:#1a1d23;
        border-bottom:1px solid #2e323b;
        z-index:100;
    }}

    /* bottom nav */
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
    st.markdown("<h1 style='text-align:center'>Bar de la FIB Dashboard</h1>", unsafe_allow_html=True)
with header_r:
    st.markdown(img_tag(PROFILE_PIC, 30), unsafe_allow_html=True)

# ---------- Load and (optionally) simulate sales data ---------- #
def load_data() -> pd.DataFrame:
    if SALES_FILE.exists():
        return pd.read_csv(SALES_FILE, parse_dates=["date"])
    else:
        rng = pd.date_range(end=datetime.now(), periods=365*4, freq="6h")
        n   = len(rng)
        return pd.DataFrame({
            "date": rng,
            "amount": np.random.gamma(3,4,n).round(2),
            "vendor_name": "Bar de la FIB",
            "product": np.random.choice(
                ["Drink", "Food", "Merch"], size=n, p=[.7, .25, .05]
            )
        })

raw_df = load_data()
df = raw_df[raw_df["vendor_name"] == "Bar de la FIB"].copy()
if df.empty:
    st.warning("No sales found for vendor 'Bar de la FIB'")
    st.stop()

# If CSV has a 'product' column but no 'product_category', use 'product' as category
if "product" in df.columns and "product_category" not in df.columns:
    df["product_category"] = df["product"]

# Ensure there are no missing categories
df["product_category"] = df["product_category"].fillna("Unknown")

# ---------- SUMMARY METRICS ---------- #
total_sales = df["amount"].sum()
order_count = len(df)
avg_order   = df["amount"].mean()

c1, c2, c3 = st.columns(3)
c1.metric("Total Sales",      f"€ {total_sales:,.2f}")
c2.metric("Number of Orders", f"{order_count}")
c3.metric("Avg. Order Value", f"€ {avg_order:,.2f}")

st.divider()

# ---------- SALES OVER TIME ---------- #
st.subheader("Sales Over Time")
daily = df.groupby(df["date"].dt.date)["amount"].sum().reset_index()
line_fig = px.line(daily, x="date", y="amount", title="Daily Total Sales", markers=True)
st.plotly_chart(line_fig, use_container_width=True)

# ---------- DEEPER INSIGHTS ---------- #
# ---------- DEEPER INSIGHTS ---------- #
st.subheader("Deeper Insights")

# create two equal‐width columns
col1, col2 = st.columns(2)

# 1. Sales by Weekday in the left column
with col1:
    wday_totals = (
        df
        .groupby(df["date"].dt.day_name())["amount"]
        .sum()
        .reindex(["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
        .reset_index(name="total")
    )
    bar_fig = px.bar(
        wday_totals,
        x="date",
        y="total",
        title="Sales by Weekday"
    )
    st.plotly_chart(bar_fig, use_container_width=True)

# 2. Sales by Hour Heatmap in the right column
with col2:
    df["hour"]    = df["date"].dt.hour
    df["weekday"] = df["date"].dt.day_name()
    heat = (
        df
        .pivot_table(index="weekday", columns="hour", values="amount", aggfunc="sum")
        .fillna(0)
        .reindex(index=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
    )
    heat_df = heat.reset_index().melt(id_vars="weekday", var_name="hour", value_name="amount")
    heat_chart = alt.Chart(heat_df).mark_rect().encode(
        x=alt.X('hour:O', title='Hour of Day'),
        y=alt.Y('weekday:O', sort=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]),
        color=alt.Color('amount:Q', scale=alt.Scale(scheme='greens'), legend=None),
        tooltip=['weekday','hour','amount']
    ).properties(title="Heatmap: Sales Intensity")
    st.altair_chart(heat_chart, use_container_width=True)

# ---------- Product Mix ---------- #
st.subheader("Product Mix")
cat_totals = (
    df.groupby("product_category")["amount"]
      .sum()
      .reset_index(name="total")
)
cat_pie = px.pie(
    cat_totals,
    names="product_category",
    values="total",
    hole=.4,
    title="Sales by Product Category"
)
st.plotly_chart(cat_pie, use_container_width=True)

# ---------- Cumulative Sales ---------- #
st.subheader("Cumulative Performance")
cum_df = df.sort_values("date").assign(cum=lambda d: d["amount"].cumsum())
cum_fig = px.area(cum_df, x="date", y="cum", title="Cumulative Sales to Date")
st.plotly_chart(cum_fig, use_container_width=True)

# ---------- RECENT TRANSACTIONS ---------- #
st.subheader("Recent Transactions")
recent_df = (
    df
    .sort_values("date", ascending=False)
    .head(10)
    .reset_index(drop=True)
    .drop(columns=["vendor_name"])
)
st.table(recent_df)

# ---------- Bottom Navigation ---------- #
st.markdown('<div class="mobile-nav">', unsafe_allow_html=True)
cols = st.columns(len(NAV))
for (label, icon, target), col in zip(NAV, cols):
    with col:
        st.page_link(page=target, label=label, icon=icon, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
