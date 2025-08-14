# app.py
import streamlit as st
import numpy as np
import plotly.express as px

# --- Page Configuration ---
st.set_page_config(
    page_title="Central Limit Theorem Demo",
    page_icon="📊",
    layout="wide"
)

# --- App Title and Description ---
st.title("📊 Interactive Central Limit Theorem Demonstration")
st.markdown("""
The **Central Limit Theorem (CLT)** is a cornerstone of statistics. It states that if you take sufficiently large random samples from a population with any shape of distribution, the distribution of the *sample means* will approximate a normal distribution (a bell curve).

**How to use this dashboard:**
1.  **Choose a population distribution** from the sidebar. Notice that some are not bell-shaped at all!
2.  **Adjust the sample size (n)**, which is how many data points are in each sample.
3.  **Adjust the number of samples**, which is how many times we repeat the sampling experiment.

Watch how the histogram on the right, the *Distribution of Sample Means*, becomes more and more like a perfect bell curve as you increase the sample size, regardless of the original population's shape.
""")

# --- Sidebar Controls for User Input ---
st.sidebar.header("⚙️ Dashboard Controls")

dist_options = ['Uniform', 'Normal', 'Exponential', 'Bimodal']
dist_choice = st.sidebar.selectbox(
    "1. Choose a population distribution:",
    options=dist_options
)

sample_size = st.sidebar.slider(
    "2. Select the sample size (n):",
    min_value=2,
    max_value=500,
    value=30, # A common starting value
    step=1,
    help="The number of data points to draw in each individual sample."
)

num_samples = st.sidebar.slider(
    "3. Select the number of samples:",
    min_value=100,
    max_value=10000,
    value=1000,
    step=100,
    help="The number of times the sampling experiment is repeated."
)

# --- Data Generation Logic ---

# We'll create a large population to sample from
population_size = 100000

# Generate the population based on user's choice
if dist_choice == 'Uniform':
    # A flat distribution
    population = np.random.uniform(0, 1, population_size)
elif dist_choice == 'Normal':
    # A standard bell curve
    population = np.random.normal(0, 1, population_size)
elif dist_choice == 'Exponential':
    # A right-skewed distribution
    population = np.random.exponential(1, population_size)
elif dist_choice == 'Bimodal':
    # A distribution with two peaks
    pop1 = np.random.normal(-2, 0.5, population_size // 2)
    pop2 = np.random.normal(2, 0.5, population_size // 2)
    population = np.concatenate([pop1, pop2])

# --- Sampling and Calculation ---
# This is the core of the CLT demonstration
# We perform the experiment 'num_samples' times
sample_means = []
for _ in range(num_samples):
    # Draw a random sample from the population
    sample = np.random.choice(population, size=sample_size)
    # Calculate the mean of that sample and store it
    sample_means.append(np.mean(sample))


# --- Visualization ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Population Distribution")
    # Use Plotly for interactive and clean charts
    fig1 = px.histogram(
        population, 
        nbins=100, 
        title=f"Distribution of the '{dist_choice}' Population"
    )
    fig1.update_layout(showlegend=False, yaxis_title="Frequency", xaxis_title="Value")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Distribution of Sample Means")
    fig2 = px.histogram(
        sample_means, 
        nbins=60, 
        title=f"Distribution of {num_samples} Sample Means (Sample Size n={sample_size})"
    )
    # Overlay a vertical line at the true population mean for reference
    fig2.add_vline(
        x=np.mean(population), 
        line_width=3, 
        line_dash="dash", 
        line_color="red",
        annotation_text="Population Mean",
        annotation_position="top right"
    )
    fig2.update_layout(showlegend=False, yaxis_title="Frequency", xaxis_title="Sample Mean Value")
    st.plotly_chart(fig2, use_container_width=True)
