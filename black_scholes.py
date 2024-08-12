import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import norm


# Black-Scholes pricing function
def black_scholes(S, K, T, r, sigma, option_type='call'):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        option_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        option_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("Invalid option type. Use 'call' or 'put'.")

    return option_price


# Streamlit interface
def display_favicon():
    st.markdown(
        """
        <head>
            <link rel="icon" href="favicon.ico" type="image/x-icon">
        </head>
        """,
        unsafe_allow_html=True
    )
display_favicon()

st.title("📊 Black-Scholes Model")
st.markdown("Created by: [Reda Akdim](https://www.linkedin.com/in/reda-akdim/)")
st.markdown("### Formula for black-scholes model")
st.latex(r'''
\begin{align*}
    \text{Call Price (C)} &= S_0 \Phi(d_1) - K e^{-rT} \Phi(d_2) \\
    \text{Put Price (P)} &= K e^{-rT} \Phi(-d_2) - S_0 \Phi(-d_1) \\
    \text{where} \\
    d_1 &= \frac{\ln(S_0 / K) + (r + \sigma^2 / 2)T}{\sigma \sqrt{T}} \\
    d_2 &= d_1 - \sigma \sqrt{T} \\
    \Phi(x) &= \text{CDF of the standard normal distribution}
\end{align*}
''')
# Sidebar for parameter inputs
st.sidebar.header("Input Parameters")

# Input parameters
S = st.sidebar.number_input("Current Asset Price", min_value=0.0, value=100.0, step=0.1)
K = st.sidebar.number_input("Strike Price", min_value=0.0, value=100.0, step=0.1)
T = st.sidebar.number_input("Time to Maturity (Years)", min_value=0.0, value=1.0, step=0.01)
r = st.sidebar.slider("Risk-Free Interest Rate", min_value=0.0, max_value=0.2, value=0.05, step=0.01)
sigma = st.sidebar.slider("Volatility (σ)", min_value=0.0, max_value=1.0, value=0.2, step=0.01)

# Additional parameters for heatmap
st.sidebar.subheader("Heatmap Parameters")
min_S = st.sidebar.number_input("Min Spot Price", min_value=0.0, value=80.0, step=0.1)
max_S = st.sidebar.number_input("Max Spot Price", min_value=0.0, value=120.0, step=0.1)
min_sigma = st.sidebar.slider("Min Volatility for Heatmap", min_value=0.01, max_value=1.0, value=0.01, step=0.01)
max_sigma = st.sidebar.slider("Max Volatility for Heatmap", min_value=0.01, max_value=1.0, value=0.5, step=0.01)
num_S_points = st.sidebar.slider("Number of Stock Price Points", min_value=5, max_value=20, value=8)
num_sigma_points = st.sidebar.slider("Number of Volatility Points", min_value=5, max_value=20, value=8)
colorscale = st.sidebar.selectbox("Color Scale", options=['Viridis', 'Cividis', 'Plasma', 'Inferno'], index=0)

# Display the parameters in a table
st.subheader("Input Parameters Overview")
parameter_data = {
    "Current Asset Price": [f"{S:.2f}"],
    "Strike Price": [f"{K:.2f}"],
    "Time to Maturity (Years)": [f"{T:.2f}"],
    "Volatility (σ)": [f"{sigma:.2f}"],
    "Risk-Free Interest Rate": [f"{r:.2f}"],
    "Min Spot Price": [f"{min_S:.2f}"],
    "Max Spot Price": [f"{max_S:.2f}"],
    "Min Volatility for Heatmap": [f"{min_sigma:.2f}"],
    "Max Volatility for Heatmap": [f"{max_sigma:.2f}"]
}
st.table(parameter_data)

# Option prices
call_price = black_scholes(S, K, T, r, sigma, option_type='call')
put_price = black_scholes(S, K, T, r, sigma, option_type='put')

# Displaying prices in colored boxes
st.markdown(f"""
<div style="display: flex; justify-content: space-around; margin-bottom: 20px;">
    <div style="background-color: green; padding: 15px; border-radius: 5px; color: white;">
        Call Option Price: <strong>${call_price:.2f}</strong>
    </div>
    <div style="background-color: tomato; padding: 15px; border-radius: 5px; color: white;">
        Put Option Price: <strong>${put_price:.2f}</strong>
    </div>
</div>
""", unsafe_allow_html=True)

# Creating heatmaps for the option prices across different stock prices and volatilities
st.subheader("Call and Put Option Price Heatmaps")
st.markdown(''' :blue-background[Gain insights into how option prices fluctuate across different spot prices and volatility levels using interactive heatmap parameters, all while ensuring a constant strike price.]''')
S_range = np.linspace(min_S, max_S, num_S_points)
sigma_range = np.linspace(min_sigma, max_sigma, num_sigma_points)

call_prices = np.zeros((len(S_range), len(sigma_range)))
put_prices = np.zeros((len(S_range), len(sigma_range)))

for i, S_val in enumerate(S_range):
    for j, sigma_val in enumerate(sigma_range):
        call_prices[i, j] = black_scholes(S_val, K, T, r, sigma_val, 'call')
        put_prices[i, j] = black_scholes(S_val, K, T, r, sigma_val, 'put')

# Plotly heatmaps in subplots
fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=("Call Option Price Heatmap", "Put Option Price Heatmap"),
    shared_yaxes=True,
    column_widths=[0.42, 0.42],  # Adjust column width to fit within the page
    horizontal_spacing=0.05  # Adjust spacing between subplots
)

# Call Option Heatmap
fig.add_trace(
    go.Heatmap(
        z=call_prices,
        x=np.round(sigma_range, 2),
        y=np.round(S_range, 2),
        colorscale=colorscale,
        text=np.round(call_prices, 2),
        hoverinfo="x+y+z",
        showscale=True,
    ),
    row=1, col=1
)

# Put Option Heatmap
fig.add_trace(
    go.Heatmap(
        z=put_prices,
        x=np.round(sigma_range, 2),
        y=np.round(S_range, 2),
        colorscale=colorscale,
        text=np.round(put_prices, 2),
        hoverinfo="x+y+z",
        showscale=True,
    ),
    row=1, col=2
)

fig.update_traces(texttemplate="%{text:.2f}", textfont_size=12)

fig.update_layout(
    margin=dict(l=20, r=20, t=40, b=40),
    xaxis_title='Volatility (σ)',
    yaxis_title='Stock Price (S)',
    width=900,  # Adjusted width to fit within Streamlit layout
    height=500,  # Adjusted height for better proportions
    yaxis=dict(
        tickvals=np.round(S_range, 2)
    )
)

st.plotly_chart(fig)

# Adding styling to improve layout
st.markdown(
    """
    <style>
    .reportview-container {
        background: #f5f5f5;
    }
    .sidebar .sidebar-content {
        background: #f5f5f5;
    }
    h1 {
        
    }
    </style>
    """, unsafe_allow_html=True
)
