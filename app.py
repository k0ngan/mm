"""
Smart Balance - App para estudiantes trabajadores
Ejecutar con: streamlit run app.py
"""

import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Smart Balance",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ════════════════════════════════════════════════════════════════════════════════
# MOTOR DE TEMAS
# Tokens semánticos centralizados. Cada tema aporta valores OKLCH con contraste
# WCAG AA verificado. Los roles "fondo" y "texto" del color de marca se separan
# (--color-primary vs --color-accent) para evitar acentos ilegibles en modo oscuro.
# ════════════════════════════════════════════════════════════════════════════════

FONTS = {
    "fd": "'Josefin Sans', system-ui, -apple-system, sans-serif",
    "fb": "'Figtree', system-ui, -apple-system, sans-serif",
}
RADII = {"sm": "8px", "md": "12px", "lg": "18px", "xl": "24px"}

# Paletas de categorías (fondo, texto) — claro: fondo tenue + texto saturado;
# oscuro: fondo profundo + texto claro. Todas con contraste ≥ 4.5:1.
LIGHT_CATS = {
    "Trabajo":  ("oklch(0.938 0.026 17.6)", "oklch(0.350 0.118 25.7)"),
    "Estudio":  ("oklch(0.942 0.026 266.6)", "oklch(0.334 0.134 268.1)"),
    "Descanso": ("oklch(0.949 0.031 145.3)", "oklch(0.410 0.123 142.9)"),
    "Tarea":    ("oklch(0.961 0.030 77.0)", "oklch(0.408 0.087 61.2)"),
}
DARK_CATS = {
    "Trabajo":  ("oklch(0.311 0.059 16.3)", "oklch(0.871 0.054 18.2)"),
    "Estudio":  ("oklch(0.316 0.057 264.4)", "oklch(0.875 0.055 265.8)"),
    "Descanso": ("oklch(0.329 0.057 148.1)", "oklch(0.896 0.065 146.4)"),
    "Tarea":    ("oklch(0.358 0.050 81.7)", "oklch(0.900 0.068 83.6)"),
}

# Paletas de estados de ánimo (fondo, texto).
LIGHT_MOODS = {
    "feliz":     ("oklch(0.988 0.026 99.9)", "oklch(0.463 0.095 93.4)"),
    "bien":      ("oklch(0.973 0.029 137.4)", "oklch(0.410 0.123 142.9)"),
    "normal":    ("oklch(0.961 0.018 240.0)", "oklch(0.358 0.098 252.8)"),
    "estresada": ("oklch(0.948 0.029 298.9)", "oklch(0.333 0.150 293.0)"),
    "agotada":   ("oklch(0.949 0.024 351.3)", "oklch(0.363 0.118 358.5)"),
}
DARK_MOODS = {
    "feliz":     ("oklch(0.327 0.049 93.4)", "oklch(0.928 0.078 96.5)"),
    "bien":      ("oklch(0.329 0.057 148.1)", "oklch(0.896 0.065 146.4)"),
    "normal":    ("oklch(0.307 0.048 250.7)", "oklch(0.884 0.047 243.4)"),
    "estresada": ("oklch(0.290 0.083 293.3)", "oklch(0.861 0.065 300.9)"),
    "agotada":   ("oklch(0.290 0.055 348.0)", "oklch(0.870 0.060 349.8)"),
}

THEMES = {
    "Claro Lavanda": {
        "is_dark": False,
        "bg": "oklch(0.970 0.011 292)", "surface": "oklch(0.998 0.003 292)",
        "surface_alt": "oklch(0.962 0.013 292)",
        "text": "oklch(0.215 0.050 292)", "text_muted": "oklch(0.425 0.038 292)",
        "text_subtle": "oklch(0.560 0.024 292)",
        "border": "oklch(0.892 0.020 292)", "border_strong": "oklch(0.852 0.028 292)",
        "primary": "oklch(0.520 0.140 292)", "primary_hover": "oklch(0.450 0.140 292)",
        "on_primary": "oklch(0.990 0.003 292)", "accent": "oklch(0.500 0.150 292)",
        "secondary": "oklch(0.530 0.110 218)", "secondary_soft": "oklch(0.940 0.045 218)",
        "primary_soft": "oklch(0.940 0.045 292)", "primary_tint": "oklch(0.968 0.018 292)",
        "shadow_sm": "0 1px 3px oklch(0.52 0.14 292/0.10),0 1px 2px oklch(0.52 0.14 292/0.06)",
        "shadow_md": "0 4px 16px oklch(0.52 0.14 292/0.12),0 2px 6px oklch(0.52 0.14 292/0.07)",
        "cats": LIGHT_CATS, "moods": LIGHT_MOODS,
    },
    "Claro Azul": {
        "is_dark": False,
        "bg": "oklch(0.972 0.011 255)", "surface": "oklch(0.998 0.003 255)",
        "surface_alt": "oklch(0.962 0.014 255)",
        "text": "oklch(0.220 0.045 255)", "text_muted": "oklch(0.430 0.040 255)",
        "text_subtle": "oklch(0.560 0.026 255)",
        "border": "oklch(0.892 0.022 255)", "border_strong": "oklch(0.852 0.030 255)",
        "primary": "oklch(0.510 0.130 255)", "primary_hover": "oklch(0.440 0.130 255)",
        "on_primary": "oklch(0.990 0.003 255)", "accent": "oklch(0.490 0.140 255)",
        "secondary": "oklch(0.560 0.100 205)", "secondary_soft": "oklch(0.940 0.040 205)",
        "primary_soft": "oklch(0.940 0.045 255)", "primary_tint": "oklch(0.968 0.018 255)",
        "shadow_sm": "0 1px 3px oklch(0.45 0.13 255/0.10),0 1px 2px oklch(0.45 0.13 255/0.06)",
        "shadow_md": "0 4px 16px oklch(0.45 0.13 255/0.12),0 2px 6px oklch(0.45 0.13 255/0.07)",
        "cats": LIGHT_CATS, "moods": LIGHT_MOODS,
    },
    "Claro Verde": {
        "is_dark": False,
        "bg": "oklch(0.972 0.012 158)", "surface": "oklch(0.998 0.004 158)",
        "surface_alt": "oklch(0.962 0.015 158)",
        "text": "oklch(0.220 0.045 160)", "text_muted": "oklch(0.415 0.040 160)",
        "text_subtle": "oklch(0.545 0.030 160)",
        "border": "oklch(0.890 0.024 158)", "border_strong": "oklch(0.850 0.032 158)",
        "primary": "oklch(0.480 0.110 158)", "primary_hover": "oklch(0.410 0.110 158)",
        "on_primary": "oklch(0.992 0.004 158)", "accent": "oklch(0.450 0.120 158)",
        "secondary": "oklch(0.560 0.100 235)", "secondary_soft": "oklch(0.940 0.040 235)",
        "primary_soft": "oklch(0.935 0.050 158)", "primary_tint": "oklch(0.966 0.020 158)",
        "shadow_sm": "0 1px 3px oklch(0.45 0.10 158/0.10),0 1px 2px oklch(0.45 0.10 158/0.06)",
        "shadow_md": "0 4px 16px oklch(0.45 0.10 158/0.12),0 2px 6px oklch(0.45 0.10 158/0.07)",
        "cats": LIGHT_CATS, "moods": LIGHT_MOODS,
    },
    "Claro Neutro": {
        "is_dark": False,
        "bg": "oklch(0.968 0.004 270)", "surface": "oklch(0.999 0.001 270)",
        "surface_alt": "oklch(0.957 0.005 270)",
        "text": "oklch(0.225 0.012 270)", "text_muted": "oklch(0.440 0.010 270)",
        "text_subtle": "oklch(0.565 0.008 270)",
        "border": "oklch(0.888 0.006 270)", "border_strong": "oklch(0.848 0.008 270)",
        "primary": "oklch(0.400 0.020 270)", "primary_hover": "oklch(0.320 0.022 270)",
        "on_primary": "oklch(0.995 0.001 270)", "accent": "oklch(0.380 0.030 270)",
        "secondary": "oklch(0.540 0.080 235)", "secondary_soft": "oklch(0.935 0.030 235)",
        "primary_soft": "oklch(0.930 0.006 270)", "primary_tint": "oklch(0.962 0.004 270)",
        "shadow_sm": "0 1px 3px oklch(0.30 0.01 270/0.10),0 1px 2px oklch(0.30 0.01 270/0.06)",
        "shadow_md": "0 4px 16px oklch(0.30 0.01 270/0.11),0 2px 6px oklch(0.30 0.01 270/0.07)",
        "cats": LIGHT_CATS, "moods": LIGHT_MOODS,
    },
    "Oscuro Lavanda": {
        "is_dark": True,
        "bg": "oklch(0.190 0.030 292)", "surface": "oklch(0.245 0.035 292)",
        "surface_alt": "oklch(0.300 0.038 292)",
        "text": "oklch(0.945 0.012 292)", "text_muted": "oklch(0.795 0.022 292)",
        "text_subtle": "oklch(0.665 0.028 292)",
        "border": "oklch(0.355 0.035 292)", "border_strong": "oklch(0.435 0.045 292)",
        "primary": "oklch(0.640 0.150 292)", "primary_hover": "oklch(0.700 0.150 292)",
        "on_primary": "oklch(0.160 0.040 292)", "accent": "oklch(0.810 0.130 292)",
        "secondary": "oklch(0.730 0.110 218)", "secondary_soft": "oklch(0.320 0.050 218)",
        "primary_soft": "oklch(0.320 0.050 292)", "primary_tint": "oklch(0.278 0.038 292)",
        "shadow_sm": "0 1px 3px oklch(0 0 0/0.40),0 1px 2px oklch(0 0 0/0.30)",
        "shadow_md": "0 6px 20px oklch(0 0 0/0.45),0 2px 8px oklch(0 0 0/0.35)",
        "cats": DARK_CATS, "moods": DARK_MOODS,
    },
}

DEFAULT_THEME = "Claro Lavanda"

# Texto de las recomendaciones de bienestar (se mantiene idéntico; los colores
# salen del tema activo). El primer valor de cada tupla es la clave de la paleta.
MOOD_TEXT = {
    "😊 Feliz":     ("feliz",     "¡Qué buena energía! Aprovéchala para esos temas difíciles. Hoy es un gran día para avanzar con tus metas más retadoras. Comparte tu buena vibra con quienes te rodean. ✨"),
    "🙂 Bien":      ("bien",      "Estás en un buen punto de equilibrio. Mantén tus hábitos de estudio y descanso. Una caminata corta puede mantenerte así todo el día. 🌿"),
    "😐 Normal":    ("normal",    "Día tranquilo. Haz una lista de prioridades y empieza por la más pequeña. A veces el movimiento crea motivación. 📋"),
    "😰 Estresada": ("estresada", "Tómate un respiro antes de continuar. Prueba la respiración guiada abajo. Divide tus tareas en partes pequeñas y recuerda: no tienes que hacerlo todo hoy. 💜"),
    "😩 Agotada":   ("agotada",   "Tu mente y cuerpo necesitan recuperarse. Prioriza el descanso sobre cualquier tarea. Una siesta de 20 min puede hacer maravillas. Hoy, solo lo esencial. 🌙"),
}


# ── Reglas CSS estáticas (solo referencian tokens var(--color-*) / fuentes / radios) ──
STATIC_CSS = """
*,*::before,*::after { box-sizing:border-box; }

html,body,[class*="css"] {
    font-family: var(--fb) !important;
    color: var(--color-text);
}

.stApp { background: var(--color-bg) !important; }
[data-testid="stHeader"] { background: transparent !important; }

.main .block-container {
    animation: pageIn 0.22s ease-out both;
    padding-top: 2.5rem !important;
}
@keyframes pageIn {
    from { opacity:0; transform:translateY(6px); }
    to   { opacity:1; transform:translateY(0); }
}
@media (prefers-reduced-motion: reduce) {
    .main .block-container { animation: none; }
    * { transition: none !important; }
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--color-surface) !important;
    border-right: 1px solid var(--color-border) !important;
}
[data-testid="stSidebar"] * { color: var(--color-text); }
[data-testid="stSidebar"] .stRadio > div > label {
    border-radius: var(--radius-md) !important;
    padding: 9px 14px !important;
    margin: 2px 0 !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    transition: background 0.12s !important;
    cursor: pointer !important;
    display: block !important;
}
[data-testid="stSidebar"] .stRadio > div > label:hover {
    background: var(--color-surface-alt) !important;
}

/* ── Typography ── */
h1,h2,h3,h4 { font-family: var(--fd) !important; }
h1 {
    font-weight:700 !important;
    font-size:clamp(1.75rem,2.5vw,2.4rem) !important;
    letter-spacing:-0.025em !important;
    color:var(--color-text) !important;
    line-height:1.15 !important;
}
h2 { font-weight:600 !important; color:var(--color-text) !important; letter-spacing:-0.01em !important; }
h3 { font-weight:600 !important; color:var(--color-text-muted) !important; font-size:1.05rem !important; }

/* ── Cards — sin border-left stripes ── */
.card {
    background:var(--color-surface); border-radius:var(--radius-xl);
    padding:24px; margin:12px 0;
    box-shadow:var(--shadow-sm); border:1px solid var(--color-border);
    transition: box-shadow 0.2s;
}
.card:hover { box-shadow:var(--shadow-md); }
.card-tinted {
    background:var(--color-primary-tint); border-radius:var(--radius-xl);
    padding:24px; margin:12px 0; border:1px solid var(--color-border);
}
.card-teal {
    background:var(--color-secondary-soft); border-radius:var(--radius-xl);
    padding:24px; margin:12px 0; border:1px solid var(--color-border);
}

/* ── Score ring ── */
.score-wrap {
    background:var(--color-surface); border-radius:var(--radius-xl);
    padding:32px 24px; box-shadow:var(--shadow-md);
    border:1px solid var(--color-border); text-align:center;
}
.score-ring {
    width:110px; height:110px; border-radius:50%;
    background: conic-gradient(
        var(--color-accent) 0% calc(var(--p)*1%),
        var(--color-surface-alt) calc(var(--p)*1%) 100%
    );
    display:flex; align-items:center; justify-content:center;
    margin:12px auto 14px; position:relative;
}
.score-ring::after {
    content:''; position:absolute;
    width:84px; height:84px;
    background:var(--color-surface); border-radius:50%;
}
.score-num {
    position:relative; z-index:1;
    font-family:var(--fd); font-size:1.7rem; font-weight:700;
    color:var(--color-accent); line-height:1;
}
.score-cap {
    font-size:10px; font-weight:700; text-transform:uppercase;
    letter-spacing:0.14em; color:var(--color-text-subtle);
}
.score-sub { font-size:14px; font-weight:500; color:var(--color-text-muted); margin-top:8px; }

/* ── Stat cards ── */
.stat-card {
    background:var(--color-surface); border-radius:var(--radius-lg);
    padding:20px 16px; box-shadow:var(--shadow-sm); border:1px solid var(--color-border);
    text-align:center; transition: transform 0.2s, box-shadow 0.2s;
}
.stat-card:hover { transform:translateY(-2px); box-shadow:var(--shadow-md); }
.stat-num {
    font-family:var(--fd); font-size:2.2rem; font-weight:700;
    color:var(--color-accent); line-height:1; margin-bottom:8px;
}
.stat-lbl {
    font-size:11px; font-weight:700; text-transform:uppercase;
    letter-spacing:0.06em; color:var(--color-text-subtle);
    line-height:1.35; text-wrap:balance; hyphens:none;
}

/* ── Progress bars ── */
.prog-row { margin:4px 0 14px; }
.prog-head {
    display:flex; justify-content:space-between;
    align-items:baseline; margin-bottom:6px;
}
.prog-head span { font-size:13px; font-weight:600; color:var(--color-text-muted); }
.prog-head b { font-family:var(--fd); font-size:12px; font-weight:700; color:var(--color-accent); }
.prog-track { background:var(--color-surface-alt); border-radius:100px; height:5px; overflow:hidden; }
.prog-fill { height:100%; border-radius:100px; background:var(--color-accent); }
.prog-fill-teal { background:var(--color-secondary); }

/* ── Eyebrow label ── */
.eyebrow {
    font-family:var(--fd); font-size:10px; font-weight:700;
    text-transform:uppercase; letter-spacing:0.14em; color:var(--color-accent);
    margin-bottom:4px;
}

/* ── Buttons ── */
.stButton>button {
    background:var(--color-primary) !important;
    color:var(--color-on-primary) !important;
    border:none !important; border-radius:100px !important;
    font-family:var(--fb) !important; font-weight:600 !important;
    font-size:13px !important; padding:10px 22px !important;
    letter-spacing:0.01em !important;
    box-shadow:var(--shadow-sm) !important;
    transition:transform 0.12s ease,box-shadow 0.12s ease,background 0.12s ease !important;
}
.stButton>button:hover {
    background:var(--color-primary-hover) !important;
    transform:translateY(-1px) !important; box-shadow:var(--shadow-md) !important;
}
.stButton>button:active { transform:translateY(0) !important; }
.stButton>button:focus-visible {
    outline:3px solid var(--color-accent) !important; outline-offset:2px !important;
}

/* ── Inputs ── */
.stTextInput>div>div>input,
.stTextArea textarea {
    border-radius:var(--radius-sm) !important;
    border:1.5px solid var(--color-border-strong) !important;
    background:var(--color-surface) !important; font-family:var(--fb) !important;
    font-size:14px !important; color:var(--color-text) !important;
    padding:10px 14px !important;
    transition:border-color 0.15s,box-shadow 0.15s !important;
}
.stTextInput>div>div>input::placeholder,
.stTextArea textarea::placeholder { color:var(--color-text-subtle) !important; }
.stTextInput>div>div>input:focus,
.stTextArea textarea:focus {
    border-color:var(--color-primary) !important;
    box-shadow:0 0 0 3px color-mix(in oklch, var(--color-primary) 25%, transparent) !important;
    outline:none !important;
}
.stSelectbox>div>div {
    border-radius:var(--radius-sm) !important;
    border:1.5px solid var(--color-border-strong) !important;
    background:var(--color-surface) !important;
    font-family:var(--fb) !important; font-size:14px !important;
    color:var(--color-text) !important;
}
.stSelectbox div[data-baseweb="select"] * { color:var(--color-text) !important; }

/* ── Streamlit metrics ── */
[data-testid="stMetricValue"] {
    font-family:var(--fd) !important; font-weight:700 !important;
    color:var(--color-accent) !important;
}
[data-testid="stMetricLabel"] p {
    font-size:11px !important; text-transform:uppercase !important;
    letter-spacing:0.06em !important; color:var(--color-text-subtle) !important;
    font-weight:700 !important;
}

/* ── Chat bubbles ── */
.chat-bot {
    background:var(--color-surface); border:1px solid var(--color-border); color:var(--color-text);
    padding:14px 18px; border-radius:18px 18px 18px 4px;
    margin:8px 0; margin-right:22%; font-size:14px; font-weight:500;
    line-height:1.65; box-shadow:var(--shadow-sm);
}
.chat-user {
    background:var(--color-primary-soft); color:var(--color-text);
    padding:14px 18px; border-radius:18px 18px 4px 18px;
    margin:8px 0; margin-left:22%; font-size:14px; font-weight:500;
    line-height:1.65;
}
.chat-who {
    font-size:10px; font-weight:700; text-transform:uppercase;
    letter-spacing:0.1em; color:var(--color-text-subtle); margin-bottom:5px;
}

/* ── Tags base (colores por tema se inyectan aparte) ── */
.tag {
    display:inline-flex; align-items:center;
    padding:3px 10px; border-radius:100px; font-size:10px;
    font-weight:700; text-transform:uppercase; letter-spacing:0.05em;
}

/* ── Habit cards ── */
.habit-card {
    background:var(--color-surface); border-radius:var(--radius-lg);
    padding:18px 20px; box-shadow:var(--shadow-sm);
    border:1px solid var(--color-border); margin:8px 0;
    display:flex; gap:14px; align-items:flex-start;
    transition: box-shadow 0.2s;
}
.habit-card:hover { box-shadow:var(--shadow-md); }
.habit-icon { font-size:22px; line-height:1; margin-top:2px; flex-shrink:0; }
.habit-title {
    font-family:var(--fd); font-size:14px; font-weight:600;
    color:var(--color-text); margin-bottom:3px;
}
.habit-desc { font-size:13px; color:var(--color-text-subtle); line-height:1.5; margin:0; }

/* ── Breathing ── */
.breath-box {
    background:var(--color-surface-alt); border-radius:var(--radius-xl);
    padding:32px; border:1px solid var(--color-border); text-align:center;
}
.breath-step {
    background:var(--color-surface); border-radius:var(--radius-lg);
    padding:22px 18px; min-width:120px;
    box-shadow:var(--shadow-sm); border:1px solid var(--color-border);
    text-align:center; display:inline-block; margin:8px; vertical-align:top;
}

/* ── Sidebar brand ── */
.sb-brand {
    font-family:var(--fd); font-size:20px; font-weight:700;
    letter-spacing:-0.01em; color:var(--color-accent) !important;
}
.sb-sub {
    font-size:10px; font-weight:700; text-transform:uppercase;
    letter-spacing:0.1em; color:var(--color-text-subtle) !important; margin-top:2px;
}
.sb-date {
    background:var(--color-surface-alt); border-radius:var(--radius-md);
    padding:10px 14px; font-size:13px; font-weight:600; color:var(--color-text-muted) !important;
}
.sb-quote {
    font-size:12px; font-style:italic;
    color:var(--color-text-subtle) !important; line-height:1.6; padding:0 2px;
}
.sb-label {
    font-family:var(--fd); font-size:10px; font-weight:700;
    text-transform:uppercase; letter-spacing:0.12em;
    color:var(--color-text-subtle) !important; margin-bottom:2px;
}

/* ── Suggestion chips ── */
.chip {
    background:var(--color-surface); border:1.5px solid var(--color-border-strong);
    border-radius:100px; padding:7px 14px; font-size:12px;
    font-weight:600; color:var(--color-text-muted); text-align:center;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border-radius:var(--radius-lg) !important;
    overflow:hidden; border:1px solid var(--color-border) !important;
}

footer,#MainMenu { visibility:hidden; }
[data-testid="stDecoration"] { display:none; }
"""

_FONT_IMPORT = ("@import url('https://fonts.googleapis.com/css2?"
                "family=Josefin+Sans:wght@300;400;600;700&"
                "family=Figtree:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap');")


def _root_block(t):
    """Construye el bloque :root con los tokens del tema activo."""
    pairs = {
        "--color-bg": t["bg"],
        "--color-surface": t["surface"],
        "--color-surface-alt": t["surface_alt"],
        "--color-text": t["text"],
        "--color-text-muted": t["text_muted"],
        "--color-text-subtle": t["text_subtle"],
        "--color-border": t["border"],
        "--color-border-strong": t["border_strong"],
        "--color-primary": t["primary"],
        "--color-primary-hover": t["primary_hover"],
        "--color-on-primary": t["on_primary"],
        "--color-accent": t["accent"],
        "--color-secondary": t["secondary"],
        "--color-secondary-soft": t["secondary_soft"],
        "--color-primary-soft": t["primary_soft"],
        "--color-primary-tint": t["primary_tint"],
        "--shadow-sm": t["shadow_sm"],
        "--shadow-md": t["shadow_md"],
        "--fd": FONTS["fd"],
        "--fb": FONTS["fb"],
        "--radius-sm": RADII["sm"],
        "--radius-md": RADII["md"],
        "--radius-lg": RADII["lg"],
        "--radius-xl": RADII["xl"],
    }
    body = "".join(f"{k}:{v};" for k, v in pairs.items())
    return ":root{" + body + "}"


def _tag_block(t):
    """Genera las clases de tag con los colores de categoría del tema activo."""
    names = {"Trabajo": "trabajo", "Estudio": "estudio",
             "Descanso": "descanso", "Tarea": "tarea"}
    parts = []
    for cat, cls in names.items():
        bg, tx = t["cats"][cat]
        parts.append(".tag-" + cls + "{background:" + bg + ";color:" + tx + ";}")
    return "".join(parts)


def build_css(t):
    """Devuelve el bloque <style> completo para el tema activo."""
    return ("<style>" + _FONT_IMPORT + _root_block(t)
            + STATIC_CSS + _tag_block(t) + "</style>")


# ── Estado del tema + inyección de CSS (debe ir antes de renderizar la UI) ──
if "theme" not in st.session_state:
    st.session_state.theme = DEFAULT_THEME

active = THEMES[st.session_state.theme]
st.markdown(build_css(active), unsafe_allow_html=True)


# ── Session state ──────────────────────────────────────────────────────────────
if "agenda" not in st.session_state:
    st.session_state.agenda = pd.DataFrame([
        {"Día": "Lunes",     "Hora": "08:00", "Tipo": "Trabajo",  "Descripción": "Turno mañana"},
        {"Día": "Lunes",     "Hora": "18:00", "Tipo": "Estudio",  "Descripción": "Clases virtuales"},
        {"Día": "Martes",    "Hora": "09:00", "Tipo": "Trabajo",  "Descripción": "Reunión equipo"},
        {"Día": "Miércoles", "Hora": "14:00", "Tipo": "Estudio",  "Descripción": "Preparar prueba Cálculo"},
        {"Día": "Jueves",    "Hora": "20:00", "Tipo": "Descanso", "Descripción": "Tiempo libre / deporte"},
        {"Día": "Viernes",   "Hora": "08:00", "Tipo": "Trabajo",  "Descripción": "Turno completo"},
        {"Día": "Sábado",    "Hora": "10:00", "Tipo": "Tarea",    "Descripción": "Entrega informe Física"},
        {"Día": "Domingo",   "Hora": "12:00", "Tipo": "Descanso", "Descripción": "Descanso y familia"},
    ])

if "tareas" not in st.session_state:
    st.session_state.tareas = [
        {"texto": "📚 Estudiar para prueba de Cálculo", "completada": False},
        {"texto": "📝 Entregar informe de Física",       "completada": False},
        {"texto": "💼 Enviar reporte al jefe",           "completada": True},
        {"texto": "📖 Leer capítulo 5 de Biología",      "completada": False},
        {"texto": "🗂️ Organizar apuntes de la semana",   "completada": False},
    ]

if "chat_historial" not in st.session_state:
    st.session_state.chat_historial = [
        {"rol": "bot", "mensaje": "¡Hola! 🌸 Soy tu asistente Smart Balance. Cuéntame cómo te sientes hoy o qué necesitas organizar."}
    ]


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div class='sb-brand'>🌸 Smart Balance</div>", unsafe_allow_html=True)
    st.markdown("<div class='sb-sub'>Para estudiantes que trabajan</div>", unsafe_allow_html=True)
    st.markdown("---")

    pagina = st.radio(
        "Navegar a:",
        ["🏠 Inicio", "📅 Agenda Semanal", "✅ Recordatorios", "🤖 Chatbot", "💆 Bienestar"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("<div class='sb-label'>Tema visual</div>", unsafe_allow_html=True)
    st.selectbox(
        "Tema visual",
        list(THEMES.keys()),
        key="theme",
        label_visibility="collapsed"
    )

    st.markdown("---")
    fecha = datetime.now().strftime('%A %d de %B').title()
    st.markdown(f"<div class='sb-date'>📆 {fecha}</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "<div class='sb-quote'>Cada pequeño paso que das hoy construye la persona que serás mañana.</div>",
        unsafe_allow_html=True
    )


# ══════════════════════════════════════════════
# PÁGINA 1: INICIO
# ══════════════════════════════════════════════
if pagina == "🏠 Inicio":

    col1, col2 = st.columns([2.2, 1])
    with col1:
        st.markdown("<div class='eyebrow'>Dashboard</div>", unsafe_allow_html=True)
        st.markdown("# 🌸 Smart Balance")
        st.markdown("""
        <div class='card-tinted'>
            <p style='font-size:15px;color:var(--color-text-muted);margin:0;line-height:1.75;'>
            Tu compañera para <strong>organizar el tiempo</strong>, gestionar tus
            <strong>tareas</strong> y cuidar tu <strong>bienestar emocional</strong>.
            Diseñada para estudiantes que también trabajan. 💜
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        score = 74
        st.markdown(f"""
        <div class='score-wrap'>
            <div class='score-cap'>Balance Score</div>
            <div class='score-ring' style='--p:{score}'>
                <span class='score-num'>{score}</span>
            </div>
            <div class='score-sub'>¡Vas muy bien! 🌟</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    tareas_pendientes = sum(1 for t in st.session_state.tareas if not t["completada"])
    tareas_completas  = sum(1 for t in st.session_state.tareas if t["completada"])
    pct = int(tareas_completas / max(len(st.session_state.tareas), 1) * 100)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"<div class='stat-card'><div class='stat-num'>{len(st.session_state.agenda)}</div><div class='stat-lbl'>Actividades</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='stat-card'><div class='stat-num'>{tareas_completas}</div><div class='stat-lbl'>Completadas</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='stat-card'><div class='stat-num'>{tareas_pendientes}</div><div class='stat-lbl'>Pendientes</div></div>", unsafe_allow_html=True)
    with c4:
        st.markdown(f"<div class='stat-card'><div class='stat-num'>{pct}%</div><div class='stat-lbl'>Progreso</div></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class='prog-row'>
        <div class='prog-head'><span>Progreso de tareas</span><b>{pct}%</b></div>
        <div class='prog-track'><div class='prog-fill' style='width:{pct}%'></div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='card-teal'>
        <div class='eyebrow'>Consejo del día</div>
        <p style='color:var(--color-text-muted);margin:8px 0 0;font-size:15px;line-height:1.7;'>
        Haz pausas de <strong>5 minutos</strong> cada hora de estudio.
        Tu cerebro las necesita para consolidar lo aprendido. 🧠
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='eyebrow'>Desglose del score</div>", unsafe_allow_html=True)
    st.markdown("<h2>Tus dimensiones</h2>", unsafe_allow_html=True)

    dimensiones = [
        ("📚 Estudio organizado",  80, ""),
        ("💼 Trabajo gestionado",  70, "teal"),
        ("😴 Descanso adecuado",   60, ""),
        ("💆 Bienestar emocional", 85, "teal"),
    ]
    for label, val, cls in dimensiones:
        fill_class = "prog-fill-teal" if cls == "teal" else "prog-fill"
        st.markdown(f"""
        <div class='prog-row'>
            <div class='prog-head'><span>{label}</span><b>{val}%</b></div>
            <div class='prog-track'>
                <div class='{fill_class}' style='width:{val}%'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# PÁGINA 2: AGENDA SEMANAL
# ══════════════════════════════════════════════
elif pagina == "📅 Agenda Semanal":

    st.markdown("<div class='eyebrow'>Organización</div>", unsafe_allow_html=True)
    st.markdown("# 📅 Agenda Semanal")
    st.markdown("<p style='color:var(--color-text-muted);margin-top:-8px;'>Visualiza y organiza tus actividades de la semana.</p>", unsafe_allow_html=True)

    st.markdown("### Actividades registradas")

    df = st.session_state.agenda.copy()
    cats = THEMES[st.session_state.theme]["cats"]

    def color_tipo(val):
        pair = cats.get(val)
        if pair:
            return f"background-color: {pair[0]}; color: {pair[1]};"
        return ""

    styled = df.style.map(color_tipo, subset=["Tipo"])
    st.dataframe(styled, use_container_width=True, hide_index=True)

    st.markdown("""
    <div style='display:flex;gap:10px;margin:8px 0 24px;flex-wrap:wrap;'>
        <span class='tag tag-trabajo'>💼 Trabajo</span>
        <span class='tag tag-estudio'>📚 Estudio</span>
        <span class='tag tag-descanso'>😴 Descanso</span>
        <span class='tag tag-tarea'>📝 Tarea</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Agregar actividad")
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        nuevo_dia  = st.selectbox("Día", dias)
        nueva_hora = st.text_input("Hora (ej: 14:30)", placeholder="14:30")
    with col2:
        tipos = ["Trabajo", "Estudio", "Descanso", "Tarea"]
        nuevo_tipo = st.selectbox("Tipo de actividad", tipos)
        nueva_desc = st.text_input("Descripción", placeholder="Describe la actividad...")

    if st.button("Agregar actividad →"):
        if nueva_hora and nueva_desc:
            nueva_fila = {"Día": nuevo_dia, "Hora": nueva_hora, "Tipo": nuevo_tipo, "Descripción": nueva_desc}
            st.session_state.agenda = pd.concat(
                [st.session_state.agenda, pd.DataFrame([nueva_fila])], ignore_index=True
            )
            st.success(f"Actividad '{nueva_desc}' agregada para el {nuevo_dia}.")
            st.rerun()
        else:
            st.warning("Completa la hora y la descripción.")

    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# PÁGINA 3: RECORDATORIOS
# ══════════════════════════════════════════════
elif pagina == "✅ Recordatorios":

    st.markdown("<div class='eyebrow'>Productividad</div>", unsafe_allow_html=True)
    st.markdown("# ✅ Recordatorios")
    st.markdown("<p style='color:var(--color-text-muted);margin-top:-8px;'>Organiza tus pendientes y marca lo que ya completaste.</p>", unsafe_allow_html=True)

    total      = len(st.session_state.tareas)
    completas  = sum(1 for t in st.session_state.tareas if t["completada"])
    pendientes = total - completas

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"<div class='stat-card'><div class='stat-num'>{total}</div><div class='stat-lbl'>Total</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='stat-card'><div class='stat-num'>{completas}</div><div class='stat-lbl'>Completadas</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='stat-card'><div class='stat-num'>{pendientes}</div><div class='stat-lbl'>Pendientes</div></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Lista de tareas")

    for i, tarea in enumerate(st.session_state.tareas):
        col_check, col_text = st.columns([0.08, 0.92])
        with col_check:
            completada = st.checkbox(
                "", value=tarea["completada"],
                key=f"tarea_{i}", label_visibility="collapsed"
            )
            st.session_state.tareas[i]["completada"] = completada
        with col_text:
            if completada:
                st.markdown(
                    f"<p style='color:var(--color-text-subtle);text-decoration:line-through;margin:8px 0;font-size:14px;'>{tarea['texto']}</p>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<p style='color:var(--color-text);font-weight:600;margin:8px 0;font-size:14px;'>{tarea['texto']}</p>",
                    unsafe_allow_html=True
                )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Agregar tarea")
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    nueva_tarea = st.text_input(
        "Nueva tarea", placeholder="Ej: Estudiar capítulo 3 de Historia...",
        label_visibility="collapsed"
    )

    col_btn1, col_btn2, _ = st.columns([1, 1.4, 3])
    with col_btn1:
        if st.button("Agregar →"):
            if nueva_tarea.strip():
                st.session_state.tareas.append({"texto": f"📌 {nueva_tarea.strip()}", "completada": False})
                st.success(f"Tarea '{nueva_tarea}' agregada.")
                st.rerun()
            else:
                st.warning("Escribe algo antes de agregar.")
    with col_btn2:
        if st.button("Limpiar completadas"):
            st.session_state.tareas = [t for t in st.session_state.tareas if not t["completada"]]
            st.success("Tareas completadas eliminadas.")
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# PÁGINA 4: CHATBOT
# ══════════════════════════════════════════════
elif pagina == "🤖 Chatbot":

    st.markdown("<div class='eyebrow'>Apoyo emocional</div>", unsafe_allow_html=True)
    st.markdown("# 🤖 Chatbot Smart Balance")
    st.markdown("<p style='color:var(--color-text-muted);margin-top:-8px;'>Cuéntame cómo te sientes o qué necesitas organizar. Estoy aquí para ayudarte. 💜</p>", unsafe_allow_html=True)

    def obtener_respuesta(mensaje):
        msg = mensaje.lower()
        if any(p in msg for p in ["estresada", "estresado", "estrés", "estres", "agobiada", "agobiado"]):
            return ("💜 Respira profundo. Parece que estás sintiendo mucho estrés. "
                    "Prueba esta pausa: inhala contando hasta 4, mantén 4 segundos y exhala en 6. "
                    "Repite 3 veces. Recuerda: no puedes dar lo mejor de ti si no te cuidas. 🌿")
        elif any(p in msg for p in ["prueba", "examen", "test", "evaluación", "evaluacion"]):
            return ("📚 ¡Tú puedes con esa prueba! Organiza tu estudio en bloques de 25 minutos "
                    "con 5 de descanso (técnica Pomodoro). Empieza por los temas más difíciles cuando "
                    "estés más fresca/fresco. ¿Quieres planificar en la Agenda? 📅")
        elif any(p in msg for p in ["cansada", "cansado", "agotada", "agotado", "sin energía", "sin energia"]):
            return ("😴 Tu cuerpo te está pidiendo descanso y eso es completamente válido. "
                    "Si puedes, toma una siesta corta de 20 minutos. Hidrátate y trata de "
                    "dormir al menos 7 horas esta noche. El descanso también es rendimiento. 💙")
        elif any(p in msg for p in ["organizar", "organización", "organizacion", "orden", "planificar"]):
            return ("📋 ¡Excelente que quieras organizarte! "
                    "1️⃣ Anota tus tareas en Recordatorios. "
                    "2️⃣ Agrega actividades a la Agenda Semanal. "
                    "3️⃣ Prioriza lo más urgente primero. ¿Por dónde empezamos? 🌟")
        elif any(p in msg for p in ["bien", "feliz", "contenta", "contento", "genial", "excelente"]):
            return ("🌸 ¡Me alegra escuchar eso! Aprovecha esta buena energía para avanzar "
                    "con tus tareas más retadoras. Cuando estamos bien, aprendemos mejor. ✨")
        elif any(p in msg for p in ["triste", "mal", "horrible", "pésimo", "pesimo", "deprimida", "deprimido"]):
            return ("💜 Lo siento mucho. Está bien no estar bien siempre. "
                    "Permítete sentir lo que sientes. Si puedes, habla con alguien de confianza. "
                    "Eres más que tus resultados. 🤗")
        elif any(p in msg for p in ["motivación", "motivacion", "motivada", "motivado", "ánimo", "animo"]):
            return ("🚀 Cada día que estudias y trabajas construyes una versión más fuerte de ti. "
                    "Los resultados no siempre se ven de inmediato, pero el esfuerzo siempre cuenta. "
                    "¡Tú tienes lo que se necesita! 💪")
        else:
            return ("🌸 Gracias por escribirme. Puedo ayudarte con: "
                    "**estrés**, **cansancio**, **pruebas o exámenes**, **organización**, "
                    "o simplemente cómo te sientes. ¿Qué necesitas hoy? 💜")

    st.markdown("### Conversación")
    for msg in st.session_state.chat_historial:
        if msg["rol"] == "bot":
            st.markdown(
                f"<div class='chat-bot'><div class='chat-who'>🤖 Smart Balance</div>{msg['mensaje']}</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div class='chat-user'><div class='chat-who'>Tú</div>{msg['mensaje']}</div>",
                unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)

    col_input, col_btn = st.columns([4, 1])
    with col_input:
        user_input = st.text_input(
            "Mensaje", placeholder="Ej: me siento estresada con los exámenes...",
            key="chat_input", label_visibility="collapsed"
        )
    with col_btn:
        enviar = st.button("Enviar →")

    if enviar and user_input.strip():
        st.session_state.chat_historial.append({"rol": "usuario", "mensaje": user_input.strip()})
        respuesta = obtener_respuesta(user_input.strip())
        st.session_state.chat_historial.append({"rol": "bot", "mensaje": respuesta})
        st.rerun()

    if st.button("Limpiar conversación"):
        st.session_state.chat_historial = [
            {"rol": "bot", "mensaje": "¡Hola de nuevo! 🌸 ¿Cómo te sientes hoy? Estoy aquí para ayudarte."}
        ]
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='eyebrow'>Puedes escribir sobre</div>", unsafe_allow_html=True)
    sugerencias = ["😰 Estrés", "📚 Examen", "😴 Cansancio", "📋 Organización", "😊 Cómo me siento"]
    cols = st.columns(len(sugerencias))
    for i, sug in enumerate(sugerencias):
        with cols[i]:
            st.markdown(f"<div class='chip'>{sug}</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# PÁGINA 5: BIENESTAR
# ══════════════════════════════════════════════
elif pagina == "💆 Bienestar":

    st.markdown("<div class='eyebrow'>Autocuidado</div>", unsafe_allow_html=True)
    st.markdown("# 💆 Bienestar")
    st.markdown("<p style='color:var(--color-text-muted);margin-top:-8px;'>Chequea cómo estás y recibe recomendaciones personalizadas. 🌿</p>", unsafe_allow_html=True)

    st.markdown("### ¿Cómo te sientes ahora?")

    # Construye los estados desde la paleta del tema activo (textos idénticos).
    moods = THEMES[st.session_state.theme]["moods"]
    estados = {}
    for label, (key, texto) in MOOD_TEXT.items():
        bg, tx = moods[key]
        estados[label] = (bg, tx, texto)

    estado_sel = st.radio(
        "Estado:", list(estados.keys()), horizontal=True, label_visibility="collapsed"
    )

    if estado_sel:
        bg, tx, rec = estados[estado_sel]
        st.markdown(f"""
        <div style='background:{bg};border-radius:var(--radius-xl);padding:20px 24px;margin:16px 0;border:1px solid var(--color-border);'>
            <div class='eyebrow' style='color:{tx};margin-bottom:8px;'>Recomendación para ti</div>
            <p style='color:{tx};margin:0;font-size:15px;font-weight:500;line-height:1.75;'>{rec}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("### Respiración Guiada")
    st.markdown("""
    <div class='breath-box'>
        <div class='eyebrow' style='margin-bottom:16px;'>Técnica 4-4-6</div>
        <div>
            <div class='breath-step'>
                <div style='font-size:30px;margin-bottom:10px;'>👃</div>
                <div style='font-family:var(--fd);font-size:13px;font-weight:600;color:var(--color-text);margin-bottom:4px;'>Inhala</div>
                <div style='font-family:var(--fd);font-size:2rem;font-weight:700;color:var(--color-accent);line-height:1;'>4</div>
                <div style='font-size:11px;color:var(--color-text-subtle);margin-top:2px;'>segundos</div>
            </div>
            <div class='breath-step'>
                <div style='font-size:30px;margin-bottom:10px;'>⏸️</div>
                <div style='font-family:var(--fd);font-size:13px;font-weight:600;color:var(--color-text);margin-bottom:4px;'>Mantén</div>
                <div style='font-family:var(--fd);font-size:2rem;font-weight:700;color:var(--color-secondary);line-height:1;'>4</div>
                <div style='font-size:11px;color:var(--color-text-subtle);margin-top:2px;'>segundos</div>
            </div>
            <div class='breath-step'>
                <div style='font-size:30px;margin-bottom:10px;'>💨</div>
                <div style='font-family:var(--fd);font-size:13px;font-weight:600;color:var(--color-text);margin-bottom:4px;'>Exhala</div>
                <div style='font-family:var(--fd);font-size:2rem;font-weight:700;color:var(--color-accent);line-height:1;'>6</div>
                <div style='font-size:11px;color:var(--color-text-subtle);margin-top:2px;'>segundos</div>
            </div>
        </div>
        <p style='color:var(--color-text-subtle);margin-top:20px;font-size:13px;font-weight:600;'>
            Repite este ciclo <strong>3 a 5 veces</strong> para sentir el efecto calmante.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Hábitos de bienestar")

    habitos = [
        ("💧", "Hidratación",      "Toma al menos 8 vasos de agua al día. La deshidratación afecta directamente la concentración."),
        ("🥗", "Alimentación",     "Come algo nutritivo antes de estudiar. El cerebro necesita energía real para funcionar."),
        ("🚶", "Movimiento",       "15 minutos de caminata diaria reducen el estrés y mejoran la consolidación de memoria."),
        ("📵", "Descanso digital", "Apaga el celular 30 min antes de dormir para mejorar la calidad del sueño."),
        ("📓", "Journaling",       "Escribe 3 cosas positivas del día. Este hábito activa patrones de bienestar emocional."),
        ("🤝", "Apoyo social",     "Comparte cómo te sientes con alguien de confianza. No tienes que cargarlo todo sola/solo."),
    ]

    col1, col2 = st.columns(2)
    for i, (emoji, titulo, desc) in enumerate(habitos):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
            <div class='habit-card'>
                <div class='habit-icon'>{emoji}</div>
                <div>
                    <div class='habit-title'>{titulo}</div>
                    <p class='habit-desc'>{desc}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
