import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# ── Theme tokens (light pastel — matches utils.py) ────────────────────────────
FONT      = '#2D3A4A'
FONT_SUB  = '#5A6B7D'
FONT_MUTE = '#8899AA'
PLOT_BG   = '#DFE5F0'
GRID_CLR  = 'rgba(123,143,212,0.15)'

def _layout(**kw):
    return dict(
        paper_bgcolor=PLOT_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(color=FONT, family='Syne, Inter, sans-serif'),
        **kw
    )


# ── Hero ──────────────────────────────────────────────────────────────────────
def render_hero(rfm: pd.DataFrame):
    champ = len(rfm[rfm['Segment'] == 'Champions'])
    rev   = rfm['Monetary'].sum()
    st.markdown(f"""
<div class="hero-wrap">
<div class="hero-glow-left"></div>
<div class="hero-glow-right"></div>
<div class="hero-badge">✦ ML-Powered Customer Intelligence</div>
<div class="hero-title">ShopLens</div>
<div class="hero-sub">
Understand your customers beyond surface-level metrics.<br>
RFM segmentation + deep learning, built for real business decisions.
</div>
<div class="hero-stats">
<div class="hstat"><span class="hstat-val">{len(rfm):,}</span><span class="hstat-lbl">Customers</span></div>
<div class="hstat"><span class="hstat-val">5</span><span class="hstat-lbl">Segments</span></div>
<div class="hstat"><span class="hstat-val">{champ}</span><span class="hstat-lbl">Champions</span></div>
<div class="hstat"><span class="hstat-val">£{rev/1e6:.1f}M</span><span class="hstat-lbl">Total Revenue</span></div>
</div>
</div>
""", unsafe_allow_html=True)


# ── KPI row ───────────────────────────────────────────────────────────────────
def render_kpis(rfm: pd.DataFrame):
    c1, c2, c3, c4 = st.columns(4)
    champ_n   = len(rfm[rfm['Segment'] == 'Champions'])
    risk_n    = len(rfm[rfm['Segment'] == 'At Risk'])
    champ_avg = rfm[rfm['Segment'] == 'Champions']['Monetary'].mean()
    lost_n    = len(rfm[rfm['Segment'] == 'Lost Customers'])
    with c1: st.metric("Total Customers",  f"{len(rfm):,}")
    with c2: st.metric("Champions 👑",      f"{champ_n:,}", f"£{champ_avg:,.0f} avg spend")
    with c3: st.metric("At Risk ⚠️",        f"{risk_n:,}",  f"{risk_n/len(rfm)*100:.1f}% of base", delta_color="inverse")
    with c4: st.metric("Lost Customers 💤", f"{lost_n:,}",  f"{lost_n/len(rfm)*100:.1f}% of base", delta_color="inverse")


# ── Scatter ───────────────────────────────────────────────────────────────────
def render_scatter(rfm, color_map):
    fig = px.scatter(
        rfm, x='Recency', y='Monetary',
        color='Segment', size='Frequency',
        color_discrete_map=color_map,
        title='Recency vs Monetary — by Segment',
        labels={'Recency': 'Recency (days)', 'Monetary': 'Monetary (£)'},
        opacity=0.75, size_max=18,
    )
    fig.update_layout(
        **_layout(height=420),
        xaxis=dict(gridcolor=GRID_CLR, zerolinecolor=GRID_CLR),
        yaxis=dict(gridcolor=GRID_CLR, zerolinecolor=GRID_CLR),
        legend=dict(orientation='h', yanchor='bottom', y=-0.38, bgcolor='rgba(0,0,0,0)'),
        title_font_size=14,
    )
    st.plotly_chart(fig, use_container_width=True)


# ── Donut ─────────────────────────────────────────────────────────────────────
def render_donut(rfm, color_map):
    counts = rfm['Segment'].value_counts().reset_index()
    counts.columns = ['Segment', 'Count']
    fig = go.Figure(go.Pie(
        labels=counts['Segment'], values=counts['Count'],
        hole=0.58,
        marker_colors=[color_map.get(s, '#888') for s in counts['Segment']],
        textinfo='label+percent', textfont_size=11,
        hovertemplate='<b>%{label}</b><br>%{value} customers<br>%{percent}<extra></extra>'
    ))
    fig.update_layout(**_layout(height=420, title='Segment Distribution', showlegend=False))
    st.plotly_chart(fig, use_container_width=True)


# ── RFM averages ──────────────────────────────────────────────────────────────
def render_rfm_averages(rfm, color_map):
    avg = rfm.groupby('Segment')[['Recency','Frequency','Monetary']].mean().round(1).reset_index()
    fig = make_subplots(rows=1, cols=3,
                        subplot_titles=['Avg Recency (days)', 'Avg Frequency (orders)', 'Avg Monetary (£)'])
    for i, col in enumerate(['Recency','Frequency','Monetary'], 1):
        fig.add_trace(go.Bar(
            x=avg['Segment'], y=avg[col],
            marker_color=[color_map.get(s,'#888') for s in avg['Segment']],
            showlegend=False,
            hovertemplate='%{x}: %{y}<extra></extra>'
        ), row=1, col=i)
    fig.update_layout(**_layout(height=320))
    fig.update_xaxes(tickangle=-20, gridcolor=GRID_CLR)
    fig.update_yaxes(gridcolor=GRID_CLR)
    st.plotly_chart(fig, use_container_width=True)


# ── Cluster view (2D — replaces old 3D expander) ─────────────────────────────
def render_cluster_view(rfm, color_map):
    fig = px.scatter(
        rfm, x='Recency', y='Frequency',
        color='Segment', size='Monetary',
        color_discrete_map=color_map,
        title='Customer Clusters — Recency vs Frequency',
        labels={'Recency': 'Recency (days)', 'Frequency': 'Frequency (orders)'},
        opacity=0.72, size_max=22,
        hover_data={'Monetary': ':,.0f', 'Segment': True}
    )
    fig.update_layout(
        **_layout(height=460),
        xaxis=dict(gridcolor=GRID_CLR, zerolinecolor=GRID_CLR),
        yaxis=dict(gridcolor=GRID_CLR, zerolinecolor=GRID_CLR),
        legend=dict(orientation='h', yanchor='bottom', y=-0.28, bgcolor='rgba(0,0,0,0)'),
        title_font_size=14,
    )
    st.plotly_chart(fig, use_container_width=True)


# ── Prediction result card ────────────────────────────────────────────────────
def render_prediction_card(segment, confidence, config):
    cfg = config.get(segment, {})
    st.markdown(f"""
<div class="pred-card">
<div style="font-size:3.2rem;margin-bottom:4px">{cfg.get('emoji','🎯')}</div>
<div class="pred-name" style="color:{cfg.get('color','#7B8FD4')}">{segment}</div>
<div style="color:{FONT_SUB};font-size:0.88rem">{cfg.get('desc','')}</div>
<div class="action-box">
<div class="action-lbl">Recommended Action</div>
<div style="color:{FONT};font-size:0.92rem">{cfg.get('action','')}</div>
</div>
<div class="conf-badge">Confidence: {confidence:.1f}%</div>
</div>
""", unsafe_allow_html=True)


# ── Confidence bar chart ──────────────────────────────────────────────────────
def render_confidence_chart(probas, classes, color_map):
    fig = go.Figure(go.Bar(
        x=probas * 100, y=classes,
        orientation='h',
        marker_color=[color_map.get(c,'#888') for c in classes],
        text=[f'{p*100:.1f}%' for p in probas],
        textposition='outside',
        textfont=dict(color=FONT),
    ))
    fig.update_layout(
        **_layout(height=260),
        title='Probability per Segment',
        xaxis=dict(range=[0, 118], gridcolor=GRID_CLR),
        yaxis=dict(gridcolor=GRID_CLR),
        margin=dict(l=10, r=60, t=40, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)


# ── Batch summary bar ─────────────────────────────────────────────────────────
def render_batch_summary(df, color_map):
    s = df['Segment'].value_counts().reset_index()
    s.columns = ['Segment', 'Count']
    fig = px.bar(s, x='Segment', y='Count', color='Segment',
                 color_discrete_map=color_map, title='Predicted Segment Distribution')
    fig.update_layout(
        **_layout(), showlegend=False,
        xaxis=dict(gridcolor=GRID_CLR),
        yaxis=dict(gridcolor=GRID_CLR),
    )
    st.plotly_chart(fig, use_container_width=True)


# ── Segment guide cards ───────────────────────────────────────────────────────
def render_segment_guide(rfm, config):
    avg    = rfm.groupby('Segment')[['Recency','Frequency','Monetary']].mean().round(1)
    counts = rfm['Segment'].value_counts()

    for i, (seg, cfg) in enumerate(config.items()):
        if seg not in avg.index:
            continue
        row   = avg.loc[seg]
        count = counts.get(seg, 0)
        pct   = count / len(rfm) * 100
        delay = i * 0.08

        st.markdown(f"""
<div class="seg-card" style="animation-delay:{delay}s;border-left:3px solid {cfg['color']}">
<div style="display:flex;justify-content:space-between;align-items:flex-start">
<div>
<span style="font-size:1.9rem">{cfg['emoji']}</span>
<span style="font-family:'Syne',sans-serif;font-size:1.15rem;font-weight:700;color:{cfg['color']};margin-left:10px">{seg}</span>
<div style="color:{FONT_SUB};font-size:0.86rem;margin-top:5px">{cfg['desc']}</div>
</div>
<div style="text-align:right">
<div style="font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:700;color:{cfg['color']}">{count:,}</div>
<div style="color:{FONT_SUB};font-size:0.78rem">{pct:.1f}% of base</div>
</div>
</div>
<div style="margin-top:14px">
<span class="pill">⏱ Recency: {row['Recency']:.0f} days</span>
<span class="pill">🔁 Frequency: {row['Frequency']:.1f} orders</span>
<span class="pill">💰 Monetary: £{row['Monetary']:,.0f}</span>
</div>
<div style="margin-top:14px;background:rgba(123,143,212,0.08);border-radius:12px;padding:12px 16px;border-left:3px solid {cfg['color']}">
<div style="color:{cfg['color']};font-size:0.7rem;font-weight:600;letter-spacing:1.3px;text-transform:uppercase;margin-bottom:4px">Recommended Action</div>
<div style="color:{FONT};font-size:0.9rem">{cfg['action']}</div>
</div>
</div>
""", unsafe_allow_html=True)