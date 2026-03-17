# ─────────────────────────────────────────────────────────────────────────────
# fetch.py  ·  Data fetching for both Heat Map + CCA Screener
# ─────────────────────────────────────────────────────────────────────────────

import os, time, pickle, warnings
import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime, date, timedelta
from src.config import NSE500, ALL_TICKERS, SECTOR_HIST_PARAMS

warnings.filterwarnings("ignore")

CACHE_DIR = "data/cache"
os.makedirs(CACHE_DIR, exist_ok=True)


# ── Cache helpers ─────────────────────────────────────────────────────────────

def _cp(key):      return os.path.join(CACHE_DIR, f"{key}.pkl")
def _fresh(key, h=6):
    p = _cp(key)
    if not os.path.exists(p): return False
    return (datetime.now() - datetime.fromtimestamp(os.path.getmtime(p))).total_seconds() / 3600 < h
def _save(key, obj):
    with open(_cp(key), "wb") as f: pickle.dump(obj, f)
def _load(key):
    with open(_cp(key), "rb") as f: return pickle.load(f)


# ── Single ticker fetch ───────────────────────────────────────────────────────

def fetch_ticker_info(ticker: str) -> dict:
    """Fetch all available info for a single ticker from yfinance."""
    cache_key = f"info_{ticker.replace('.','_')}"
    if _fresh(cache_key, h=4):
        return _load(cache_key)
    try:
        info = yf.Ticker(ticker).info
        result = {
            "ticker":      ticker,
            "name":        info.get("shortName", ALL_TICKERS.get(ticker,{}).get("name",ticker)),
            "sector":      ALL_TICKERS.get(ticker, {}).get("sector","Unknown"),
            "cap_tier":    ALL_TICKERS.get(ticker, {}).get("cap_tier","mid"),
            "pe":          info.get("trailingPE"),
            "fwd_pe":      info.get("forwardPE"),
            "pb":          info.get("priceToBook"),
            "ev_ebitda":   info.get("enterpriseToEbitda"),
            "ev_sales":    info.get("enterpriseToRevenue"),
            "div_yield":   (info.get("dividendYield") or 0) * 100,
            "mktcap":      info.get("marketCap"),
            "ev":          info.get("enterpriseValue"),
            "revenue":     info.get("totalRevenue"),
            "ebitda":      info.get("ebitda"),
            "net_income":  info.get("netIncomeToCommon"),
            "total_debt":  info.get("totalDebt"),
            "cash":        info.get("totalCash"),
            "price":       info.get("currentPrice") or info.get("regularMarketPrice"),
            "52w_high":    info.get("fiftyTwoWeekHigh"),
            "52w_low":     info.get("fiftyTwoWeekLow"),
            "beta":        info.get("beta"),
            "roe":         info.get("returnOnEquity"),
            "roce":        info.get("returnOnAssets"),
            "revenue_growth": info.get("revenueGrowth"),
            "earnings_growth":info.get("earningsGrowth"),
            "gross_margin":   info.get("grossMargins"),
            "operating_margin":info.get("operatingMargins"),
            "net_margin":     info.get("profitMargins"),
            "analyst_target": info.get("targetMeanPrice"),
            "recommend":      info.get("recommendationKey",""),
        }
        _save(cache_key, result)
        return result
    except Exception:
        return {"ticker": ticker, "name": ticker, "sector": "Unknown",
                "cap_tier":"mid", "pe":None,"fwd_pe":None,"pb":None,
                "ev_ebitda":None,"ev_sales":None,"div_yield":0,
                "mktcap":None,"ev":None,"revenue":None,"ebitda":None,
                "net_income":None,"total_debt":None,"cash":None,
                "price":None,"52w_high":None,"52w_low":None,"beta":None,
                "roe":None,"roce":None,"revenue_growth":None,
                "earnings_growth":None,"gross_margin":None,
                "operating_margin":None,"net_margin":None,
                "analyst_target":None,"recommend":""}


def fetch_sector_batch(sector: str, status_cb=None) -> list[dict]:
    """Fetch all tickers in a sector."""
    cache_key = f"sector_{sector.replace(' ','_').replace('&','and')}"
    if _fresh(cache_key, h=4):
        return _load(cache_key)

    companies = NSE500.get(sector, [])
    results = []
    for i, (ticker, name, cap_tier) in enumerate(companies):
        if status_cb: status_cb(ticker)
        data = fetch_ticker_info(ticker)
        results.append(data)
        time.sleep(0.25)

    _save(cache_key, results)
    return results


def fetch_all_sectors(status_cb=None) -> pd.DataFrame:
    """Fetch all NSE500 companies. Returns combined DataFrame."""
    cache_key = "all_nse500"
    if _fresh(cache_key, h=4):
        return _load(cache_key)

    all_rows = []
    for sector in NSE500:
        if status_cb: status_cb(f"Loading {sector}…")
        rows = fetch_sector_batch(sector)
        all_rows.extend(rows)
        time.sleep(0.1)

    df = pd.DataFrame(all_rows)
    _save(cache_key, df)
    return df


# ── Historical data ───────────────────────────────────────────────────────────

def _generate_synthetic_history(sector: str, years: int = 10) -> pd.DataFrame:
    params  = SECTOR_HIST_PARAMS.get(sector, SECTOR_HIST_PARAMS["Information Technology"])
    n_days  = years * 252
    dates   = pd.date_range(end=date.today(), periods=n_days, freq="B")
    rng     = np.random.default_rng(abs(hash(sector)) % (2**32))

    def ou_series(lo, hi, mean, std, n):
        s = np.zeros(n); s[0] = mean
        for i in range(1, n):
            s[i] = s[i-1] + 0.015*(mean-s[i-1]) + std*0.04*rng.normal()
            s[i] = np.clip(s[i], lo*0.7, hi*1.3)
        return s

    data = {m: ou_series(*p, n_days) for m, p in params.items()}
    df   = pd.DataFrame(data, index=dates)
    df.index.name = "date"

    # COVID crash
    crash = (df.index >= "2020-02-20") & (df.index <= "2020-04-30")
    for c in ["pe","pb","ev_ebitda"]:
        df.loc[crash, c] *= rng.uniform(0.55, 0.72)
    # 2021 surge
    surge = (df.index >= "2021-01-01") & (df.index <= "2021-12-31")
    for c in ["pe","pb"]:
        df.loc[surge, c] *= rng.uniform(1.15, 1.35)

    return df.reset_index()


def fetch_historical(sector: str, years: int = 10) -> pd.DataFrame:
    key = f"hist_{sector.replace(' ','_').replace('&','and')}_{years}y"
    if _fresh(key, h=24): return _load(key)
    df = _generate_synthetic_history(sector, years)
    _save(key, df)
    return df


def fetch_all_historical(years: int = 10, status_cb=None) -> dict:
    key = f"all_hist_{years}y"
    if _fresh(key, h=24): return _load(key)
    result = {}
    for sector in NSE500:
        if status_cb: status_cb(f"History: {sector}…")
        result[sector] = fetch_historical(sector, years)
    _save(key, result)
    return result


# ── Price history for a single ticker (for 52W chart) ─────────────────────────

def fetch_price_history(ticker: str, period: str = "1y") -> pd.DataFrame:
    key = f"price_{ticker.replace('.','_')}_{period}"
    if _fresh(key, h=4): return _load(key)
    try:
        df = yf.Ticker(ticker).history(period=period)[["Close","Volume"]]
        _save(key, df)
        return df
    except Exception:
        return pd.DataFrame()


def clear_cache():
    for f in os.listdir(CACHE_DIR):
        try: os.remove(os.path.join(CACHE_DIR, f))
        except: pass
