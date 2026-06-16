"""
Steam Game Discovery Dashboard
A professional Steam analytics and recommendation platform
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from functools import lru_cache
from pathlib import Path
import urllib.request
import urllib.error

ROOT_DIR = Path(__file__).resolve().parent

# ─────────────────────────────────────────
#  PAGE CONFIG & THEME
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Steam Discovery Dashboard",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────
#  CUSTOM CSS — DARK & LIGHT THEME SUPPORT
# ─────────────────────────────────────────
st.markdown("""
<style>
/* ════════════════════════════════════════ */
/*          DARK THEME (DEFAULT)            */
/* ════════════════════════════════════════ */

/* ── Base & Background ────────────────── */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0a0e1a 0%, #0f1e36 40%, #1a0a2e 100%);
    min-height: 100vh;
}
[data-testid="stSidebar"] {
    background: rgba(10, 14, 26, 0.92) !important;
    border-right: 1px solid rgba(100, 180, 255, 0.15) !important;
}
[data-testid="stHeader"] {
    background: transparent !important;
}
/* ── Glassmorphism Cards ──────────────── */
.glass-card {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(100, 180, 255, 0.18);
    border-radius: 16px;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    padding: 20px;
    margin: 10px 0;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}
.glass-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(100, 180, 255, 0.18);
}
/* ── Game Card ────────────────────────── */
.game-card {
    background: linear-gradient(145deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02));
    border: 1px solid rgba(100, 180, 255, 0.2);
    border-radius: 14px;
    padding: 14px;
    margin: 8px 0;
    transition: all 0.25s ease;
    position: relative;
    overflow: hidden;
}
.game-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #3b82f6, #8b5cf6, #06b6d4);
    opacity: 0;
    transition: opacity 0.25s ease;
}
.game-card:hover {
    transform: translateY(-3px);
    border-color: rgba(100, 180, 255, 0.45);
    box-shadow: 0 8px 30px rgba(59, 130, 246, 0.22);
}
.game-card:hover::before { opacity: 1; }
/* ── Section Headers ──────────────────── */
.section-title {
    font-size: 1.6rem;
    font-weight: 700;
    background: linear-gradient(90deg, #60a5fa, #a78bfa, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 4px;
    letter-spacing: -0.02em;
}
.section-subtitle {
    color: rgba(148, 163, 184, 0.85);
    font-size: 0.9rem;
    margin-bottom: 18px;
}
/* ── Stat Chips ───────────────────────── */
.stat-chip {
    display: inline-block;
    background: rgba(59, 130, 246, 0.15);
    border: 1px solid rgba(59, 130, 246, 0.3);
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.78rem;
    color: #93c5fd;
    margin: 2px 4px 2px 0;
}
.stat-chip-green {
    background: rgba(16, 185, 129, 0.15);
    border-color: rgba(16, 185, 129, 0.3);
    color: #6ee7b7;
}
.stat-chip-purple {
    background: rgba(139, 92, 246, 0.15);
    border-color: rgba(139, 92, 246, 0.3);
    color: #c4b5fd;
}
.stat-chip-amber {
    background: rgba(245, 158, 11, 0.15);
    border-color: rgba(245, 158, 11, 0.3);
    color: #fcd34d;
}
/* ── Price Badge ──────────────────────── */
.price-badge {
    background: linear-gradient(135deg, #1d4ed8, #7c3aed);
    border-radius: 8px;
    padding: 4px 12px;
    font-weight: 700;
    font-size: 0.9rem;
    color: #fff;
    display: inline-block;
}
.price-free {
    background: linear-gradient(135deg, #065f46, #047857);
}
/* ── Rating Bar ───────────────────────── */
.rating-bar-wrap {
    background: rgba(255,255,255,0.07);
    border-radius: 4px;
    height: 6px;
    overflow: hidden;
    margin: 4px 0;
}
.rating-bar-fill {
    height: 100%;
    border-radius: 4px;
    background: linear-gradient(90deg, #3b82f6, #8b5cf6);
}
/* ── Hero Banner ──────────────────────── */
.hero-banner {
    background: linear-gradient(135deg, rgba(59,130,246,0.15) 0%, rgba(139,92,246,0.12) 50%, rgba(6,182,212,0.1) 100%);
    border: 1px solid rgba(100,180,255,0.2);
    border-radius: 20px;
    padding: 32px 36px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '🎮';
    position: absolute;
    right: 36px; top: 50%;
    transform: translateY(-50%);
    font-size: 5rem;
    opacity: 0.12;
}
/* ── Match Score ──────────────────────── */
.match-score {
    font-size: 1.3rem;
    font-weight: 800;
    background: linear-gradient(90deg, #34d399, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
/* ── Divider ──────────────────────────── */
.gradient-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(100,180,255,0.4), transparent);
    margin: 24px 0;
}
/* ── Typography ───────────────────────── */
h1, h2, h3 { color: #e2e8f0 !important; }
p, li, label { color: #cbd5e1; }
/* ── Sidebar labels ───────────────────── */
[data-testid="stSidebar"] label {
    color: #94a3b8 !important;
    font-size: 0.82rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: rgba(30, 41, 59, 0.8) !important;
    border-color: rgba(100,180,255,0.2) !important;
}
/* ── Buttons ──────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, #1d4ed8, #7c3aed) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    letter-spacing: 0.03em !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 15px rgba(59,130,246,0.25) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(59,130,246,0.4) !important;
}
/* ── Tabs ─────────────────────────────── */
[data-testid="stTabs"] [role="tablist"] {
    background: rgba(255,255,255,0.03) !important;
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
}
[data-testid="stTabs"] button[role="tab"] {
    border-radius: 8px !important;
    color: #94a3b8 !important;
    font-weight: 500 !important;
}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, rgba(59,130,246,0.3), rgba(139,92,246,0.3)) !important;
    color: #e2e8f0 !important;
}
/* ── Metrics ──────────────────────────── */
[data-testid="stMetricValue"] { color: #60a5fa !important; font-weight: 700; }
[data-testid="stMetricLabel"] { color: #94a3b8 !important; }
/* ── Expander ─────────────────────────── */
[data-testid="stExpander"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(100,180,255,0.15) !important;
    border-radius: 12px !important;
}
[data-testid="stExpander"] button { color: #cbd5e1 !important; }

/* ════════════════════════════════════════ */
/*          LIGHT THEME                     */
/* ════════════════════════════════════════ */
@media (prefers-color-scheme: light) {
    /* ── Global Defaults ────────────────── */
    * { color-scheme: light !important; }
    html, body { background-color: #ffffff !important; color: #0f172a !important; }
    
    /* ── Base & Background ────────────────── */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 40%, #f0f1f3 100%) !important;
        min-height: 100vh;
        color: #0f172a !important;
    }
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.98) !important;
        border-right: 1px solid rgba(59, 130, 246, 0.2) !important;
    }
    [data-testid="stHeader"] {
        background: transparent !important;
    }
    
    /* ── Main Content Area ─────────────── */
    [data-testid="stMainBlockContainer"] {
        background: transparent !important;
    }
    [data-testid="stColumn"] {
        background: transparent !important;
    }
    
    /* ── Glassmorphism Cards ──────────────── */
    .glass-card {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 1px solid rgba(59, 130, 246, 0.15) !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08) !important;
    }
    .glass-card:hover {
        box-shadow: 0 12px 40px rgba(59, 130, 246, 0.15) !important;
    }
    /* ── Game Card ────────────────────────── */
    .game-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.95), rgba(248,249,250,0.9)) !important;
        border: 1px solid rgba(59, 130, 246, 0.15) !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06) !important;
    }
    .game-card:hover {
        border-color: rgba(59, 130, 246, 0.35) !important;
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.12) !important;
    }
    
    /* ── Section Headers ──────────────────── */
    .section-title {
        background: linear-gradient(90deg, #1d4ed8, #7c3aed, #0891b2) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
    }
    .section-subtitle {
        color: #64748b !important;
    }
    
    /* ── Markdown & Text ─────────────────── */
    [data-testid="stMarkdownContainer"] {
        color: #0f172a !important;
    }
    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3,
    [data-testid="stMarkdownContainer"] h4,
    [data-testid="stMarkdownContainer"] h5,
    [data-testid="stMarkdownContainer"] h6 {
        color: #0f172a !important;
    }
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] span,
    [data-testid="stMarkdownContainer"] li {
        color: #475569 !important;
    }
    
    /* ── Stat Chips ───────────────────────── */
    .stat-chip {
        background: rgba(59, 130, 246, 0.08) !important;
        border: 1px solid rgba(59, 130, 246, 0.25) !important;
        color: #1d4ed8 !important;
    }
    .stat-chip-green {
        background: rgba(16, 185, 129, 0.08) !important;
        border-color: rgba(16, 185, 129, 0.25) !important;
        color: #047857 !important;
    }
    .stat-chip-purple {
        background: rgba(139, 92, 246, 0.08) !important;
        border-color: rgba(139, 92, 246, 0.25) !important;
        color: #7c3aed !important;
    }
    .stat-chip-amber {
        background: rgba(245, 158, 11, 0.08) !important;
        border-color: rgba(245, 158, 11, 0.25) !important;
        color: #d97706 !important;
    }
    
    /* ── Price Badge ──────────────────────── */
    .price-badge {
        background: linear-gradient(135deg, #2563eb, #9333ea) !important;
        color: #fff !important;
    }
    .price-free {
        background: linear-gradient(135deg, #059669, #10b981) !important;
    }
    
    /* ── Rating Bar ───────────────────────── */
    .rating-bar-wrap {
        background: rgba(59, 130, 246, 0.12) !important;
    }
    
    /* ── Hero Banner ──────────────────────── */
    .hero-banner {
        background: linear-gradient(135deg, rgba(59,130,246,0.08) 0%, rgba(139,92,246,0.06) 50%, rgba(6,182,212,0.05) 100%) !important;
        border: 1px solid rgba(59, 130, 246, 0.15) !important;
    }
    
    /* ── Divider ──────────────────────────── */
    .gradient-divider {
        background: linear-gradient(90deg, transparent, rgba(59,130,246,0.25), transparent) !important;
    }
    
    /* ── Typography ───────────────────────── */
    h1, h2, h3, h4, h5, h6 { color: #0f172a !important; }
    p, li, label, div, span, a { color: #475569 !important; }
    
    /* ── Sidebar labels ───────────────────── */
    [data-testid="stSidebar"] label {
        color: #475569 !important;
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #475569 !important;
    }
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background: rgba(59, 130, 246, 0.05) !important;
        border-color: rgba(59, 130, 246, 0.2) !important;
        color: #0f172a !important;
    }
    [data-testid="stSidebar"] input, 
    [data-testid="stSidebar"] select,
    [data-testid="stSidebar"] textarea {
        background: white !important;
        color: #0f172a !important;
        border-color: rgba(59, 130, 246, 0.2) !important;
    }
    
    /* ── Buttons ──────────────────────────── */
    .stButton > button {
        background: linear-gradient(135deg, #2563eb, #7c3aed) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(59,130,246,0.2) !important;
    }
    .stButton > button:hover {
        box-shadow: 0 8px 25px rgba(59,130,246,0.3) !important;
    }
    
    /* ── Tabs ─────────────────────────────── */
    [data-testid="stTabs"] [role="tablist"] {
        background: rgba(59, 130, 246, 0.05) !important;
    }
    [data-testid="stTabs"] button[role="tab"] {
        color: #64748b !important;
    }
    [data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, rgba(59,130,246,0.15), rgba(139,92,246,0.15)) !important;
        color: #1d4ed8 !important;
    }
    
    /* ── Metrics ──────────────────────────– */
    [data-testid="stMetricValue"] { color: #1d4ed8 !important; font-weight: 700; }
    [data-testid="stMetricLabel"] { color: #64748b !important; }
    [data-testid="stMetricContainer"] {
        background: rgba(59, 130, 246, 0.03) !important;
    }
    
    /* ── Expander ─────────────────────────── */
    [data-testid="stExpander"] {
        background: rgba(59, 130, 246, 0.03) !important;
        border: 1px solid rgba(59, 130, 246, 0.15) !important;
    }
    [data-testid="stExpander"] button { color: #0f172a !important; }
    [data-testid="stExpander"] [data-testid="stMarkdownContainer"] { color: #475569 !important; }
    
    /* ── Input & Select ─────────────────── */
    input[type="text"], 
    input[type="number"], 
    input[type="date"],
    input[type="password"],
    textarea, 
    select {
        background: white !important;
        color: #0f172a !important;
        border-color: rgba(59, 130, 246, 0.2) !important;
    }
    input::placeholder,
    textarea::placeholder {
        color: #94a3b8 !important;
    }
    
    /* ── Selectbox & Multiselect ─────────── */
    [data-testid="stSelectbox"] [role="combobox"],
    [data-testid="stMultiSelect"] [role="listbox"] {
        background: white !important;
        border-color: rgba(59, 130, 246, 0.2) !important;
        color: #0f172a !important;
    }
    
    /* ── Slider ────────────────────────── */
    [data-testid="stSlider"] [role="slider"] {
        background: rgba(59, 130, 246, 0.2) !important;
    }
    
    /* ── Checkbox & Radio ──────────────── */
    [data-testid="stCheckbox"] label,
    [data-testid="stRadio"] label {
        color: #0f172a !important;
    }
}
</style>
<script>
(function() {
    const updateThemeClass = () => {
        const themeAttr = document.documentElement.getAttribute('data-theme') || document.body.getAttribute('data-theme');
        const classNames = document.documentElement.className + ' ' + document.body.className;
        const isLight = (themeAttr && themeAttr.toLowerCase().includes('light')) || classNames.toLowerCase().includes('theme-light') || classNames.toLowerCase().includes('light');
        document.documentElement.classList.toggle('st-light-theme', isLight);
        document.body.classList.toggle('st-light-theme', isLight);
    };
    updateThemeClass();
    const observer = new MutationObserver(updateThemeClass);
    observer.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme', 'class'] });
    observer.observe(document.body, { attributes: true, attributeFilter: ['data-theme', 'class'] });
})();
</script>
<style>
.st-light-theme, .st-light-theme *,
html.theme-light, html.theme-light *,
body.theme-light, body.theme-light *,
html[data-theme="light"], html[data-theme="light"] *,
body[data-theme="light"], body[data-theme="light"] *,
.theme-light, .theme-light *,
.streamlit-theme-light, .streamlit-theme-light * {
    color: #0f172a !important;
}
:is(.st-light-theme, html.theme-light, body.theme-light, html[data-theme="light"], body[data-theme="light"], .theme-light, .streamlit-theme-light) [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 40%, #f0f1f3 100%) !important;
}
:is(.st-light-theme, html.theme-light, body.theme-light, html[data-theme="light"], body[data-theme="light"], .theme-light, .streamlit-theme-light) [data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.98) !important;
    border-right: 1px solid rgba(59, 130, 246, 0.2) !important;
}
:is(.st-light-theme, html.theme-light, body.theme-light, html[data-theme="light"], body[data-theme="light"], .theme-light, .streamlit-theme-light) [data-testid="stHeader"] {
    background: transparent !important;
}
:is(.st-light-theme, html.theme-light, body.theme-light, html[data-theme="light"], body[data-theme="light"], .theme-light, .streamlit-theme-light) .glass-card,
:is(.st-light-theme, html.theme-light, body.theme-light, html[data-theme="light"], body[data-theme="light"], .theme-light, .streamlit-theme-light) .game-card,
:is(.st-light-theme, html.theme-light, body.theme-light, html[data-theme="light"], body[data-theme="light"], .theme-light, .streamlit-theme-light) .hero-banner,
:is(.st-light-theme, html.theme-light, body.theme-light, html[data-theme="light"], body[data-theme="light"], .theme-light, .streamlit-theme-light) [data-testid="stExpander"] {
    background: rgba(255, 255, 255, 0.95) !important;
    border: 1px solid rgba(59, 130, 246, 0.15) !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08) !important;
}
:is(.st-light-theme, html.theme-light, body.theme-light, html[data-theme="light"], body[data-theme="light"], .theme-light, .streamlit-theme-light) .game-card {
    background: linear-gradient(145deg, rgba(255,255,255,0.95), rgba(248,249,250,0.9)) !important;
}
:is(.st-light-theme, html.theme-light, body.theme-light, html[data-theme="light"], body[data-theme="light"], .theme-light, .streamlit-theme-light) .section-subtitle,
:is(.st-light-theme, html.theme-light, body.theme-light, html[data-theme="light"], body[data-theme="light"], .theme-light, .streamlit-theme-light) [data-testid="stMarkdownContainer"] p,
:is(.st-light-theme, html.theme-light, body.theme-light, html[data-theme="light"], body[data-theme="light"], .theme-light, .streamlit-theme-light) [data-testid="stMarkdownContainer"] li,
:is(.st-light-theme, html.theme-light, body.theme-light, html[data-theme="light"], body[data-theme="light"], .theme-light, .streamlit-theme-light) [data-testid="stMarkdownContainer"] span {
    color: #475569 !important;
}
:is(.st-light-theme, html.theme-light, body.theme-light, html[data-theme="light"], body[data-theme="light"], .theme-light, .streamlit-theme-light) .stButton > button {
    background: linear-gradient(135deg, #2563eb, #7c3aed) !important;
    color: white !important;
    box-shadow: 0 4px 15px rgba(59,130,246,0.2) !important;
}
:is(.st-light-theme, html.theme-light, body.theme-light, html[data-theme="light"], body[data-theme="light"], .theme-light, .streamlit-theme-light) .stButton > button:hover {
    box-shadow: 0 8px 25px rgba(59,130,246,0.3) !important;
}
:is(.st-light-theme, html.theme-light, body.theme-light, html[data-theme="light"], body[data-theme="light"], .theme-light, .streamlit-theme-light) input,
:is(.st-light-theme, html.theme-light, body.theme-light, html[data-theme="light"], body[data-theme="light"], .theme-light, .streamlit-theme-light) textarea,
:is(.st-light-theme, html.theme-light, body.theme-light, html[data-theme="light"], body[data-theme="light"], .theme-light, .streamlit-theme-light) select,
:is(.st-light-theme, html.theme-light, body.theme-light, html[data-theme="light"], body[data-theme="light"], .theme-light, .streamlit-theme-light) [data-testid="stTextInput"] input,
:is(.st-light-theme, html.theme-light, body.theme-light, html[data-theme="light"], body[data-theme="light"], .theme-light, .streamlit-theme-light) [data-testid="stNumberInput"] input,
:is(.st-light-theme, html.theme-light, body.theme-light, html[data-theme="light"], body[data-theme="light"], .theme-light, .streamlit-theme-light) [data-testid="stTextArea"] textarea {
    background: white !important;
    color: #0f172a !important;
    border-color: rgba(59, 130, 246, 0.2) !important;
}
:is(.st-light-theme, html.theme-light, body.theme-light, html[data-theme="light"], body[data-theme="light"], .theme-light, .streamlit-theme-light) [data-testid="stSelectbox"] > div > div,
:is(.st-light-theme, html.theme-light, body.theme-light, html[data-theme="light"], body[data-theme="light"], .theme-light, .streamlit-theme-light) [data-testid="stMultiSelect"] > div > div {
    background: white !important;
    color: #0f172a !important;
    border-color: rgba(59, 130, 246, 0.2) !important;
}
:is(.st-light-theme, html.theme-light, body.theme-light, html[data-theme="light"], body[data-theme="light"], .theme-light, .streamlit-theme-light) [data-testid="stTabs"] [role="tablist"] {
    background: rgba(59, 130, 246, 0.05) !important;
}
:is(.st-light-theme, html.theme-light, body.theme-light, html[data-theme="light"], body[data-theme="light"], .theme-light, .streamlit-theme-light) [data-testid="stTabs"] button[role="tab"] {
    color: #64748b !important;
}
:is(.st-light-theme, html.theme-light, body.theme-light, html[data-theme="light"], body[data-theme="light"], .theme-light, .streamlit-theme-light) [data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, rgba(59,130,246,0.15), rgba(139,92,246,0.15)) !important;
    color: #1d4ed8 !important;
}
:is(.st-light-theme, html.theme-light, body.theme-light, html[data-theme="light"], body[data-theme="light"], .theme-light, .streamlit-theme-light) [data-testid="stMetricValue"] { color: #1d4ed8 !important; }
:is(.st-light-theme, html.theme-light, body.theme-light, html[data-theme="light"], body[data-theme="light"], .theme-light, .streamlit-theme-light) [data-testid="stMetricLabel"] { color: #64748b !important; }
:is(.st-light-theme, html.theme-light, body.theme-light, html[data-theme="light"], body[data-theme="light"], .theme-light, .streamlit-theme-light) .price-badge {
    background: linear-gradient(135deg, #2563eb, #9333ea) !important;
}
:is(.st-light-theme, html.theme-light, body.theme-light, html[data-theme="light"], body[data-theme="light"], .theme-light, .streamlit-theme-light) .price-free {
    background: linear-gradient(135deg, #059669, #10b981) !important;
}
:is(.st-light-theme, html.theme-light, body.theme-light, html[data-theme="light"], body[data-theme="light"], .theme-light, .streamlit-theme-light) .seasonal-card,
:is(.st-light-theme, html.theme-light, body.theme-light, html[data-theme="light"], body[data-theme="light"], .theme-light, .streamlit-theme-light) .stat-chip,
:is(.st-light-theme, html.theme-light, body.theme-light, html[data-theme="light"], body[data-theme="light"], .theme-light, .streamlit-theme-light) .stat-chip-green,
:is(.st-light-theme, html.theme-light, body.theme-light, html[data-theme="light"], body[data-theme="light"], .theme-light, .streamlit-theme-light) .stat-chip-purple,
:is(.st-light-theme, html.theme-light, body.theme-light, html[data-theme="light"], body[data-theme="light"], .theme-light, .streamlit-theme-light) .stat-chip-amber {
    background: rgba(255,255,255,0.9) !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
#  CONSTANTS
# ─────────────────────────────────────────
USD_TO_INR = 82
PLACEHOLDER_IMG = "https://via.placeholder.com/460x215/1a2744/4a90d9?text=No+Image"
STEAM_IMG_URL = "https://cdn.akamai.steamstatic.com/steam/apps/{appid}/header.jpg"

GENRE_LIST = ["Action", "Adventure", "RPG", "Strategy", "Simulation",
              "Indie", "Sports", "Racing", "Horror", "Puzzle", "Casual"]
DNA_CATEGORIES = ["Action", "Adventure", "RPG", "Strategy", "Multiplayer"]


# ─────────────────────────────────────────
#  DATA LOADING & CACHING
# ─────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data():
    """Load and clean the Steam dataset."""
    csv_path = ROOT_DIR / "steam.csv"
    if not csv_path.exists():
        st.error(f"Data file not found: {csv_path}")
        return pd.DataFrame()

    df = pd.read_csv(csv_path, on_bad_lines="skip")

    # Keep English games only
    df = df[df["languages"].str.contains("english", case=False, na=False)].copy()

    # Select relevant columns
    cols = ["appid", "name", "genres", "price", "positive_ratings",
            "negative_ratings", "average_playtime"]
    df = df[cols].copy()

    # Clean data
    df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0)
    df["price_inr"] = df["price"].round(2)
    df["positive_ratings"] = pd.to_numeric(df["positive_ratings"], errors="coerce").fillna(0)
    df["negative_ratings"] = pd.to_numeric(df["negative_ratings"], errors="coerce").fillna(0)
    df["average_playtime"] = pd.to_numeric(df["average_playtime"], errors="coerce").fillna(0)

    # Rating percentage
    total = df["positive_ratings"] + df["negative_ratings"]
    df["rating_pct"] = np.where(
        total > 0,
        (df["positive_ratings"] / total * 100).round(1),
        0.0
    )

    # Remove Counter-Strike: Global Offensive
    df = df[~df["name"].str.contains("Counter-Strike: Global Offensive", na=False)]

    # Remove duplicates by name (keep highest rated)
    df = df.sort_values("positive_ratings", ascending=False)
    df = df.drop_duplicates(subset="name", keep="first")

    # Genre flags for ML
    for genre in GENRE_LIST:
        df[f"genre_{genre}"] = df["genres"].str.contains(genre, case=False, na=False).astype(int)

    df = df.reset_index(drop=True)
    return df


@lru_cache(maxsize=256)
def validate_image_url(url: str) -> bool:
    """Validate if an image URL is reachable (LRU cached)."""
    try:
        req = urllib.request.Request(url, method="HEAD",
                                      headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=2) as r:
            return r.status == 200
    except Exception:
        return False


def get_game_image(appid: int) -> str:
    """Return Steam header image URL or a placeholder."""
    url = STEAM_IMG_URL.format(appid=appid)
    if validate_image_url(url):
        return url
    return PLACEHOLDER_IMG


# ─────────────────────────────────────────
#  GENRE EXTRACTION
# ─────────────────────────────────────────
@st.cache_data(show_spinner=False)
def get_all_genres(df: pd.DataFrame):
    """Extract sorted unique genres from the dataset."""
    genres = set()
    for g in df["genres"].dropna():
        for item in g.split(";"):
            item = item.strip()
            if item:
                genres.add(item)
    return sorted(genres)


# ─────────────────────────────────────────
#  FILTERING
# ─────────────────────────────────────────
def apply_filters(df: pd.DataFrame, genre: str, player_style: str,
                  price_range: tuple, min_ratings: int,
                  free_only: bool, sort_by: str) -> pd.DataFrame:
    """Apply sidebar filters to the dataframe."""
    fdf = df.copy()

    # Genre filter
    if genre != "All":
        fdf = fdf[fdf["genres"].str.contains(genre, case=False, na=False)]

    # Player style filter
    if player_style == "Casual":
        threshold = fdf["average_playtime"].quantile(0.4)
        fdf = fdf[fdf["average_playtime"] <= threshold]
    elif player_style == "Hardcore":
        threshold = fdf["average_playtime"].quantile(0.7)
        fdf = fdf[fdf["average_playtime"] >= threshold]
    elif player_style == "Competitive":
        fdf = fdf[fdf["genres"].str.contains("Multiplayer|Action", case=False, na=False)]
    elif player_style == "Story Lover":
        fdf = fdf[fdf["genres"].str.contains("Adventure|RPG", case=False, na=False)]

    # Price filter (INR)
    fdf = fdf[
        (fdf["price_inr"] >= price_range[0]) &
        (fdf["price_inr"] <= price_range[1])
    ]

    # Minimum ratings
    fdf = fdf[fdf["positive_ratings"] >= min_ratings]

    # Free-to-play
    if free_only:
        fdf = fdf[fdf["price"] == 0]

    # Sort
    if sort_by == "Recommended":
        fdf = fdf.sort_values("rating_pct", ascending=False)
    elif sort_by == "Popularity":
        fdf = fdf.sort_values("positive_ratings", ascending=False)
    elif sort_by == "Price":
        fdf = fdf.sort_values("price_inr", ascending=True)
    elif sort_by == "Playtime":
        fdf = fdf.sort_values("average_playtime", ascending=False)

    return fdf.reset_index(drop=True)


# ─────────────────────────────────────────
#  GAME SECTIONS LOGIC
# ─────────────────────────────────────────
def get_popular(df: pd.DataFrame, n: int = 12) -> pd.DataFrame:
    return df.nlargest(n, "positive_ratings")


def get_trending(df: pd.DataFrame, n: int = 12) -> pd.DataFrame:
    if df.empty or len(df) < 2:
        return df.head(n)
    scaler = MinMaxScaler()
    tmp = df.copy()
    tmp["norm_ratings"] = scaler.fit_transform(tmp[["positive_ratings"]])
    tmp["norm_playtime"] = scaler.fit_transform(tmp[["average_playtime"]])
    tmp["trend_score"] = 0.7 * tmp["norm_ratings"] + 0.3 * tmp["norm_playtime"]
    return tmp.nlargest(n, "trend_score")


def get_hidden_gems(df: pd.DataFrame, n: int = 12) -> pd.DataFrame:
    """High rating % but relatively low positive rating count."""
    if df.empty or len(df) < 2:
        return df.head(n)
    scaler = MinMaxScaler()
    tmp = df.copy()
    tmp["norm_ratings"] = scaler.fit_transform(tmp[["positive_ratings"]])
    tmp["gem_score"] = tmp["rating_pct"] * (1 - tmp["norm_ratings"])
    return tmp[tmp["positive_ratings"] >= 1000].nlargest(n, "gem_score")


# ─────────────────────────────────────────
#  RECOMMENDATION ENGINE
# ─────────────────────────────────────────
def compute_recommendations(df: pd.DataFrame, game_name: str, top_n: int = 5) -> pd.DataFrame:
    """Recommend similar games using genre overlap + rating + price factors."""
    game_row = df[df["name"] == game_name]
    if game_row.empty:
        return pd.DataFrame()

    game = game_row.iloc[0]
    game_genres = set(str(game["genres"]).lower().split(";"))
    game_price = game["price_inr"]
    game_rating = game["rating_pct"]

    scores = []
    for _, row in df.iterrows():
        if row["name"] == game_name:
            continue

        # Genre overlap score (0–1)
        row_genres = set(str(row["genres"]).lower().split(";"))
        union = game_genres | row_genres
        intersection = game_genres & row_genres
        genre_score = len(intersection) / len(union) if union else 0

        # Rating similarity (0–1)
        rating_diff = abs(row["rating_pct"] - game_rating)
        rating_score = max(0, 1 - rating_diff / 100)

        # Price proximity (0–1)
        max_price = df["price_inr"].max() or 1
        price_diff = abs(row["price_inr"] - game_price)
        price_score = max(0, 1 - price_diff / max_price)

        match = round((0.5 * genre_score + 0.3 * rating_score + 0.2 * price_score) * 100, 1)
        scores.append((row, match))

    scores.sort(key=lambda x: x[1], reverse=True)
    top = scores[:top_n]
    if not top:
        return pd.DataFrame()

    result = pd.DataFrame([r[0] for r in top])
    result["match_score"] = [r[1] for r in top]
    return result


# ─────────────────────────────────────────
#  AI-STYLE DESCRIPTION
# ─────────────────────────────────────────
def generate_description(row: pd.Series) -> str:
    """Generate a dynamic AI-style description from game attributes."""
    name = row["name"]
    genres = str(row["genres"]).replace(";", ", ")
    rating = row["rating_pct"]
    playtime = int(row["average_playtime"])
    price_inr = row["price_inr"]

    sentiment = (
        "universally loved" if rating >= 90 else
        "highly acclaimed" if rating >= 80 else
        "well-received" if rating >= 70 else
        "mixed-reviewed" if rating >= 50 else
        "polarizing"
    )

    playtime_desc = (
        "a quick pick-up-and-play experience" if playtime < 200 else
        "a moderately engaging journey" if playtime < 600 else
        "a deep, time-sinking adventure" if playtime < 1200 else
        "an endlessly replayable epic"
    )

    price_desc = (
        "free-to-play" if price_inr == 0 else
        f"budget-friendly at ₹{price_inr:.0f}" if price_inr < 500 else
        f"mid-range at ₹{price_inr:.0f}" if price_inr < 2000 else
        f"premium-priced at ₹{price_inr:.0f}"
    )

    desc = (
        f"**{name}** is a {sentiment} title in the **{genres}** space. "
        f"It offers {playtime_desc} with an average of **{playtime} minutes** "
        f"of gameplay, and is {price_desc}. "
    )

    if "Multiplayer" in str(row["genres"]) or "Multi-player" in str(row.get("categories", "")):
        desc += "Its multiplayer component keeps the community thriving long after release. "

    if rating >= 85:
        desc += "Critics and players alike consistently praise this title as a must-play."
    elif rating >= 70:
        desc += "Most players find great value in this game's core experience."
    else:
        desc += "A niche title that resonates deeply with its dedicated fanbase."

    return desc


# ─────────────────────────────────────────
#  GAME DNA RADAR CHART
# ─────────────────────────────────────────
def render_dna_chart(row: pd.Series):
    """Plotly Radar (Spider) chart for game DNA."""
    values = []
    for cat in DNA_CATEGORIES:
        val = 1.0 if cat.lower() in str(row["genres"]).lower() else 0.2
        values.append(val)

    fig = go.Figure(go.Scatterpolar(
        r=values + [values[0]],
        theta=DNA_CATEGORIES + [DNA_CATEGORIES[0]],
        fill="toself",
        fillcolor="rgba(59, 130, 246, 0.2)",
        line=dict(color="#60a5fa", width=2),
        marker=dict(color="#60a5fa", size=7),
        name=str(row["name"])[:30],
    ))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(255,255,255,0.02)",
            radialaxis=dict(
                visible=True, range=[0, 1],
                tickfont=dict(color="#94a3b8", size=10),
                gridcolor="rgba(100,180,255,0.15)",
                linecolor="rgba(100,180,255,0.1)",
            ),
            angularaxis=dict(
                tickfont=dict(color="#cbd5e1", size=11),
                gridcolor="rgba(100,180,255,0.12)",
                linecolor="rgba(100,180,255,0.15)",
            ),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=50, r=50, t=40, b=40),
        height=340,
        showlegend=False,
    )
    return fig


# ─────────────────────────────────────────
#  GAME SIMILARITY MAP (PCA)
# ─────────────────────────────────────────
@st.cache_data(show_spinner=False)
def compute_pca_map(df_tuple):
    """Reduce game features to 2D via PCA for similarity scatter plot."""
    df = pd.DataFrame(df_tuple[1], columns=df_tuple[0])
    genre_cols = [c for c in df.columns if c.startswith("genre_")]
    scaler = MinMaxScaler()
    numeric_scaled = scaler.fit_transform(df[["positive_ratings", "price_inr", "average_playtime"]])
    genre_vals = df[genre_cols].values
    features = np.hstack([genre_vals, numeric_scaled])
    pca = PCA(n_components=2, random_state=42)
    coords = pca.fit_transform(features)
    return coords


# ─────────────────────────────────────────
#  GAME CARD RENDERER
# ─────────────────────────────────────────
def render_game_card(row: pd.Series, show_recommend_btn: bool = False,
                     key_prefix: str = ""):
    """Render a single glassmorphism game card."""
    price_label = "FREE" if row["price_inr"] == 0 else f"₹{row['price_inr']:.0f}"
    price_class = "price-free" if row["price_inr"] == 0 else ""
    rating_color = (
        "#34d399" if row["rating_pct"] >= 80 else
        "#fbbf24" if row["rating_pct"] >= 60 else "#f87171"
    )
    bar_pct = row["rating_pct"]

    img_url = get_game_image(int(row["appid"]))

    st.markdown(f"""
    <div class="game-card">
        <img src="{img_url}" style="width:100%;border-radius:10px;margin-bottom:10px;object-fit:cover;max-height:130px;" />
        <div style="font-size:1rem;font-weight:700;color:#e2e8f0;margin-bottom:6px;line-height:1.3;">{row['name']}</div>
        <div style="font-size:0.75rem;color:#94a3b8;margin-bottom:8px;">{str(row['genres']).replace(';',' · ')}</div>
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
            <span class="price-badge {price_class}">{price_label}</span>
            <span style="font-size:0.78rem;color:{rating_color};font-weight:600;">⭐ {row['rating_pct']:.1f}%</span>
        </div>
        <div class="rating-bar-wrap">
            <div class="rating-bar-fill" style="width:{bar_pct}%;background:linear-gradient(90deg,{rating_color},{rating_color}88);"></div>
        </div>
        <div style="margin-top:8px;">
            <span class="stat-chip">⏱ {int(row['average_playtime'])} min avg</span>
            <span class="stat-chip stat-chip-green">👍 {int(row['positive_ratings']):,}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if show_recommend_btn:
        if st.button("🔍 Recommend Similar", key=f"{key_prefix}_rec_{row['name'][:20]}"):
            st.session_state["recommend_game"] = row["name"]
            st.session_state["show_recommendations"] = True


# ─────────────────────────────────────────
#  RECOMMENDATION CARD RENDERER
# ─────────────────────────────────────────
def render_rec_card(row: pd.Series, match_score: float):
    price_label = "FREE" if row["price_inr"] == 0 else f"₹{row['price_inr']:.0f}"
    img_url = get_game_image(int(row["appid"]))
    st.markdown(f"""
    <div class="glass-card" style="display:flex;gap:14px;align-items:center;">
        <img src="{img_url}" style="width:120px;height:60px;object-fit:cover;border-radius:8px;flex-shrink:0;" />
        <div style="flex:1;min-width:0;">
            <div style="font-weight:700;color:#e2e8f0;font-size:0.95rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{row['name']}</div>
            <div style="font-size:0.73rem;color:#94a3b8;margin:2px 0;">{str(row['genres']).replace(';',' · ')}</div>
            <div style="display:flex;gap:8px;align-items:center;margin-top:4px;">
                <span class="stat-chip">⭐ {row['rating_pct']:.1f}%</span>
                <span class="price-badge" style="font-size:0.75rem;padding:2px 8px;">{'FREE' if row['price_inr']==0 else f'₹{row["price_inr"]:.0f}'}</span>
            </div>
        </div>
        <div style="text-align:center;flex-shrink:0;">
            <div class="match-score">{match_score:.0f}%</div>
            <div style="font-size:0.68rem;color:#94a3b8;">match</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────
#  PLOTLY CHART STYLE
# ─────────────────────────────────────────
CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#cbd5e1"),
    xaxis=dict(gridcolor="rgba(100,180,255,0.1)", linecolor="rgba(100,180,255,0.2)"),
    yaxis=dict(gridcolor="rgba(100,180,255,0.1)", linecolor="rgba(100,180,255,0.2)"),
    margin=dict(l=40, r=20, t=40, b=40),
)


# ─────────────────────────────────────────
#  MAIN APP
# ─────────────────────────────────────────
def main():
    # ── Load data ──────────────────────────
    with st.spinner("Loading game data..."):
        df = load_data()

    all_genres = get_all_genres(df)

    # ── Session state init ──────────────────
    if "recommend_game" not in st.session_state:
        st.session_state["recommend_game"] = None
    if "show_recommendations" not in st.session_state:
        st.session_state["show_recommendations"] = False

    # ─────────────────────────────────────────
    #  SIDEBAR
    # ─────────────────────────────────────────
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center;padding:16px 0 8px;">
            <span style="font-size:2.2rem;">🎮</span>
            <div style="font-size:1.1rem;font-weight:800;background:linear-gradient(90deg,#60a5fa,#a78bfa);
                        -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                        background-clip:text;margin-top:4px;">Steam Discovery</div>
            <div style="font-size:0.7rem;color:#64748b;margin-top:2px;">Analytics Platform</div>
        </div>
        <div class="gradient-divider" style="margin:12px 0;"></div>
        """, unsafe_allow_html=True)

        st.markdown("**🎯 Genre**")
        genre_filter = st.selectbox("Genre", ["All"] + all_genres, label_visibility="collapsed")

        st.markdown("**🕹️ Player Style**")
        player_style = st.selectbox(
            "Player Style",
            ["All", "Casual", "Hardcore", "Competitive", "Story Lover"],
            label_visibility="collapsed"
        )

        st.markdown("**💰 Price Range (₹)**")
        max_price_inr = int(df["price_inr"].max()) + 1
        price_range = st.slider("Price (INR)", 0, max_price_inr, (0, max_price_inr),
                                 step=100, label_visibility="collapsed")

        st.markdown("**⭐ Minimum Positive Ratings**")
        min_ratings = st.slider("Min Ratings", 0, int(df["positive_ratings"].max()),
                                 1000, step=500, label_visibility="collapsed",
                                 format="%d")

        st.markdown("**🔧 Options**")
        free_only = st.checkbox("🆓 Free-to-Play Only", value=False)

        st.markdown("**📊 Sort By**")
        sort_by = st.selectbox("Sort By",
                                ["Recommended", "Popularity", "Price", "Playtime"],
                                label_visibility="collapsed")

        st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

        st.markdown("**🔎 Search Game**")
        game_names = sorted(df["name"].tolist())
        search_game = st.selectbox("Search Game", ["— Select a game —"] + game_names,
                                    label_visibility="collapsed")

        # Quick stats
        st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="text-align:center;">
            <div style="color:#94a3b8;font-size:0.7rem;text-transform:uppercase;letter-spacing:0.07em;">Total Games</div>
            <div style="font-size:1.6rem;font-weight:800;color:#60a5fa;">{len(df):,}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Apply Filters ───────────────────────
    filtered_df = apply_filters(df, genre_filter, player_style,
                                 price_range, min_ratings, free_only, sort_by)

    # ─────────────────────────────────────────
    #  HERO BANNER
    # ─────────────────────────────────────────
    st.markdown(f"""
    <div class="hero-banner">
        <div style="font-size:0.72rem;color:#60a5fa;text-transform:uppercase;letter-spacing:0.12em;margin-bottom:6px;">🎮 Steam Analytics Platform</div>
        <div style="font-size:2.2rem;font-weight:900;color:#e2e8f0;line-height:1.1;margin-bottom:8px;">
            Discover Your Next <span style="background:linear-gradient(90deg,#60a5fa,#a78bfa,#38bdf8);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">Favorite Game</span>
        </div>
        <div style="color:#94a3b8;font-size:0.95rem;">
            Explore {len(filtered_df):,} games · Smart recommendations · Deep analytics
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Summary Metrics ─────────────────────
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("🎮 Games Found", f"{len(filtered_df):,}")
    with m2:
        avg_rating = filtered_df["rating_pct"].mean() if not filtered_df.empty else 0
        st.metric("⭐ Avg Rating", f"{avg_rating:.1f}%")
    with m3:
        free_count = int((filtered_df["price_inr"] == 0).sum())
        st.metric("🆓 Free Games", f"{free_count:,}")
    with m4:
        avg_playtime = int(filtered_df["average_playtime"].mean()) if not filtered_df.empty else 0
        st.metric("⏱ Avg Playtime", f"{avg_playtime:,} min")

    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

    # ─────────────────────────────────────────
    #  GAME DETAIL (Search-selected game)
    # ─────────────────────────────────────────
    if search_game and search_game != "— Select a game —":
        game_row = df[df["name"] == search_game]
        if not game_row.empty:
            game_data = game_row.iloc[0]
            st.markdown(f'<div class="section-title">🎯 {game_data["name"]}</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-subtitle">Game Profile & Analytics</div>', unsafe_allow_html=True)

            col_img, col_desc, col_dna = st.columns([1.4, 2, 1.6])

            with col_img:
                img_url = get_game_image(int(game_data["appid"]))
                st.image(img_url, use_container_width=True)
                price_label = "FREE" if game_data["price_inr"] == 0 else f"₹{game_data['price_inr']:.0f}"
                st.markdown(f"""
                <div style="margin-top:10px;text-align:center;">
                    <span class="price-badge {'price-free' if game_data['price_inr']==0 else ''}" style="font-size:1.1rem;padding:6px 18px;">{price_label}</span>
                </div>
                <div style="margin-top:10px;text-align:center;">
                    <span class="stat-chip stat-chip-green">👍 {int(game_data['positive_ratings']):,}</span>
                    <span class="stat-chip stat-chip-purple">👎 {int(game_data['negative_ratings']):,}</span>
                </div>
                """, unsafe_allow_html=True)

            with col_desc:
                st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)
                # Genre chips
                for g in str(game_data["genres"]).split(";"):
                    st.markdown(f'<span class="stat-chip stat-chip-purple">{g.strip()}</span>',
                                unsafe_allow_html=True)
                st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)

                # Rating bar
                rp = game_data["rating_pct"]
                rc = "#34d399" if rp >= 80 else "#fbbf24" if rp >= 60 else "#f87171"
                st.markdown(f"""
                <div style="margin-bottom:12px;">
                    <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                        <span style="color:#94a3b8;font-size:0.8rem;">Approval Rating</span>
                        <span style="color:{rc};font-weight:700;">{rp:.1f}%</span>
                    </div>
                    <div class="rating-bar-wrap" style="height:10px;">
                        <div class="rating-bar-fill" style="width:{rp}%;background:{rc};"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # AI Description
                st.markdown('<div style="margin-bottom:6px;color:#94a3b8;font-size:0.78rem;text-transform:uppercase;letter-spacing:0.07em;">✨ AI Description</div>', unsafe_allow_html=True)
                desc = generate_description(game_data)
                st.markdown(f'<div style="font-size:0.88rem;color:#cbd5e1;line-height:1.6;">{desc}</div>',
                            unsafe_allow_html=True)

                st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)
                st.markdown(f"""
                <span class="stat-chip stat-chip-amber">⏱ {int(game_data['average_playtime'])} min avg playtime</span>
                """, unsafe_allow_html=True)

            with col_dna:
                st.markdown('<div style="color:#94a3b8;font-size:0.78rem;text-transform:uppercase;letter-spacing:0.07em;margin-bottom:4px;">🧬 Game DNA</div>', unsafe_allow_html=True)
                fig_dna = render_dna_chart(game_data)
                st.plotly_chart(fig_dna, use_container_width=True, config={"displayModeBar": False})

            # Recommend button
            st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
            if st.button(f"🤖 Recommend Games Similar to {game_data['name'][:35]}...",
                         use_container_width=True):
                st.session_state["recommend_game"] = game_data["name"]
                st.session_state["show_recommendations"] = True

    # ─────────────────────────────────────────
    #  RECOMMENDATIONS PANEL
    # ─────────────────────────────────────────
    if st.session_state.get("show_recommendations") and st.session_state.get("recommend_game"):
        rec_game = st.session_state["recommend_game"]
        st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="section-title">🤖 Games Similar to "{rec_game}"</div>',
                    unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">Powered by genre overlap · rating score · price factor</div>',
                    unsafe_allow_html=True)

        recs = compute_recommendations(df, rec_game)
        if recs.empty:
            st.info("No recommendations found. Try a different game.")
        else:
            for _, rec_row in recs.iterrows():
                render_rec_card(rec_row, rec_row["match_score"])

        if st.button("✕ Close Recommendations"):
            st.session_state["show_recommendations"] = False
            st.rerun()

    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

    # ─────────────────────────────────────────
    #  GAME TABS
    # ─────────────────────────────────────────
    st.markdown('<div class="section-title">🕹️ Game Browser</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Browse curated game collections</div>', unsafe_allow_html=True)

    tab_popular, tab_trending, tab_gems = st.tabs([
        "🔥 Popular Games", "📈 Trending Games", "💎 Hidden Gems"
    ])

    def render_game_grid(games_df: pd.DataFrame, tab_key: str):
        if games_df.empty:
            st.info("No games match current filters.")
            return
        cols_per_row = 4
        rows = [games_df.iloc[i:i+cols_per_row] for i in range(0, len(games_df), cols_per_row)]
        for row_data in rows:
            cols = st.columns(cols_per_row)
            for col, (_, game) in zip(cols, row_data.iterrows()):
                with col:
                    render_game_card(game, show_recommend_btn=True, key_prefix=tab_key)

    with tab_popular:
        pop_games = get_popular(filtered_df)
        render_game_grid(pop_games, "pop")

    with tab_trending:
        trend_games = get_trending(filtered_df)
        render_game_grid(trend_games, "trend")

    with tab_gems:
        gem_games = get_hidden_gems(filtered_df)
        render_game_grid(gem_games, "gems")

    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

    # ─────────────────────────────────────────
    #  COMPARE TWO GAMES
    # ─────────────────────────────────────────
    st.markdown('<div class="section-title">⚖️ Compare Two Games</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Side-by-side comparison of price, ratings and playtime</div>',
                unsafe_allow_html=True)

    c1, c2, c3 = st.columns([2, 2, 1])
    game_names_list = sorted(df["name"].tolist())
    with c1:
        game_a = st.selectbox("🎮 Game A", ["— Select —"] + game_names_list, key="cmp_a")
    with c2:
        game_b = st.selectbox("🎮 Game B", ["— Select —"] + game_names_list, key="cmp_b")
    with c3:
        st.markdown('<div style="height:28px;"></div>', unsafe_allow_html=True)
        compare_btn = st.button("⚡ Compare", use_container_width=True)

    if compare_btn and game_a != "— Select —" and game_b != "— Select —" and game_a != game_b:
        row_a = df[df["name"] == game_a].iloc[0]
        row_b = df[df["name"] == game_b].iloc[0]

        img_a = get_game_image(int(row_a["appid"]))
        img_b = get_game_image(int(row_b["appid"]))

        col_a, col_sep, col_b = st.columns([5, 0.5, 5])
        with col_a:
            st.image(img_a, use_container_width=True)
            st.markdown(f"<div style='text-align:center;font-weight:700;color:#e2e8f0;font-size:1.05rem;'>{game_a}</div>", unsafe_allow_html=True)
        with col_sep:
            st.markdown('<div style="height:80px;border-left:1px solid rgba(100,180,255,0.2);margin:auto;"></div>', unsafe_allow_html=True)
        with col_b:
            st.image(img_b, use_container_width=True)
            st.markdown(f"<div style='text-align:center;font-weight:700;color:#e2e8f0;font-size:1.05rem;'>{game_b}</div>", unsafe_allow_html=True)

        compare_data = {
            "Metric": ["💰 Price (₹)", "⭐ Rating %", "👍 Positive Ratings",
                        "👎 Negative Ratings", "⏱ Avg Playtime (min)"],
            game_a: [
                f"₹{row_a['price_inr']:.0f}" if row_a['price_inr'] > 0 else "FREE",
                f"{row_a['rating_pct']:.1f}%",
                f"{int(row_a['positive_ratings']):,}",
                f"{int(row_a['negative_ratings']):,}",
                f"{int(row_a['average_playtime']):,}",
            ],
            game_b: [
                f"₹{row_b['price_inr']:.0f}" if row_b['price_inr'] > 0 else "FREE",
                f"{row_b['rating_pct']:.1f}%",
                f"{int(row_b['positive_ratings']):,}",
                f"{int(row_b['negative_ratings']):,}",
                f"{int(row_b['average_playtime']):,}",
            ],
        }
        cmp_df = pd.DataFrame(compare_data)
        st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)
        st.dataframe(cmp_df.set_index("Metric"), use_container_width=True)

        # Radar comparison
        st.markdown('<div style="margin-top:16px;color:#94a3b8;font-size:0.78rem;text-transform:uppercase;letter-spacing:0.07em;">🧬 DNA Comparison</div>', unsafe_allow_html=True)
        col_dna_a, col_dna_b = st.columns(2)
        with col_dna_a:
            st.markdown(f"<div style='text-align:center;color:#60a5fa;font-weight:600;margin-bottom:4px;'>{game_a[:30]}</div>", unsafe_allow_html=True)
            st.plotly_chart(render_dna_chart(row_a), use_container_width=True, config={"displayModeBar": False})
        with col_dna_b:
            st.markdown(f"<div style='text-align:center;color:#a78bfa;font-weight:600;margin-bottom:4px;'>{game_b[:30]}</div>", unsafe_allow_html=True)
            fig_b = render_dna_chart(row_b)
            for trace in fig_b.data:
                trace.fillcolor = "rgba(139, 92, 246, 0.2)"
                trace.line.color = "#a78bfa"
                trace.marker.color = "#a78bfa"
            st.plotly_chart(fig_b, use_container_width=True, config={"displayModeBar": False})

    elif compare_btn:
        if game_a == game_b and game_a != "— Select —":
            st.warning("Please select two different games to compare.")
        else:
            st.warning("Please select both games to compare.")

    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

    # ─────────────────────────────────────────
    #  GAME SIMILARITY MAP
    # ─────────────────────────────────────────
    st.markdown('<div class="section-title">🗺️ Game Similarity Map</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">PCA-reduced 2D scatter — games close together share similar traits</div>',
                unsafe_allow_html=True)

    if len(filtered_df) >= 5:
        pca_df = filtered_df.copy()
        # Convert to hashable tuple for caching
        col_order = list(pca_df.columns)
        data_tuple = (col_order, [list(r) for r in pca_df.itertuples(index=False)])

        genre_cols = [c for c in pca_df.columns if c.startswith("genre_")]
        scaler = MinMaxScaler()
        numeric_scaled = scaler.fit_transform(pca_df[["positive_ratings", "price_inr", "average_playtime"]])
        genre_vals = pca_df[genre_cols].values
        features = np.hstack([genre_vals, numeric_scaled])
        pca = PCA(n_components=2, random_state=42)
        coords = pca.fit_transform(features)

        pca_df["pca_x"] = coords[:, 0]
        pca_df["pca_y"] = coords[:, 1]
        pca_df["label"] = pca_df.apply(lambda r: f"{r['name'][:25]}<br>⭐{r['rating_pct']:.0f}% | {('FREE' if r['price_inr']==0 else '₹'+str(int(r['price_inr'])))}", axis=1)

        # Color by primary genre
        primary_genre = pca_df["genres"].str.split(";").str[0].str.strip()
        color_seq = ["#60a5fa", "#a78bfa", "#34d399", "#fbbf24", "#f87171",
                     "#38bdf8", "#fb923c", "#e879f9", "#4ade80", "#f472b6"]

        fig_pca = px.scatter(
            pca_df, x="pca_x", y="pca_y",
            color=primary_genre,
            hover_name="name",
            hover_data={"pca_x": False, "pca_y": False, "rating_pct": ":.1f",
                        "price_inr": ":.0f", "average_playtime": True},
            color_discrete_sequence=color_seq,
            size="positive_ratings",
            size_max=28,
        )
        fig_pca.update_traces(
            marker=dict(opacity=0.82, line=dict(width=0.5, color="rgba(255,255,255,0.2)")),
        )
        fig_pca.update_layout(
            **CHART_LAYOUT,
            height=480,
            legend=dict(
                font=dict(color="#94a3b8", size=11),
                bgcolor="rgba(10,14,26,0.7)",
                bordercolor="rgba(100,180,255,0.2)",
                borderwidth=1,
            ),
            xaxis_title="Component 1",
            yaxis_title="Component 2",
        )
        st.plotly_chart(fig_pca, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("Apply broader filters to see the similarity map (need at least 5 games).")

    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

    # ─────────────────────────────────────────
    #  DATA VISUALIZATION DASHBOARD
    # ─────────────────────────────────────────
    st.markdown('<div class="section-title">📊 Analytics Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Explore price distributions, ratings spread and market insights</div>',
                unsafe_allow_html=True)

    dash_df = filtered_df if not filtered_df.empty else df

    # Row 1: Price distribution + Ratings distribution
    ch1, ch2 = st.columns(2)

    with ch1:
        paid_games = dash_df[dash_df["price_inr"] > 0]
        fig_price = px.histogram(
            paid_games, x="price_inr", nbins=30,
            title="💰 Price Distribution (Paid Games, ₹)",
            color_discrete_sequence=["#60a5fa"],
        )
        fig_price.update_traces(marker_line_width=0.5, marker_line_color="rgba(255,255,255,0.1)")
        fig_price.update_layout(**CHART_LAYOUT, height=340, title_font_color="#e2e8f0")
        st.plotly_chart(fig_price, use_container_width=True, config={"displayModeBar": False})

    with ch2:
        fig_rating = px.histogram(
            dash_df, x="rating_pct", nbins=20,
            title="⭐ Rating Distribution (%)",
            color_discrete_sequence=["#a78bfa"],
        )
        fig_rating.update_traces(marker_line_width=0.5, marker_line_color="rgba(255,255,255,0.1)")
        fig_rating.update_layout(**CHART_LAYOUT, height=340, title_font_color="#e2e8f0")
        st.plotly_chart(fig_rating, use_container_width=True, config={"displayModeBar": False})

    # Row 2: Scatter (price vs ratings) + Top genres bar
    ch3, ch4 = st.columns(2)

    with ch3:
        fig_scatter = px.scatter(
            dash_df.head(200), x="price_inr", y="rating_pct",
            size="positive_ratings", size_max=30,
            color="rating_pct",
            color_continuous_scale=["#f87171", "#fbbf24", "#34d399"],
            hover_name="name",
            title="📈 Price vs. Rating (bubble = popularity)",
            labels={"price_inr": "Price (₹)", "rating_pct": "Rating %"},
        )
        fig_scatter.update_traces(marker=dict(opacity=0.75))
        fig_scatter.update_layout(**CHART_LAYOUT, height=360, title_font_color="#e2e8f0",
                                   coloraxis_showscale=False)
        st.plotly_chart(fig_scatter, use_container_width=True, config={"displayModeBar": False})

    with ch4:
        # Genre popularity bar
        genre_counts = {}
        for g_str in dash_df["genres"].dropna():
            for g in g_str.split(";"):
                g = g.strip()
                if g:
                    genre_counts[g] = genre_counts.get(g, 0) + 1
        genre_series = pd.Series(genre_counts).sort_values(ascending=True).tail(12)
        fig_genres = go.Figure(go.Bar(
            x=genre_series.values, y=genre_series.index,
            orientation="h",
            marker=dict(
                color=genre_series.values,
                colorscale=[[0, "#3b82f6"], [0.5, "#8b5cf6"], [1.0, "#06b6d4"]],
                line=dict(width=0),
            ),
        ))
        # Merge yaxis config from CHART_LAYOUT with additional tickfont
        merged_yaxis = {**CHART_LAYOUT["yaxis"], "tickfont": {"color": "#cbd5e1", "size": 11}}
        layout_config = {**CHART_LAYOUT, "height": 360, "yaxis": merged_yaxis, "title": "🎭 Genre Distribution", "title_font_color": "#e2e8f0"}
        fig_genres.update_layout(**layout_config)
        st.plotly_chart(fig_genres, use_container_width=True, config={"displayModeBar": False})

    # Row 3: Playtime distribution
    fig_playtime = px.box(
        dash_df[dash_df["average_playtime"] < dash_df["average_playtime"].quantile(0.95)],
        x="average_playtime",
        title="⏱ Average Playtime Distribution (minutes)",
        color_discrete_sequence=["#38bdf8"],
        points="outliers",
    )
    fig_playtime.update_layout(**CHART_LAYOUT, height=260, title_font_color="#e2e8f0")
    st.plotly_chart(fig_playtime, use_container_width=True, config={"displayModeBar": False})

    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

    # ─────────────────────────────────────────
    #  RAW DATA EXPANDER
    # ─────────────────────────────────────────
    with st.expander("📋 Raw Data Explorer"):
        display_cols = ["name", "genres", "price_inr", "positive_ratings",
                        "negative_ratings", "rating_pct", "average_playtime"]
        show_df = filtered_df[display_cols].rename(columns={
            "name": "Name", "genres": "Genres",
            "price_inr": "Price (₹)", "positive_ratings": "Positive",
            "negative_ratings": "Negative", "rating_pct": "Rating %",
            "average_playtime": "Avg Playtime (min)"
        })
        st.dataframe(show_df, use_container_width=True, height=380)
        st.download_button(
            "⬇️ Download CSV", show_df.to_csv(index=False).encode("utf-8"),
            file_name="steam_filtered.csv", mime="text/csv"
        )

    # ── Footer ──────────────────────────────
    st.markdown("""
    <div style="text-align:center;padding:32px 0 16px;color:#475569;font-size:0.78rem;">
        <div style="margin-bottom:4px;">
            🎮 <strong style="color:#64748b;">Steam Discovery Dashboard</strong> · Built with Streamlit & Python
        </div>
        <div>Data sourced from Steam API · Prices converted to INR (rate: ₹82/USD)</div>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
