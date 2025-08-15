# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Configuration ---
st.set_page_config(
    page_title="Raptive Interactive Analysis",
    page_icon="\src\cafemedia_logo.jpg",
    # page_icon="📈",
    layout="wide"
)

# --- Data Loading and Caching ---
@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce')
    df['top'] = pd.to_numeric(df['top'], errors='coerce')
    df.dropna(inplace=True)
    return df

# --- Main App Logic ---
try:
    df = load_data('testdata (1).csv')

    # --- Sidebar ---
    st.sidebar.image("\src\cafemedia_logo.jpg", width=200)
    st.sidebar.title("Interactive Dashboard")
    st.sidebar.markdown("This dashboard demonstrates how high-level trends can be misleading, a phenomenon known as **Simpson's Paradox**.")
    st.sidebar.markdown("---")

    # Create filters in the sidebar
    st.sidebar.header("📊 Segmentation Controls")
    selected_platforms = st.sidebar.multiselect(
        'Filter by Platform:',
        options=df['platform'].unique(),
        default=df['platform'].unique()
    )

    selected_browsers = st.sidebar.multiselect(
        'Filter by Browser:',
        options=df['browser'].unique(),
        default=df['browser'].unique()
    )

    # Filter the data based on selection
    filtered_df = df[df['platform'].isin(selected_platforms) & df['browser'].isin(selected_browsers)]

    st.sidebar.markdown("---")
    # TODO: Remember to replace with your actual information!
    st.sidebar.markdown("Built by Taksha Thosani")
    st.sidebar.markdown("[LinkedIn](https://www.linkedin.com/in/taksha-thosani17) | [GitHub](https://github.com/taksha17)")


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
        trendline="ols",
        color_discrete_sequence=['#6a0dad']
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
        fig_segmented = px.scatter(
            filtered_df,
            x='top',
            y='revenue',
            color='platform',
            symbol='browser',
            title="Segmented Trend: Revenue vs. Time on Page",
            trendline="ols",
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
        
        with st.expander("View Filtered Data"):
            st.dataframe(filtered_df.head(10))
    else:
        st.warning("No data to display. Please select at least one Platform and Browser from the sidebar.")

# Add a broad exception to catch errors like missing files or library issues
except FileNotFoundError:
    st.error("Error: `testdata (1).csv` not found. Please make sure the data file is in the same directory as `app.py` in your GitHub repository.")
except Exception as e:
    st.error(f"An error occurred while running the app. Please ensure all required libraries are listed in requirements.txt. Error: {e}")

