# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Configuration ---
st.set_page_config(
    page_title="Raptive Interactive Analysis",
    page_icon="📈",
    layout="wide"
)

# --- Data Loading and Caching ---
# Use caching to prevent reloading data on every interaction
@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    # Perform the same cleaning as in your analysis
    df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce')
    df['top'] = pd.to_numeric(df['top'], errors='coerce')
    df.dropna(inplace=True)
    return df

df = load_data('testdata (1).csv')

# --- Sidebar ---
st.sidebar.image("https://raptive.com/wp-content/uploads/2023/04/Raptive_Logo_wordmark_white.svg", width=200)
st.sidebar.title("Interactive Dashboard")
st.sidebar.markdown("This dashboard demonstrates how high-level trends can be misleading, a phenomenon known as **Simpson's Paradox**.")
st.sidebar.markdown("---")

# Create filters in the sidebar
st.sidebar.header("📊 Segmentation Controls")
selected_platforms = st.sidebar.multiselect(
    'Filter by Platform:',
    options=df['platform'].unique(),
    default=df['platform'].unique() # Default to all selected
)

selected_browsers = st.sidebar.multiselect(
    'Filter by Browser:',
    options=df['browser'].unique(),
    default=df['browser'].unique() # Default to all selected
)

# Filter the data based on selection
filtered_df = df[df['platform'].isin(selected_platforms) & df['browser'].isin(selected_browsers)]

st.sidebar.markdown("---")
st.sidebar.markdown("Built by [Your Name Here]")
st.sidebar.markdown("[LinkedIn](https://www.linkedin.com/) | [GitHub](https://github.com/)")


# --- Main Page Content ---
st.title("💡 Uncovering the Real Drivers of Revenue")
st.markdown("An interactive analysis of Time on Page vs. Revenue.")
st.markdown("---")

# --- Part 1: The Misleading Overall Trend ---
st.header("Part 1: The High-Level View (The Illusion)")
st.markdown("At first glance, it appears that as users spend **more** time on a page, revenue **decreases**. The regression line below shows a clear negative correlation.")

fig_overall = px.scatter(
    df, x='top', y='revenue',
    title="Overall Trend: Revenue vs. Time on Page",
    trendline="ols", # Ordinary Least Squares regression line
    color_discrete_sequence=['#6a0dad'] # A nice purple
)
fig_overall.update_layout(
    xaxis_title="Time on Page",
    yaxis_title="Revenue",
    font=dict(family="sans-serif", size=12, color="#333")
)
st.plotly_chart(fig_overall, use_container_width=True)

st.info("This initial finding is counter-intuitive. Let's dig deeper by segmenting the data.")
st.markdown("---")


# --- Part 2: The Segmented, True Trend ---
st.header("Part 2: The Segmented View (The Reality)")
st.markdown("When we segment the data by **Platform** and **Browser**, the opposite story emerges. Within each specific user group, spending **more** time on page is positively correlated with **more** revenue.")

if not filtered_df.empty:
    # Create the segmented scatter plot
    fig_segmented = px.scatter(
        filtered_df,
        x='top',
        y='revenue',
        color='platform',  # Color points by platform
        symbol='browser',  # Use different symbols for browsers
        title="Segmented Trend: Revenue vs. Time on Page",
        trendline="ols",   # Show regression line for each segment
        labels={'top': 'Time on Page', 'revenue': 'Revenue'}
    )
    fig_segmented.update_layout(
        legend_title_text='Segments',
        font=dict(family="sans-serif", size=12, color="#333")
    )
    st.plotly_chart(fig_segmented, use_container_width=True)
    
    st.success(
        """
        **Insight:** The negative trend was an illusion! It was caused by lower-revenue segments (like mobile users) also happening to have longer average session times. 
        The real business driver is user engagement within each platform.
        """
    )
    
    # Show a snippet of the filtered data
    with st.expander("View Filtered Data"):
        st.dataframe(filtered_df.head(10))
else:
    st.warning("No data to display. Please select at least one Platform and Browser from the sidebar.")

