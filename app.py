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
The **Central Limit Theorem (CLT)** is a fundamental concept in statistics. It states that if you have a population with any shape of distribution, the distribution of the *sample means* will approach a normal distribution (a bell curve) as the sample size gets larger.

**Instructions:**
1.  **Choose a population distribution** from the dropdown menu in the sidebar.
2.  **Adjust the sample size** (how many data points to pick in each sample).
3.  **Adjust the number of samples** (how many times to repeat the experiment).

Observe how the *Distribution of Sample Means* (right chart) becomes more bell-shaped as you increase the sample size, no matter how weird the original *Population Distribution* (left chart) looks!
""")

# --- Sidebar Controls ---
st.sidebar.header("⚙️ Controls")

dist_options = ['Uniform', 'Normal', 'Exponential', 'Bimodal']
dist_choice = st.sidebar.selectbox(
    "1. Choose a population distribution:",
    options=dist_options
)

sample_size = st.sidebar.slider(
    "2. Select the sample size (n):",
    min_value=2,
    max_value=500,
    value=30,
    step=1
)

num_samples = st.sidebar.slider(
    "3. Select the number of samples:",
    min_value=100,
    max_value=10000,
    value=1000,
    step=100
)

# --- Data Generation and Sampling Logic ---

# Create a large population of 100,000 data points
population_size = 100000

if dist_choice == 'Uniform':
    population = np.random.uniform(0, 1, population_size)
elif dist_choice == 'Normal':
    population = np.random.normal(0, 1, population_size)
elif dist_choice == 'Exponential':
    population = np.random.exponential(1, population_size)
elif dist_choice == 'Bimodal':
    # Create two normal distributions and concatenate them
    pop1 = np.random.normal(-2, 0.5, population_size // 2)
    pop2 = np.random.normal(2, 0.5, population_size // 2)
    population = np.concatenate([pop1, pop2])

# Generate the samples and calculate their means
sample_means = [np.mean(np.random.choice(population, size=sample_size)) for _ in range(num_samples)]


# --- Visualization ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Population Distribution")
    fig1 = px.histogram(population, nbins=100, title=f"Distribution of the '{dist_choice}' Population")
    fig1.update_layout(showlegend=False, yaxis_title="Frequency")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Distribution of Sample Means")
    fig2 = px.histogram(sample_means, nbins=50, title=f"Distribution of {num_samples} Sample Means (n={sample_size})")
    fig2.update_layout(showlegend=False, yaxis_title="Frequency")
    st.plotly_chart(fig2, use_container_width=True)