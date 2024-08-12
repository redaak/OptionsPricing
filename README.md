# **Black-Scholes Pricing Model Visualizer**

## Overview

The **Black-Scholes Pricing Model Visualizer** is a Streamlit application designed to visualize the pricing of options using the Black-Scholes formula. This app allows users to interactively adjust parameters and view the effects on option prices through dynamic heatmaps.

## Features

- **Interactive Parameters:**
  - Current Asset Price
  - Strike Price
  - Time to Maturity (Years)
  - Volatility (σ)
  - Risk-Free Interest Rate (r)
  - Min/Max Spot Price for Heatmap
  - Min/Max Volatility for Heatmap

- **Visualizations:**
  - **Call Price Heatmap:** Displays how call option prices vary with asset price and volatility.
  - **Put Price Heatmap:** Displays how put option prices vary with asset price and volatility.
  - **Parameter Table:** Shows current parameter values and settings.

## Installation

To run this app locally, follow these steps:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/redaak/OptionsPricing.git
   cd black-scholes-visualizer
  Usage
Adjust Parameters:
Use the sliders and input fields to set the current asset price, strike price, time to maturity, volatility, and risk-free interest rate.

View Heatmaps:
The app generates two heatmaps:

Call Price Heatmap: Shows the variation in call option prices based on asset price and volatility.
Put Price Heatmap: Shows the variation in put option prices based on asset price and volatility.
Review Parameter Table:
The table at the top displays the current values of all parameters used in the calculations.

Troubleshooting
ModuleNotFoundError: Ensure all dependencies are installed. If using a virtual environment, verify it's activated and dependencies are correctly listed in Pipfile or requirements.txt.

Favicon Issues: Streamlit may have limitations with favicons. Ensure your favicon is correctly named and placed in the root directory.

Development
Streamlit: Used for the app's interface.
Plotly: Used for interactive visualizations.
NumPy: Used for numerical calculations.
To contribute or report issues, please open an issue or submit a pull request on the GitHub repository.
