# NSE Valuation Suite 📊

**Sector Heat Map + Comparable Company Analysis (CCA) Screener for NSE 500**

A combined equity research tool that answers two questions every analyst asks:
1. **Which sectors are cheap or expensive right now?** (Heat Map)
2. **Does this company trade at a premium or discount to its peers?** (CCA Screener)

---

## Features

### Sector Heat Map
- 12 NSE sectors tracked across P/E, P/BV, EV/EBITDA, Dividend Yield
- Historical percentile rank vs 10-year history
- Composite Richness Score per sector (0=cheapest, 100=most expensive)
- Sector drill-down with 10-year history chart + radar

### CCA Screener
- Search any of 180+ NSE 500 companies
- Auto peer identification (same sector + market cap tier)
- Full trading comps table (6 multiples)
- Premium / Discount vs peer median
- Football field chart (peer range with target overlay)
- Implied price from peer median re-rating
- 1-year price chart + fundamental data

---

## Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Cloud
1. Push to public GitHub repository
2. Go to share.streamlit.io → New app → select repo → app.py → Deploy

---

## Project Structure
```
nse-valuation-suite/
├── app.py                 ← Streamlit dashboard
├── src/
│   ├── config.py          ← NSE 500 universe, sectors, weights
│   ├── fetch.py           ← Data fetching (yfinance + synthetic fallback)
│   ├── comps.py           ← CCA engine (peer finding, multiples, premium/discount)
│   ├── percentile.py      ← Heat map percentile ranking
│   └── visuals.py         ← All chart generation
├── requirements.txt
└── README.md
```
