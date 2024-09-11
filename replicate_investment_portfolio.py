# Replicate investment portfolio.
# https://www.pyquantnews.com/the-pyquant-newsletter/replicate-your-favorite-investment-portfolio?utm_source=linkedin&utm_medium=post&utm_campaign=8.22.24.12.LI

# Imports
import riskfolio as rp
import pandas as pd
import yfinance as yf
import warnings
warnings.filterwarnings("ignore")

# Download price data for portfolio
assets = [
    "JCI",
    "TGT",
    "CMCSA",
    "CPB",
    "MO",
    "APA",
    "MMC",
    "JPM",
    "ZION",
    "PSA",
    "BAX",
    "BMY",
    "LUV",
    "PCAR",
    "TXT",
    "TMO",
    "DE",
    "MSFT",
    "HPQ",
    "SEE",
    "VZ",
    "CNP",
    "NI",
    "T",
    "BA",
    "^GSPC",
]

data = yf.download(assets, start="2023-01-01", end="2024-12-31")
data = data.loc[:, ("Adj Close", slice(None))]
data.columns = assets

# Compute portfolio and index returns
returns = data.pct_change().dropna()
bench_returns = returns.pop("^GSPC").to_frame()

# Build portfolio
port = rp.Portfolio(returns=returns)
port.assets_stats(method_mu="hist", method_cov="hist", d=0.94)
port.kindbench = False
port.benchindex = bench_returns
port.allowTE = True
port.TE = 0.008

# Run optimization
model = "Classic"
rm = "CVaR"
obj = "Sharpe"
hist = True
rf = 0
l = 0
w = port.optimization(
    model=model,
    rm=rm,
    obj=obj,
    rf=rf,
    l=l,
    hist=hist
)

# Plot optimal weights
ax = rp.plot_pie(
    w=w,
    title="Sharpe Mean CVaR",
    others=0.05,
    nrow=25,
    cmap="tab20",
    height=6,
    width=10,
    ax=None,
)

frontier = port.efficient_frontier(
    model=model, 
    rm=rm, 
    points=50, 
    rf=rf, 
    hist=hist
)

ax = rp.plot_frontier(
    w_frontier=frontier,
    mu=port.mu,
    cov=port.cov,
    returns=port.returns,
    rm=rm,
    rf=rf,
    cmap="viridis",
    w=w,
    label="Max Risk Adjusted Return Portfolio",
    marker="*",
)