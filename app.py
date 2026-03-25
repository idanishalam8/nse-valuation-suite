# ─────────────────────────────────────────────────────────────────────────────
# app.py  ·  NSE Valuation Suite — Bloomberg Terminal Style
# ─────────────────────────────────────────────────────────────────────────────

import warnings, time
import numpy as np
import pandas as pd
import streamlit as st
from datetime import date, datetime

warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="NSE VALUATION TERMINAL",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;500;600&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

html,body,.stApp{background-color:#000000 !important;color:#ffffff;font-family:'IBM Plex Mono','Courier New',monospace !important;}
[data-testid="stSidebar"]{background:#0a0a0a !important;border-right:1px solid #ff6600 !important;}
[data-testid="stSidebar"] *{color:#cccccc !important;font-family:'IBM Plex Mono',monospace !important;}
[data-testid="stSidebar"] .stSelectbox label,[data-testid="stSidebar"] .stSlider label,[data-testid="stSidebar"] .stMultiselect label{color:#ff6600 !important;font-size:10px !important;letter-spacing:.1em !important;text-transform:uppercase !important;}

.stTabs [data-baseweb="tab-list"]{background:#000000 !important;border-bottom:1px solid #ff6600 !important;gap:0 !important;}
.stTabs [data-baseweb="tab"]{color:#666666 !important;font-family:'IBM Plex Mono',monospace !important;font-size:11px !important;font-weight:500 !important;letter-spacing:.08em !important;text-transform:uppercase !important;padding:8px 20px !important;border:1px solid transparent !important;background:transparent !important;}
.stTabs [aria-selected="true"]{color:#000000 !important;background:#ff6600 !important;border-color:#ff6600 !important;}
.stTabs [data-baseweb="tab"]:hover{color:#ff6600 !important;}

.stButton button{background:#ff6600 !important;color:#000000 !important;font-family:'IBM Plex Mono',monospace !important;font-weight:600 !important;font-size:11px !important;letter-spacing:.1em !important;text-transform:uppercase !important;border:none !important;border-radius:0 !important;}
.stButton button:hover{background:#cc5200 !important;}

.stSelectbox>div>div,.stMultiselect>div>div{background:#0a0a0a !important;border:1px solid #333333 !important;border-radius:0 !important;color:#ffffff !important;font-family:'IBM Plex Mono',monospace !important;}
.stSelectbox label,.stMultiselect label{color:#ff6600 !important;font-size:10px !important;letter-spacing:.1em !important;text-transform:uppercase !important;font-family:'IBM Plex Mono',monospace !important;}
.stSlider label{color:#ff6600 !important;font-size:10px !important;letter-spacing:.1em !important;text-transform:uppercase !important;}
.stCheckbox label{color:#cccccc !important;font-size:11px !important;}

h1,h2,h3,h4{font-family:'IBM Plex Mono',monospace !important;color:#ffffff !important;font-weight:500 !important;letter-spacing:.05em !important;}

.bb-card{background:#0a0a0a;border:1px solid #1a1a1a;border-top:2px solid #ff6600;padding:10px 12px;font-family:'IBM Plex Mono',monospace;}
.bb-card .lbl{font-size:9px;color:#ff6600;text-transform:uppercase;letter-spacing:.15em;margin-bottom:4px;}
.bb-card .val{font-size:20px;font-weight:600;letter-spacing:.02em;line-height:1.1;}
.bb-card .sub{font-size:10px;color:#555555;margin-top:3px;letter-spacing:.05em;text-transform:uppercase;}

.bb-header{background:#ff6600;color:#000000;padding:6px 16px;font-family:'IBM Plex Mono',monospace;font-size:11px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;display:flex;justify-content:space-between;align-items:center;margin-bottom:0;}
.bb-section{font-family:'IBM Plex Mono',monospace;font-size:10px;color:#ff6600;text-transform:uppercase;letter-spacing:.15em;border-bottom:1px solid #ff6600;padding-bottom:4px;margin:16px 0 10px;}
.bb-ticker{background:#ff6600;color:#000000;font-family:'IBM Plex Mono',monospace;font-size:10px;font-weight:600;padding:4px 0;letter-spacing:.05em;white-space:nowrap;overflow:hidden;margin-bottom:12px;}
.bb-co-header{background:#0a0a0a;border:1px solid #1a1a1a;border-left:3px solid #ff6600;padding:12px 16px;margin-bottom:12px;font-family:'IBM Plex Mono',monospace;}
.bb-co-name{font-size:16px;font-weight:600;color:#ffffff;letter-spacing:.05em;}
.bb-co-meta{font-size:10px;color:#555555;letter-spacing:.08em;text-transform:uppercase;margin-top:3px;}
.bb-co-price{font-size:22px;font-weight:600;color:#ffffff;text-align:right;}
.bb-co-mktcap{font-size:10px;color:#555555;text-align:right;letter-spacing:.05em;}
.bb-mini{background:#0a0a0a;border:1px solid #1a1a1a;padding:8px 10px;font-family:'IBM Plex Mono',monospace;text-align:center;}
.bb-mini .mlbl{font-size:9px;color:#555;text-transform:uppercase;letter-spacing:.1em;margin-bottom:3px;}
.bb-mini .mval{font-size:16px;font-weight:600;}
.bb-mini .mpeer{font-size:9px;color:#444;margin-top:2px;}
.bb-mini .mchange{font-size:10px;font-weight:600;margin-top:2px;}

table{width:100%;border-collapse:collapse;font-family:'IBM Plex Mono',monospace !important;}
th{background:#111111 !important;color:#ff6600 !important;font-size:9px !important;font-weight:500 !important;text-transform:uppercase !important;letter-spacing:.1em !important;padding:7px 10px !important;border-bottom:1px solid #ff6600 !important;font-family:'IBM Plex Mono',monospace !important;}
td{color:#cccccc !important;font-size:11px !important;padding:6px 10px !important;border-bottom:1px solid #111111 !important;font-family:'IBM Plex Mono',monospace !important;}
tr:hover td{background:#0d0d0d !important;}
tr:first-child td{color:#ffaa44 !important;font-weight:600 !important;background:#110800 !important;border-left:2px solid #ff6600 !important;}

hr{border:none;border-top:1px solid #1a1a1a;margin:12px 0;}
.stDataFrame{background:#000000 !important;}
[data-testid="stDataFrame"]{border:1px solid #1a1a1a !important;}
.streamlit-expanderHeader{background:#0a0a0a !important;color:#ff6600 !important;font-family:'IBM Plex Mono',monospace !important;font-size:10px !important;text-transform:uppercase !important;letter-spacing:.1em !important;border:1px solid #1a1a1a !important;}
::-webkit-scrollbar{width:4px;height:4px;}
::-webkit-scrollbar-track{background:#000;}
::-webkit-scrollbar-thumb{background:#ff6600;}
p,li{color:#aaaaaa;font-family:'IBM Plex Mono',monospace !important;font-size:12px !important;}
</style>
""", unsafe_allow_html=True)

from src.config import NSE500, ALL_TICKERS, CCA_METRICS, LOOKBACK_OPTIONS, NUMERIC_COLS, ZONE_COLORS
from src.fetch import fetch_all_sectors, fetch_all_historical, fetch_price_history, clear_cache
from src.comps import (aggregate_sector_multiples, find_peers, clean_comps,
                       build_comps_table, build_premium_discount_table, football_field_data)
from src.percentile import (build_percentile_matrix, build_zscore_matrix,
                             build_richness_series, composite_score, interpret_score)
from src.visuals import (draw_heatmap, draw_ranking_chart, draw_history_chart,
                         draw_spider, draw_football_field, draw_premium_discount,
                         draw_price_chart, style_comps_table as vis_style, METRIC_LABELS)

SECTOR_LIST  = list(NSE500.keys())
TICKER_NAMES = {t: f"{d['name']}  [{t.replace('.NS','')}]" for t,d in ALL_TICKERS.items()}


@st.cache_data(ttl=14400, show_spinner=False)
def load_all_data(years):
    raw    = fetch_all_sectors()
    hist   = fetch_all_historical(years)
    sec_df = aggregate_sector_multiples(raw)
    pct    = build_percentile_matrix(sec_df, hist)
    rich   = build_richness_series(pct)
    return raw, hist, sec_df, pct, rich


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='background:#ff6600;color:#000;padding:8px 12px;font-family:IBM Plex Mono,monospace;
                font-size:13px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;margin-bottom:12px'>
      NSE TERMINAL
    </div>
    <div style='font-family:IBM Plex Mono,monospace;font-size:10px;color:#555;
                letter-spacing:.08em;text-transform:uppercase;padding:0 4px;margin-bottom:12px'>
      Valuation Intelligence Suite<br>
      <span style='color:#ff6600'>◆</span> NSE 500 &nbsp;·&nbsp; 12 SECTORS
    </div>
    """, unsafe_allow_html=True)

    lookback_label = st.selectbox("LOOKBACK PERIOD", list(LOOKBACK_OPTIONS.keys()), index=2)
    years = LOOKBACK_OPTIONS[lookback_label]

    st.markdown("")
    sel_metrics = st.multiselect("HEAT MAP METRICS", NUMERIC_COLS, default=NUMERIC_COLS,
                                  format_func=lambda m: METRIC_LABELS.get(m,m))
    if not sel_metrics: sel_metrics = NUMERIC_COLS

    st.markdown("")
    st.markdown("<div style='font-family:IBM Plex Mono,monospace;font-size:9px;color:#ff6600;letter-spacing:.15em;text-transform:uppercase;margin-bottom:6px'>CCA PARAMETERS</div>", unsafe_allow_html=True)
    n_peers       = st.slider("PEER COUNT", 4, 12, 8)
    strict_sector = st.checkbox("STRICT SECTOR MATCH", value=True)

    st.markdown("<div style='border-top:1px solid #1a1a1a;margin:12px 0'></div>", unsafe_allow_html=True)
    if st.button("⟳  REFRESH DATA", use_container_width=True):
        clear_cache(); st.cache_data.clear()
        st.success("CACHE CLEARED"); time.sleep(1); st.rerun()

    now = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
    <div style='font-family:IBM Plex Mono,monospace;font-size:9px;color:#333;text-transform:uppercase;
                letter-spacing:.08em;margin-top:16px;border-top:1px solid #111;padding-top:10px'>
      DATA: NSE INDIA · YAHOO FINANCE<br>
      DATE: {date.today().strftime('%d %b %Y').upper()}<br>
      TIME: {now} IST<br>
      <span style='color:#ff6600'>STATUS: ● LIVE</span>
    </div>""", unsafe_allow_html=True)


# ── LOAD DATA ─────────────────────────────────────────────────────────────────
with st.spinner("LOADING MARKET DATA..."):
    raw_df, hist_dict, sec_df, pct_matrix, richness = load_all_data(years)


# ── TERMINAL HEADER ───────────────────────────────────────────────────────────
st.markdown(f"""
<div class='bb-header'>
  <span>◆ NSE VALUATION TERMINAL &nbsp;·&nbsp; SECTOR HEAT MAP + COMPARABLE ANALYSIS</span>
  <span>{date.today().strftime('%d %b %Y').upper()} &nbsp;·&nbsp; NSE 500 &nbsp;·&nbsp; 12 SECTORS</span>
</div>""", unsafe_allow_html=True)

# Ticker strip
if len(richness) > 0:
    items = []
    for s in richness.index:
        sc = richness[s]
        short = (s.replace("Information Technology","IT").replace("Capital Goods & Infra","INFRA")
                  .replace("Metals & Mining","METALS").replace("Energy & Oil Gas","ENERGY")
                  .replace("Financial Services","FIN SVCS").replace("Consumer Durables","CONS DUR")
                  .replace("Pharmaceuticals","PHARMA"))
        c = "#00cc44" if sc < 35 else ("#ff3333" if sc > 65 else "#ffaa00")
        items.append(f'<span style="color:{c};margin:0 14px">{short}: {int(sc) if sc is not None and sc == sc else 0}</span>')
    st.markdown(f"""
    <div class='bb-ticker'>
      &nbsp;&nbsp;◆&nbsp;&nbsp;{'  ◆  '.join(items)}&nbsp;&nbsp;◆&nbsp;&nbsp;
      MKT RICHNESS: {richness.mean():.0f}/100
    </div>""", unsafe_allow_html=True)

# Summary cards
if len(richness) > 0:
    avg_r = richness.mean(); zl,zc = interpret_score(avg_r)
    cheapest = richness.idxmin(); priciest = richness.idxmax()
    n_cheap = (richness < 35).sum(); n_exp = (richness > 65).sum()

    c1,c2,c3,c4,c5 = st.columns(5)
    for col_ui,lbl,val,suf,color,sub in [
        (c1,"MARKET RICHNESS",f"{avg_r:.0f}","/100",zc,zl.upper()),
        (c2,"CHEAPEST SECTOR",cheapest.replace("Information Technology","Info Tech").replace("Capital Goods & Infra","Cap Goods"),"","#00cc44","LOWEST SCORE"),
        (c3,"MOST EXPENSIVE",priciest.replace("Information Technology","Info Tech"),"","#ff3333","HIGHEST SCORE"),
        (c4,"CHEAP SECTORS",str(n_cheap),"/12","#00cc44","SCORE < 35"),
        (c5,"EXPENSIVE SECTORS",str(n_exp),"/12","#ff3333","SCORE > 65"),
    ]:
        with col_ui:
            st.markdown(f"""
            <div class='bb-card'>
              <div class='lbl'>{lbl}</div>
              <div class='val' style='color:{color}'>{val}<span style='font-size:12px;color:#444'>{suf}</span></div>
              <div class='sub'>{sub}</div>
            </div>""", unsafe_allow_html=True)

st.markdown("<div style='margin:8px 0'></div>", unsafe_allow_html=True)


# ── TABS ──────────────────────────────────────────────────────────────────────
tab_hm, tab_rank, tab_drill, tab_cca, tab_method = st.tabs([
    "SECTOR HEAT MAP", "SECTOR RANKING", "SECTOR DEEP DIVE", "CCA SCREENER", "METHODOLOGY"
])


# ── TAB 1: HEAT MAP ───────────────────────────────────────────────────────────
with tab_hm:
    st.markdown("<div class='bb-section'>VALUATION PERCENTILE MATRIX  ·  0=CHEAPEST  ·  100=MOST EXPENSIVE</div>", unsafe_allow_html=True)
    disp_pct = pct_matrix[sel_metrics].copy() if sel_metrics else pct_matrix.copy()
    st.pyplot(draw_heatmap(disp_pct, date.today().strftime("%d %b %Y").upper()), use_container_width=True)

    st.markdown("")
    leg_cols = st.columns(5)
    for lc,(zone,rng,color) in zip(leg_cols,[("VERY CHEAP","0–20","#00cc44"),("CHEAP","20–35","#44ff88"),
                                             ("FAIR VALUE","35–65","#888888"),("EXPENSIVE","65–80","#ffaa00"),
                                             ("VERY EXP.","80–100","#ff3333")]):
        with lc:
            st.markdown(f"""<div style='text-align:center;background:#0a0a0a;border-top:2px solid {color};
                padding:5px;font-family:IBM Plex Mono,monospace'>
              <div style='font-size:9px;color:{color};font-weight:600;letter-spacing:.1em'>{zone}</div>
              <div style='font-size:9px;color:#444'>{rng}</div>
            </div>""", unsafe_allow_html=True)

    with st.expander("RAW PERCENTILE DATA"):
        st.dataframe((disp_pct.rename(columns=METRIC_LABELS)
                              .rename(index=lambda s: s.upper())
                              .style.background_gradient(cmap="RdYlGn_r",vmin=0,vmax=100,axis=None)
                              .format("{:.0f}", na_rep="—")), use_container_width=True)
    with st.expander("CURRENT SECTOR MULTIPLES"):
        st.dataframe(sec_df.rename(columns=METRIC_LABELS).rename(index=lambda s: s.upper())
                           .style.format("{:.2f}", na_rep="N/A"), use_container_width=True)


# ── TAB 2: SECTOR RANKING ─────────────────────────────────────────────────────
with tab_rank:
    st.markdown("<div class='bb-section'>SECTOR RICHNESS RANKING  ·  COMPOSITE SCORE</div>", unsafe_allow_html=True)
    st.plotly_chart(draw_ranking_chart(richness), use_container_width=True)

    st.markdown("<div class='bb-section'>SECTOR SCORECARD</div>", unsafe_allow_html=True)
    rows = []
    for sector in richness.index:
        sc = richness[sector]; zl,_ = interpret_score(sc)
        mults = sec_df.loc[sector] if sector in sec_df.index else pd.Series()
        rows.append({
            "SECTOR": sector.upper(), "SCORE": f"{int(sc) if sc is not None and sc == sc else 0}/100", "ZONE": zl.upper(),
            "P/E":   f"{mults.get('pe',float('nan')):.1f}x" if not pd.isna(mults.get("pe",float("nan"))) else "N/A",
            "P/BV":  f"{mults.get('pb',float('nan')):.2f}x" if not pd.isna(mults.get("pb",float("nan"))) else "N/A",
            "EV/EBITDA": f"{mults.get('ev_ebitda',float('nan')):.1f}x" if not pd.isna(mults.get("ev_ebitda",float("nan"))) else "N/A",
            "DIV YLD":   f"{mults.get('div_yield',float('nan')):.2f}%" if not pd.isna(mults.get("div_yield",float("nan"))) else "N/A",
        })
    st.dataframe(pd.DataFrame(rows).style.applymap(
        lambda v: "color:#00cc44;font-weight:600" if "CHEAP" in str(v) else
                  ("color:#ff3333;font-weight:600" if "EXP" in str(v) else ""),
        subset=["ZONE"]), hide_index=True, use_container_width=True)


# ── TAB 3: SECTOR DEEP DIVE ───────────────────────────────────────────────────
with tab_drill:
    st.markdown("<div class='bb-section'>SECTOR ANALYSIS  ·  HISTORICAL CONTEXT</div>", unsafe_allow_html=True)
    col_sel, col_met = st.columns([1,1])
    with col_sel:
        sel_sector = st.selectbox("SELECT SECTOR", SECTOR_LIST, format_func=lambda s: s.upper(), key="drill_sec")
    with col_met:
        sel_metric = st.selectbox("SELECT METRIC", NUMERIC_COLS, format_func=lambda m: METRIC_LABELS.get(m,m), key="drill_met")

    if sel_sector in pct_matrix.index:
        pct_row = pct_matrix.loc[sel_sector]
        sc = composite_score(pct_matrix, sel_sector); zl,zc = interpret_score(sc or 50)
        mults = sec_df.loc[sel_sector] if sel_sector in sec_df.index else pd.Series()

        st.markdown(f"""
        <div style='background:#0a0a0a;border-left:3px solid #ff6600;padding:10px 14px;margin:10px 0;
                    font-family:IBM Plex Mono,monospace;display:flex;justify-content:space-between;align-items:center'>
          <span style='font-size:14px;font-weight:600;color:#fff;letter-spacing:.08em'>{sel_sector.upper()}</span>
          <span>
            <span style='font-size:10px;color:{zc};font-weight:600;letter-spacing:.1em'>◆ {zl.upper()}</span>
            <span style='font-size:20px;font-weight:600;color:{zc};margin-left:12px'>{int(sc) if sc is not None and sc == sc else 0}</span>
            <span style='font-size:10px;color:#444'>/100</span>
          </span>
        </div>""", unsafe_allow_html=True)

        m1,m2,m3,m4 = st.columns(4)
        for col_ui,(mk,ml) in zip([m1,m2,m3,m4],[("pe","P/E"),("pb","P/BV"),("ev_ebitda","EV/EBITDA"),("div_yield","DIV YIELD")]):
            val = mults.get(mk); pct = pct_row.get(mk)
            _,pc = interpret_score(float(pct) if pct and not pd.isna(pct) else 50)
            col_ui.markdown(f"""
            <div class='bb-card'>
              <div class='lbl'>{ml}</div>
              <div class='val' style='color:{pc}'>{f"{float(val):.1f}" if (val and not pd.isna(val)) else "N/A"}</div>
              <div class='sub' style='color:{pc}'>{f"{float(pct):.0f}TH PCT" if (pct and not pd.isna(pct)) else "N/A"}</div>
            </div>""", unsafe_allow_html=True)

    ch1, ch2 = st.columns([2,1])
    with ch1:
        curr_v = None
        if sel_sector in sec_df.index:
            v = sec_df.loc[sel_sector, sel_metric]
            if not pd.isna(v): curr_v = float(v)
        if sel_sector in hist_dict:
            st.plotly_chart(draw_history_chart(sel_sector, sel_metric, hist_dict[sel_sector], curr_v, years), use_container_width=True)
    with ch2:
        if sel_sector in pct_matrix.index:
            st.plotly_chart(draw_spider(pct_matrix.loc[sel_sector], sel_sector), use_container_width=True)


# ── TAB 4: CCA SCREENER ───────────────────────────────────────────────────────
with tab_cca:
    st.markdown("<div class='bb-section'>COMPARABLE COMPANY ANALYSIS  ·  NSE 500  ·  TRADING MULTIPLES</div>", unsafe_allow_html=True)
    st.markdown("""<div style='background:#0a0800;border:1px solid #2a1800;border-left:3px solid #ff6600;
                padding:8px 12px;margin-bottom:12px;font-family:IBM Plex Mono,monospace;font-size:10px;
                color:#666;letter-spacing:.05em'>
    SELECT TARGET → AUTO-IDENTIFY PEERS → COMPUTE 6 TRADING MULTIPLES → PREMIUM/DISCOUNT VS PEER MEDIAN
    </div>""", unsafe_allow_html=True)

    search_col, _ = st.columns([2,2])
    with search_col:
        sel_ticker = st.selectbox("SELECT COMPANY", options=list(TICKER_NAMES.keys()),
                                   format_func=lambda t: TICKER_NAMES.get(t,t), index=0)

    if sel_ticker:
        target_info = ALL_TICKERS.get(sel_ticker, {})
        target_name = target_info.get("name", sel_ticker)
        target_sec  = target_info.get("sector","Unknown")
        target_cap  = target_info.get("cap_tier","mid")

        with st.spinner(f"COMPUTING COMPS FOR {target_name.upper()}..."):
            peers_df = find_peers(sel_ticker, raw_df, n_peers=n_peers, strict_sector=strict_sector)

        if peers_df.empty:
            st.warning("NO DATA AVAILABLE. TRY REFRESHING.")
        else:
            peers_clean = clean_comps(peers_df)
            comps_tbl   = build_comps_table(peers_clean)
            pd_tbl      = build_premium_discount_table(comps_tbl)
            ff_data     = football_field_data(comps_tbl)
            target_rows = peers_clean[peers_clean["ticker"] == sel_ticker]
            target_row  = target_rows.iloc[0] if not target_rows.empty else pd.Series()

            price  = target_row.get("price"); mktcap = target_row.get("mktcap")
            high52 = target_row.get("52w_high"); low52 = target_row.get("52w_low")
            rec    = str(target_row.get("recommend","")).upper(); beta = target_row.get("beta")
            rec_c  = "#00cc44" if "BUY" in rec else ("#ff3333" if "SELL" in rec else "#ffaa00")

            st.markdown(f"""
            <div class='bb-co-header'>
              <div style='display:flex;justify-content:space-between;align-items:flex-start'>
                <div>
                  <div class='bb-co-name'>{target_name.upper()}</div>
                  <div class='bb-co-meta'>{sel_ticker.replace('.NS','')} | {target_sec.upper()} | {target_cap.upper()} CAP | PEERS: {len(peers_df)-1}</div>
                </div>
                <div style='text-align:right'>
                  <div class='bb-co-price'>{"₹"+f"{float(price):,.1f}" if price else "N/A"}</div>
                  <div class='bb-co-mktcap'>{"₹"+f"{float(mktcap)/1e7:,.0f} CR MKT CAP" if mktcap else ""}</div>
                </div>
              </div>
              <div style='display:flex;gap:24px;margin-top:10px;border-top:1px solid #1a1a1a;
                          padding-top:8px;font-family:IBM Plex Mono,monospace;font-size:10px'>
                <span style='color:#555'>52W HIGH: <b style="color:#ccc">{"₹"+f"{float(high52):,.1f}" if high52 else "N/A"}</b></span>
                <span style='color:#555'>52W LOW: <b style="color:#ccc">{"₹"+f"{float(low52):,.1f}" if low52 else "N/A"}</b></span>
                <span style='color:#555'>BETA: <b style="color:#ccc">{f"{float(beta):.2f}" if beta else "N/A"}</b></span>
                <span style='color:#555'>ANALYST: <b style="color:{rec_c}">{rec or "N/A"}</b></span>
              </div>
            </div>""", unsafe_allow_html=True)

            st.markdown("<div class='bb-section'>CURRENT MULTIPLES VS PEER MEDIAN</div>", unsafe_allow_html=True)
            metric_cols = st.columns(6)
            for i,(m,cfg) in enumerate(CCA_METRICS.items()):
                with metric_cols[i]:
                    tv = target_row.get(m)
                    peer_vals = pd.to_numeric(peers_clean[peers_clean["ticker"]!=sel_ticker].get(m,pd.Series()), errors="coerce").dropna()
                    pm  = float(peer_vals.median()) if not peer_vals.empty else None
                    tv_f = float(tv) if (tv and not (isinstance(tv,float) and np.isnan(tv))) else None
                    prem = None
                    if tv_f and pm:
                        prem = (tv_f/pm-1)*100
                        if not cfg["higher_is_expensive"]: prem = -prem
                    color = "#ff3333" if (prem and prem>10) else ("#00cc44" if (prem and prem<-10) else "#888888")
                    st.markdown(f"""
                    <div class='bb-mini'>
                      <div class='mlbl'>{cfg['label']}</div>
                      <div class='mval' style='color:{color}'>{f"{tv_f:.1f}{cfg['suffix']}" if tv_f else "N/A"}</div>
                      <div class='mpeer'>{f"PEER: {pm:.1f}{cfg['suffix']}" if pm else "N/A"}</div>
                      <div class='mchange' style='color:{color}'>{f"{prem:+.1f}%" if prem else "—"}</div>
                    </div>""", unsafe_allow_html=True)

            st.markdown("")
            st.markdown("<div class='bb-section'>TRADING COMPARABLES TABLE</div>", unsafe_allow_html=True)
            st.markdown("<div style='font-family:IBM Plex Mono,monospace;font-size:9px;color:#444;margin-bottom:6px;letter-spacing:.08em'>▶ FIRST ROW = TARGET  ·  SUBSEQUENT ROWS = PEER SET</div>", unsafe_allow_html=True)
            display_df = vis_style(comps_tbl, sel_ticker)
            keep_cols  = [c for c in display_df.columns if not c.startswith("_")]
            st.markdown(display_df[keep_cols].to_html(index=False, escape=False), unsafe_allow_html=True)

            st.markdown("")
            ch_a, ch_b = st.columns([1,1])
            with ch_a:
                st.markdown("<div class='bb-section'>FOOTBALL FIELD  ·  PEER RANGE</div>", unsafe_allow_html=True)
                if ff_data:
                    st.plotly_chart(draw_football_field(ff_data, target_name), use_container_width=True)
            with ch_b:
                st.markdown("<div class='bb-section'>PREMIUM / DISCOUNT</div>", unsafe_allow_html=True)
                if not pd_tbl.empty:
                    st.plotly_chart(draw_premium_discount(pd_tbl, target_name), use_container_width=True)

            st.markdown("")
            st.markdown("<div class='bb-section'>PREMIUM / DISCOUNT ANALYSIS</div>", unsafe_allow_html=True)
            if not pd_tbl.empty:
                show_cols = ["Metric","Target","Peer Median","Peer Mean","Premium / Disc %","Pct in Peers","Implied Price"]
                available = [c for c in show_cols if c in pd_tbl.columns]
                def cpd(v):
                    try:
                        fv = float(str(v).replace("%",""))
                        if fv > 15: return "color:#ff3333;font-weight:600"
                        if fv < -15: return "color:#00cc44;font-weight:600"
                        return "color:#888888"
                    except: return ""
                st.dataframe(pd_tbl[available].style.applymap(cpd),
                             hide_index=True, use_container_width=True)

            st.markdown("")
            st.markdown("<div class='bb-section'>1-YEAR PRICE CHART</div>", unsafe_allow_html=True)
            with st.spinner("LOADING PRICE DATA..."):
                price_hist = fetch_price_history(sel_ticker, "1y")
            if not price_hist.empty:
                st.plotly_chart(draw_price_chart(price_hist, sel_ticker, target_name), use_container_width=True)

            with st.expander("FUNDAMENTAL DATA"):
                fund_items = [("REVENUE","revenue"),("EBITDA","ebitda"),("NET INCOME","net_income"),
                              ("TOTAL DEBT","total_debt"),("CASH","cash"),("ROE","roe"),
                              ("OPER MARGIN","operating_margin"),("NET MARGIN","net_margin"),
                              ("REV GROWTH","revenue_growth"),("BETA","beta")]
                fund_rows = []
                for label,key in fund_items:
                    val = target_row.get(key)
                    if val and not (isinstance(val,float) and np.isnan(val)):
                        if key in ["revenue","ebitda","net_income","total_debt","cash"]:
                            disp = f"₹{float(val)/1e7:,.0f} CR"
                        elif key in ["roe","operating_margin","net_margin","revenue_growth"]:
                            disp = f"{float(val)*100:.1f}%"
                        else: disp = f"{float(val):.2f}"
                        fund_rows.append({"METRIC":label,"VALUE":disp})
                if fund_rows:
                    st.dataframe(pd.DataFrame(fund_rows), hide_index=True, use_container_width=True)

            with st.expander("PEER SUMMARY STATISTICS"):
                from src.comps import peer_summary_stats
                stats_df = peer_summary_stats(comps_tbl)
                if not stats_df.empty and "label" in stats_df.columns:
                    fmt_cols  = ["mean","median","min","max","p25","p75"]
                    avail_fmt = [c for c in fmt_cols if c in stats_df.columns]
                    st.dataframe(
                        stats_df[["label","count"]+avail_fmt]
                        .rename(columns={"label":"METRIC","count":"N","mean":"MEAN","median":"MEDIAN",
                                         "min":"MIN","max":"MAX","p25":"P25","p75":"P75"})
                        .style.format({c:"{:.1f}" for c in avail_fmt}, na_rep="N/A"),
                        hide_index=True, use_container_width=True)


# ── TAB 5: METHODOLOGY ────────────────────────────────────────────────────────
with tab_method:
    st.markdown("<div class='bb-section'>METHODOLOGY & DATA SOURCES</div>", unsafe_allow_html=True)
    st.markdown("""
**MODULE 1 — SECTOR HEAT MAP**

Tracks P/E, P/BV, EV/EBITDA, and Dividend Yield for 12 NSE sectors.
Each cell = historical percentile rank vs own 10-year distribution.

```python
percentile = scipy.stats.percentileofscore(historical_10yr_array, today_value)
# 0 = cheapest ever  ·  50 = fair value  ·  100 = most expensive ever
```

**MODULE 2 — CCA SCREENER**

Auto-identifies peers by sector + market cap tier. Computes 6 trading multiples.
Shows premium/discount vs peer median. Football field chart. Implied price.

**DATA SOURCES**

| Source | Data |
|---|---|
| Yahoo Finance (yfinance) | Current multiples, price, fundamentals |
| NSE India | 10-year historical sector P/E, P/BV, Div Yield |
| NSE 500 universe | 180+ companies across 12 sectors |

**ZONE DEFINITIONS**

| Score | Zone |
|---|---|
| 0–20 | Very Cheap |
| 20–35 | Cheap |
| 35–65 | Fair Value |
| 65–80 | Expensive |
| 80–100 | Very Expensive |
    """)

st.markdown(f"""
<div style='background:#0a0a0a;border-top:1px solid #ff6600;padding:8px 16px;margin-top:16px;
            display:flex;justify-content:space-between;align-items:center;
            font-family:IBM Plex Mono,monospace;font-size:9px;color:#333;
            letter-spacing:.08em;text-transform:uppercase'>
  <span>◆ NSE VALUATION TERMINAL  ·  SECTOR HEAT MAP + CCA SCREENER</span>
  <span>DATA: NSE INDIA + YAHOO FINANCE  ·  {date.today().strftime('%d %b %Y').upper()}</span>
</div>""", unsafe_allow_html=True)
