import streamlit as st
import pandas as pd
import json
from pathlib import Path
import base64
import plotly.express as px
import plotly.graph_objects as go # Added for stacked bar

# -------- Paths to local assets -------- #
# Corrected paths relative to this script's location (consumer/pages/6_savings.py)
# Go up two levels to the project root, then specify the path.
PROJECT_ROOT = Path(__file__).parents[2]
# Assume the main script is consumer/home.py
# Paths for assets should be relative to the main script or absolute
# Let's keep them relative to the project root for clarity here,
# but be mindful if Streamlit has issues finding them.
ASSETS_PATH = PROJECT_ROOT / "consumer/assets"
DATA_PATH = PROJECT_ROOT / "data"
TRANSACTIONS_FILE = DATA_PATH / "revpoint_transactions.json" # Corrected path
LOGO_FILE = ASSETS_PATH / "revolut_logo.png"
PROFILE_FILE = ASSETS_PATH / "user.png"

# ---------- Helper to inline images as <img> tags ---------- #

def img_tag(path: Path, height: int) -> str:
    if not path.exists():
        # Use st.warning for non-critical errors like missing images
        st.warning(f"Asset not found: {path}")
        return ""
    try:
        mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
        data = base64.b64encode(path.read_bytes()).decode()
        return f'<img src="data:{mime};base64,{data}" height="{height}">'  # noqa: E501
    except Exception as e:
        st.error(f"Error loading image {path}: {e}")
        return ""

# ---------- Page config ---------- #

st.set_page_config(
    page_title="Savings Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------- CSS: FIXED‑WIDTH APP (600 px) & UI SHELL ---------- #
FIXED = 600  # px
BAR_HEIGHT = 20  # px for the faux status bar
# Added styles for better spacing and alignment
st.markdown(
    f"""
    <style>
    #MainMenu, footer {{visibility:hidden;}}
    html, body, [data-testid="stAppViewContainer"] {{
        max-width:{FIXED}px;width:{FIXED}px !important;margin:0 auto;overflow-x:hidden; background-color: #0e1117; /* Match Streamlit dark theme */
    }}
    .main .block-container {{padding-left:1rem;padding-right:1rem;max-width:{FIXED}px;}}
    [data-testid="stAppViewContainer"]>.main {{padding-top:{BAR_HEIGHT + 10}px;padding-bottom:5rem;}} /* Increased top padding */
    .mobile-top {{position:fixed;top:0;left:0;right:0;height:{BAR_HEIGHT}px;background:#1a1d23;border-bottom:1px solid #2e323b;z-index:100;}}
    .mobile-nav {{position:fixed;bottom:0;left:0;right:0;width:{FIXED}px;margin:0 auto;background:#1a1d23;border-top:1px solid #2e323b;display:flex;justify-content:space-around;padding:.5rem 0;z-index:999;}}
    .mobile-nav a {{color:#888;text-decoration:none;font-size:.9rem;display:flex;flex-direction:column;align-items:center;}}
    .mobile-nav a:hover {{color:#ddd;}} /* Hover effect */
    .mobile-nav a[selected]{{color:#fff; font-weight: bold;}} /* Highlight selected */
    /* Plotly chart styling */
    .plotly .plot-container {{
        max-width: 100% !important;
        overflow-x: hidden !important;
    }}
    .stPlotlyChart {{
        max-width: 100% !important;
        overflow-x: hidden !important;
    }}
    /* Metric styling */
    [data-testid="stMetric"] {{
        background-color: #262730;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
    }}
    [data-testid="stMetricLabel"] {{
        font-size: 0.9rem;
        color: #aaa;
    }}
    [data-testid="stMetricValue"] {{
        font-size: 1.5rem; /* Slightly larger metric value */
        font-weight: bold;
        color: #fff;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- TOP BLACK BAR ---------- #
st.markdown(f"<div class='mobile-top' style='height:{BAR_HEIGHT}px'></div>", unsafe_allow_html=True)

# ---------- HEADER (logo + avatar) ---------- #
# Use columns to control layout better
header_cols = st.columns([1, 5, 1])
with header_cols[0]:
    st.markdown(img_tag(LOGO_FILE, 28), unsafe_allow_html=True)
with header_cols[2]:
    st.markdown(img_tag(PROFILE_FILE, 30), unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; margin-bottom: 1rem;'>Your RevPoints Savings</h2>", unsafe_allow_html=True)

# ---------- Load Data ---------- #
if not TRANSACTIONS_FILE.exists():
    st.error(f"Transaction file not found: {TRANSACTIONS_FILE}")
    st.stop()

try:
    with open(TRANSACTIONS_FILE, "r") as f:
        data = json.load(f)
    # Filter out incomplete records and ensure numeric types
    valid_data = []
    required_keys = ["money_saved", "points_spent", "timestamp", "vendor_name", "actual_price", "percentage_saved"]
    # Ensure 'percentage_saved' is numeric and handle potential errors during load
    for t in data:
        if t and all(key in t for key in required_keys):
            try:
                # Attempt to convert numeric fields
                t['money_saved'] = float(t['money_saved'])
                t['points_spent'] = int(t['points_spent'])
                t['actual_price'] = float(t['actual_price'])
                t['percentage_saved'] = float(t['percentage_saved']) if t.get('percentage_saved') is not None else 0.0 # Ensure float, default 0
                valid_data.append(t)
            except (ValueError, TypeError):
                # Skip records where conversion fails
                continue # Or log a warning: st.warning(f"Skipping record due to invalid numeric data: {t}")

    if not valid_data:
        st.warning("No valid transaction data found after cleaning.")
        st.stop()

    df = pd.DataFrame(valid_data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['month_year'] = df['timestamp'].dt.to_period('M')
    df['month_year_str'] = df['month_year'].astype(str) # String version for display/filtering
    df['paid_amount'] = df['actual_price'] - df['money_saved'] # Calculate amount paid

except json.JSONDecodeError:
    st.error(f"Error decoding JSON from {TRANSACTIONS_FILE}")
    st.stop()
except Exception as e:
    st.error(f"Error loading or processing data: {e}")
    st.stop()

# ---------- Key Metrics ---------- #
total_savings = df['money_saved'].sum()
total_points_spent = df['points_spent'].sum()
# Calculate average saving percentage only if there are savings
average_saving_percentage = df[df['money_saved'] > 0]['percentage_saved'].mean() if not df[df['money_saved'] > 0].empty else 0

col1, col2, col3 = st.columns(3)
col1.metric("Total Saved", f"€{total_savings:,.2f}")
col2.metric("Total Points Spent", f"{total_points_spent:,}")
col3.metric("Avg. Saving %", f"{average_saving_percentage:.1f}%")

st.markdown("---", unsafe_allow_html=True) # Separator

# ---------- Savings Over Time (Overall Trend - Unfiltered) ---------- #
st.markdown("#### Overall Savings Trend")
savings_over_time = df.groupby('month_year_str')['money_saved'].sum().reset_index()
savings_over_time = savings_over_time.sort_values('month_year_str') # Ensure chronological order

if not savings_over_time.empty:
    fig_time = px.line(savings_over_time, x='month_year_str', y='money_saved',
                       title="Monthly Savings with RevPoints",
                       labels={'month_year_str': 'Month', 'money_saved': 'Total Savings (€)'},
                       markers=True, template='plotly_dark') # Use dark theme
    fig_time.update_layout(xaxis_title=None, yaxis_title="Savings (€)", margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    fig_time.update_traces(line=dict(color='#1DB954')) # Spotify green-ish color
    st.plotly_chart(fig_time, use_container_width=True)
else:
    st.write("Not enough data for a time trend.")

st.markdown("---", unsafe_allow_html=True)

# ---------- Monthly Filtering ---------- #
st.markdown("#### Explore Monthly Performance")
# Get unique months sorted chronologically
available_months = sorted(df['month_year_str'].unique())
# Add 'All Months' option
month_options = ["All Months"] + available_months
selected_month = st.selectbox("Select Month:", options=month_options)

# Filter data based on selection
if selected_month == "All Months":
    filtered_df = df.copy()
    st.markdown(f"##### Showing data for All Time")
else:
    filtered_df = df[df['month_year_str'] == selected_month].copy()
    st.markdown(f"##### Showing data for {selected_month}")

if filtered_df.empty and selected_month != "All Months":
    st.warning(f"No data available for {selected_month}.")
    # Don't stop here, allow navigation
    # st.stop()
elif filtered_df.empty:
     st.warning("No transaction data available.")
     # Don't stop here, allow navigation
     # st.stop()

# Only proceed with charts if filtered_df is not empty
if not filtered_df.empty:

    # ---------- Stacked Bar Chart: Saved vs Paid (Filtered) - MOVED UP & MODIFIED ---------- #
    st.markdown("#### Spending Breakdown at Top Vendors")
    # Aggregate saved and paid amounts for the top vendors in the filtered period
    # Use the same top_vendors definition from the Savings by Vendor chart below
    savings_by_vendor_for_top = filtered_df.groupby('vendor_name')['money_saved'].sum().reset_index()
    top_vendors_for_stack = savings_by_vendor_for_top.nlargest(10, 'money_saved')

    spend_breakdown = filtered_df[filtered_df['vendor_name'].isin(top_vendors_for_stack['vendor_name'])].groupby('vendor_name')[['money_saved', 'paid_amount']].sum().reset_index()
    # Sort by total spend (paid + saved = actual price) descending for the vertical chart
    spend_breakdown['total_spend'] = spend_breakdown['money_saved'] + spend_breakdown['paid_amount']
    spend_breakdown = spend_breakdown.sort_values('total_spend', ascending=False)

    if not spend_breakdown.empty:
        fig_stacked = go.Figure()

        # Add trace for Amount Paid (Red) - Base of the stack
        fig_stacked.add_trace(go.Bar(
            x=spend_breakdown['vendor_name'],
            y=spend_breakdown['paid_amount'],
            name='Amount Paid',
            marker_color='#EF553B' # Red-ish
        ))

        # Add trace for Money Saved (Green) - Top of the stack
        fig_stacked.add_trace(go.Bar(
            x=spend_breakdown['vendor_name'],
            y=spend_breakdown['money_saved'],
            name='Money Saved (RevPoints)',
            marker_color='#1DB954' # Green
        ))


        fig_stacked.update_layout(
            barmode='stack',
            xaxis_title=None,
            yaxis_title="Amount (€)",
            legend_title_text='Spend Type',
            template='plotly_dark',
            margin=dict(l=20, r=20, t=30, b=20), # Adjusted margins
            height=400,
            xaxis={'categoryorder':'array', 'categoryarray': spend_breakdown['vendor_name']}, # Order bars by the sorted vendor names
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_stacked, use_container_width=True)
    else:
        st.write("No spending breakdown data available for top vendors in this period.")

    st.markdown("---", unsafe_allow_html=True)


    # ---------- Savings by Vendor (Filtered) ---------- #
    st.markdown("#### Top Savings by Vendor")
    savings_by_vendor = filtered_df.groupby('vendor_name')['money_saved'].sum().reset_index()
    top_vendors = savings_by_vendor.nlargest(10, 'money_saved').sort_values('money_saved', ascending=True) # Ascending for horizontal bar

    if not top_vendors.empty:
        fig_vendor = px.bar(top_vendors, y='vendor_name', x='money_saved', # Swapped x and y for horizontal
                            # title=f"Top 10 Vendors by Savings ({selected_month})", # Title redundant with markdown
                            labels={'vendor_name': 'Vendor', 'money_saved': 'Total Savings (€)'},
                            orientation='h', template='plotly_dark') # Horizontal bar
        fig_vendor.update_layout(yaxis_title=None, xaxis_title="Savings (€)", margin=dict(l=10, r=20, t=30, b=20), height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        fig_vendor.update_traces(marker_color='#636EFA') # Plotly default blue
        st.plotly_chart(fig_vendor, use_container_width=True)
    else:
        st.write("No vendor savings data available for this period.")

    st.markdown("---", unsafe_allow_html=True)


    # ---------- Average Saving Percentage by Vendor (Filtered) - NEW PLOT ---------- #
    st.markdown("#### Average Saving Percentage by Vendor")
    # Calculate average saving percentage, handle potential division by zero or NaNs
    avg_perc_by_vendor = filtered_df.groupby('vendor_name')['percentage_saved'].mean().reset_index()
    avg_perc_by_vendor = avg_perc_by_vendor.dropna(subset=['percentage_saved']) # Remove vendors with no valid percentage
    # Show top 10 by average percentage
    top_avg_perc_vendors = avg_perc_by_vendor.nlargest(10, 'percentage_saved').sort_values('percentage_saved', ascending=False)

    if not top_avg_perc_vendors.empty:
        fig_avg_perc = px.bar(top_avg_perc_vendors, x='vendor_name', y='percentage_saved',
                              labels={'vendor_name': 'Vendor', 'percentage_saved': 'Average Saving (%)'},
                              template='plotly_dark')
        fig_avg_perc.update_layout(xaxis_title=None, yaxis_title="Average Saving (%)", margin=dict(l=20, r=20, t=30, b=20), height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        fig_avg_perc.update_traces(marker_color='#AB63FA') # Plotly purple
        st.plotly_chart(fig_avg_perc, use_container_width=True)
    else:
        st.write("No average saving percentage data available for this period.")

# ---------- BOTTOM NAVIGATION ---------- #
# Adopted structure from 5_Vendor.py but using correct relative paths for st.page_link

# Define page paths relative to the 'consumer' directory (where home.py likely is)
# Streamlit expects paths relative to the *entrypoint* script's directory OR
# just the filename if the page is in the 'pages/' subdirectory.
HOME_PATH = Path(__file__).parent.parent / "home.py"
NAV = [
    ("Home", "🏠", HOME_PATH),
    ("Explore", "🔍", Path(__file__).parent / "2_Explore.py"),
    ("Notifications", "🔔", Path(__file__).parent / "3_Notifications.py"),
    ("Savings", "💰", Path(__file__)), # Current page
    # ("Settings", "⚙️", Path(__file__).parent / "4_Settings.py"), # Removed Settings
]

st.markdown('<div class="mobile-nav">', unsafe_allow_html=True)
# Adjust columns based on the new length of NAV
cols = st.columns(len(NAV))

# Loop through NAV items and create page links using st.page_link
for i, ((label, icon, target_path_obj), col) in enumerate(zip(NAV, cols)):
    with col:
        # Pass the Path object directly to st.page_link
        # Convert Path object to the string format expected by st.page_link (relative to entrypoint)
        try:
            # Calculate path relative to the 'consumer' directory (assumed entrypoint dir)
            relative_page_path = target_path_obj.relative_to(PROJECT_ROOT / "consumer").as_posix()
            st.page_link(page=relative_page_path, label=label, icon=icon, use_container_width=True)
        except ValueError:
             # Fallback or error handling if relative path fails
             st.markdown(f"<a>{icon}<br>{label}</a>", unsafe_allow_html=True) # Non-clickable fallback
             print(f"Warning: Could not create relative path for navigation link: {label}")


st.markdown("</div>", unsafe_allow_html=True)
