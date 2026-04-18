import pandas as pd
import os

SEGMENT_CONFIG = {
    'Champions': {
        'emoji': '👑', 'color': '#5B21B6', 'bg': 'rgba(91,33,182,0.08)',
        'desc': 'Bought recently, buy often, spend the most',
        'action': 'Reward them — exclusive early access, loyalty perks, personal thank-you'
    },
    'Loyal Customers': {
        'emoji': '💎', 'color': '#0E7490', 'bg': 'rgba(14,116,144,0.08)',
        'desc': 'Buy regularly with strong spending patterns',
        'action': 'Upsell premium products — they already trust you'
    },
    'Potential Loyalists': {
        'emoji': '🌱', 'color': '#047857', 'bg': 'rgba(4,120,87,0.08)',
        'desc': 'Recent buyers with growing frequency',
        'action': 'Offer membership or loyalty program to convert habit into loyalty'
    },
    'At Risk': {
        'emoji': '⚠️', 'color': '#B45309', 'bg': 'rgba(180,83,9,0.08)',
        'desc': 'Used to buy often but going quiet recently',
        'action': 'Send personalised win-back campaign with limited-time offer'
    },
    'Lost Customers': {
        'emoji': '💤', 'color': '#B91C1C', 'bg': 'rgba(185,28,28,0.08)',
        'desc': "Haven't bought in a very long time",
        'action': 'Last-chance reactivation — steep discount or feedback survey'
    }
}

COLOR_MAP = {seg: cfg['color'] for seg, cfg in SEGMENT_CONFIG.items()}

DATA_PATH = os.path.join(
    os.path.dirname(__file__), '..', 'data', 'processed', 'rfm_labeled.csv'
)

# Folder where the project's report figures live (relative to repo root)
FIGURES_DIR = os.path.join(
    os.path.dirname(__file__), '..', 'reports', 'figures'
)

def load_rfm_data() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)

def figure_path(name: str) -> str:
    """Return absolute path to a figure file inside reports/figures/."""
    return os.path.join(FIGURES_DIR, name)


APP_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #0f172a;
    letter-spacing: -0.005em;
}

/* Full page pastel gradient background */
.stApp {
    background: linear-gradient(145deg,
        #eef2ff 0%,
        #e0f2fe 25%,
        #f0fdf4 50%,
        #fdf4ff 75%,
        #eff6ff 100%) !important;
    background-attachment: fixed !important;
}

/* Sidebar pastel */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #e0e7ff 0%, #cffafe 100%) !important;
    border-right: 1px solid rgba(99,102,241,0.15) !important;
}
section[data-testid="stSidebar"] * {
    color: #0f172a !important;
}

/* ── Sidebar logo ── */
.sidebar-logo {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.55rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: #1e1b4b !important;
    background: linear-gradient(135deg, #1e1b4b, #075985);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    padding: 8px 0 20px;
}

/* ── Page titles ── */
.page-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: #0b1020;
    margin-bottom: 4px;
}
.page-sub {
    color: #334155;
    font-size: 0.95rem;
    font-weight: 500;
    margin-bottom: 28px;
}

/* ── Hero ── */
.hero-wrap {
    background: linear-gradient(135deg,
        rgba(199,210,254,0.6) 0%,
        rgba(186,230,253,0.6) 50%,
        rgba(220,252,231,0.5) 100%);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 28px;
    padding: 60px 48px;
    text-align: center;
    position: relative;
    overflow: hidden;
    margin-bottom: 36px;
    backdrop-filter: blur(8px);
}
.hero-glow-left {
    position: absolute; top: -80px; left: -80px;
    width: 340px; height: 340px;
    background: radial-gradient(circle, rgba(99,102,241,0.18) 0%, transparent 70%);
    pointer-events: none;
}
.hero-glow-right {
    position: absolute; bottom: -80px; right: -80px;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(8,145,178,0.15) 0%, transparent 70%);
    pointer-events: none;
}
.hero-badge {
    display: inline-block;
    background: rgba(30,27,75,0.08);
    border: 1px solid rgba(30,27,75,0.25);
    border-radius: 20px;
    padding: 5px 18px;
    font-size: 0.72rem;
    font-weight: 700;
    color: #1e1b4b;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    margin-bottom: 22px;
    animation: fadeDown 0.6s ease both;
}
.hero-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 3.6rem;
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.035em;
    color: #0b1020;
    margin: 0 0 18px;
    animation: fadeDown 0.7s ease 0.1s both;
}
.hero-sub {
    font-size: 1.05rem;
    color: #1f2937;
    font-weight: 500;
    max-width: 560px;
    margin: 0 auto 36px;
    line-height: 1.7;
    animation: fadeDown 0.7s ease 0.2s both;
}
.hero-stats {
    display: flex;
    justify-content: center;
    gap: 52px;
    flex-wrap: wrap;
    animation: fadeDown 0.7s ease 0.3s both;
}
.hstat { text-align: center; }
.hstat-val {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: #0b1020;
    display: block;
}
.hstat-lbl {
    font-size: 0.74rem;
    color: #1e293b;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.2px;
}

/* ── Metric cards ── */
div[data-testid="metric-container"] {
    background: rgba(255,255,255,0.85) !important;
    border: 1px solid rgba(99,102,241,0.2) !important;
    border-radius: 18px !important;
    padding: 20px 24px !important;
    backdrop-filter: blur(6px);
    box-shadow: 0 2px 16px rgba(99,102,241,0.07);
}
div[data-testid="metric-container"] label {
    color: #1e293b !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
}
div[data-testid="metric-container"] [data-testid="metric-value"] {
    color: #0b1020 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 800 !important;
    letter-spacing: -0.02em !important;
}

/* ── Segment / general cards ── */
.seg-card {
    background: rgba(255,255,255,0.88);
    border: 1px solid rgba(99,102,241,0.18);
    border-radius: 20px;
    padding: 24px 28px;
    margin-bottom: 14px;
    backdrop-filter: blur(6px);
    box-shadow: 0 2px 20px rgba(99,102,241,0.06);
    animation: fadeUp 0.5s ease both;
    transition: transform 0.2s, box-shadow 0.2s;
    color: #0f172a;
}
.seg-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 32px rgba(99,102,241,0.14);
}

/* ── Pills ── */
.pill {
    display: inline-block;
    background: rgba(30,27,75,0.06);
    border: 1px solid rgba(30,27,75,0.18);
    border-radius: 20px;
    padding: 4px 13px;
    font-size: 0.78rem;
    font-weight: 600;
    color: #1e1b4b;
    margin: 3px 3px 3px 0;
}

/* ── Prediction result card ── */
.pred-card {
    background: rgba(255,255,255,0.95);
    border: 2px solid rgba(99,102,241,0.3);
    border-radius: 24px;
    padding: 32px;
    text-align: center;
    backdrop-filter: blur(8px);
    box-shadow: 0 4px 32px rgba(99,102,241,0.12);
    animation: popIn 0.4s cubic-bezier(0.34,1.56,0.64,1) both;
}
.pred-name {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.85rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    margin: 10px 0 6px;
}
.action-box {
    background: rgba(30,27,75,0.05);
    border-radius: 14px;
    padding: 14px 18px;
    text-align: left;
    border-left: 3px solid #1e1b4b;
    margin-top: 18px;
}
.action-lbl {
    color: #1e1b4b;
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 1.4px;
    text-transform: uppercase;
    margin-bottom: 5px;
}
.conf-badge {
    display: inline-block;
    background: rgba(14,116,144,0.1);
    border: 1px solid rgba(14,116,144,0.35);
    border-radius: 20px;
    padding: 5px 18px;
    color: #0b4a5c;
    font-size: 0.86rem;
    font-weight: 700;
    margin-top: 16px;
}

/* ── Empty state ── */
.empty-state {
    background: rgba(255,255,255,0.6);
    border: 1px dashed rgba(99,102,241,0.3);
    border-radius: 20px;
    padding: 64px 32px;
    text-align: center;
    color: #334155;
    font-weight: 500;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #1e1b4b, #0e7490) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 14px 32px !important;
    font-weight: 700 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    letter-spacing: 0.01em !important;
    width: 100% !important;
    box-shadow: 0 4px 18px rgba(30,27,75,0.28) !important;
    transition: opacity 0.2s, transform 0.15s !important;
}
.stButton > button:hover {
    opacity: 0.92 !important;
    transform: translateY(-1px) !important;
}

/* ── Download button ── */
.stDownloadButton > button {
    background: rgba(255,255,255,0.9) !important;
    color: #1e1b4b !important;
    border: 1px solid rgba(30,27,75,0.3) !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    box-shadow: none !important;
}

/* ── Section headings ── */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: #0b1020 !important;
    font-weight: 800 !important;
    letter-spacing: -0.02em !important;
}

/* Generic text */
p, span, label, li, div[data-testid="stMarkdownContainer"] {
    color: #0f172a;
}

/* ── Expander ── */
div[data-testid="stExpander"] {
    background: rgba(255,255,255,0.8);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 16px;
}
div[data-testid="stExpander"] summary,
div[data-testid="stExpander"] p {
    color: #0b1020 !important;
    font-weight: 700 !important;
}

/* ── File uploader ── */
div[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.8);
    border-radius: 16px;
    border: 1px dashed rgba(30,27,75,0.3);
    padding: 16px;
}
div[data-testid="stFileUploader"] * {
    color: #1e293b !important;
}

/* ── Radio buttons ── */
div[role="radiogroup"] label {
    color: #0f172a !important;
    font-weight: 600;
}

/* ── Image captions ── */
.gallery-cap {
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #0b1020;
    font-weight: 700;
    font-size: 0.95rem;
    margin: 6px 0 18px;
    text-align: center;
    letter-spacing: -0.01em;
}

/* ── Animations ── */
@keyframes fadeDown {
    from { opacity:0; transform:translateY(-14px); }
    to   { opacity:1; transform:translateY(0); }
}
@keyframes fadeUp {
    from { opacity:0; transform:translateY(14px); }
    to   { opacity:1; transform:translateY(0); }
}
@keyframes popIn {
    from { opacity:0; transform:scale(0.91); }
    to   { opacity:1; transform:scale(1); }
}
</style>
"""
