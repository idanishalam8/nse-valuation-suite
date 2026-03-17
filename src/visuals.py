# ─────────────────────────────────────────────────────────────────────────────
# visuals.py  ·  All chart generation
# ─────────────────────────────────────────────────────────────────────────────

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from datetime import date
from src.config import ZONES, ZONE_COLORS, CCA_METRICS, NUMERIC_COLS

METRIC_LABELS = {"pe":"P/E","pb":"P/BV","ev_ebitda":"EV/EBITDA","div_yield":"Div Yield %"}

HEAT_CMAP = mcolors.LinearSegmentedColormap.from_list("richness",[
    (0.0,"#1a7a4a"),(0.20,"#5DCAA5"),(0.50,"#f5f0e8"),(0.80,"#EF9F27"),(1.00,"#c0392b")
])

BG  = "#0f1117"
SRF = "#161b22"


def _zone_color(score):
    for lbl,(lo,hi) in ZONES.items():
        if lo <= score < hi: return ZONE_COLORS[lbl]
    return ZONE_COLORS["Fair"]


def interpret_zone(score):
    for lbl,(lo,hi) in ZONES.items():
        if lo <= score < hi: return lbl, ZONE_COLORS[lbl]
    return "Fair", ZONE_COLORS["Fair"]


# ── HEAT MAP ──────────────────────────────────────────────────────────────────

def draw_heatmap(pct_matrix, title_date=None, figsize=(15,8)):
    display = pct_matrix[NUMERIC_COLS].copy()
    display.columns = [METRIC_LABELS.get(c,c) for c in display.columns]
    display.index   = [s.replace("Information ","Info. ") for s in display.index]

    annot = display.copy().astype(object)
    for r in display.index:
        for c in display.columns:
            v = display.loc[r,c]
            annot.loc[r,c] = f"{int(round(v))}" if not pd.isna(v) else "—"

    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)

    sns.heatmap(display.astype(float), annot=annot, fmt="",
                cmap=HEAT_CMAP, vmin=0, vmax=100, center=50,
                linewidths=1.2, linecolor="#1e2228",
                annot_kws={"size":13,"weight":"bold","color":"white"},
                cbar_kws={"shrink":0.55,"pad":0.02}, ax=ax, square=False)

    ax.set_xticklabels(ax.get_xticklabels(), color="white", fontsize=11, fontweight="bold")
    ax.set_yticklabels(ax.get_yticklabels(), color="#ccc", fontsize=10, rotation=0)
    ax.tick_params(colors="white", left=False, bottom=False)

    cb = ax.collections[0].colorbar
    cb.set_label("0 = cheapest vs own history  ·  100 = most expensive vs own history",
                 color="white", fontsize=9)
    plt.setp(cb.ax.yaxis.get_ticklabels(), color="white", fontsize=8)

    ds = title_date or date.today().strftime("%B %Y")
    ax.set_title(f"NSE Sector Valuation Heat Map  ·  {ds}",
                 color="white", fontsize=14, fontweight="bold", pad=14)
    plt.tight_layout(rect=[0,0.02,1,1])
    return fig


# ── RANKING BAR ───────────────────────────────────────────────────────────────

def draw_ranking_chart(richness_series):
    df = richness_series.reset_index()
    df.columns = ["Sector","Score"]
    df["Short"] = df["Sector"].str.replace("Information ","Info. ").str.replace("Capital Goods & ","")
    df["Color"] = df["Score"].apply(_zone_color)
    df["Zone"]  = df["Score"].apply(lambda s: interpret_zone(s)[0])

    fig = go.Figure()
    for _,row in df.iterrows():
        fig.add_trace(go.Bar(
            x=[row["Score"]], y=[row["Short"]], orientation="h",
            marker_color=row["Color"],
            text=f"{row['Score']:.0f}", textposition="outside",
            textfont=dict(size=11,color="white"),
            hovertemplate=f"<b>{row['Sector']}</b><br>Score: {row['Score']:.1f}/100<br>Zone: {row['Zone']}<extra></extra>",
            showlegend=False,
        ))

    fig.add_vline(x=50, line_dash="dot", line_color="rgba(255,255,255,0.3)",
                  annotation_text="Fair value", annotation_font=dict(color="rgba(255,255,255,0.5)",size=10))
    fig.add_vrect(x0=0,  x1=35,  fillcolor="#1a7a4a", opacity=0.06, layer="below", line_width=0)
    fig.add_vrect(x0=65, x1=100, fillcolor="#c0392b", opacity=0.06, layer="below", line_width=0)

    fig.update_layout(
        title=dict(text="Sector Richness Ranking", font=dict(color="white",size=13)),
        paper_bgcolor=BG, plot_bgcolor=BG,
        xaxis=dict(range=[0,115], showgrid=True, gridcolor="#222",
                   tickfont=dict(color="white"), title="Richness Score",
                   title_font=dict(color="#aaa",size=11)),
        yaxis=dict(tickfont=dict(color="white"), autorange="reversed"),
        height=430, margin=dict(l=10,r=60,t=45,b=35),
    )
    return fig


# ── HISTORY CHART ─────────────────────────────────────────────────────────────

def draw_history_chart(sector, metric, hist_df, current_val, years=10):
    col_map = {"pe":"pe","pb":"pb","ev_ebitda":"ev_ebitda","div_yield":"div_yield"}
    col     = col_map.get(metric, metric)
    dcol    = "date" if "date" in hist_df.columns else hist_df.columns[0]
    df      = hist_df.copy()
    df[dcol]= pd.to_datetime(df[dcol], errors="coerce")
    cutoff  = pd.Timestamp.today() - pd.DateOffset(years=years)
    df      = df[df[dcol] >= cutoff]

    if col not in df.columns:
        return go.Figure().update_layout(paper_bgcolor=BG, plot_bgcolor=BG,
            title=dict(text="No data", font=dict(color="white")))

    y = pd.to_numeric(df[col], errors="coerce"); x = df[dcol]
    p25,p50,p75 = np.nanpercentile(y,25), np.nanpercentile(y,50), np.nanpercentile(y,75)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(x)+list(x)[::-1],
        y=[p75]*len(x)+[p25]*len(x),
        fill="toself", fillcolor="rgba(74,140,106,0.10)",
        line=dict(width=0), name="25–75th pct band", hoverinfo="skip",
    ))
    fig.add_hline(y=p50, line_dash="dash", line_color="rgba(74,140,106,0.4)", line_width=1)
    fig.add_trace(go.Scatter(
        x=x, y=y, mode="lines", name="Historical",
        line=dict(color="#4a7fb5",width=1.8),
        hovertemplate="%{x|%b %Y}: %{y:.1f}<extra></extra>",
    ))
    if current_val and not np.isnan(float(current_val)):
        from scipy import stats as sp
        pct = sp.percentileofscore(y.dropna().values, float(current_val), kind="rank")
        _,zc = interpret_zone(pct)
        fig.add_hline(y=float(current_val), line_dash="solid", line_color=zc, line_width=2.5,
                      annotation_text=f"  Today: {float(current_val):.1f}x  ({pct:.0f}th pct)",
                      annotation_position="top left",
                      annotation_font=dict(color=zc, size=11))

    fig.update_layout(
        title=dict(text=f"{sector.replace('Information ','Info. ')}  ·  {METRIC_LABELS.get(metric,metric)}  ·  {years}Y",
                   font=dict(color="white",size=12)),
        paper_bgcolor=BG, plot_bgcolor=SRF,
        xaxis=dict(showgrid=True,gridcolor="#1e2228",tickfont=dict(color="#aaa")),
        yaxis=dict(showgrid=True,gridcolor="#1e2228",tickfont=dict(color="#aaa"),
                   title=METRIC_LABELS.get(metric,metric),title_font=dict(color="#aaa",size=11)),
        legend=dict(font=dict(color="white"),bgcolor="rgba(0,0,0,0)"),
        height=310, margin=dict(l=10,r=20,t=45,b=25), hovermode="x unified",
    )
    return fig


# ── CCA COMPS TABLE (styled) ──────────────────────────────────────────────────

def style_comps_table(comps_table: pd.DataFrame, target_ticker: str) -> pd.DataFrame:
    """Return a display-ready DataFrame — raw values formatted as strings."""
    display_cols = ["Company","Ticker","Mkt Cap"] + [CCA_METRICS[m]["label"] for m in list(CCA_METRICS.keys())]
    available    = [c for c in display_cols if c in comps_table.columns]
    df = comps_table[available].copy()

    # Format numeric columns
    for m, cfg in CCA_METRICS.items():
        lbl = cfg["label"]
        if lbl in df.columns:
            df[lbl] = df[lbl].apply(
                lambda v: f"{v:.1f}{cfg['suffix']}" if v is not None and not (isinstance(v,float) and np.isnan(v)) else "N/A"
            )
    return df


# ── FOOTBALL FIELD CHART ──────────────────────────────────────────────────────

def draw_football_field(ff_data: dict, target_name: str) -> go.Figure:
    """
    Horizontal box-plot style chart showing peer range per metric
    with target marker overlay.
    """
    metrics = list(ff_data.keys())
    labels  = [ff_data[m]["label"] for m in metrics]
    n       = len(metrics)

    fig = go.Figure()

    for i, m in enumerate(metrics):
        d = ff_data[m]
        y = i

        # Range bar (min–max)
        fig.add_trace(go.Scatter(
            x=[d["min"], d["max"]], y=[y,y],
            mode="lines", line=dict(color="rgba(255,255,255,0.15)",width=8),
            showlegend=False, hoverinfo="skip",
        ))
        # IQR bar (p25–p75)
        fig.add_trace(go.Scatter(
            x=[d["p25"], d["p75"]], y=[y,y],
            mode="lines", line=dict(color="#4a7fb5",width=14),
            name="25th–75th pct" if i==0 else None,
            showlegend=(i==0),
            hovertemplate=f"{d['label']}: P25={d['p25']:.1f} | P75={d['p75']:.1f}<extra></extra>",
        ))
        # Median marker
        fig.add_trace(go.Scatter(
            x=[d["median"]], y=[y],
            mode="markers", marker=dict(color="white",size=10,symbol="diamond"),
            name="Peer median" if i==0 else None,
            showlegend=(i==0),
            hovertemplate=f"Median: {d['median']:.1f}<extra></extra>",
        ))
        # Target marker
        if d["target"] is not None:
            fig.add_trace(go.Scatter(
                x=[d["target"]], y=[y],
                mode="markers", marker=dict(color="#c9a84c",size=14,symbol="star"),
                name=target_name if i==0 else None,
                showlegend=(i==0),
                hovertemplate=f"{target_name}: {d['target']:.1f}<extra></extra>",
            ))

    fig.update_layout(
        title=dict(text=f"Trading Comps Range  ·  {target_name} vs Peers",
                   font=dict(color="white",size=13)),
        paper_bgcolor=BG, plot_bgcolor=SRF,
        yaxis=dict(tickvals=list(range(n)), ticktext=labels,
                   tickfont=dict(color="white",size=11), showgrid=False),
        xaxis=dict(showgrid=True,gridcolor="#222",tickfont=dict(color="#aaa"),
                   title="Multiple (x)", title_font=dict(color="#aaa",size=11)),
        legend=dict(font=dict(color="white"),bgcolor="rgba(0,0,0,0)",
                    orientation="h", y=-0.15),
        height=max(320, n*60+100),
        margin=dict(l=10,r=20,t=50,b=60),
    )
    return fig


# ── PREMIUM/DISCOUNT BAR ──────────────────────────────────────────────────────

def draw_premium_discount(pd_table: pd.DataFrame, target_name: str) -> go.Figure:
    df  = pd_table.dropna(subset=["Premium / Disc %"]).copy()
    if df.empty:
        return go.Figure().update_layout(paper_bgcolor=BG, plot_bgcolor=BG,
            title=dict(text="No premium/discount data",font=dict(color="white")))

    df["color"] = df.apply(lambda r:
        "#E24B4A" if (r["Premium / Disc %"] > 0 and r["_higher_expensive"]) else
        "#5DCAA5" if (r["Premium / Disc %"] < 0 and r["_higher_expensive"]) else
        "#EF9F27", axis=1)

    fig = go.Figure(go.Bar(
        x=df["Metric"], y=df["Premium / Disc %"],
        marker_color=df["color"],
        text=[f"{v:+.1f}%" for v in df["Premium / Disc %"]],
        textposition="outside", textfont=dict(color="white",size=11),
        hovertemplate="%{x}: %{y:+.1f}% vs peer median<extra></extra>",
    ))
    fig.add_hline(y=0, line_color="rgba(255,255,255,0.3)", line_width=1)

    fig.update_layout(
        title=dict(text=f"{target_name}  ·  Premium (+) / Discount (−) vs Peer Median",
                   font=dict(color="white",size=13)),
        paper_bgcolor=BG, plot_bgcolor=SRF,
        xaxis=dict(tickfont=dict(color="white")),
        yaxis=dict(tickfont=dict(color="#aaa"), ticksuffix="%",
                   title="% vs peer median", title_font=dict(color="#aaa",size=11)),
        height=320, margin=dict(l=10,r=20,t=50,b=30),
    )
    return fig


# ── SPIDER CHART ──────────────────────────────────────────────────────────────

def draw_spider(pct_row, sector):
    metrics = NUMERIC_COLS
    labels  = [METRIC_LABELS.get(m,m) for m in metrics]
    vals    = [float(pct_row.get(m,50) or 50) for m in metrics]
    vals   += vals[:1]; labels += labels[:1]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=vals, theta=labels, fill="toself",
        fillcolor="rgba(74,127,181,0.18)", line=dict(color="#4a7fb5",width=2),
        name=sector,
    ))
    fig.add_trace(go.Scatterpolar(
        r=[50]*len(labels), theta=labels, mode="lines",
        line=dict(color="rgba(255,255,255,0.2)",dash="dot",width=1),
        name="Fair value", hoverinfo="skip",
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True,range=[0,100],tickfont=dict(color="#888",size=9),gridcolor="#222"),
            angularaxis=dict(tickfont=dict(color="white",size=10),gridcolor="#222"),
            bgcolor=BG,
        ),
        paper_bgcolor=BG, showlegend=False,
        height=270, margin=dict(l=30,r=30,t=30,b=30),
    )
    return fig


# ── PRICE CHART ───────────────────────────────────────────────────────────────

def draw_price_chart(price_df: pd.DataFrame, ticker: str, company: str) -> go.Figure:
    if price_df.empty:
        return go.Figure().update_layout(paper_bgcolor=BG, plot_bgcolor=BG,
            title=dict(text="No price data",font=dict(color="white")))

    close = price_df["Close"]
    start = float(close.iloc[0])
    pct_change = ((close - start) / start * 100).round(2)
    color = "#5DCAA5" if float(close.iloc[-1]) >= start else "#E24B4A"

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=close.index, y=close.values,
        mode="lines", line=dict(color=color,width=1.8),
        name=company,
        hovertemplate="%{x|%d %b %Y}: ₹%{y:,.1f}<extra></extra>",
    ))
    fig.update_layout(
        title=dict(text=f"{company}  ·  1-Year Price Chart",font=dict(color="white",size=12)),
        paper_bgcolor=BG, plot_bgcolor=SRF,
        xaxis=dict(showgrid=True,gridcolor="#1e2228",tickfont=dict(color="#aaa")),
        yaxis=dict(showgrid=True,gridcolor="#1e2228",tickfont=dict(color="#aaa"),
                   tickprefix="₹",title_font=dict(color="#aaa")),
        height=260, margin=dict(l=10,r=10,t=45,b=25),
    )
    return fig
