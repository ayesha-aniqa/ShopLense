import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# Pastel light theme for all charts — DARK text everywhere
PLOT_BG   = 'rgba(255,255,255,0.9)'
PAPER_BG  = 'rgba(255,255,255,0)'
FONT_COL  = '#0b1020'
GRID_COL  = 'rgba(99,102,241,0.10)'

def _layout(**kw):
    return dict(
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PLOT_BG,
        font_color=FONT_COL,
        font_family='Plus Jakarta Sans',
        title_font_family='Plus Jakarta Sans',
        title_font_color='#0b1020',
        title_font_size=16,
        xaxis=dict(gridcolor=GRID_COL, linecolor=GRID_COL,
                   title_font_color='#0f172a', tickfont_color='#0f172a'),
        yaxis=dict(gridcolor=GRID_COL, linecolor=GRID_COL,
                   title_font_color='#0f172a', tickfont_color='#0f172a'),
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
            <div class="hstat">
                <span class="hstat-val">{len(rfm):,}</span>
                <span class="hstat-lbl">Customers</span>
            </div>
            <div class="hstat">
                <span class="hstat-val">5</span>
                <span class="hstat-lbl">Segments</span>
            </div>
            <div class="hstat">
                <span class="hstat-val">{champ}</span>
                <span class="hstat-lbl">Champions</span>
            </div>
            <div class="hstat">
                <span class="hstat-val">£{rev/1e6:.1f}M</span>
                <span class="hstat-lbl">Total Revenue</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── KPIs ──────────────────────────────────────────────────────────────────────
def render_kpis(rfm: pd.DataFrame):
    c1, c2, c3, c4 = st.columns(4)
    champ_n   = len(rfm[rfm['Segment'] == 'Champions'])
    risk_n    = len(rfm[rfm['Segment'] == 'At Risk'])
    champ_avg = rfm[rfm['Segment'] == 'Champions']['Monetary'].mean()
    lost_n    = len(rfm[rfm['Segment'] == 'Lost Customers'])
    with c1: st.metric("Total Customers",  f"{len(rfm):,}")
    with c2: st.metric("Champions 👑",      f"{champ_n:,}",
                        f"£{champ_avg:,.0f} avg spend")
    with c3: st.metric("At Risk ⚠️",        f"{risk_n:,}",
                        f"{risk_n/len(rfm)*100:.1f}% of base",
                        delta_color="inverse")
    with c4: st.metric("Lost Customers 💤", f"{lost_n:,}",
                        f"{lost_n/len(rfm)*100:.1f}% of base",
                        delta_color="inverse")


# ── Scatter ───────────────────────────────────────────────────────────────────
def render_scatter(rfm, color_map):
    fig = px.scatter(
        rfm, x='Recency', y='Monetary',
        color='Segment', size='Frequency',
        color_discrete_map=color_map,
        title='Recency vs Monetary — by Segment',
        labels={'Recency': 'Recency (days)', 'Monetary': 'Monetary (£)'},
        opacity=0.78, size_max=18
    )
    fig.update_layout(
        **_layout(height=420),
        legend=dict(
            orientation='h', yanchor='bottom', y=-0.38,
            font_color='#0f172a',
            bgcolor='rgba(255,255,255,0.85)',
            bordercolor='rgba(99,102,241,0.2)',
            borderwidth=1
        )
    )
    fig.update_traces(marker=dict(line=dict(width=0.5, color='white')))
    st.plotly_chart(fig, use_container_width=True)


# ── Donut ─────────────────────────────────────────────────────────────────────
def render_donut(rfm, color_map):
    counts = rfm['Segment'].value_counts().reset_index()
    counts.columns = ['Segment', 'Count']
    fig = go.Figure(go.Pie(
        labels=counts['Segment'], values=counts['Count'],
        hole=0.58,
        marker_colors=[color_map.get(s, '#888') for s in counts['Segment']],
        marker_line=dict(color='white', width=2),
        textinfo='label+percent', textfont_size=12,
        textfont_color='#0b1020',
        hovertemplate='<b>%{label}</b><br>%{value} customers<br>%{percent}<extra></extra>'
    ))
    fig.update_layout(
        **_layout(height=420, title='Segment Distribution', showlegend=False)
    )
    st.plotly_chart(fig, use_container_width=True)


# ── RFM averages ──────────────────────────────────────────────────────────────
def render_rfm_averages(rfm, color_map):
    avg = rfm.groupby('Segment')[['Recency','Frequency','Monetary']].mean().round(1).reset_index()
    fig = make_subplots(rows=1, cols=3,
                         subplot_titles=['Avg Recency (days)',
                                         'Avg Frequency (orders)',
                                         'Avg Monetary (£)'])
    for i, col in enumerate(['Recency','Frequency','Monetary'], 1):
        fig.add_trace(go.Bar(
            x=avg['Segment'], y=avg[col],
            marker_color=[color_map.get(s,'#888') for s in avg['Segment']],
            marker_line=dict(color='white', width=1),
            showlegend=False,
            hovertemplate='%{x}: %{y}<extra></extra>'
        ), row=1, col=i)

    fig.update_layout(**_layout(height=320))
    fig.update_xaxes(tickangle=-20, tickfont_color='#0f172a')
    fig.update_annotations(font_color='#0b1020', font_family='Plus Jakarta Sans',
                           font_size=14)
    st.plotly_chart(fig, use_container_width=True)


# ── 2D Scatter ────────────────────────────────────────────────────────────────
def render_2d_scatter(rfm, COLOR_MAP):
    fig = px.scatter(
        rfm,
        x="Recency",
        y="Monetary",
        color="Segment",
        color_discrete_map=COLOR_MAP,
        size="Frequency",
        size_max=18,
        hover_data={
            "Recency": True,
            "Frequency": True,
            "Monetary": True,
            "Segment": True
        }
    )

    fig.update_layout(
        height=420,
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis_title="Recency (Days)",
        yaxis_title="Monetary (£)",
        legend_title="Segment",
        template="plotly_white"
    )

    fig.update_traces(marker=dict(opacity=0.85))

    st.plotly_chart(fig, use_container_width=True)


# ── Prediction result card ────────────────────────────────────────────────────
def render_prediction_card(segment, confidence, config):
    cfg = config.get(segment, {})
    st.markdown(f"""
    <div class="pred-card">
        <div style="font-size:3.2rem;margin-bottom:4px">{cfg.get('emoji','🎯')}</div>
        <div class="pred-name" style="color:{cfg.get('color','#0b1020')}">{segment}</div>
        <div style="color:#1f2937;font-weight:500;font-size:0.95rem;margin-bottom:4px">
            {cfg.get('desc','')}
        </div>
        <div class="action-box">
            <div class="action-lbl">Recommended Action</div>
            <div style="color:#0f172a;font-weight:500;font-size:0.95rem">{cfg.get('action','')}</div>
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
        marker_line=dict(color='white', width=1),
        text=[f'{p*100:.1f}%' for p in probas],
        textposition='outside',
        textfont=dict(color='#0b1020', family='Plus Jakarta Sans')
    ))
    fig.update_layout(
        **_layout(height=260),
        title='Probability per Segment',
    )
    st.plotly_chart(fig, use_container_width=True)


# ── Batch summary ─────────────────────────────────────────────────────────────
def render_batch_summary(df, color_map):
    s = df['Segment'].value_counts().reset_index()
    s.columns = ['Segment', 'Count']
    fig = px.bar(s, x='Segment', y='Count', color='Segment',
                 color_discrete_map=color_map,
                 title='Predicted Segment Distribution')
    fig.update_layout(**_layout(), showlegend=False)
    fig.update_traces(marker_line=dict(color='white', width=1))
    st.plotly_chart(fig, use_container_width=True)


# ── Report figures gallery (Dashboard) ────────────────────────────────────────
def render_report_gallery():
    """Show every saved figure from reports/figures/ inside the dashboard."""
    import os
    from utils import figure_path

    # (filename, friendly title)
    figures = [
        ('segments_plot.png',     'Customer Segments — Overview'),
        ('rfm_distributions.png', 'RFM Distributions'),
        ('elbow_silhouette.png',  'Elbow & Silhouette — K Selection'),
        ('kmeans_vs_dbscan.png',  'K-Means vs DBSCAN'),
        ('autoencoder_space.png', 'Autoencoder Latent Space'),
        ('confusion_matrix.png',  'Random Forest — Confusion Matrix'),
        ('feature_importance.png','Feature Importance — Random Forest'),
        ('monthly_orders.png',    'Monthly Orders Trend'),
        ('revenue_by_country.png','Revenue by Country'),
        ('top_countries.png',     'Top Countries by Customers'),
    ]

    st.markdown("#### 📈 Model & Data Insights")
    st.markdown(
        "<div class='page-sub' style='margin-bottom:18px'>"
        "Saved analysis figures from the training pipeline</div>",
        unsafe_allow_html=True
    )

    # Render in a 2-column responsive grid
    cols = st.columns(2)
    for i, (fname, title) in enumerate(figures):
        path = figure_path(fname)
        with cols[i % 2]:
            if os.path.exists(path):
                st.markdown(
                    f"<div class='gallery-cap'>{title}</div>",
                    unsafe_allow_html=True
                )
                st.image(path, use_container_width=True)
            else:
                st.markdown(
                    f"<div class='empty-state' style='padding:28px'>"
                    f"<b>{title}</b><br>"
                    f"<span style='font-size:0.8rem;color:#475569'>"
                    f"Missing: <code>reports/figures/{fname}</code></span></div>",
                    unsafe_allow_html=True
                )


# ── Segment guide ─────────────────────────────────────────────────────────────
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
        <div class="seg-card" style="animation-delay:{delay}s;
             border-left:4px solid {cfg['color']}">
            <div style="display:flex;justify-content:space-between;align-items:flex-start">
                <div>
                    <span style="font-size:1.9rem">{cfg['emoji']}</span>
                    <span style="font-family:'Plus Jakarta Sans',sans-serif;font-size:1.2rem;
                                 font-weight:800;color:{cfg['color']};margin-left:10px;
                                 letter-spacing:-0.01em">
                        {seg}
                    </span>
                    <div style="color:#1f2937;font-weight:500;font-size:0.9rem;margin-top:5px">
                        {cfg['desc']}
                    </div>
                </div>
                <div style="text-align:right">
                    <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:1.7rem;
                                font-weight:800;color:{cfg['color']};letter-spacing:-0.02em">{count:,}</div>
                    <div style="color:#334155;font-weight:600;font-size:0.8rem">{pct:.1f}% of base</div>
                </div>
            </div>
            <div style="margin-top:14px">
                <span class="pill">⏱ Recency: {row['Recency']:.0f} days</span>
                <span class="pill">🔁 Frequency: {row['Frequency']:.1f} orders</span>
                <span class="pill">💰 Monetary: £{row['Monetary']:,.0f}</span>
            </div>
            <div style="margin-top:14px;background:rgba(30,27,75,0.05);
                        border-radius:12px;padding:12px 16px;
                        border-left:3px solid {cfg['color']}">
                <div style="color:{cfg['color']};font-size:0.72rem;font-weight:800;
                            letter-spacing:1.3px;text-transform:uppercase;margin-bottom:5px">
                    Recommended Action
                </div>
                <div style="color:#0f172a;font-weight:500;font-size:0.93rem">{cfg['action']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
