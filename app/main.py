import streamlit as st
import pandas as pd

from utils import SEGMENT_CONFIG, COLOR_MAP, APP_CSS, load_rfm_data
from predict import load_models, predict_single, predict_batch
from components import (
    render_hero, render_kpis, render_scatter, render_donut,
    render_rfm_averages, render_2d_scatter,
    render_prediction_card, render_confidence_chart,
    render_batch_summary, render_segment_guide,
)

# ── Config ────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ShopLens — Customer Intelligence",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown(APP_CSS, unsafe_allow_html=True)

# ── Load ──────────────────────────────────────────────────────────────────────
rfm                          = load_rfm_data()
kmeans, encoder, rf, scaler, le = load_models()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-logo">🛍️ ShopLens</div>', unsafe_allow_html=True)
    st.markdown("---")

    page = st.radio(
        "Navigation",
        [
            "🏠  Home",
            "📊  Dashboard",
            "🔍  Single Prediction",
            "📁  Batch Prediction",
            "🎯  Segment Guide",
        ],
        label_visibility="collapsed",
        key="main_nav_radio",
    )

    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.72rem;color:#334155;text-transform:uppercase;"
        "letter-spacing:1.2px;margin-bottom:10px'>Model Info</div>",
        unsafe_allow_html=True
    )
    st.caption(f"Customers : {len(rfm):,}")
    st.caption(f"Segments  : {rfm['Segment'].nunique()}")
    st.caption("Classifier : Random Forest")
    st.caption("Encoding   : Autoencoder 2D")
    st.caption("Dataset    : UCI Online Retail II")

# ═══════════════════════════════════════════════════════════════════════════════
# HOME
# ═══════════════════════════════════════════════════════════════════════════════
if "Home" in page:
    render_hero(rfm)

    st.markdown("---")
    st.markdown(
        "<div class='page-title' style='text-align:center'>How ShopLens Works</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<div class='page-sub' style='text-align:center;margin-bottom:28px'>"
        "Three steps from raw transactions to business action</div>",
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)
    for col, num, title, desc, color in zip(
        [c1, c2, c3],
        ['01', '02', '03'],
        ['RFM Analysis', 'ML Clustering', 'Smart Actions'],
        [
            'Every customer gets three scores — Recency, Frequency, Monetary — computed from their full purchase history.',
            'K-Means groups customers into 5 natural segments. An Autoencoder compresses features. Random Forest predicts new customers.',
            'Each segment gets a tailored marketing recommendation. From Champions to Lost Customers — every group has a clear next step.'
        ],
        ['#FFD700', '#A78BFA', '#3ECFCF']
    ):
        with col:
            st.markdown(f"""
            <div class="seg-card" style="text-align:center;padding:32px 24px;
                 border-top:3px solid {color}">
                <div style="font-family:'Syne',sans-serif;font-size:2.2rem;
                            font-weight:800;color:{color};opacity:0.4;
                            margin-bottom:10px">{num}</div>
                <div style="font-family:'Syne',sans-serif;font-size:1.05rem;
                            font-weight:700;color:#f1f5f9;margin-bottom:10px">
                    {title}
                </div>
                <div style="color:#475569;font-size:0.88rem;line-height:1.65">
                    {desc}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Segment preview strip
    st.markdown(
        "<div class='page-title' style='text-align:center;font-size:1.4rem'>"
        "Your 5 Customer Segments</div>",
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)

    cols = st.columns(5)
    counts = rfm['Segment'].value_counts()
    for col, (seg, cfg) in zip(cols, SEGMENT_CONFIG.items()):
        n = counts.get(seg, 0)
        with col:
            st.markdown(f"""
            <div class="seg-card" style="text-align:center;padding:22px 16px;
                 border-top:2px solid {cfg['color']}">
                <div style="font-size:2rem">{cfg['emoji']}</div>
                <div style="font-family:'Syne',sans-serif;font-size:0.85rem;
                            font-weight:700;color:{cfg['color']};margin:8px 0 4px">
                    {seg}
                </div>
                <div style="font-size:1.4rem;font-weight:700;color:#fff">{n:,}</div>
                <div style="color:#334155;font-size:0.72rem">customers</div>
            </div>
            """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
elif "Dashboard" in page:
    st.markdown("<div class='page-title'>Dashboard</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='page-sub'>Live overview of your customer base</div>",
        unsafe_allow_html=True
    )

    render_kpis(rfm)
    st.markdown("---")

    col_l, col_r = st.columns([1.1, 0.9])
    with col_l: render_scatter(rfm, COLOR_MAP)
    with col_r: render_donut(rfm, COLOR_MAP)

    st.markdown("#### Average RFM Values per Segment")
    render_rfm_averages(rfm, COLOR_MAP)

    st.markdown("🧊 Cluster View")
    render_2d_scatter(rfm, COLOR_MAP)

# ═══════════════════════════════════════════════════════════════════════════════
# SINGLE PREDICTION
# ═══════════════════════════════════════════════════════════════════════════════
elif "Single" in page:
    st.markdown("<div class='page-title'>Single Prediction</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='page-sub'>Enter one customer's RFM values — get their segment instantly</div>",
        unsafe_allow_html=True
    )

    col_form, col_result = st.columns([1, 1.1])

    with col_form:
        st.markdown("#### Customer RFM Input")

        recency = st.slider(
            "Recency — days since last purchase",
            min_value=1, max_value=400, value=30,
            help="Lower = more recent = better"
        )
        frequency = st.slider(
            "Frequency — number of orders placed",
            min_value=1, max_value=50, value=5,
            help="Higher = more loyal"
        )
        monetary = st.slider(
            "Monetary — total amount spent (£)",
            min_value=10, max_value=20000, value=1000, step=50,
            help="Higher = more valuable"
        )

        st.markdown("---")
        st.markdown(
            "<div style='font-size:0.85rem;color:#475569;margin-bottom:8px'>"
            "Or type exact values</div>",
            unsafe_allow_html=True
        )
        c1, c2, c3 = st.columns(3)
        with c1:
            recency   = st.number_input("Recency",   1,    400,   recency,
                                         label_visibility="collapsed")
        with c2:
            frequency = st.number_input("Frequency", 1,    200,   frequency,
                                         label_visibility="collapsed")
        with c3:
            monetary  = st.number_input("Monetary",  1, 100000,   monetary,
                                         label_visibility="collapsed")

        predict_btn = st.button("🔍 Predict Segment")

    with col_result:
        if predict_btn:
            segment, confidence, probas, classes = predict_single(
                recency, frequency, monetary, encoder, rf, scaler, le
            )
            render_prediction_card(segment, confidence, SEGMENT_CONFIG)
            render_confidence_chart(probas, classes, COLOR_MAP)
        else:
            st.markdown("""
            <div class="empty-state">
                <div style="font-size:2.8rem;margin-bottom:14px">🔍</div>
                <div style="font-size:0.95rem">
                    Adjust the sliders and click<br>
                    <span style="color:#8b5cf6;font-weight:600">Predict Segment</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# BATCH PREDICTION
# ═══════════════════════════════════════════════════════════════════════════════
elif "Batch" in page:
    st.markdown("<div class='page-title'>Batch Prediction</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='page-sub'>Upload a CSV — predict segments for all customers at once</div>",
        unsafe_allow_html=True
    )

    template = pd.DataFrame({
        'CustomerID': [12345, 12346, 12347],
        'Recency':    [15,    90,    250],
        'Frequency':  [20,    3,     1],
        'Monetary':   [5000,  800,   200]
    })
    st.download_button(
        "⬇️ Download CSV Template",
        data=template.to_csv(index=False),
        file_name="shoplens_template.csv",
        mime="text/csv"
    )

    uploaded = st.file_uploader("Upload your customer CSV", type=['csv'])

    if uploaded:
        # FIX: try utf-8 first, fall back to latin-1 (handles £ symbol)
        try:
            df_up = pd.read_csv(uploaded)
        except UnicodeDecodeError:
            uploaded.seek(0)
            df_up = pd.read_csv(uploaded, encoding='latin-1')

        st.success(f"Loaded {len(df_up):,} customers")
        st.dataframe(df_up.head(5), use_container_width=True)

        required = {'Recency', 'Frequency', 'Monetary'}
        if not required.issubset(df_up.columns):
            st.error(f"CSV must contain: {required}. Found: {list(df_up.columns)}")
        else:
            if st.button("🚀 Predict All Segments"):
                with st.spinner("Running predictions..."):
                    result = predict_batch(df_up, encoder, rf, scaler, le, SEGMENT_CONFIG)

                st.success(f"✅ Done — {len(result):,} customers predicted!")
                render_batch_summary(result, COLOR_MAP)
                st.dataframe(result, use_container_width=True)
                st.download_button(
                    "⬇️ Download Results",
                    data=result.to_csv(index=False),
                    file_name="shoplens_results.csv",
                    mime="text/csv"
                )

# ═══════════════════════════════════════════════════════════════════════════════
# SEGMENT GUIDE
# ═══════════════════════════════════════════════════════════════════════════════
elif "Segment" in page:
    st.markdown("<div class='page-title'>Segment Guide</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='page-sub'>What each segment means and exactly what to do about it</div>",
        unsafe_allow_html=True
    )
    render_segment_guide(rfm, SEGMENT_CONFIG)
