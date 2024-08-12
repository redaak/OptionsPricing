Black-Scholes Pricing Model Visualizer
Overview
The Black-Scholes Pricing Model Visualizer is a Streamlit application that allows users to visualize the pricing of options using the Black-Scholes formula. This app provides interactive features to adjust parameters and view the impact on option prices through heatmaps.

Features
Interactive Parameters:

Current Asset Price
Strike Price
Time to Maturity (Years)
Volatility (σ)
Risk-Free Interest Rate (r)
Min/Max Spot Price for Heatmap
Min/Max Volatility for Heatmap
Visualizations:

Call Price Heatmap: Shows the variation in call option prices based on asset price and volatility.
Put Price Heatmap: Shows the variation in put option prices based on asset price and volatility.
Parameter Table: Displays the current parameter values and settings.
Installation
To run this app locally, you need to have Python installed. Follow these steps:

Clone the Repository:

bash
Copy code
git clone https://github.com/your-username/black-scholes-visualizer.git
cd black-scholes-visualizer
Create a Virtual Environment (Optional but recommended):

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install Dependencies:

Make sure you have pipenv installed, then run:

bash
Copy code
pipenv install
Or, if using a requirements.txt file:

bash
Copy code
pip install -r requirements.txt
Run the App:

bash
Copy code
streamlit run your_script.py
Replace your_script.py with the filename of your Streamlit script.

Usage
Adjust Parameters:
Use the sliders and input fields to set the current asset price, strike price, time to maturity, volatility, and risk-free interest rate.

View Heatmaps:
The app will display two heatmaps:

Call Price Heatmap: Reflects how the call option price varies with asset price and volatility.
Put Price Heatmap: Reflects how the put option price varies with asset price and volatility.
Review Parameter Table:
The table at the top of the app shows the current values of all parameters used in the calculations.

Development
Streamlit: Used for building the web app interface.
Plotly: Used for interactive visualizations.
NumPy: Used for numerical calculations.
To contribute or report issues, please open an issue or submit a pull request on the GitHub repository.

License
This project is licensed under the MIT License - see the LICENSE file for details.
