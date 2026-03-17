# ─────────────────────────────────────────────────────────────────────────────
# app.py  ·  NSE Valuation Suite — Heat Map + CCA Screener
# ─────────────────────────────────────────────────────────────────────────────

import warnings, time
import numpy as np
import pandas as pd
import streamlit as st
from datetime import date

warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="NSE Valuation Suite",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
body,.stApp{background:#0f1117;color:#e8e6e0}
[data-testid="stSidebar"]{background:#111316;border-right:1px solid #1e2228}
[data-testid="stSidebar"] *{color:#cccccc !important}
.stTabs [data-baseweb="tab-list"]{background:#111316;border-bottom:1px solid #1e2228}
.stTabs [data-baseweb="tab"]{color:#888;font-size:13px;font-weight:500;padding:10px 20px}
.stTabs [aria-selected="true"]{color:white !important;border-bottom:2px solid #c9a84c !important}
.mcard{background:#111316;border:1px solid #1e2228;border-radius:8px;padding:14px 16px;text-align:center}
.mcard .lbl{font-size:10px;color:#555;text-transform:uppercase;letter-spacing:.12em;margin-bottom:4px}
.mcard .val{font-size:21px;font-weight:500}
.mcard .sub{font-size:11px;color:#444;margin-top:2px}
.zbadge{display:inline-block;padding:3px 10px;border-radius:10px;font-size:11px;font-weight:600}
.comp-header{background:#111316;border:1px solid #1e2228;border-radius:10px;padding:16px 20px;margin-bottom:16px}
.comp-header h2{font-size:18px;font-weight:500;color:white;margin-bottom:4px}
.comp-header .meta{font-size:12px;color:#555}
h1,h2,h3{color:#e8e6e0 !important}
hr{border-color:#1e2228}
p,li{color:#aaa}
.stDataFrame{background:#111316 !important}
.stButton button{background:#c9a84c;color:#0f1117;font-weight:600;border:none}
.stSelectbox label,.stMultiselect label{color:#aaa !important}
table{width:100%}
th{background:#1e2228;color:#aaa;font-size:11px;font-weight:500;text-transform:uppercase;letter-spacing:.08em;padding:8px 10px}
td{color:#ccc;font-size:12px;padding:7px 10px;border-bottom:1px solid #1e2228}
tr:first-child td{color:white;font-weight:500;background:#1a2030;border-left:3px solid #c9a84c}
</style>
""", unsafe_allow_html=True)

from src.config import NSE500, ALL_TICKERS, CCA_METRICS, LOOKBACK_OPTIONS, NUMERIC_COLS, ZONE_COLORS
from src.fetch import fetch_all_sectors, fetch_all_historical, fetch_price_history, clear_cache
from src.comps import (aggregate_sector_multiples, find_peers, clean_comps,
                       build_comps_table, build_premium_discount_table,
                       football_field_data)
from src.percentile import (build_percentile_matrix, build_zscore_matrix,
                             build_richness_series, composite_score, interpret_score)
from src.visuals import (draw_heatmap, draw_ranking_chart, draw_history_chart,
                         draw_spider, draw_football_field, draw_premium_discount,
                         draw_price_chart, style_comps_table as vis_style, METRIC_LABELS)

SECTOR_LIST  = list(NSE500.keys())
TICKER_NAMES = {t: f"{d['name']} ({t.replace('.NS','')})" for t,d in ALL_TICKERS.items()}


# ══════════════════════════════════════════════════════════════════════════════
# DATA LOADING
# ══════════════════════════════════════════════════════════════════════════════

@st.cache_data(ttl=14400, show_spinner=False)
def load_all_data(years):
    raw     = fetch_all_sectors()
    hist    = fetch_all_historical(years)
    sec_df  = aggregate_sector_multiples(raw)
    pct_mat = build_percentile_matrix(sec_df, hist)
    rich    = build_richness_series(pct_mat)
    return raw, hist, sec_df, pct_mat, rich


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
    <div style='padding:10px 0 16px'>
      <div style='font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:#c9a84c;margin-bottom:6px'>NSE Valuation Suite</div>
      <div style='font-size:16px;font-weight:500;color:white;line-height:1.3'>Heat Map<br>+ CCA Screener</div>
      <div style='font-size:11px;color:#444;margin-top:4px'>NSE 500 · 12 Sectors</div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    lookback_label = st.selectbox("Historical lookback", list(LOOKBACK_OPTIONS.keys()), index=2)
    years          = LOOKBACK_OPTIONS[lookback_label]

    st.markdown("")
    sel_metrics = st.multiselect("Heat map metrics", NUMERIC_COLS,
                                  default=NUMERIC_COLS,
                                  format_func=lambda m: METRIC_LABELS.get(m,m))
    if not sel_metrics: sel_metrics = NUMERIC_COLS

    st.divider()
    st.markdown("##### CCA Settings")
    n_peers       = st.slider("Number of peers", 4, 12, 8)
    strict_sector = st.checkbox("Strict sector matching", value=True,
                                help="If unchecked, peers from adjacent sectors are included")

    st.divider()
    if st.button("🔄  Refresh data", use_container_width=True):
        clear_cache(); st.cache_data.clear()
        st.success("Cache cleared."); time.sleep(1); st.rerun()

    st.markdown(f"<div style='margin-top:20px;font-size:11px;color:#333'>Data: NSE India · Yahoo Finance<br>Updated: {date.today().strftime('%d %b %Y')}</div>",
                unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# LOAD DATA
# ══════════════════════════════════════════════════════════════════════════════

with st.spinner("Loading market data — first run may take 60–90 seconds…"):
    raw_df, hist_dict, sec_df, pct_matrix, richness = load_all_data(years)


# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════

st.markdown(f"""
<div style='padding:6px 0 18px'>
  <div style='font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:#c9a84c;margin-bottom:6px'>
    NSE Valuation Suite  ·  {date.today().strftime('%B %Y')}
  </div>
  <div style='font-size:24px;font-weight:500;color:white;line-height:1.2;margin-bottom:4px'>
    Sector Heat Map  &  Comparable Company Analysis
  </div>
  <div style='font-size:12px;color:#666'>
    12 sectors · NSE 500 universe · {lookback_label} historical lookback · Live data
  </div>
</div>
""", unsafe_allow_html=True)

# Summary cards
if len(richness) > 0:
    cheapest  = richness.idxmin().replace("Information ","Info. ")
    priciest  = richness.idxmax().replace("Information ","Info. ")
    avg_r     = richness.mean()
    n_cheap   = (richness < 35).sum()
    n_exp     = (richness > 65).sum()
    zl,zc     = interpret_score(avg_r)

    c1,c2,c3,c4,c5 = st.columns(5)
    for col_ui, lbl, val, color, sub in [
        (c1,"Market Richness",f"{avg_r:.0f}/100",zc,zl),
        (c2,"Cheapest Sector",cheapest,"#5DCAA5","lowest score"),
        (c3,"Most Expensive",priciest,"#EF9F27","highest score"),
        (c4,"Cheap Sectors",f"{n_cheap}/12","#5DCAA5","score < 35"),
        (c5,"Exp. Sectors",f"{n_exp}/12","#E24B4A","score > 65"),
    ]:
        with col_ui:
            st.markdown(f"""<div class='mcard'>
              <div class='lbl'>{lbl}</div>
              <div class='val' style='color:{color}'>{val}</div>
              <div class='sub'>{sub}</div>
            </div>""", unsafe_allow_html=True)

st.markdown("")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN TABS
# ══════════════════════════════════════════════════════════════════════════════

tab_hm, tab_rank, tab_drill, tab_cca, tab_method = st.tabs([
    "📊  Sector Heat Map",
    "📈  Sector Ranking",
    "🔍  Sector Deep Dive",
    "🏦  CCA Screener",
    "📖  Methodology",
])


# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 · HEAT MAP
# ─────────────────────────────────────────────────────────────────────────────
with tab_hm:
    st.markdown("")
    disp_pct = pct_matrix[sel_metrics].copy() if sel_metrics else pct_matrix.copy()
    fig_hm   = draw_heatmap(disp_pct, date.today().strftime("%B %Y"))
    st.pyplot(fig_hm, use_container_width=True)

    st.markdown("")
    leg_cols = st.columns(5)
    for i,(zone,color) in enumerate(ZONE_COLORS.items()):
        with leg_cols[i]:
            st.markdown(f"<div style='text-align:center'><span class='zbadge' style='background:{color}22;color:{color};border:1px solid {color}55'>{zone}</span></div>",
                        unsafe_allow_html=True)

    st.markdown("")
    with st.expander("Show raw percentile data table"):
        styled = (disp_pct.rename(columns=METRIC_LABELS)
                          .rename(index=lambda s: s.replace("Information ","Info. "))
                          .style.background_gradient(cmap="RdYlGn_r",vmin=0,vmax=100,axis=None)
                          .format("{:.0f}", na_rep="—"))
        st.dataframe(styled, use_container_width=True)

    with st.expander("Show current sector multiples"):
        st.dataframe(sec_df.rename(columns=METRIC_LABELS)
                           .rename(index=lambda s: s.replace("Information ","Info. "))
                           .style.format("{:.2f}", na_rep="N/A"),
                     use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 · SECTOR RANKING
# ─────────────────────────────────────────────────────────────────────────────
with tab_rank:
    st.markdown("")
    st.plotly_chart(draw_ranking_chart(richness), use_container_width=True)

    st.markdown("##### Sector Score Table")
    rows = []
    for sector in richness.index:
        sc = richness[sector]; zl,zc = interpret_score(sc)
        mults = sec_df.loc[sector] if sector in sec_df.index else pd.Series()
        rows.append({
            "Sector":    sector.replace("Information ","Info. "),
            "Score":     f"{sc:.0f} / 100",
            "Zone":      zl,
            "P/E":       f"{mults.get('pe',float('nan')):.1f}x" if not pd.isna(mults.get("pe",float("nan"))) else "N/A",
            "P/BV":      f"{mults.get('pb',float('nan')):.2f}x" if not pd.isna(mults.get("pb",float("nan"))) else "N/A",
            "EV/EBITDA": f"{mults.get('ev_ebitda',float('nan')):.1f}x" if not pd.isna(mults.get("ev_ebitda",float("nan"))) else "N/A",
            "Div Yield": f"{mults.get('div_yield',float('nan')):.2f}%" if not pd.isna(mults.get("div_yield",float("nan"))) else "N/A",
        })
    df_tbl = pd.DataFrame(rows)
    st.dataframe(df_tbl.style.applymap(
        lambda v: f"color:{ZONE_COLORS.get(v,'#aaa')}" if v in ZONE_COLORS else "",
        subset=["Zone"]),
        hide_index=True, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 · SECTOR DEEP DIVE
# ─────────────────────────────────────────────────────────────────────────────
with tab_drill:
    st.markdown("")
    col_sel, col_met = st.columns([1,1])
    with col_sel:
        sel_sector = st.selectbox("Select sector", SECTOR_LIST,
                                   format_func=lambda s: s.replace("Information ","Info. "), key="drill_sec")
    with col_met:
        sel_metric = st.selectbox("Select metric", NUMERIC_COLS,
                                   format_func=lambda m: METRIC_LABELS.get(m,m), key="drill_met")

    st.markdown("")
    if sel_sector in pct_matrix.index:
        pct_row = pct_matrix.loc[sel_sector]
        sc = composite_score(pct_matrix, sel_sector)
        zl,zc = interpret_score(sc or 50)
        mults = sec_df.loc[sel_sector] if sel_sector in sec_df.index else pd.Series()

        m1,m2,m3,m4,m5 = st.columns(5)
        m1.markdown(f"<div class='mcard'><div class='lbl'>Richness Score</div><div class='val' style='color:{zc}'>{sc:.0f}</div><div class='sub'>{zl}</div></div>", unsafe_allow_html=True)
        for col_ui,(mk,ml) in zip([m2,m3,m4,m5],[("pe","P/E"),("pb","P/BV"),("ev_ebitda","EV/EBITDA"),("div_yield","Div Yield")]):
            val = mults.get(mk); pct = pct_row.get(mk)
            _,pc = interpret_score(float(pct) if pct else 50)
            disp = f"{float(val):.1f}" if (val and not pd.isna(val)) else "N/A"
            pdisp = f"{float(pct):.0f}th pct" if (pct and not pd.isna(pct)) else ""
            col_ui.markdown(f"<div class='mcard'><div class='lbl'>{ml}</div><div class='val' style='color:{pc}'>{disp}</div><div class='sub'>{pdisp}</div></div>", unsafe_allow_html=True)

    st.markdown("")
    ch1, ch2 = st.columns([2,1])
    with ch1:
        curr_v = None
        if sel_sector in sec_df.index:
            v = sec_df.loc[sel_sector, sel_metric]
            if not pd.isna(v): curr_v = float(v)
        if sel_sector in hist_dict:
            st.plotly_chart(draw_history_chart(sel_sector, sel_metric, hist_dict[sel_sector], curr_v, years),
                            use_container_width=True)
    with ch2:
        if sel_sector in pct_matrix.index:
            st.markdown("<div style='padding-top:8px'></div>", unsafe_allow_html=True)
            st.plotly_chart(draw_spider(pct_matrix.loc[sel_sector], sel_sector), use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 · CCA SCREENER
# ─────────────────────────────────────────────────────────────────────────────
with tab_cca:
    st.markdown("")

    st.markdown("""
    <div style='background:#111316;border:1px solid #1e2228;border-radius:8px;padding:12px 16px;margin-bottom:16px;font-size:12px;color:#666'>
      Select any NSE 500 company → the engine auto-identifies comparable peers in the same sector →
      computes P/E, Fwd P/E, EV/EBITDA, EV/Sales, P/BV, Dividend Yield →
      shows where your company trades vs peers (premium or discount)
    </div>
    """, unsafe_allow_html=True)

    # Company selector
    search_col, _ = st.columns([2,2])
    with search_col:
        sel_ticker = st.selectbox(
            "Select company",
            options=list(TICKER_NAMES.keys()),
            format_func=lambda t: TICKER_NAMES.get(t, t),
            index=0,
        )

    st.markdown("")

    if sel_ticker:
        target_info = ALL_TICKERS.get(sel_ticker, {})
        target_name = target_info.get("name", sel_ticker)
        target_sec  = target_info.get("sector", "Unknown")
        target_cap  = target_info.get("cap_tier", "mid")

        # Fetch peers
        with st.spinner(f"Finding peers for {target_name}…"):
            peers_df = find_peers(sel_ticker, raw_df, n_peers=n_peers, strict_sector=strict_sector)

        if peers_df.empty:
            st.warning("Could not load data for this company. Try refreshing.")
        else:
            peers_clean = clean_comps(peers_df)
            comps_tbl   = build_comps_table(peers_clean)
            pd_tbl      = build_premium_discount_table(comps_tbl)
            ff_data     = football_field_data(comps_tbl)

            # Target row
            target_rows = peers_clean[peers_clean["ticker"] == sel_ticker]
            target_row  = target_rows.iloc[0] if not target_rows.empty else pd.Series()

            # ── Company header ────────────────────────────────────────────────
            price    = target_row.get("price")
            mktcap   = target_row.get("mktcap")
            high52   = target_row.get("52w_high")
            low52    = target_row.get("52w_low")
            rec      = str(target_row.get("recommend","")).upper()
            rec_color = "#5DCAA5" if "BUY" in rec else ("#E24B4A" if "SELL" in rec else "#EF9F27")

            price_str   = f"₹{float(price):,.1f}"  if price   else "N/A"
            mktcap_str  = f"₹{float(mktcap)/1e7:,.0f} Cr" if mktcap else "N/A"
            h52_str     = f"₹{float(high52):,.1f}" if high52  else "N/A"
            l52_str     = f"₹{float(low52):,.1f}"  if low52   else "N/A"

            st.markdown(f"""
            <div class='comp-header'>
              <div style='display:flex;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;gap:8px'>
                <div>
                  <h2>{target_name}</h2>
                  <div class='meta'>{sel_ticker.replace('.NS','')} &nbsp;·&nbsp; {target_sec} &nbsp;·&nbsp; {target_cap.title()} cap</div>
                </div>
                <div style='text-align:right'>
                  <div style='font-size:22px;font-weight:500;color:white'>{price_str}</div>
                  <div style='font-size:11px;color:#555'>{mktcap_str} mkt cap</div>
                </div>
              </div>
              <div style='display:flex;gap:16px;margin-top:12px;flex-wrap:wrap'>
                <span style='font-size:12px;color:#666'>52W High: <b style="color:#aaa">{h52_str}</b></span>
                <span style='font-size:12px;color:#666'>52W Low: <b style="color:#aaa">{l52_str}</b></span>
                <span style='font-size:12px;color:#666'>Analyst: <b style="color:{rec_color}">{rec or "N/A"}</b></span>
                <span style='font-size:12px;color:#666'>Peers found: <b style="color:#aaa">{len(peers_df)-1}</b></span>
              </div>
            </div>
            """, unsafe_allow_html=True)

            # ── Key metrics row ───────────────────────────────────────────────
            st.markdown("##### Current Multiples vs Peer Median")
            metric_cols = st.columns(6)
            for i, (m, cfg) in enumerate(CCA_METRICS.items()):
                with metric_cols[i]:
                    tv = target_row.get(m)
                    peer_vals = pd.to_numeric(
                        peers_clean[peers_clean["ticker"]!=sel_ticker].get(m, pd.Series()),
                        errors="coerce"
                    ).dropna()
                    pm = float(peer_vals.median()) if not peer_vals.empty else None
                    tv_f = float(tv) if (tv and not (isinstance(tv,float) and np.isnan(tv))) else None
                    prem = None
                    if tv_f and pm:
                        prem = (tv_f/pm-1)*100
                        if not cfg["higher_is_expensive"]: prem = -prem
                    color = "#E24B4A" if (prem and prem>10) else ("#5DCAA5" if (prem and prem<-10) else "#aaa")
                    tv_disp = f"{tv_f:.1f}{cfg['suffix']}" if tv_f else "N/A"
                    pm_disp = f"Peer: {pm:.1f}{cfg['suffix']}" if pm else ""
                    pr_disp = f"{prem:+.1f}%" if prem else ""
                    st.markdown(f"""<div class='mcard'>
                      <div class='lbl'>{cfg['label']}</div>
                      <div class='val' style='color:{color};font-size:18px'>{tv_disp}</div>
                      <div class='sub'>{pm_disp}</div>
                      <div style='font-size:11px;color:{color};font-weight:500'>{pr_disp}</div>
                    </div>""", unsafe_allow_html=True)

            st.markdown("")

            # ── Full comps table ──────────────────────────────────────────────
            st.markdown("##### Trading Comparables Table")
            st.markdown("<div style='font-size:11px;color:#444;margin-bottom:8px'>First row (gold border) = selected company · Remaining rows = peer set</div>", unsafe_allow_html=True)

            display_df = vis_style(comps_tbl, sel_ticker)
            keep_cols  = [c for c in display_df.columns if not c.startswith("_")]
            st.markdown(display_df[keep_cols].to_html(index=False, escape=False,
                        classes="comps-table"), unsafe_allow_html=True)

            st.markdown("")

            # ── Summary stats row ──────────────────────────────────────────────
            with st.expander("Show peer summary statistics (mean, median, min, max, quartiles)"):
                from src.comps import peer_summary_stats
                stats_df = peer_summary_stats(comps_tbl)
                if not stats_df.empty and "label" in stats_df.columns:
                    fmt_cols = ["mean","median","min","max","p25","p75"]
                    avail_fmt = [c for c in fmt_cols if c in stats_df.columns]
                    st.dataframe(
                        stats_df[["label","count"]+avail_fmt]
                        .rename(columns={"label":"Metric","count":"N","mean":"Mean",
                                         "median":"Median","min":"Min","max":"Max",
                                         "p25":"25th Pct","p75":"75th Pct"})
                        .style.format({c:"{:.1f}" for c in avail_fmt}, na_rep="N/A"),
                        hide_index=True, use_container_width=True,
                    )
                else:
                    st.info("Summary statistics not available for this selection.")

            st.markdown("")

            # ── Charts row ────────────────────────────────────────────────────
            ch_a, ch_b = st.columns([1,1])

            with ch_a:
                st.markdown("##### Football Field — Peer Range vs Target")
                if ff_data:
                    st.plotly_chart(draw_football_field(ff_data, target_name),
                                    use_container_width=True)
                else:
                    st.info("Insufficient data for football field chart.")

            with ch_b:
                st.markdown("##### Premium / Discount vs Peer Median")
                if not pd_tbl.empty:
                    st.plotly_chart(draw_premium_discount(pd_tbl, target_name),
                                    use_container_width=True)

            st.markdown("")

            # ── Premium discount table ─────────────────────────────────────────
            st.markdown("##### Detailed Premium / Discount Analysis")
            if not pd_tbl.empty:
                show_cols = ["Metric","Target","Peer Median","Peer Mean","Premium / Disc %","Pct in Peers","Implied Price"]
                available = [c for c in show_cols if c in pd_tbl.columns]
                def color_pd(v):
                    try:
                        fv = float(str(v).replace("%",""))
                        if fv > 15: return "color:#E24B4A"
                        if fv < -15: return "color:#5DCAA5"
                        return "color:#aaa"
                    except: return ""
                st.dataframe(
                    pd_tbl[available].style.applymap(color_pd, subset=["Premium / Disc %"]),
                    hide_index=True, use_container_width=True,
                )

            st.markdown("")

            # ── Price chart ───────────────────────────────────────────────────
            st.markdown("##### 1-Year Price Chart")
            with st.spinner("Loading price history…"):
                price_hist = fetch_price_history(sel_ticker, "1y")
            if not price_hist.empty:
                st.plotly_chart(draw_price_chart(price_hist, sel_ticker, target_name),
                                use_container_width=True)

            # ── Fundamentals ─────────────────────────────────────────────────
            with st.expander("Show fundamental data"):
                fund_items = [
                    ("Revenue","revenue"),("EBITDA","ebitda"),("Net Income","net_income"),
                    ("Total Debt","total_debt"),("Cash","cash"),
                    ("ROE","roe"),("Operating Margin","operating_margin"),
                    ("Net Margin","net_margin"),("Revenue Growth","revenue_growth"),
                    ("Beta","beta"),
                ]
                fund_rows = []
                for label, key in fund_items:
                    val = target_row.get(key)
                    if val and not (isinstance(val,float) and np.isnan(val)):
                        if key in ["revenue","ebitda","net_income","total_debt","cash"]:
                            disp = f"₹{float(val)/1e7:,.0f} Cr"
                        elif key in ["roe","operating_margin","net_margin","revenue_growth"]:
                            disp = f"{float(val)*100:.1f}%"
                        else:
                            disp = f"{float(val):.2f}"
                        fund_rows.append({"Metric":label,"Value":disp})
                if fund_rows:
                    st.dataframe(pd.DataFrame(fund_rows), hide_index=True, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 5 · METHODOLOGY
# ─────────────────────────────────────────────────────────────────────────────
with tab_method:
    st.markdown("""
## NSE Valuation Suite — Methodology

### Module 1 · Sector Heat Map
Tracks P/E, P/BV, EV/EBITDA, and Dividend Yield for 12 NSE sectors. Each cell shows a **historical percentile rank** — where today's multiple sits within its own 10-year distribution.

```python
from scipy import stats
percentile = stats.percentileofscore(historical_10yr_array, today_value)
# 0 = cheapest ever  ·  50 = fair value  ·  100 = most expensive ever
```

Dividend Yield is inverted (higher yield = cheaper).

A **Composite Richness Score** (0–100) combines all four metrics using sector-specific weights.

---

### Module 2 · Comparable Company Analysis (CCA) Screener
For any selected NSE 500 company:
1. **Peer selection** — same sector + adjacent market cap tier (large/mid/small)
2. **Multiples computed** — P/E, Forward P/E, EV/EBITDA, EV/Sales, P/BV, Dividend Yield
3. **Trading comps table** — formatted like an IB pitch book
4. **Premium / Discount** — where target trades vs peer median for each multiple
5. **Football field chart** — visual range of peer multiples with target overlay
6. **Implied price** — if target re-rated to peer median, what would the price be?

---

### Data Sources
| Source | Data |
|---|---|
| Yahoo Finance (yfinance) | Current multiples, price, fundamentals |
| NSE India (synthetic fallback) | 10-year historical sector P/E, P/BV, Div Yield |
| NSE 500 universe | 180+ companies across 12 sectors |

---

### Key Design Choices
| Choice | Reason |
|---|---|
| Median not mean for aggregation | Outlier-robust — one 200x P/E company doesn't distort sector |
| Percentile not raw multiples | Context-aware — 20x IT P/E means different things in 2016 vs 2024 |
| Sector-specific weights | Banks: P/BV dominates; Metals: EV/EBITDA dominates |
| Cap tier adjacency for peers | Micro-cap vs mega-cap comparison is meaningless |
    """)

st.divider()
st.markdown(f"<div style='text-align:center;font-size:11px;color:#333;padding:8px'>NSE Valuation Suite · Heat Map + CCA Screener · {date.today().strftime('%d %b %Y')}</div>",
            unsafe_allow_html=True)
