"""Black-Scholes Options Pricing Desk.

Streamlit entry point. The interface lives in ``desk.html`` — a self-contained
page that prices European options, backs out implied volatility, renders the
Greeks, the price surface and the payoff charts entirely client side. This
module serves that page and keeps a reference implementation of the pricing
formula in Python so the model can be imported and tested on its own.
"""

from pathlib import Path

import numpy as np
import streamlit as st
import streamlit.components.v1 as components
from scipy.stats import norm

BASE_DIR = Path(__file__).parent
DESK_HTML = BASE_DIR / "desk.html"
FAVICON = BASE_DIR / "static" / "favicon-32x32.png"

# Fallback height for the embedded desk. The page reports its real height back
# through the Streamlit component channel as soon as it renders, so this only
# matters for the first paint and for browsers that block postMessage.
FALLBACK_HEIGHT = 1650


def black_scholes(S, K, T, r, sigma, option_type="call"):
    """Price a European option with the Black-Scholes formula.

    Args:
        S: Current price of the underlying asset.
        K: Strike price.
        T: Time to maturity, in years.
        r: Continuously compounded risk-free rate.
        sigma: Annualised volatility of the underlying.
        option_type: Either ``"call"`` or ``"put"``.

    Returns:
        The theoretical option price.

    Raises:
        ValueError: If ``option_type`` is neither ``"call"`` nor ``"put"``.
    """
    if option_type not in ("call", "put"):
        raise ValueError("Invalid option type. Use 'call' or 'put'.")

    # At or past expiry, or with no volatility, the option is worth its
    # intrinsic value and the d1/d2 terms are undefined.
    if T <= 0 or sigma <= 0:
        return max(S - K, 0.0) if option_type == "call" else max(K - S, 0.0)

    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == "call":
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)


def greeks(S, K, T, r, sigma, option_type="call"):
    """Return delta, gamma, vega, theta, rho and the risk-neutral P(ITM).

    Vega is quoted per volatility point, theta per calendar day and rho per
    1% move in rates, matching the units shown in the interface.
    """
    if option_type not in ("call", "put"):
        raise ValueError("Invalid option type. Use 'call' or 'put'.")

    if S <= 0 or K <= 0 or T <= 0 or sigma <= 0:
        return {"delta": 0.0, "gamma": 0.0, "vega": 0.0, "theta": 0.0, "rho": 0.0, "prob_itm": 0.0}

    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    sqrt_t = np.sqrt(T)
    disc = np.exp(-r * T)
    pdf = norm.pdf(d1)
    is_call = option_type == "call"

    if is_call:
        theta = -S * pdf * sigma / (2 * sqrt_t) - r * K * disc * norm.cdf(d2)
    else:
        theta = -S * pdf * sigma / (2 * sqrt_t) + r * K * disc * norm.cdf(-d2)

    return {
        "delta": norm.cdf(d1) if is_call else norm.cdf(d1) - 1,
        "gamma": pdf / (S * sigma * sqrt_t),
        "vega": S * pdf * sqrt_t / 100,
        "theta": theta / 365,
        "rho": (K * T * disc * norm.cdf(d2) if is_call else -K * T * disc * norm.cdf(-d2)) / 100,
        "prob_itm": norm.cdf(d2) if is_call else norm.cdf(-d2),
    }


def implied_volatility(target, S, K, T, r, option_type="call", tol=1e-8, max_iter=100):
    """Back out the volatility that reprices an option at ``target``.

    Uses bisection over a wide bracket, which is unconditionally stable for
    the monotone price-vs-volatility relationship. Returns ``None`` when the
    target price sits outside the no-arbitrage bounds.
    """
    if target <= 0 or T <= 0:
        return None

    if option_type == "call":
        floor, ceiling = max(S - K * np.exp(-r * T), 0.0), S
    else:
        floor, ceiling = max(K * np.exp(-r * T) - S, 0.0), K

    if target < floor - 1e-6 or target > ceiling:
        return None

    lo, hi = 0.0005, 5.0
    for _ in range(max_iter):
        mid = (lo + hi) / 2
        if black_scholes(S, K, T, r, mid, option_type) > target:
            hi = mid
        else:
            lo = mid
        if hi - lo < tol:
            break
    return (lo + hi) / 2


def main():
    """Serve the pricing desk as a full-bleed Streamlit page."""
    st.set_page_config(
        page_title="Options Pricing Desk · Black-Scholes",
        page_icon=str(FAVICON) if FAVICON.exists() else "📊",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    # The desk owns the whole page: strip Streamlit's chrome and padding so the
    # embedded document sits flush against the viewport.
    st.markdown(
        """
        <style>
          header[data-testid="stHeader"] { display: none; }
          div[data-testid="stToolbar"] { display: none; }
          div[data-testid="stDecoration"] { display: none; }
          section[data-testid="stSidebar"] { display: none; }
          footer { display: none; }
          .stApp { background: #F4F3EF; }
          .block-container { padding: 0 !important; max-width: 100% !important; }
          div[data-testid="stAppViewBlockContainer"] { padding: 0 !important; }
          iframe { display: block; border: none; width: 100%; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    components.html(DESK_HTML.read_text(encoding="utf-8"), height=FALLBACK_HEIGHT, scrolling=True)


# Streamlit runs this file as "__main__", so the guard covers both
# `streamlit run black_scholes.py` and `python black_scholes.py`, while
# leaving the pricing helpers importable without side effects.
if __name__ == "__main__":
    main()
