# ─────────────────────────────────────────────────────────────────────────────
# comps.py  ·  Comparable Company Analysis (CCA) Engine
#   · Auto peer selection (same sector + adjacent cap tier)
#   · Trading multiples table (P/E, Fwd P/E, EV/EBITDA, EV/Sales, P/BV, Div Yield)
#   · Premium / Discount vs peer median
#   · Percentile rank within peer set
#   · Upside / downside to peer median implied price
#   · Football field chart data
# ─────────────────────────────────────────────────────────────────────────────

import numpy as np
import pandas as pd
from scipy import stats
from src.config import (
    NSE500, ALL_TICKERS, CCA_METRICS,
    CAP_ADJACENCY, NUMERIC_COLS,
)

COMP_COLS = list(CCA_METRICS.keys())

# Cleaning bounds for CCA
CCA_BOUNDS = {
    "pe":        (1,    150),
    "fwd_pe":    (1,    100),
    "pb":        (0.1,   60),
    "ev_ebitda": (1,     60),
    "ev_sales":  (0.1,   30),
    "div_yield": (0,     20),
}


# ── Peer selection ────────────────────────────────────────────────────────────

def find_peers(
    target_ticker: str,
    all_df: pd.DataFrame,
    n_peers: int = 8,
    strict_sector: bool = True,
) -> pd.DataFrame:
    """
    Find the best comparable peers for a target company.

    Criteria (in order of priority):
    1. Same sector (strict) or adjacent sector (relaxed)
    2. Adjacent market cap tier (large ↔ mid ↔ small)
    3. Exclude target itself
    4. Take up to n_peers companies sorted by market cap proximity

    Returns DataFrame of peer rows (including target as first row).
    """
    if target_ticker not in ALL_TICKERS:
        return pd.DataFrame()

    target_info = ALL_TICKERS[target_ticker]
    target_sector   = target_info["sector"]
    target_cap_tier = target_info["cap_tier"]
    allowed_tiers   = CAP_ADJACENCY.get(target_cap_tier, ["mid"])

    # Get target row
    target_rows = all_df[all_df["ticker"] == target_ticker]
    if target_rows.empty:
        return pd.DataFrame()
    target_row = target_rows.iloc[0]
    target_mktcap = target_row.get("mktcap") or 0

    # Filter candidates
    candidates = all_df[
        (all_df["ticker"] != target_ticker) &
        (all_df["sector"] == target_sector) &
        (all_df["cap_tier"].isin(allowed_tiers))
    ].copy()

    if len(candidates) < 3 and not strict_sector:
        # Relax: adjacent sectors
        candidates = all_df[
            (all_df["ticker"] != target_ticker) &
            (all_df["cap_tier"].isin(allowed_tiers))
        ].copy()

    # Score by mktcap proximity (log distance)
    def mktcap_score(row):
        mc = row.get("mktcap") or 0
        if mc <= 0 or target_mktcap <= 0: return 999
        return abs(np.log(mc) - np.log(target_mktcap))

    candidates["_score"] = candidates.apply(mktcap_score, axis=1)
    candidates = candidates.sort_values("_score").head(n_peers)

    # Combine target + peers
    combined = pd.concat([target_rows, candidates], ignore_index=True)
    combined["_is_target"] = combined["ticker"] == target_ticker
    return combined.drop(columns=["_score"], errors="ignore")


# ── Multiples cleaning ────────────────────────────────────────────────────────

def clean_comps(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col, (lo, hi) in CCA_BOUNDS.items():
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            df.loc[df[col] < lo, col] = np.nan
            df[col] = df[col].clip(upper=hi)
    return df


# ── Summary statistics ────────────────────────────────────────────────────────

def peer_summary_stats(peers_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute mean, median, min, max, 25th, 75th percentile
    for each multiple across the peer set (excluding target).
    """
    non_target = peers_df[~peers_df.get("_is_target", pd.Series(False, index=peers_df.index))]
    rows = []
    for col in COMP_COLS:
        if col not in non_target.columns: continue
        arr = pd.to_numeric(non_target[col], errors="coerce").dropna()
        if len(arr) == 0: continue
        rows.append({
            "metric":  col,
            "label":   CCA_METRICS[col]["label"],
            "count":   len(arr),
            "mean":    arr.mean(),
            "median":  arr.median(),
            "min":     arr.min(),
            "max":     arr.max(),
            "p25":     arr.quantile(0.25),
            "p75":     arr.quantile(0.75),
        })
    if not rows:
        return pd.DataFrame()
    df = pd.DataFrame(rows)
    if "metric" not in df.columns:
        return df
    return df.set_index("metric")


# ── Premium / Discount ────────────────────────────────────────────────────────

def premium_discount(target_val, peer_median) -> float | None:
    """% premium (+) or discount (-) of target vs peer median."""
    if target_val is None or peer_median is None: return None
    try:
        tv = float(target_val); pm = float(peer_median)
        if pm == 0: return None
        return round((tv / pm - 1) * 100, 1)
    except: return None


def pct_rank_in_peers(target_val, peer_vals: pd.Series) -> float | None:
    """Percentile of target within peer set (0=cheapest, 100=most expensive)."""
    try:
        tv  = float(target_val)
        arr = peer_vals.dropna().values
        if len(arr) < 2: return None
        return round(stats.percentileofscore(arr, tv, kind="rank"), 1)
    except: return None


# ── Full CCA table ────────────────────────────────────────────────────────────

def build_comps_table(peers_df: pd.DataFrame) -> pd.DataFrame:
    """
    Build the formatted comparable company analysis table.
    Rows = companies, Columns = Name, Mkt Cap, and all multiples.
    Target company row is first.
    """
    clean_df = clean_comps(peers_df)

    rows = []
    for _, row in clean_df.iterrows():
        mktcap = row.get("mktcap")
        mktcap_cr = f"₹{mktcap/1e7:,.0f} Cr" if mktcap else "N/A"

        entry = {
            "Company":     row.get("name", row.get("ticker","")),
            "Ticker":      row.get("ticker",""),
            "Mkt Cap":     mktcap_cr,
            "_mktcap_raw": mktcap or 0,
            "_is_target":  row.get("_is_target", False),
        }

        for col in COMP_COLS:
            val = row.get(col)
            cfg = CCA_METRICS[col]
            if val is None or (isinstance(val, float) and np.isnan(val)):
                entry[cfg["label"]] = None
                entry[f"_{col}"]    = None
            else:
                entry[cfg["label"]] = round(float(val), 1)
                entry[f"_{col}"]    = float(val)

        rows.append(entry)

    return pd.DataFrame(rows)


def build_premium_discount_table(comps_table: pd.DataFrame) -> pd.DataFrame:
    """
    For each multiple: target value, peer median, premium/discount, percentile rank.
    """
    target_rows = comps_table[comps_table["_is_target"] == True]
    peer_rows   = comps_table[comps_table["_is_target"] == False]

    if target_rows.empty:
        return pd.DataFrame()

    target_row = target_rows.iloc[0]
    results = []

    for col in COMP_COLS:
        cfg        = CCA_METRICS[col]
        label      = cfg["label"]
        raw_col    = f"_{col}"
        target_val = target_row.get(raw_col)
        peer_vals  = pd.to_numeric(peer_rows[raw_col], errors="coerce") if raw_col in peer_rows.columns else pd.Series(dtype=float)
        peer_med   = float(peer_vals.median()) if not peer_vals.dropna().empty else None
        peer_mean  = float(peer_vals.mean())   if not peer_vals.dropna().empty else None
        prem_disc  = premium_discount(target_val, peer_med)
        pct        = pct_rank_in_peers(target_val, peer_vals)

        # For div_yield: invert interpretation
        is_expensive = cfg["higher_is_expensive"]
        if pct is not None and not is_expensive:
            pct = 100 - pct

        # Implied price from peer median (if target has price)
        target_price = float(target_row.get("price") or 0)
        implied_price = None
        if target_val and peer_med and target_val > 0 and target_price > 0:
            implied_price = round(target_price * (peer_med / target_val), 1)

        results.append({
            "Metric":           label,
            "Target":           round(target_val, 1) if target_val else None,
            "Peer Median":      round(peer_med, 1)   if peer_med   else None,
            "Peer Mean":        round(peer_mean, 1)  if peer_mean  else None,
            "Premium / Disc %": prem_disc,
            "Pct in Peers":     pct,
            "Implied Price":    f"₹{implied_price:,.0f}" if implied_price else "N/A",
            "_higher_expensive":is_expensive,
        })

    return pd.DataFrame(results)


# ── Football field data ───────────────────────────────────────────────────────

def football_field_data(comps_table: pd.DataFrame) -> dict:
    """
    For each multiple: returns dict with
    min, p25, median, p75, max of peer set, and target value.
    Used to draw football field / waterfall charts.
    """
    peer_rows = comps_table[comps_table.get("_is_target", pd.Series(False)) == False]
    target_rows = comps_table[comps_table.get("_is_target", pd.Series(False)) == True]
    result = {}

    for col in COMP_COLS:
        raw_col = f"_{col}"
        if raw_col not in peer_rows.columns: continue
        arr = pd.to_numeric(peer_rows[raw_col], errors="coerce").dropna()
        if arr.empty: continue
        target_val = None
        if not target_rows.empty and raw_col in target_rows.columns:
            tv = target_rows.iloc[0].get(raw_col)
            if tv: target_val = float(tv)

        result[col] = {
            "label":  CCA_METRICS[col]["label"],
            "min":    float(arr.min()),
            "p25":    float(arr.quantile(0.25)),
            "median": float(arr.median()),
            "p75":    float(arr.quantile(0.75)),
            "max":    float(arr.max()),
            "target": target_val,
        }
    return result


# ── Sector aggregate for heat map ─────────────────────────────────────────────

def aggregate_sector_multiples(all_df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate company-level multiples to sector medians.
    Returns DataFrame indexed by sector.
    """
    df = all_df.copy()
    for col in NUMERIC_COLS:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df.loc[df[col] < 0, col] = np.nan
        if col == "pe": df[col] = df[col].clip(upper=150)

    return df.groupby("sector")[NUMERIC_COLS].median()
