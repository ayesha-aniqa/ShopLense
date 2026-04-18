import pandas as pd
import os

SEGMENT_CONFIG = {
    'Champions': {
        'emoji': '👑', 'color': '#7B8FD4', 'bg': 'rgba(123,143,212,0.10)',
        'desc': 'Bought recently, buy often, spend the most',
        'action': 'Reward them — exclusive early access, loyalty perks, personal thank-you'
    },
    'Loyal Customers': {
        'emoji': '💎', 'color': '#6BAED6', 'bg': 'rgba(107,174,214,0.10)',
        'desc': 'Buy regularly with strong spending patterns',
        'action': 'Upsell premium products — they already trust you'
    },
    'Potential Loyalists': {
        'emoji': '🌱', 'color': '#74C4B7', 'bg': 'rgba(116,196,183,0.10)',
        'desc': 'Recent buyers with growing frequency',
        'action': 'Offer membership or loyalty program to convert habit into loyalty'
    },
    'At Risk': {
        'emoji': '⚠️', 'color': '#A8A0D2', 'bg': 'rgba(168,160,210,0.10)',
        'desc': 'Used to buy often but going quiet recently',
        'action': 'Send personalised win-back campaign with limited-time offer'
    },
    'Lost Customers': {
        'emoji': '💤', 'color': '#95A5BD', 'bg': 'rgba(149,165,189,0.10)',
        'desc': "Haven't bought in a very long time",
        'action': 'Last-chance reactivation — steep discount or feedback survey'
    }
}

COLOR_MAP = {seg: cfg['color'] for seg, cfg in SEGMENT_CONFIG.items()}

DATA_PATH = os.path.join(
    os.path.dirname(__file__), '..', 'data', 'processed', 'rfm_labeled.csv'
)

def load_rfm_data() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)

# Font is loaded via <link> tag (not @import) so it works inside Streamlit's CSP
FONT_LINK = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">"""

APP_CSS = """
<style>
/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #2D3A4A;
}

/* Full page background */
.stApp {
    background: #E8EDF5 !important;
    background-attachment: fixed !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #D6DEF0 0%, #CDDBE8 100%) !important;
    border-right: 1px solid rgba(123,143,212,0.20) !important;
}
section[data-testid="stSidebar"] * {
    color: #2D3A4A !important;
}

/* ── Sidebar logo ── */
.sidebar-logo {
    font-family: 'Syne', sans-serif;
    font-size: 1.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #7B8FD4, #6BAED6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    padding: 8px 0 20px;
}

/* ── Page titles ── */
.page-title {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #2D3A4A;
    margin-bottom: 4px;
    animation: fadeDown 0.5s ease both;
}
.page-sub {
    color: #6B7B8D;
    font-size: 0.93rem;
    margin-bottom: 28px;
    animation: fadeDown 0.5s ease 0.1s both;
}

/* ── Hero ── */
.hero-wrap {
    background: #D6DEF0 !important;
    border: 1px solid rgba(123,143,212,0.25) !important;
    border-radius: 28px !important;
    padding: 60px 48px !important;
    text-align: center !important;
    position: relative !important;
    overflow: hidden !important;
    margin-bottom: 36px !important;
    animation: fadeScale 0.7s ease both;
}
.hero-glow-left {
    position: absolute; top: -80px; left: -80px;
    width: 340px; height: 340px;
    background: radial-gradient(circle, rgba(123,143,212,0.18) 0%, transparent 70%);
    pointer-events: none;
    animation: pulseGlow 4s ease-in-out infinite;
}
.hero-glow-right {
    position: absolute; bottom: -80px; right: -80px;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(107,174,214,0.15) 0%, transparent 70%);
    pointer-events: none;
    animation: pulseGlow 4s ease-in-out 2s infinite;
}
.hero-badge {
    display: inline-block !important;
    background: rgba(123,143,212,0.15) !important;
    border: 1px solid rgba(123,143,212,0.35) !important;
    border-radius: 20px !important;
    padding: 5px 18px !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    color: #5A6FA8 !important;
    letter-spacing: 1.8px !important;
    text-transform: uppercase !important;
    margin-bottom: 22px !important;
    animation: fadeDown 0.6s ease both;
}
.hero-title {
    font-family: 'Syne', sans-serif !important;
    font-size: 3.8rem !important;
    font-weight: 800 !important;
    line-height: 1.05 !important;
    background: linear-gradient(135deg, #2D3A4A 0%, #5A6FA8 50%, #6BAED6 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    margin: 0 0 18px !important;
    display: block !important;
    animation: fadeDown 0.7s ease 0.1s both;
}
.hero-sub {
    font-size: 1.05rem !important;
    color: #5A6B7D !important;
    max-width: 500px !important;
    margin: 0 auto 36px !important;
    line-height: 1.75 !important;
    display: block !important;
    animation: fadeDown 0.7s ease 0.2s both;
}
.hero-stats {
    display: flex !important;
    justify-content: center !important;
    gap: 52px !important;
    animation: fadeDown 0.7s ease 0.3s both;
}
.hstat { text-align: center !important; }
.hstat-val {
    font-family: 'Syne', sans-serif !important;
    font-size: 2rem !important;
    font-weight: 800 !important;
    color: #2D3A4A !important;
    display: block !important;
}
.hstat-lbl {
    font-size: 0.72rem !important;
    color: #8899AA !important;
    text-transform: uppercase !important;
    letter-spacing: 1.2px !important;
}

/* ── Metric cards ── */
div[data-testid="metric-container"] {
    background: #DFE5F0 !important;
    border: 1px solid rgba(123,143,212,0.20) !important;
    border-radius: 18px !important;
    padding: 20px 24px !important;
    box-shadow: 0 2px 12px rgba(123,143,212,0.08);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    animation: slideUp 0.5s ease both;
}
div[data-testid="metric-container"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 24px rgba(123,143,212,0.15);
}
div[data-testid="metric-container"] label {
    color: #6B7B8D !important;
    font-size: 0.82rem !important;
}
div[data-testid="metric-container"] [data-testid="metric-value"] {
    color: #2D3A4A !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
}

/* ── Segment / general cards ── */
.seg-card {
    background: #DFE5F0 !important;
    border: 1px solid rgba(123,143,212,0.18) !important;
    border-radius: 20px !important;
    padding: 24px 28px !important;
    margin-bottom: 14px !important;
    box-shadow: 0 2px 16px rgba(123,143,212,0.07);
    animation: slideUp 0.5s ease both;
    transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
}
.seg-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 32px rgba(123,143,212,0.15);
    border-color: rgba(123,143,212,0.35) !important;
}

/* ── Pills ── */
.pill {
    display: inline-block !important;
    background: rgba(123,143,212,0.10) !important;
    border: 1px solid rgba(123,143,212,0.22) !important;
    border-radius: 20px !important;
    padding: 4px 13px !important;
    font-size: 0.77rem !important;
    color: #5A6FA8 !important;
    margin: 3px 3px 3px 0 !important;
}

/* ── Prediction result card ── */
.pred-card {
    background: #DFE5F0 !important;
    border: 2px solid rgba(123,143,212,0.30) !important;
    border-radius: 24px !important;
    padding: 32px !important;
    text-align: center !important;
    box-shadow: 0 4px 28px rgba(123,143,212,0.12);
    animation: popIn 0.5s cubic-bezier(0.34,1.56,0.64,1) both;
}
.pred-name {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.85rem !important;
    font-weight: 800 !important;
    margin: 10px 0 6px !important;
    display: block !important;
}
.action-box {
    background: rgba(123,143,212,0.08) !important;
    border-radius: 14px !important;
    padding: 14px 18px !important;
    text-align: left !important;
    border-left: 3px solid #7B8FD4 !important;
    margin-top: 18px !important;
}
.action-lbl {
    color: #5A6FA8 !important;
    font-size: 0.7rem !important;
    font-weight: 700 !important;
    letter-spacing: 1.4px !important;
    text-transform: uppercase !important;
    margin-bottom: 5px !important;
    display: block !important;
}
.conf-badge {
    display: inline-block !important;
    background: rgba(107,174,214,0.15) !important;
    border: 1px solid rgba(107,174,214,0.35) !important;
    border-radius: 20px !important;
    padding: 5px 18px !important;
    color: #5A8EB5 !important;
    font-size: 0.84rem !important;
    font-weight: 600 !important;
    margin-top: 16px !important;
}

/* ── Empty state ── */
.empty-state {
    background: #DFE5F0 !important;
    border: 1px dashed rgba(123,143,212,0.30) !important;
    border-radius: 20px !important;
    padding: 64px 32px !important;
    text-align: center !important;
    color: #8899AA !important;
    animation: fadeScale 0.5s ease both;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #7B8FD4, #6BAED6) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 14px 32px !important;
    font-weight: 600 !important;
    width: 100% !important;
    box-shadow: 0 4px 18px rgba(123,143,212,0.25) !important;
    transition: opacity 0.2s, transform 0.25s ease, box-shadow 0.25s ease !important;
}
.stButton > button:hover {
    opacity: 0.92 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 24px rgba(123,143,212,0.35) !important;
}

/* ── Download button ── */
.stDownloadButton > button {
    background: #DFE5F0 !important;
    color: #5A6FA8 !important;
    border: 1px solid rgba(123,143,212,0.30) !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    box-shadow: none !important;
}

/* ── Section headings ── */
h1, h2, h3, h4, h5 {
    font-family: 'Syne', sans-serif !important;
    color: #2D3A4A !important;
}

/* ── Expander ── */
div[data-testid="stExpander"] {
    background: #DFE5F0 !important;
    border: 1px solid rgba(123,143,212,0.18) !important;
    border-radius: 16px !important;
}

/* ── File uploader ── */
div[data-testid="stFileUploader"] {
    background: #DFE5F0 !important;
    border-radius: 16px !important;
    border: 1px dashed rgba(123,143,212,0.35) !important;
    padding: 16px !important;
}

/* ── Radio buttons ── */
div[role="radiogroup"] label {
    color: #3D4D5C !important;
    font-weight: 500;
}
div[role="radiogroup"] label:hover {
    color: #5A6FA8 !important;
}

/* ── Animations ── */
@keyframes fadeDown {
    from { opacity:0; transform:translateY(-14px); }
    to   { opacity:1; transform:translateY(0); }
}
@keyframes slideUp {
    from { opacity:0; transform:translateY(20px); }
    to   { opacity:1; transform:translateY(0); }
}
@keyframes popIn {
    from { opacity:0; transform:scale(0.88); }
    to   { opacity:1; transform:scale(1); }
}
@keyframes fadeScale {
    from { opacity:0; transform:scale(0.96) translateY(8px); }
    to   { opacity:1; transform:scale(1) translateY(0); }
}
@keyframes pulseGlow {
    0%, 100% { opacity: 0.6; transform: scale(1); }
    50%      { opacity: 1; transform: scale(1.08); }
}
</style>
"""