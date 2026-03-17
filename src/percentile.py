# ─────────────────────────────────────────────────────────────────────────────
# percentile.py  ·  Percentile ranking engine for heat map
# ─────────────────────────────────────────────────────────────────────────────

import numpy as np
import pandas as pd
from scipy import stats
from src.config import (
    NSE500, DEFAULT_WEIGHTS, SECTOR_WEIGHTS,
    ZONES, ZONE_COLORS, NUMERIC_COLS,
)

INVERTED = {"div_yield"}


def _hist_arr(hist_df: pd.DataFrame, metric: str) -> np.ndarray:
    col_map = {
        "pe":        ["pe","p/e","pe_ratio"],
        "pb":        ["pb","p/b","p/bv","pb_ratio"],
        "ev_ebitda": ["ev_ebitda","ev/ebitda"],
        "div_yield": ["div_yield","dividend_yield"],
    }
    for cand in col_map.get(metric, [metric]):
        for col in hist_df.columns:
            if col.lower().replace(" ","_") == cand:
                arr = pd.to_numeric(hist_df[col], errors="coerce").dropna().values
                return arr[arr > 0]
    return np.array([])


def percentile_rank(val, arr) -> float | None:
    if val is None or (isinstance(val, float) and np.isnan(val)): return None
    if len(arr) < 20: return None
    return round(stats.percentileofscore(arr, float(val), kind="rank"), 1)


def z_score(val, arr) -> float | None:
    if val is None or len(arr) < 20: return None
    mu, sigma = arr.mean(), arr.std()
    if sigma == 0: return 0.0
    return round((float(val) - mu) / sigma, 2)


def richness_pct(raw, metric) -> float | None:
    if raw is None: return None
    return round(100 - raw, 1) if metric in INVERTED else raw


def build_percentile_matrix(sector_df, hist_dict):
    sectors = list(NSE500.keys())
    matrix  = pd.DataFrame(index=sectors, columns=NUMERIC_COLS, dtype=float)
    for sector in sectors:
        if sector not in hist_dict: continue
        for metric in NUMERIC_COLS:
            arr = _hist_arr(hist_dict[sector], metric)
            try:    val = float(sector_df.loc[sector, metric])
            except: val = None
            matrix.loc[sector, metric] = richness_pct(percentile_rank(val, arr), metric)
    return matrix


def build_zscore_matrix(sector_df, hist_dict):
    sectors = list(NSE500.keys())
    zmat    = pd.DataFrame(index=sectors, columns=NUMERIC_COLS, dtype=float)
    for sector in sectors:
        if sector not in hist_dict: continue
        for metric in NUMERIC_COLS:
            arr = _hist_arr(hist_dict[sector], metric)
            try:    val = float(sector_df.loc[sector, metric])
            except: val = None
            z = z_score(val, arr)
            zmat.loc[sector, metric] = -z if (z and metric in INVERTED) else z
    return zmat


def composite_score(pct_matrix, sector) -> float | None:
    weights = SECTOR_WEIGHTS.get(sector, DEFAULT_WEIGHTS)
    tw = ts = 0.0
    for m, w in weights.items():
        v = pct_matrix.loc[sector, m] if sector in pct_matrix.index else None
        if v is not None and not (isinstance(v, float) and np.isnan(v)):
            ts += float(v) * w; tw += w
    return round(ts / tw, 1) if tw > 0 else None


def build_richness_series(pct_matrix):
    return pd.Series(
        {s: composite_score(pct_matrix, s) for s in pct_matrix.index},
        name="richness"
    ).dropna().sort_values()


def interpret_score(score) -> tuple:
    for label, (lo, hi) in ZONES.items():
        if lo <= score < hi:
            return label, ZONE_COLORS[label]
    return "Fair", ZONE_COLORS["Fair"]
