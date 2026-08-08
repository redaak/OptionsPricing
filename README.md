# **Options Pricing Desk — Black-Scholes**

## Overview

An interactive desk for pricing European options with the Black-Scholes model. Enter a contract — or paste a raw option quote — and the whole page reprices on every keystroke: theoretical value, the full set of Greeks, implied volatility, put-call parity, payoff and decay curves, and a price surface across spot and volatility.

Built with Streamlit; the interface itself is a self-contained page (`desk.html`) that computes everything client side, so there is no server round-trip between a keystroke and a new number.

## Features

**Pricing**
- Call and put value, split into intrinsic and time value
- Moneyness, break-even for both legs, and risk-neutral probability of finishing in the money
- Put-call parity check with the residual, as a live sanity check on the inputs

**Greeks**
- Delta (per $1 of spot), Gamma (delta change per $1), Vega (per volatility point), Theta (per calendar day), Rho (per 1% in rates) — for both call and put

**Implied volatility**
- Enter what the option actually trades at and solve for the volatility the market is charging
- Bisection over the no-arbitrage bracket, with explicit messages when a price sits below intrinsic value or above the theoretical maximum

**Quote parser**
- Paste something like `AAPL 231.40 C 235 2026-09-19 @ 6.85` and it fills spot, strike, expiry and option type, then backs out implied volatility from the premium

**Charts**
- Value vs spot, with intrinsic value at expiry overlaid
- Call P&L at expiry vs today, with the break-even marked
- Value vs volatility, marking where today's σ sits
- Time decay from today out to expiry

**Price surface**
- Call and put heatmaps across spot × volatility, with ranges either auto-derived from your inputs or set manually, and your current point outlined

**Leg comparison**
- Two contracts side by side under the same spot, rate and volatility, with the B − A difference on price, each Greek, break-even, probability ITM and days to expiry

**Presets**
- At the money, OTM call, earnings (short-dated, high σ), LEAPS, deep ITM put, low-vol index

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/redaak/OptionsPricing.git
   ```

2. **Install dependencies:**

   ```bash
   pipenv install
   ```

3. **Run the app:**

   ```bash
   pipenv run streamlit run black_scholes.py
   ```

The app opens at `http://localhost:8501`.

`desk.html` is fully self-contained apart from its web font, so you can also open it directly in a browser without Python at all.

## Using the Python model on its own

`black_scholes.py` keeps a reference implementation of the model that can be imported independently of the interface:

```python
from black_scholes import black_scholes, greeks, implied_volatility

black_scholes(S=100, K=100, T=90 / 365, r=0.045, sigma=0.25, option_type="call")
greeks(S=100, K=100, T=90 / 365, r=0.045, sigma=0.25, option_type="call")
implied_volatility(target=5.49, S=100, K=100, T=90 / 365, r=0.045, option_type="call")
```

The Python and browser implementations agree to the displayed precision; the Python side exists for scripting, testing and notebook use.

## Model assumptions

European exercise, no dividends, constant volatility and constant risk-free rate. Time to maturity is computed from today's date to the chosen expiry on a 365-day basis. Φ is the standard normal CDF.

## Project layout

| Path | Purpose |
| --- | --- |
| `black_scholes.py` | Streamlit entry point, plus the Python pricing/Greeks/IV reference model |
| `desk.html` | The interface — layout, pricing logic, charts and heatmaps, all client side |
| `static/` | Favicons and web manifest |
| `.devcontainer/` | Codespaces / dev container definition |

## Troubleshooting

**ModuleNotFoundError** — ensure dependencies are installed. If you are using a virtual environment, verify it is activated and that the packages are listed in the `Pipfile`.

**Blank or clipped page** — the interface sizes its own frame after it renders. A hard refresh (Cmd/Ctrl + Shift + R) clears a stale cached copy of `desk.html`.

## Author

Created by [Reda Akdim](https://www.linkedin.com/in/reda-akdim/).
