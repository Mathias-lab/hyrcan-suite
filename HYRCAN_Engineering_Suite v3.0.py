# -*- coding: utf-8 -*-
"""
HYRCAN Engineering Suite v4.0
Developed by Mathias Adjei Tawiah
Hohai University — College of Harbor, Coastal & Offshore Engineering
Standards: EurOtop 2018 | JTS 154-1-2011 | GB 50286-2013
"""

import streamlit as st
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import numpy as np
import json
import io
import math
import pandas as pd
import datetime
import os

# ─── Page config (MUST be first Streamlit call) ─────────────────────────────
st.set_page_config(
    page_title="HYRCAN Engineering Suite v4.0",
    page_icon="⚓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ════════════════════════════════════════════════════════════════════
#  GLOBAL STYLES
# ════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', sans-serif;
}
.stApp { background-color: #080c12; color: #cdd9e5; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #0d1117;
    border-bottom: 1px solid #21262d;
    gap: 0; padding: 0;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #8b949e;
    border-radius: 0;
    font-weight: 500;
    font-size: 13px;
    padding: 10px 22px;
    border-bottom: 2px solid transparent;
    letter-spacing: 0.3px;
}
.stTabs [aria-selected="true"] {
    background: transparent !important;
    color: #e6edf3 !important;
    border-bottom: 2px solid #2f81f7 !important;
}

/* ── Inputs ── */
.stNumberInput input, .stTextInput input {
    background: #0d1117 !important;
    border: 1px solid #30363d !important;
    color: #cdd9e5 !important;
    border-radius: 6px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
}
.stNumberInput input:focus, .stTextInput input:focus {
    border-color: #2f81f7 !important;
    box-shadow: 0 0 0 3px rgba(47,129,247,0.12) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: #1a7f37;
    color: #ffffff;
    border: 1px solid #2ea043;
    border-radius: 6px;
    font-weight: 600;
    font-size: 13px;
    padding: 8px 18px;
    letter-spacing: 0.3px;
    transition: all 0.15s ease;
}
.stButton > button:hover {
    background: #238636;
    border-color: #3fb950;
}

/* ── Metrics ── */
[data-testid="metric-container"] {
    background: #0d1117;
    border: 1px solid #21262d;
    border-radius: 8px;
    padding: 14px 16px;
}
[data-testid="metric-container"] [data-testid="metric-label"] {
    font-size: 11px !important;
    color: #8b949e !important;
    font-weight: 500 !important;
    letter-spacing: 0.5px !important;
    text-transform: uppercase !important;
}
[data-testid="metric-container"] [data-testid="metric-value"] {
    font-size: 22px !important;
    font-weight: 700 !important;
    color: #e6edf3 !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* ── DataFrames ── */
.stDataFrame { border-radius: 8px; overflow: hidden; }
.stDataFrame table { font-size: 12px !important; }

/* ── Alerts ── */
.stAlert { border-radius: 6px; font-size: 13px; }

/* ── Divider ── */
.hd { border: none; border-top: 1px solid #21262d; margin: 14px 0; }

/* ── Section labels ── */
.sec-lbl {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: #8b949e;
    margin: 20px 0 8px 0;
    padding-bottom: 6px;
    border-bottom: 1px solid #21262d;
}

/* ── Monospace output blocks ── */
.code-out {
    background: #0d1117;
    border: 1px solid #21262d;
    border-radius: 8px;
    padding: 18px 22px;
    font-family: 'JetBrains Mono', 'Consolas', monospace;
    font-size: 12px;
    color: #cdd9e5;
    line-height: 1.7;
    overflow-x: auto;
    white-space: pre;
}

/* ── Equation blocks ── */
.eq-block {
    background: #0d1117;
    border: 1px solid #21262d;
    border-left: 3px solid #2f81f7;
    border-radius: 0 8px 8px 0;
    padding: 14px 20px;
    margin: 8px 0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    color: #cdd9e5;
}
.eq-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: #2f81f7;
    margin-bottom: 6px;
}
.eq-main { font-size: 15px; color: #e6edf3; font-weight: 500; }
.eq-sub { font-size: 12px; color: #8b949e; margin-top: 4px; }
.eq-result { font-size: 14px; color: #3fb950; font-weight: 700; margin-top: 8px; }

/* ── Professional table ── */
.pro-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 12px;
    font-family: 'Inter', sans-serif;
}
.pro-table th {
    background: #161b22;
    color: #8b949e;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    padding: 10px 14px;
    border-bottom: 2px solid #2f81f7;
    text-align: left;
}
.pro-table td {
    padding: 9px 14px;
    border-bottom: 1px solid #21262d;
    color: #cdd9e5;
    vertical-align: middle;
}
.pro-table tr:last-child td { border-bottom: none; }
.pro-table tr:hover td { background: #161b22; }
.pro-table .mat-name { font-weight: 600; color: #e6edf3; }
.pro-table .num-cell { font-family: 'JetBrains Mono', monospace; text-align: right; }

/* ── Status pill ── */
.pill-ok  { background:#1a3626; color:#3fb950; border:1px solid #238636; border-radius:20px; padding:2px 10px; font-size:11px; font-weight:600; }
.pill-err { background:#3b1219; color:#f85149; border:1px solid #b91c1c; border-radius:20px; padding:2px 10px; font-size:11px; font-weight:600; }
.pill-warn{ background:#2d2208; color:#e3b341; border:1px solid #9e6a03; border-radius:20px; padding:2px 10px; font-size:11px; font-weight:600; }

/* ── Sidebar ── */
[data-testid="stSidebar"] { background: #0d1117; border-right: 1px solid #21262d; }
[data-testid="stSidebar"] .stSlider { padding-top: 4px; }

/* ── Info card ── */
.info-card {
    background: #0d1117;
    border: 1px solid #21262d;
    border-radius: 8px;
    padding: 14px 18px;
    margin-bottom: 10px;
}
.info-card .ic-title {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: #8b949e;
    margin-bottom: 8px;
}
.info-card .ic-body { font-size: 12px; color: #8b949e; line-height: 2; }

/* ── Project history card ── */
.proj-card {
    background: #0d1117;
    border: 1px solid #21262d;
    border-radius: 8px;
    padding: 14px 18px;
    margin-bottom: 8px;
    cursor: pointer;
    transition: border-color 0.15s;
}
.proj-card:hover { border-color: #2f81f7; }
.proj-card .pc-name { font-weight: 600; font-size: 14px; color: #e6edf3; }
.proj-card .pc-meta { font-size: 11px; color: #8b949e; margin-top: 3px; }

/* ── Header brand ── */
.brand-header {
    background: #0d1117;
    border-bottom: 1px solid #21262d;
    padding: 16px 24px;
    margin-bottom: 0;
    display: flex;
    align-items: center;
    gap: 16px;
}
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
#  SESSION STATE — HISTORY / PROJECTS
# ════════════════════════════════════════════════════════════════════

def _default(key, val):
    if key not in st.session_state:
        st.session_state[key] = val

# ── Geometry defaults ──────────────────────────────────────────────
_default('rm_crest_elev',   14.55)
_default('rm_seabed_elev',  -3.30)
_default('rm_crest_width',   6.0)
_default('rm_upper_height',  4.85)
_default('rm_lower_height', 13.0)
_default('rm_sw_upper',      2.5)
_default('rm_sw_lower',      2.5)
_default('rm_sw_berm',       6.5)
_default('rm_lw_upper',      1.5)
_default('rm_lw_lower',      1.5)
_default('rm_lw_berm',       2.0)
_default('rm_dhw',           4.99)
_default('rm_surcharge',    10.0)
_default('rm_num_slices',   50.0)
_default('rm_n_layers',      3)

_default('rm_n1', 'Soft Silt');    _default('rm_t1', 7.8)
_default('rm_g1', 16.5);  _default('rm_c1', 6.0);  _default('rm_phi1', 8.0)
_default('rm_n2', 'Silty Clay');   _default('rm_t2', 10.2)
_default('rm_g2', 19.0);  _default('rm_c2', 20.0); _default('rm_phi2', 18.0)
_default('rm_n3', 'Fine Sand');    _default('rm_t3', 10.0)
_default('rm_g3', 19.5);  _default('rm_c3', 0.0);  _default('rm_phi3', 30.0)
_default('rm_n4', 'Dense Sand');   _default('rm_t4', 8.0)
_default('rm_g4', 20.0);  _default('rm_c4', 0.0);  _default('rm_phi4', 35.0)
_default('rm_n5', 'Gravel');       _default('rm_t5', 6.0)
_default('rm_g5', 21.0);  _default('rm_c5', 0.0);  _default('rm_phi5', 40.0)
_default('rm_gr', 19.0);  _default('rm_cr_', 0.0); _default('rm_phir', 38.0)

_default('cs_B',       16.0)
_default('cs_H_c',     14.0)
_default('cs_gamma_c', 24.0)
_default('cs_d',        4.59)
_default('cs_H1pct',    2.71)
_default('cs_gamma_w', 10.25)
_default('cs_mu',       0.60)
_default('cs_q_allow', 500.0)

_default('wu_H',       2.0)
_default('wu_T',      10.0)
_default('wu_slope',   2.5)
_default('wu_Rc',      1.5)
_default('wu_gamma_f', 0.55)
_default('wu_gamma_b', 1.0)
_default('wu_beta',    0.0)

# ── Project history ────────────────────────────────────────────────
_default('project_history', [])   # list of dicts
_default('rm_generated', False)


# ════════════════════════════════════════════════════════════════════
#  CORE CALCULATION FUNCTIONS
# ════════════════════════════════════════════════════════════════════

def compute_layer_elevations(seabed_elev, thicknesses):
    tops, bots, cur = [], [], seabed_elev
    for t in thicknesses:
        tops.append(cur); bots.append(cur - t); cur -= t
    datum = abs(bots[-1])
    def Y(e): return e + datum
    result = {'datum': datum, 'Y_seabed': Y(seabed_elev)}
    for i, (top, bot) in enumerate(zip(tops, bots)):
        result[f'top{i+1}'] = top
        result[f'bot{i+1}'] = bot
        result[f'Y_top{i+1}'] = Y(top)
        result[f'Y_bot{i+1}'] = Y(bot)
    return result


def compute_geometry(crest_elev, seabed_elev, crest_width,
                     upper_height, lower_height,
                     sw_upper, sw_lower, seaward_berm,
                     lw_upper, lw_lower, landward_berm, layers):
    datum = layers['datum']
    def Y(e): return e + datum
    crest_y  = Y(crest_elev)
    seabed_y = Y(seabed_elev)
    single_sw = (seaward_berm == 0)
    single_lw = (landward_berm == 0)

    if single_sw:
        total_sw_dx = (upper_height + lower_height) * sw_upper
        x_sw_toe = 0.0; x_sw_be = 0.0; x_sw_bs = 0.0
        x_cl = x_sw_toe + total_sw_dx
    else:
        sw_udx = upper_height * sw_upper; sw_ldx = lower_height * sw_lower
        x_sw_toe = 0.0; x_sw_be = x_sw_toe + sw_ldx
        x_sw_bs = x_sw_be + seaward_berm; x_cl = x_sw_bs + sw_udx
    x_cr = x_cl + crest_width

    if single_lw:
        total_lw_dx = (upper_height + lower_height) * lw_upper
        x_lw_bs = x_cr; x_lw_be = x_cr; x_lw_toe = x_cr + total_lw_dx
    else:
        lw_udx = upper_height * lw_upper; lw_ldx = lower_height * lw_lower
        x_lw_bs = x_cr + lw_udx; x_lw_be = x_lw_bs + landward_berm
        x_lw_toe = x_lw_be + lw_ldx

    berm_y = Y(crest_elev - upper_height)
    sw_udx = upper_height * sw_upper; sw_ldx = lower_height * sw_lower
    lw_udx = upper_height * lw_upper; lw_ldx = lower_height * lw_lower

    if single_sw:
        pts = {'sw_toe': (x_sw_toe, seabed_y), 'sw_be': (x_sw_toe, seabed_y), 'sw_bs': (x_sw_toe, seabed_y)}
    else:
        pts = {'sw_toe': (x_sw_toe, seabed_y), 'sw_be': (x_sw_be, berm_y), 'sw_bs': (x_sw_bs, berm_y)}

    pts['cl'] = (x_cl, crest_y); pts['cr'] = (x_cr, crest_y)
    lw_by = berm_y if not single_lw else seabed_y
    pts['lw_bs'] = (x_lw_bs, lw_by); pts['lw_be'] = (x_lw_be, lw_by)
    pts['lw_toe'] = (x_lw_toe, seabed_y)

    return {
        'pts': pts, 'crest_y': crest_y, 'seabed_y': seabed_y, 'berm_y': berm_y,
        'model_right': x_lw_toe, 'model_bottom': 0.0,
        'sw_udx': sw_udx, 'sw_ldx': sw_ldx, 'lw_udx': lw_udx, 'lw_ldx': lw_ldx,
        'x_sw_be': x_sw_be if not single_sw else 0,
        'x_sw_bs': x_sw_bs if not single_sw else 0,
        'x_cl': x_cl, 'x_cr': x_cr,
        'x_lw_bs': x_lw_bs, 'x_lw_be': x_lw_be, 'x_lw_toe': x_lw_toe,
        'single_slope_sw': single_sw, 'single_slope_lw': single_lw,
    }


def verify_geometry(g, crest_elev, seabed_elev, crest_width,
                    upper_height, lower_height,
                    sw_upper, sw_lower, seaward_berm,
                    lw_upper, lw_lower, landward_berm):
    pts = g['pts']; tol = 0.001; checks = []
    def ck(name, exp, got):
        checks.append((name, exp, got, abs(exp - got) <= tol))
    ck('Crest width', crest_width, pts['cr'][0] - pts['cl'][0])
    ck('Total height', crest_elev - seabed_elev, upper_height + lower_height)
    if not g['single_slope_sw']:
        ck('Seaward lower ΔX', lower_height * sw_lower, g['sw_ldx'])
        ck('Seaward berm width', seaward_berm, g['x_sw_bs'] - g['x_sw_be'])
        ck('Seaward upper ΔX', upper_height * sw_upper, g['sw_udx'])
    else:
        ck('Seaward single-slope ΔX', (upper_height + lower_height) * sw_upper, g['x_cl'] - pts['sw_toe'][0])
    if not g['single_slope_lw']:
        ck('Landward upper ΔX', upper_height * lw_upper, g['lw_udx'])
        ck('Landward berm width', landward_berm, g['x_lw_be'] - g['x_lw_bs'])
        ck('Landward lower ΔX', lower_height * lw_lower, g['lw_ldx'])
    else:
        ck('Landward single-slope ΔX', (upper_height + lower_height) * lw_upper, g['x_lw_toe'] - g['x_cr'])
    return checks


def caisson_fos(B, H_c, gamma_c, d, H1pct, gamma_w, mu, q_allow):
    W     = B * H_c * gamma_c
    P     = 0.5 * gamma_w * H1pct**2 + gamma_w * d * H1pct
    F_res = mu * W
    M_res = W * (B / 2)
    arm   = d / 2 + H1pct / 3
    M_ot  = P * arm
    FOS_s = F_res / P if P > 0 else float('inf')
    FOS_o = M_res / M_ot if M_ot > 0 else float('inf')
    q_max = W / B
    return dict(W=W, P=P, F_res=F_res, M_res=M_res, arm=arm,
                M_ot=M_ot, FOS_s=FOS_s, FOS_o=FOS_o, q_max=q_max)


# ── Wave run-up (EurOtop 2018) ─────────────────────────────────────
def calc_wavelength(T):      return 9.81 * T**2 / (2 * math.pi)
def calc_iribarren(ta, H, L): return ta / math.sqrt(H / L) if H > 0 and L > 0 else 0.0
def calc_runup_2pct(H, xi, gf, gb, gbeta):
    ru  = 1.65 * gb * gf * gbeta * xi * H
    cap = (4.0 - 1.5 / math.sqrt(max(gf * gbeta * xi, 1e-12))) * gb * H
    return min(ru, cap)
def calc_runup_1pct(H, xi, gf, gb, gbeta):
    return 1.4 * calc_runup_2pct(H, xi, gf, gb, gbeta)
def calc_reflection(xi):    return min(0.1 * xi**2, 1.0)
def calc_overtopping(H, L0, xi, Rc, gf, gbeta):
    if H <= 0 or L0 <= 0 or xi <= 0: return 0.0
    term = (Rc / (gf * gbeta * H)) * (1.0 / xi)
    return max(math.sqrt(9.81 * H**3) / math.sqrt(L0 / H) * 0.2 * math.exp(-2.3 * term), 0.0)
def calc_obliquity(beta_deg):
    b = abs(beta_deg)
    return max(1.0 - 0.0033 * b, 0.736) if b <= 80 else 0.736
def breaker_type(xi):
    if xi < 0.5:  return "Spilling"
    if xi < 2.0:  return "Plunging"
    if xi < 3.0:  return "Collapsing"
    return "Surging"


# ════════════════════════════════════════════════════════════════════
#  BOUNDARY BUILDER
# ════════════════════════════════════════════════════════════════════

def build_clean_boundary(g, pts, L, R, B_mdl, sy, cy, by, seaward_berm, landward_berm):
    raw = [(L, sy), (L, B_mdl), (R, B_mdl), (R, sy)]
    if not g['single_slope_lw']:
        if g['lw_ldx'] > 0.001: raw.append((pts['lw_be'][0], by))
        if landward_berm > 0.001: raw.append((pts['lw_bs'][0], by))
    raw.append((pts['cr'][0], cy))
    raw.append((pts['cl'][0], cy))
    if not g['single_slope_sw']:
        if g['sw_udx'] > 0.001: raw.append((pts['sw_bs'][0], by))
        if seaward_berm > 0.001: raw.append((pts['sw_be'][0], by))
    raw.append((pts['sw_toe'][0], sy))
    clean = []
    for pt in raw:
        if not clean or abs(pt[0]-clean[-1][0]) > 0.001 or abs(pt[1]-clean[-1][1]) > 0.001:
            clean.append(pt)
    return clean


# ════════════════════════════════════════════════════════════════════
#  EXPORT — WORD
# ════════════════════════════════════════════════════════════════════

def export_rubble_mound_docx(g, layers, dhw, surcharge, crest_elev, seabed_elev,
                              upper_height, lower_height, sw_upper, sw_lower, seaward_berm,
                              lw_upper, lw_lower, landward_berm, crest_width,
                              layer_names, layer_props, n_layers, mat_rubble,
                              checks, fig_bytes):
    try:
        from docx import Document
        from docx.shared import Pt, RGBColor, Inches, Cm
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        from docx.enum.table import WD_ALIGN_VERTICAL
        from docx.oxml.ns import qn
        from docx.oxml import OxmlElement
        import copy

        doc = Document()
        style = doc.styles['Normal']
        style.font.name = 'Calibri'; style.font.size = Pt(11)
        for sec in doc.sections:
            sec.page_width = Cm(21); sec.page_height = Cm(29.7)
            sec.left_margin = Cm(2.5); sec.right_margin = Cm(2.5)
            sec.top_margin = Cm(2.0); sec.bottom_margin = Cm(2.0)

        def add_h1(text):
            p = doc.add_heading(text, level=1)
            p.runs[0].font.color.rgb = RGBColor(0x1a, 0x7f, 0x37)
        def add_h2(text):
            p = doc.add_heading(text, level=2)
            p.runs[0].font.color.rgb = RGBColor(0x2f, 0x81, 0xf7)
        def add_p(text, bold=False):
            p = doc.add_paragraph(text)
            if bold:
                for r in p.runs: r.bold = True
        def add_kv(key, val):
            p = doc.add_paragraph()
            r1 = p.add_run(f"{key}: "); r1.bold = True
            r2 = p.add_run(str(val))
        def set_cell_bg(cell, hex_color):
            tc = cell._tc; tcPr = tc.get_or_add_tcPr()
            shd = OxmlElement('w:shd')
            shd.set(qn('w:fill'), hex_color)
            shd.set(qn('w:val'), 'clear')
            tcPr.append(shd)

        # ── Title
        add_h1("HYRCAN Engineering Suite v4.0 — Rubble Mound Report")
        add_p(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d  %H:%M')}")
        add_p("Developer: Mathias Adjei Tawiah  |  Hohai University — Coastal Engineering")
        add_p("Standards: EurOtop 2018 | JTS 154-1-2011 | GB 50286-2013")
        doc.add_paragraph()

        # ── Geometry summary
        add_h2("1  Embankment Geometry")
        geo_rows = [
            ("Crest Elevation", f"{crest_elev:.3f} m"),
            ("Seabed Elevation", f"{seabed_elev:.3f} m"),
            ("Total Height", f"{crest_elev - seabed_elev:.3f} m"),
            ("Upper Section Height", f"{upper_height:.3f} m"),
            ("Lower Section Height", f"{lower_height:.3f} m"),
            ("Crest Width", f"{crest_width:.3f} m"),
            ("Seaward Slope (upper, H:V)", f"1 : {sw_upper:.2f}"),
            ("Seaward Slope (lower, H:V)", f"1 : {sw_lower:.2f}"),
            ("Seaward Berm Width", f"{seaward_berm:.3f} m"),
            ("Landward Slope (upper, H:V)", f"1 : {lw_upper:.2f}"),
            ("Landward Slope (lower, H:V)", f"1 : {lw_lower:.2f}"),
            ("Landward Berm Width", f"{landward_berm:.3f} m"),
            ("Design High Water Level", f"{dhw:.3f} m"),
            ("Crest Surcharge Load", f"{surcharge:.1f} kN/m²"),
        ]
        t = doc.add_table(rows=1, cols=2)
        t.style = 'Table Grid'
        hdr = t.rows[0].cells
        hdr[0].text = "Parameter"; hdr[1].text = "Value"
        for cell in hdr: set_cell_bg(cell, "0D1117")
        for cell in hdr:
            for run in cell.paragraphs[0].runs:
                run.font.bold = True; run.font.color.rgb = RGBColor(0x8b, 0x94, 0x9e)
        for param, val in geo_rows:
            row = t.add_row().cells
            row[0].text = param; row[1].text = val
        doc.add_paragraph()

        # ── Layer elevations
        add_h2("2  Soil Layer Elevations")
        t2 = doc.add_table(rows=1, cols=6)
        t2.style = 'Table Grid'
        hdrs = ["Layer", "Top Elev. (m)", "Bottom Elev. (m)", "Thickness (m)", "HYRCAN Y-top", "HYRCAN Y-bot"]
        for i, h in enumerate(hdrs):
            c = t2.rows[0].cells[i]; c.text = h
            set_cell_bg(c, "0D1117")
            c.paragraphs[0].runs[0].font.bold = True
            c.paragraphs[0].runs[0].font.color.rgb = RGBColor(0x8b, 0x94, 0x9e)
        for i in range(n_layers):
            r = t2.add_row().cells
            r[0].text = layer_names[i]
            r[1].text = f"{layers[f'top{i+1}']:.3f}"
            r[2].text = f"{layers[f'bot{i+1}']:.3f}"
            r[3].text = f"{i+1 and (layers[f'top{i+1}'] - layers[f'bot{i+1}']):.3f}"
            r[4].text = f"{layers[f'Y_top{i+1}']:.3f}"
            r[5].text = f"{layers[f'Y_bot{i+1}']:.3f}"
        doc.add_paragraph(f"Datum shift applied: +{layers['datum']:.3f} m to all elevations")
        doc.add_paragraph()

        # ── Material properties
        add_h2("3  Material Properties")
        t3 = doc.add_table(rows=1, cols=4)
        t3.style = 'Table Grid'
        mhdrs = ["Material", "Unit Weight γ (kN/m³)", "Cohesion c (kPa)", "Friction Angle φ (°)"]
        for i, h in enumerate(mhdrs):
            c = t3.rows[0].cells[i]; c.text = h
            set_cell_bg(c, "0D1117")
            c.paragraphs[0].runs[0].font.bold = True
            c.paragraphs[0].runs[0].font.color.rgb = RGBColor(0x8b, 0x94, 0x9e)
        # Rubble
        rr = t3.add_row().cells
        rr[0].text = "Rubble Mound (Embankment)"
        rr[1].text = f"{mat_rubble[0]:.1f}"; rr[2].text = f"{mat_rubble[1]:.1f}"; rr[3].text = f"{mat_rubble[2]:.1f}"
        for i in range(n_layers):
            lr = t3.add_row().cells
            lr[0].text = layer_names[i]
            lr[1].text = f"{layer_props[i][0]:.1f}"
            lr[2].text = f"{layer_props[i][1]:.1f}"
            lr[3].text = f"{layer_props[i][2]:.1f}"
        doc.add_paragraph()

        # ── Geometry verification
        add_h2("4  Geometry Verification")
        t4 = doc.add_table(rows=1, cols=4)
        t4.style = 'Table Grid'
        for i, h in enumerate(["Check", "Expected", "Calculated", "Status"]):
            c = t4.rows[0].cells[i]; c.text = h
            set_cell_bg(c, "0D1117")
            c.paragraphs[0].runs[0].font.bold = True
            c.paragraphs[0].runs[0].font.color.rgb = RGBColor(0x8b, 0x94, 0x9e)
        for chk in checks:
            cr = t4.add_row().cells
            cr[0].text = chk[0]; cr[1].text = f"{chk[1]:.4f}"; cr[2].text = f"{chk[2]:.4f}"
            status_run = cr[3].paragraphs[0].add_run("PASS" if chk[3] else "FAIL")
            status_run.font.bold = True
            status_run.font.color.rgb = RGBColor(0x3f, 0xb9, 0x50) if chk[3] else RGBColor(0xf8, 0x51, 0x49)
        doc.add_paragraph()

        # ── Cross-section image
        add_h2("5  Cross-Section")
        if fig_bytes:
            doc.add_picture(io.BytesIO(fig_bytes), width=Inches(6.0))
        doc.add_paragraph()

        buf = io.BytesIO()
        doc.save(buf); buf.seek(0)
        return buf.getvalue()
    except Exception as e:
        return None


def export_caisson_docx(cs_p, r, fig_bytes):
    try:
        from docx import Document
        from docx.shared import Pt, RGBColor, Inches, Cm
        from docx.oxml.ns import qn
        from docx.oxml import OxmlElement

        doc = Document()
        for sec in doc.sections:
            sec.page_width = Cm(21); sec.page_height = Cm(29.7)
            sec.left_margin = Cm(2.5); sec.right_margin = Cm(2.5)
            sec.top_margin = Cm(2.0); sec.bottom_margin = Cm(2.0)

        def set_cell_bg(cell, hex_color):
            tc = cell._tc; tcPr = tc.get_or_add_tcPr()
            shd = OxmlElement('w:shd')
            shd.set(qn('w:fill'), hex_color)
            shd.set(qn('w:val'), 'clear')
            tcPr.append(shd)

        p = doc.add_heading("HYRCAN Engineering Suite v4.0 — Caisson Stability Report", level=1)
        p.runs[0].font.color.rgb = RGBColor(0x1a, 0x7f, 0x37)
        doc.add_paragraph(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d  %H:%M')}")
        doc.add_paragraph("Standards: JTS 154-1-2011 | GB 50286-2013")
        doc.add_paragraph()

        p2 = doc.add_heading("1  Input Parameters", level=2)
        p2.runs[0].font.color.rgb = RGBColor(0x2f, 0x81, 0xf7)
        t = doc.add_table(rows=1, cols=2); t.style = 'Table Grid'
        for c, h in zip(t.rows[0].cells, ["Parameter", "Value"]):
            c.text = h; set_cell_bg(c, "0D1117")
            c.paragraphs[0].runs[0].font.bold = True
            c.paragraphs[0].runs[0].font.color.rgb = RGBColor(0x8b, 0x94, 0x9e)
        for k, v in [("Caisson Width B", f"{cs_p['B']:.2f} m"),
                     ("Caisson Height H_c", f"{cs_p['H_c']:.2f} m"),
                     ("Concrete Unit Weight γ_c", f"{cs_p['gamma_c']:.2f} kN/m³"),
                     ("Water Depth d", f"{cs_p['d']:.2f} m"),
                     ("Wave Height H₁%", f"{cs_p['H1pct']:.2f} m"),
                     ("Water Unit Weight γ_w", f"{cs_p['gamma_w']:.2f} kN/m³"),
                     ("Friction Coefficient μ", f"{cs_p['mu']:.3f}"),
                     ("Allowable Bearing Pressure q_allow", f"{cs_p['q_allow']:.0f} kPa")]:
            rr = t.add_row().cells; rr[0].text = k; rr[1].text = v
        doc.add_paragraph()

        p3 = doc.add_heading("2  Stability Results", level=2)
        p3.runs[0].font.color.rgb = RGBColor(0x2f, 0x81, 0xf7)
        s_ok = r['FOS_s'] >= 1.25; o_ok = r['FOS_o'] >= 1.50; b_ok = r['q_max'] < cs_p['q_allow']
        t2 = doc.add_table(rows=1, cols=5); t2.style = 'Table Grid'
        for c, h in zip(t2.rows[0].cells, ["Check", "Calculated", "Required", "Standard", "Status"]):
            c.text = h; set_cell_bg(c, "0D1117")
            c.paragraphs[0].runs[0].font.bold = True
            c.paragraphs[0].runs[0].font.color.rgb = RGBColor(0x8b, 0x94, 0x9e)
        rows = [
            ("Self-weight W", f"{r['W']:,.1f} kN/m", "—", "—", True),
            ("Wave Force P", f"{r['P']:,.2f} kN/m", "—", "JTS 154-1-2011", True),
            ("Sliding FOS", f"{r['FOS_s']:.3f}", "≥ 1.25", "GB 50286-2013 §5.3.2", s_ok),
            ("Overturning FOS", f"{r['FOS_o']:.3f}", "≥ 1.50", "GB 50286-2013 §5.3.3", o_ok),
            ("Bearing q_max", f"{r['q_max']:,.1f} kPa", f"< {int(cs_p['q_allow'])} kPa", "JTS 154-1-2011 §5.3.4", b_ok),
        ]
        for nm, calc, req, std, ok in rows:
            rr = t2.add_row().cells
            rr[0].text = nm; rr[1].text = calc; rr[2].text = req; rr[3].text = std
            run = rr[4].paragraphs[0].add_run("PASS" if ok else ("FAIL" if req != "—" else "—"))
            run.font.bold = True
            if req != "—":
                run.font.color.rgb = RGBColor(0x3f, 0xb9, 0x50) if ok else RGBColor(0xf8, 0x51, 0x49)
        doc.add_paragraph()

        p4 = doc.add_heading("3  Cross-Section", level=2)
        p4.runs[0].font.color.rgb = RGBColor(0x2f, 0x81, 0xf7)
        if fig_bytes:
            doc.add_picture(io.BytesIO(fig_bytes), width=Inches(5.5))

        buf = io.BytesIO()
        doc.save(buf); buf.seek(0)
        return buf.getvalue()
    except Exception as e:
        return None


def export_waverunup_docx(wu_data):
    try:
        from docx import Document
        from docx.shared import Pt, RGBColor, Cm
        from docx.oxml.ns import qn
        from docx.oxml import OxmlElement

        doc = Document()
        for sec in doc.sections:
            sec.page_width = Cm(21); sec.page_height = Cm(29.7)
            sec.left_margin = Cm(2.5); sec.right_margin = Cm(2.5)
            sec.top_margin = Cm(2.0); sec.bottom_margin = Cm(2.0)

        def set_cell_bg(cell, hex_color):
            tc = cell._tc; tcPr = tc.get_or_add_tcPr()
            shd = OxmlElement('w:shd')
            shd.set(qn('w:fill'), hex_color)
            shd.set(qn('w:val'), 'clear')
            tcPr.append(shd)

        p = doc.add_heading("HYRCAN Engineering Suite v4.0 — Wave Run-Up Report", level=1)
        p.runs[0].font.color.rgb = RGBColor(0x1a, 0x7f, 0x37)
        doc.add_paragraph(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d  %H:%M')}")
        doc.add_paragraph("Standard: EurOtop 2018 (Van der Meer et al.)")
        doc.add_paragraph()

        p2 = doc.add_heading("1  Input Parameters", level=2)
        p2.runs[0].font.color.rgb = RGBColor(0x2f, 0x81, 0xf7)
        t = doc.add_table(rows=1, cols=2); t.style = 'Table Grid'
        for c, h in zip(t.rows[0].cells, ["Parameter", "Value"]):
            c.text = h; set_cell_bg(c, "0D1117")
            c.paragraphs[0].runs[0].font.bold = True
            c.paragraphs[0].runs[0].font.color.rgb = RGBColor(0x8b, 0x94, 0x9e)
        inp = wu_data['inputs']
        for k, v in [("Significant Wave Height H_m0", f"{inp['H']:.3f} m"),
                     ("Peak Wave Period T_p", f"{inp['T']:.3f} s"),
                     ("Slope Ratio (H:V)", f"1 : {inp['slope']:.2f}"),
                     ("tan(α)", f"{1/inp['slope']:.4f}"),
                     ("Freeboard R_c", f"{inp['Rc']:.3f} m"),
                     ("Roughness Factor γ_f", f"{inp['gf']:.3f}"),
                     ("Berm Factor γ_b", f"{inp['gb']:.3f}"),
                     ("Wave Obliquity β", f"{inp['beta']:.1f}°")]:
            rr = t.add_row().cells; rr[0].text = k; rr[1].text = v
        doc.add_paragraph()

        p3 = doc.add_heading("2  Results Summary", level=2)
        p3.runs[0].font.color.rgb = RGBColor(0x2f, 0x81, 0xf7)
        res = wu_data['results']
        t2 = doc.add_table(rows=1, cols=2); t2.style = 'Table Grid'
        for c, h in zip(t2.rows[0].cells, ["Result", "Value"]):
            c.text = h; set_cell_bg(c, "0D1117")
            c.paragraphs[0].runs[0].font.bold = True
            c.paragraphs[0].runs[0].font.color.rgb = RGBColor(0x8b, 0x94, 0x9e)
        for k, v in [("Deep-Water Wavelength L₀", f"{res['L0']:.3f} m"),
                     ("Iribarren Number ξ₀", f"{res['xi']:.4f}"),
                     ("Breaker Type", res['btype']),
                     ("Obliquity Factor γ_β", f"{res['gbeta']:.4f}"),
                     ("Run-Up R_u2% (EurOtop Eq. 5.2)", f"{res['Ru2']:.4f} m"),
                     ("Run-Up R_u1%", f"{res['Ru1']:.4f} m"),
                     ("Reflection Coefficient C_r", f"{res['Cr']:.4f}"),
                     ("Mean Overtopping Rate q", f"{res['q']*1000:.5f} L/s/m  ({res['q']:.6f} m³/s/m)")]:
            rr = t2.add_row().cells; rr[0].text = k; rr[1].text = v
        doc.add_paragraph()

        buf = io.BytesIO(); doc.save(buf); buf.seek(0)
        return buf.getvalue()
    except Exception as e:
        return None


# ════════════════════════════════════════════════════════════════════
#  EXPORT — EXCEL
# ════════════════════════════════════════════════════════════════════

def export_rubble_mound_xlsx(g, layers, layer_names, layer_props, n_layers, mat_rubble,
                              crest_elev, seabed_elev, crest_width, upper_height, lower_height,
                              sw_upper, sw_lower, seaward_berm, lw_upper, lw_lower, landward_berm,
                              dhw, surcharge, checks):
    try:
        import openpyxl
        from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
        from openpyxl.utils import get_column_letter

        wb = openpyxl.Workbook()

        HDR_FILL   = PatternFill("solid", fgColor="161B22")
        HDR_FONT   = Font(name="Calibri", bold=True, color="8B949E", size=10)
        TITLE_FONT = Font(name="Calibri", bold=True, color="2F81F7", size=13)
        SUB_FONT   = Font(name="Calibri", bold=True, color="3FB950", size=11)
        DATA_FONT  = Font(name="Calibri", size=10, color="CDD9E5")
        MONO_FONT  = Font(name="Consolas", size=10, color="E6EDF3")
        SHEET_FILL = PatternFill("solid", fgColor="080C12")
        ROW_FILL   = PatternFill("solid", fgColor="0D1117")
        ALT_FILL   = PatternFill("solid", fgColor="161B22")
        PASS_FONT  = Font(name="Calibri", bold=True, color="3FB950", size=10)
        FAIL_FONT  = Font(name="Calibri", bold=True, color="F85149", size=10)
        thin = Side(style='thin', color="21262D")
        border = Border(left=thin, right=thin, top=thin, bottom=thin)
        center_align = Alignment(horizontal="center", vertical="center")
        left_align   = Alignment(horizontal="left",   vertical="center")

        def style_sheet(ws):
            ws.sheet_properties.tabColor = "0D1117"

        def header_row(ws, row, cols, fill=HDR_FILL):
            for c, col in enumerate(cols, 1):
                cell = ws.cell(row=row, column=c, value=col)
                cell.fill = fill; cell.font = HDR_FONT
                cell.alignment = center_align; cell.border = border

        def data_row(ws, row, vals, alt=False):
            f = ALT_FILL if alt else ROW_FILL
            for c, val in enumerate(vals, 1):
                cell = ws.cell(row=row, column=c, value=val)
                cell.fill = f; cell.font = DATA_FONT
                cell.alignment = left_align; cell.border = border
            return row + 1

        # ── Sheet 1: Geometry
        ws1 = wb.active; ws1.title = "Geometry"; style_sheet(ws1)
        ws1.sheet_view.showGridLines = False
        ws1["A1"] = "HYRCAN v4.0 — Rubble Mound Geometry"
        ws1["A1"].font = TITLE_FONT
        ws1["A2"] = f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
        ws1["A2"].font = Font(name="Calibri", color="8B949E", size=10, italic=True)

        ws1["A4"] = "EMBANKMENT GEOMETRY"; ws1["A4"].font = SUB_FONT
        header_row(ws1, 5, ["Parameter", "Value", "Unit"])
        params = [
            ("Crest Elevation", crest_elev, "m"),
            ("Seabed Elevation", seabed_elev, "m"),
            ("Total Height", crest_elev - seabed_elev, "m"),
            ("Upper Section Height", upper_height, "m"),
            ("Lower Section Height", lower_height, "m"),
            ("Crest Width", crest_width, "m"),
            ("Seaward Slope — Upper (H:V)", sw_upper, "—"),
            ("Seaward Slope — Lower (H:V)", sw_lower, "—"),
            ("Seaward Berm Width", seaward_berm, "m"),
            ("Landward Slope — Upper (H:V)", lw_upper, "—"),
            ("Landward Slope — Lower (H:V)", lw_lower, "—"),
            ("Landward Berm Width", landward_berm, "m"),
            ("Design High Water Level", dhw, "m"),
            ("Crest Surcharge Load", surcharge, "kN/m²"),
        ]
        row = 6
        for i, (p, v, u) in enumerate(params):
            row = data_row(ws1, row, [p, v, u], i % 2 == 1)

        ws1["A21"] = "LAYER ELEVATIONS"; ws1["A21"].font = SUB_FONT
        header_row(ws1, 22, ["Layer", "Top Elev. (m)", "Bottom Elev. (m)", "Thickness (m)", "HYRCAN Y-top", "HYRCAN Y-bot"])
        row = 23
        for i in range(n_layers):
            t_el = layers[f'top{i+1}']; b_el = layers[f'bot{i+1}']
            row = data_row(ws1, row, [layer_names[i], t_el, b_el, t_el - b_el,
                                      layers[f'Y_top{i+1}'], layers[f'Y_bot{i+1}']], i % 2 == 1)
        ws1[f"A{row}"] = f"Datum shift: +{layers['datum']:.3f} m"
        ws1[f"A{row}"].font = Font(name="Calibri", color="8B949E", size=10, italic=True)

        ws1.column_dimensions["A"].width = 34
        ws1.column_dimensions["B"].width = 18
        ws1.column_dimensions["C"].width = 18
        ws1.column_dimensions["D"].width = 18
        ws1.column_dimensions["E"].width = 18
        ws1.column_dimensions["F"].width = 18
        for r in range(1, row + 2):
            ws1.row_dimensions[r].fill = SHEET_FILL

        # ── Sheet 2: Materials
        ws2 = wb.create_sheet("Materials"); style_sheet(ws2)
        ws2.sheet_view.showGridLines = False
        ws2["A1"] = "HYRCAN v4.0 — Material Properties"; ws2["A1"].font = TITLE_FONT
        ws2["A3"] = "MATERIAL PROPERTIES"; ws2["A3"].font = SUB_FONT
        header_row(ws2, 4, ["Material", "γ (kN/m³)", "c (kPa)", "φ (°)"])
        row = 5
        row = data_row(ws2, row, ["Rubble Mound (Embankment)", mat_rubble[0], mat_rubble[1], mat_rubble[2]])
        for i in range(n_layers):
            row = data_row(ws2, row, [layer_names[i], layer_props[i][0], layer_props[i][1], layer_props[i][2]], i % 2 == 1)
        ws2.column_dimensions["A"].width = 34
        for col in ["B","C","D"]: ws2.column_dimensions[col].width = 20

        # ── Sheet 3: Verification
        ws3 = wb.create_sheet("Verification"); style_sheet(ws3)
        ws3.sheet_view.showGridLines = False
        ws3["A1"] = "HYRCAN v4.0 — Geometry Verification"; ws3["A1"].font = TITLE_FONT
        ws3["A3"] = "GEOMETRY CHECKS"; ws3["A3"].font = SUB_FONT
        header_row(ws3, 4, ["Check", "Expected (m)", "Calculated (m)", "Difference", "Status"])
        row = 5
        for i, chk in enumerate(checks):
            f = ALT_FILL if i % 2 == 1 else ROW_FILL
            for c, val in enumerate([chk[0], f"{chk[1]:.4f}", f"{chk[2]:.4f}", f"{abs(chk[1]-chk[2]):.4f}"], 1):
                cell = ws3.cell(row=row, column=c, value=val)
                cell.fill = f; cell.font = DATA_FONT
                cell.alignment = left_align; cell.border = border
            sc = ws3.cell(row=row, column=5, value="PASS" if chk[3] else "FAIL")
            sc.fill = f; sc.font = PASS_FONT if chk[3] else FAIL_FONT
            sc.alignment = center_align; sc.border = border
            row += 1
        ws3.column_dimensions["A"].width = 34
        for col in ["B","C","D","E"]: ws3.column_dimensions[col].width = 18

        buf = io.BytesIO(); wb.save(buf); buf.seek(0)
        return buf.getvalue()
    except Exception as e:
        return None


def export_caisson_xlsx(cs_p, r):
    try:
        import openpyxl
        from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

        wb = openpyxl.Workbook()
        ws = wb.active; ws.title = "Caisson Stability"
        ws.sheet_view.showGridLines = False

        HDR_FILL  = PatternFill("solid", fgColor="161B22")
        HDR_FONT  = Font(name="Calibri", bold=True, color="8B949E", size=10)
        TITLE_F   = Font(name="Calibri", bold=True, color="2F81F7", size=13)
        DATA_F    = Font(name="Calibri", size=10, color="CDD9E5")
        PASS_F    = Font(name="Calibri", bold=True, color="3FB950", size=10)
        FAIL_F    = Font(name="Calibri", bold=True, color="F85149", size=10)
        thin      = Side(style='thin', color="21262D")
        border    = Border(left=thin, right=thin, top=thin, bottom=thin)
        center_a  = Alignment(horizontal="center", vertical="center")
        left_a    = Alignment(horizontal="left",   vertical="center")
        ROW_F     = PatternFill("solid", fgColor="0D1117")
        ALT_F     = PatternFill("solid", fgColor="161B22")

        ws["A1"] = "HYRCAN v4.0 — Vertical Caisson Stability"
        ws["A1"].font = TITLE_F
        ws["A2"] = f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
        ws["A2"].font = Font(name="Calibri", color="8B949E", size=10, italic=True)

        def hr(r, cols):
            for i, col in enumerate(cols, 1):
                c = ws.cell(row=r, column=i, value=col)
                c.fill = HDR_FILL; c.font = HDR_FONT
                c.alignment = center_a; c.border = border

        row = 4
        ws[f"A{row}"] = "INPUT PARAMETERS"
        ws[f"A{row}"].font = Font(name="Calibri", bold=True, color="3FB950", size=11)
        row += 1; hr(row, ["Parameter", "Value", "Unit"]); row += 1
        inp = [("Caisson Width B", cs_p['B'], "m"),
               ("Caisson Height H_c", cs_p['H_c'], "m"),
               ("Concrete Unit Weight γ_c", cs_p['gamma_c'], "kN/m³"),
               ("Water Depth d", cs_p['d'], "m"),
               ("Wave Height H₁%", cs_p['H1pct'], "m"),
               ("Water Unit Weight γ_w", cs_p['gamma_w'], "kN/m³"),
               ("Friction Coefficient μ", cs_p['mu'], "—"),
               ("Allowable Bearing Pressure q_allow", cs_p['q_allow'], "kPa")]
        for i, (p, v, u) in enumerate(inp):
            f = ALT_F if i % 2 else ROW_F
            for ci, val in enumerate([p, v, u], 1):
                c = ws.cell(row=row, column=ci, value=val)
                c.fill = f; c.font = DATA_F; c.alignment = left_a; c.border = border
            row += 1

        row += 1
        ws[f"A{row}"] = "STABILITY RESULTS"
        ws[f"A{row}"].font = Font(name="Calibri", bold=True, color="3FB950", size=11)
        row += 1
        hr(row, ["Check", "Calculated", "Required", "Standard", "Status"]); row += 1
        s_ok = r['FOS_s'] >= 1.25; o_ok = r['FOS_o'] >= 1.50; b_ok = r['q_max'] < cs_p['q_allow']
        results = [
            ("Self-weight W", f"{r['W']:,.1f} kN/m", "—", "—", None),
            ("Wave Force P", f"{r['P']:,.2f} kN/m", "—", "JTS 154-1-2011", None),
            ("Sliding FOS", f"{r['FOS_s']:.3f}", "≥ 1.25", "GB 50286-2013 §5.3.2", s_ok),
            ("Overturning FOS", f"{r['FOS_o']:.3f}", "≥ 1.50", "GB 50286-2013 §5.3.3", o_ok),
            ("Bearing q_max", f"{r['q_max']:,.1f} kPa", f"< {int(cs_p['q_allow'])} kPa", "JTS 154-1-2011 §5.3.4", b_ok),
        ]
        for i, (nm, calc, req, std, ok) in enumerate(results):
            f = ALT_F if i % 2 else ROW_F
            for ci, val in enumerate([nm, calc, req, std], 1):
                c = ws.cell(row=row, column=ci, value=val)
                c.fill = f; c.font = DATA_F; c.alignment = left_a; c.border = border
            sc = ws.cell(row=row, column=5)
            if ok is None: sc.value = "—"; sc.font = DATA_F
            elif ok: sc.value = "PASS"; sc.font = PASS_F
            else: sc.value = "FAIL"; sc.font = FAIL_F
            sc.fill = f; sc.alignment = center_a; sc.border = border
            row += 1

        ws.column_dimensions["A"].width = 36
        ws.column_dimensions["B"].width = 22
        ws.column_dimensions["C"].width = 16
        ws.column_dimensions["D"].width = 30
        ws.column_dimensions["E"].width = 12

        buf = io.BytesIO(); wb.save(buf); buf.seek(0)
        return buf.getvalue()
    except Exception as e:
        return None


def export_waverunup_xlsx(wu_data):
    try:
        import openpyxl
        from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

        wb = openpyxl.Workbook(); ws = wb.active
        ws.title = "Wave Run-Up"; ws.sheet_view.showGridLines = False
        HDR_F = PatternFill("solid", fgColor="161B22")
        HDR_N = Font(name="Calibri", bold=True, color="8B949E", size=10)
        TIT_F = Font(name="Calibri", bold=True, color="2F81F7", size=13)
        DAT_F = Font(name="Calibri", size=10, color="CDD9E5")
        ROW_F = PatternFill("solid", fgColor="0D1117")
        ALT_F = PatternFill("solid", fgColor="161B22")
        thin  = Side(style='thin', color="21262D")
        brd   = Border(left=thin, right=thin, top=thin, bottom=thin)
        ca    = Alignment(horizontal="center", vertical="center")
        la    = Alignment(horizontal="left",   vertical="center")

        ws["A1"] = "HYRCAN v4.0 — Wave Run-Up Analysis"; ws["A1"].font = TIT_F
        ws["A2"] = f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
        ws["A2"].font = Font(name="Calibri", color="8B949E", size=10, italic=True)
        ws["A3"] = "Standard: EurOtop 2018"
        ws["A3"].font = Font(name="Calibri", color="8B949E", size=10, italic=True)

        def hr(r, cols):
            for i, col in enumerate(cols, 1):
                c = ws.cell(row=r, column=i, value=col)
                c.fill = HDR_F; c.font = HDR_N; c.alignment = ca; c.border = brd

        row = 5
        ws[f"A{row}"] = "INPUTS"; ws[f"A{row}"].font = Font(name="Calibri", bold=True, color="3FB950", size=11)
        row += 1; hr(row, ["Parameter", "Value", "Unit"]); row += 1
        inp = wu_data['inputs']
        for i, (p, v, u) in enumerate([
            ("H_m0 — Significant Wave Height", inp['H'], "m"),
            ("T_p — Peak Wave Period", inp['T'], "s"),
            ("Slope Ratio (H:V) = 1:", inp['slope'], "—"),
            ("tan(α)", 1/inp['slope'], "—"),
            ("Freeboard R_c", inp['Rc'], "m"),
            ("Roughness Factor γ_f", inp['gf'], "—"),
            ("Berm Factor γ_b", inp['gb'], "—"),
            ("Wave Obliquity β", inp['beta'], "°"),
        ]):
            f = ALT_F if i % 2 else ROW_F
            for ci, val in enumerate([p, v, u], 1):
                c = ws.cell(row=row, column=ci, value=val)
                c.fill = f; c.font = DAT_F; c.alignment = la; c.border = brd
            row += 1

        row += 1
        ws[f"A{row}"] = "RESULTS"; ws[f"A{row}"].font = Font(name="Calibri", bold=True, color="3FB950", size=11)
        row += 1; hr(row, ["Result Parameter", "Value", "Unit"]); row += 1
        res = wu_data['results']
        for i, (p, v, u) in enumerate([
            ("Deep-Water Wavelength L₀", res['L0'], "m"),
            ("Iribarren Number ξ₀", res['xi'], "—"),
            ("Breaker Classification", res['btype'], "—"),
            ("Obliquity Reduction Factor γ_β", res['gbeta'], "—"),
            ("Run-Up Elevation R_u2% (EurOtop Eq. 5.2)", res['Ru2'], "m"),
            ("Run-Up Elevation R_u1%", res['Ru1'], "m"),
            ("Reflection Coefficient C_r (Postma 1989)", res['Cr'], "—"),
            ("Mean Overtopping Rate q", res['q'], "m³/s/m"),
            ("Mean Overtopping Rate q (litre units)", res['q'] * 1000, "L/s/m"),
        ]):
            f = ALT_F if i % 2 else ROW_F
            for ci, val in enumerate([p, v, u], 1):
                c = ws.cell(row=row, column=ci, value=val)
                c.fill = f; c.font = DAT_F; c.alignment = la; c.border = brd
            row += 1

        ws.column_dimensions["A"].width = 46
        ws.column_dimensions["B"].width = 22
        ws.column_dimensions["C"].width = 16
        buf = io.BytesIO(); wb.save(buf); buf.seek(0)
        return buf.getvalue()
    except Exception as e:
        return None


# ════════════════════════════════════════════════════════════════════
#  PROJECT HISTORY
# ════════════════════════════════════════════════════════════════════

RM_KEYS = ['rm_crest_elev','rm_seabed_elev','rm_crest_width','rm_upper_height',
           'rm_lower_height','rm_sw_upper','rm_sw_lower','rm_sw_berm',
           'rm_lw_upper','rm_lw_lower','rm_lw_berm','rm_dhw','rm_surcharge',
           'rm_num_slices','rm_n_layers',
           'rm_n1','rm_t1','rm_g1','rm_c1','rm_phi1',
           'rm_n2','rm_t2','rm_g2','rm_c2','rm_phi2',
           'rm_n3','rm_t3','rm_g3','rm_c3','rm_phi3',
           'rm_n4','rm_t4','rm_g4','rm_c4','rm_phi4',
           'rm_n5','rm_t5','rm_g5','rm_c5','rm_phi5',
           'rm_gr','rm_cr_','rm_phir']
CS_KEYS = ['cs_B','cs_H_c','cs_gamma_c','cs_d','cs_H1pct','cs_gamma_w','cs_mu','cs_q_allow']
WU_KEYS = ['wu_H','wu_T','wu_slope','wu_Rc','wu_gamma_f','wu_gamma_b','wu_beta']

def save_project_json():
    data = {k: st.session_state[k] for k in RM_KEYS + CS_KEYS + WU_KEYS if k in st.session_state}
    return json.dumps(data, indent=2)

def load_project_json(uploaded):
    data = json.loads(uploaded.read().decode())
    for k, v in data.items():
        st.session_state[k] = v

def snapshot_to_history(name):
    data = {k: st.session_state.get(k) for k in RM_KEYS + CS_KEYS + WU_KEYS}
    entry = {
        'name': name,
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d  %H:%M'),
        'data': data,
        'summary': {
            'crest_elev': st.session_state.get('rm_crest_elev'),
            'seabed_elev': st.session_state.get('rm_seabed_elev'),
            'cs_B': st.session_state.get('cs_B'),
            'wu_H': st.session_state.get('wu_H'),
        }
    }
    st.session_state['project_history'].append(entry)

def restore_from_history(entry):
    for k, v in entry['data'].items():
        if v is not None:
            st.session_state[k] = v


# ════════════════════════════════════════════════════════════════════
#  HYRCAN INSTRUCTIONS TEXT
# ════════════════════════════════════════════════════════════════════

def generate_hyrcan_instructions(
        g, layers, dhw, surcharge, num_slices, crest_elev, seabed_elev,
        upper_height, lower_height, sw_upper, sw_lower, seaward_berm,
        lw_upper, lw_lower, landward_berm, crest_width,
        layer_names, layer_props, n_layers, mat_rubble):
    pts   = g['pts']
    cy    = g['crest_y']; sy = g['seabed_y']; by = g['berm_y']
    L     = 0.0; R = g['model_right']; B_mdl = 0.0
    datum = layers['datum']; dy = dhw + datum
    slope_note = "Single-slope" if g['single_slope_sw'] else "Double-slope with berm"
    clean_pts  = build_clean_boundary(g, pts, L, R, B_mdl, sy, cy, by, seaward_berm, landward_berm)
    boundary_lines = "\n".join([f"  {x:.3f},{y:.3f}" for x, y in clean_pts]) + "\n  c"

    bound_lines = ""
    for i in range(n_layers - 1):
        key = f'Y_bot{i+1}'
        n_top = layer_names[i]; n_bot = layer_names[i+1]
        bound_lines += f"\n  ── Boundary {i+1}: Bottom of {n_top} / Top of {n_bot}\n  {L:.3f},{layers[key]:.3f}\n  {R:.3f},{layers[key]:.3f}\n  d\n"

    mat_rows = []
    all_mats = [("Rubble (Embankment)", mat_rubble[0], mat_rubble[1], mat_rubble[2])]
    for i in range(n_layers):
        all_mats.append((layer_names[i], layer_props[i][0], layer_props[i][1], layer_props[i][2]))
    col_w = [max(len(m[0]) for m in all_mats) + 2, 16, 16, 14]
    mat_sep = "  ╔" + "╦".join(["═"*w for w in col_w]) + "╗"
    mat_hdr = "  ║" + "║".join([h.center(col_w[i]) for i, h in enumerate(["Material","γ (kN/m³)","c (kPa)","φ (°)"])]) + "║"
    mat_div = "  ╠" + "╬".join(["═"*w for w in col_w]) + "╣"
    mat_bot = "  ╚" + "╩".join(["═"*w for w in col_w]) + "╝"
    mrows_str = []
    for nm, gv, cv, phiv in all_mats:
        mrows_str.append("  ║" + "║".join([nm.ljust(col_w[0]), f"{gv:.1f}".center(col_w[1]),
                                             f"{cv:.1f}".center(col_w[2]), f"{phiv:.1f}".center(col_w[3])]) + "║")
    mat_table = "\n".join([mat_sep, mat_hdr, mat_div] + mrows_str + [mat_bot])

    out = f"""\
{'═'*72}
  HYRCAN ENGINEERING SUITE v4.0 — SLOPE STABILITY SETUP
  Mathias Adjei Tawiah  |  Hohai University — Coastal Engineering
  Geometry: {slope_note}  |  Soil layers: {n_layers}
{'═'*72}

STEP 1 — NEW PROJECT
  File → New Project
  Name : Embankment_Stability
  Units: SI  (kN, m, degrees)

──────────────────────────────────────────────────────────────────────
STEP 2 — PROJECT SETTINGS
  Analysis → Project Settings

  [ General ]
    Failure Direction : Left to Right
    Surface Type      : Circular
    Search Method     : Slope Search

  [ Methods ]
    ☑ Bishop Simplified
    ☑ Spencer
    ☑ GLE / Morgenstern-Price
    Number of slices  : {int(num_slices)}

──────────────────────────────────────────────────────────────────────
STEP 3 — EXTERNAL BOUNDARY
  Geometry → External Boundary
  Enter coordinates below (one per line, close with c):

{boundary_lines}

──────────────────────────────────────────────────────────────────────
STEP 4 — MATERIAL BOUNDARIES
  Geometry → Material Boundary

  ── Boundary 0: Seabed / Top of {layer_names[0]}
  {L:.3f},{layers['Y_seabed']:.3f}
  {R:.3f},{layers['Y_seabed']:.3f}
  d
{bound_lines}
  Expected: {n_layers + 1} coloured regions visible.

──────────────────────────────────────────────────────────────────────
STEP 5 — WATER TABLE
  Geometry → Add Water Table

  {L:.3f},{dy:.3f}
  {R:.3f},{dy:.3f}
  d

  Water table Y = {dy:.3f}  (real elevation = {dhw:.2f} m)

──────────────────────────────────────────────────────────────────────
STEP 6 — SURCHARGE LOAD
  Loading → Distributed Load
  Load Type  : Vertical (Downward)
  Magnitude  : {surcharge:.1f} kN/m²
  Crest coordinates:

  {pts['cl'][0]:.3f},{cy:.3f}
  {pts['cr'][0]:.3f},{cy:.3f}
  d

──────────────────────────────────────────────────────────────────────
STEP 7 — MATERIAL PROPERTIES

{mat_table}

  Properties → Assign Properties
  Assign Rubble to the embankment body (above seabed).
  Assign each soil layer to its respective region.

──────────────────────────────────────────────────────────────────────
STEP 8 — COMPUTE
  Analysis → Compute  (allow 15–30 s)

──────────────────────────────────────────────────────────────────────
STEP 9 — RESULTS
  Result tab → record Bishop and Spencer FOS values
  Minimum required FOS: 1.30 (static)

{'═'*72}
DATUM SHIFT REFERENCE
  Bottom of {layer_names[-1]} = {layers[f'bot{n_layers}']:.2f} m → Y = 0.000 (HYRCAN)
  Datum shift: +{datum:.3f} m applied to all elevations

MODEL DIMENSIONS
  Total width  : {R:.3f} m
  Crest        : X = {pts['cl'][0]:.3f} → {pts['cr'][0]:.3f}  (width = {pts['cr'][0]-pts['cl'][0]:.3f} m)
  Seaward toe  : X = {pts['sw_toe'][0]:.3f}
  Landward toe : X = {pts['lw_toe'][0]:.3f}
{'═'*72}
"""
    return out


def generate_coordinates_txt(g, layers, dhw, surcharge, crest_elev, seabed_elev, n_layers, sw_b=0, lw_b=0):
    pts = g['pts']; cy = g['crest_y']; sy = g['seabed_y']; by = g['berm_y']
    L = 0.0; R = g['model_right']; datum = layers['datum']; dy = dhw + datum
    clean_pts  = build_clean_boundary(g, pts, L, R, 0.0, sy, cy, by, sw_b, lw_b)
    clean_lines = [f"{x:.3f},{y:.3f}" for x, y in clean_pts] + ["c"]
    lines = ["HYRCAN COORDINATE EXPORT — v4.0", f"Datum shift: +{datum:.3f} m", "",
             "EXTERNAL BOUNDARY", *clean_lines, "",
             f"MATERIAL BOUNDARY 0 (Seabed):", f"{L:.3f},{layers['Y_seabed']:.3f}", f"{R:.3f},{layers['Y_seabed']:.3f}", "d"]
    for i in range(n_layers - 1):
        lines += ["", f"MATERIAL BOUNDARY {i+1} (Bottom Layer {i+1}):",
                  f"{L:.3f},{layers[f'Y_bot{i+1}']:.3f}", f"{R:.3f},{layers[f'Y_bot{i+1}']:.3f}", "d"]
    lines += ["", "WATER TABLE:", f"{L:.3f},{dy:.3f}", f"{R:.3f},{dy:.3f}", "d",
              "", f"SURCHARGE ({surcharge:.1f} kN/m²):",
              f"{pts['cl'][0]:.3f},{cy:.3f}", f"{pts['cr'][0]:.3f},{cy:.3f}", "d"]
    return "\n".join(lines)


# ════════════════════════════════════════════════════════════════════
#  VISUALIZATIONS
# ════════════════════════════════════════════════════════════════════

LAYER_COLORS = ['#C9B99A', '#A8B5A0', '#B5C4D1', '#D1B5C4', '#B5D1C4']

def draw_rubble_mound(g, layers, dhw, crest_elev, seabed_elev, upper_height, lower_height, layer_names, n_layers):
    pts = g['pts']; ce = crest_elev; se = seabed_elev; berm_e = ce - upper_height
    fig, ax = plt.subplots(figsize=(12, 6), dpi=120)
    fig.patch.set_facecolor('#0d1117'); ax.set_facecolor('#0d1117')
    xl = pts['sw_toe'][0]; xr = pts['lw_toe'][0]
    for i in range(n_layers):
        top_e = layers[f'top{i+1}']; bot_e = layers[f'bot{i+1}']
        col   = LAYER_COLORS[i % len(LAYER_COLORS)]
        ax.fill_betweenx([bot_e, top_e], xl - 999, xr + 999, facecolor=col, alpha=0.5 - i*0.02, zorder=1)
        ax.axhline(y=top_e, color='#333d47', lw=0.8, ls=':', zorder=2)
    ax.axhline(y=se, color='#607d8b', lw=1.3, ls='--', zorder=2)
    if g['single_slope_sw'] and g['single_slope_lw']:
        xs = [pts['sw_toe'][0], pts['cl'][0], pts['cr'][0], pts['lw_toe'][0], pts['sw_toe'][0]]
        ys = [se, ce, ce, se, se]
    elif g['single_slope_sw']:
        xs = [pts['sw_toe'][0], pts['cl'][0], pts['cr'][0], pts['lw_bs'][0], pts['lw_be'][0], pts['lw_toe'][0], pts['sw_toe'][0]]
        ys = [se, ce, ce, berm_e, berm_e, se, se]
    elif g['single_slope_lw']:
        xs = [pts['sw_toe'][0], pts['sw_be'][0], pts['sw_bs'][0], pts['cl'][0], pts['cr'][0], pts['lw_toe'][0], pts['sw_toe'][0]]
        ys = [se, berm_e, berm_e, ce, ce, se, se]
    else:
        xs = [pts['sw_toe'][0], pts['sw_be'][0], pts['sw_bs'][0], pts['cl'][0], pts['cr'][0],
              pts['lw_bs'][0], pts['lw_be'][0], pts['lw_toe'][0], pts['sw_toe'][0]]
        ys = [se, berm_e, berm_e, ce, ce, berm_e, berm_e, se, se]
    ax.fill(xs, ys, facecolor='#C9A96E', alpha=0.88, edgecolor='#7B5E3A', lw=1.8, zorder=3)
    ax.axhline(y=dhw, color='#2f81f7', ls='--', lw=2.0, zorder=4)
    surcharge_val = st.session_state.get('rm_surcharge', 10.0)
    cl_x = pts['cl'][0]; cr_x = pts['cr'][0]; crest_w = cr_x - cl_x
    block_h = max(crest_w * 0.05, 0.4)
    load_rect = mpatches.FancyBboxPatch((cl_x, ce + 0.12), crest_w, block_h,
        boxstyle='square,pad=0', facecolor='#f7931e22', edgecolor='#f7931e', lw=1.5, hatch='////', zorder=10)
    ax.add_patch(load_rect)
    ax.text((cl_x + cr_x)/2, ce + 0.12 + block_h + 0.6,
            f'{surcharge_val:.1f} kN/m²', ha='center', va='bottom',
            fontsize=9, fontweight='600', color='#f7931e', zorder=12)
    lx = xl - (xr - xl) * 0.015
    for i in range(n_layers):
        ax.text(lx, (layers[f'top{i+1}'] + layers[f'bot{i+1}'])/2, layer_names[i],
                fontsize=9, va='center', ha='right', fontstyle='italic', color='#8b949e', zorder=5)
    handles = [
        mpatches.Patch(facecolor='#C9A96E', alpha=0.88, edgecolor='#7B5E3A', label='Rubble Mound (Embankment)'),
        *[mpatches.Patch(facecolor=LAYER_COLORS[i % len(LAYER_COLORS)], alpha=0.7,
                         label=f'{layer_names[i]}  [{layers[f"top{i+1}"]:.1f} → {layers[f"bot{i+1}"]:.1f} m]')
          for i in range(n_layers)],
        mlines.Line2D([], [], color='#2f81f7', ls='--', lw=2, label=f'Design High Water  ({dhw:.2f} m)'),
    ]
    legend = ax.legend(handles=handles, loc='upper center', bbox_to_anchor=(0.5, -0.14),
                       ncol=3, fontsize=9, frameon=True, facecolor='#0d1117',
                       edgecolor='#21262d', framealpha=0.97, labelspacing=0.5)
    for t in legend.get_texts(): t.set_color('#cdd9e5')
    ax.set_xlabel('Distance  (m)', fontsize=11, color='#8b949e')
    ax.set_ylabel('Elevation  (m)', fontsize=11, color='#8b949e')
    ax.set_title('Rubble Mound Embankment — Cross-Section', fontsize=13, fontweight='bold', color='#e6edf3', pad=12)
    ax.grid(True, alpha=0.12, color='#333d47', lw=0.5)
    ax.tick_params(colors='#8b949e', labelsize=9)
    for sp in ax.spines.values(): sp.set_color('#21262d')
    mx = (xr - xl) * 0.08
    ax.set_xlim(xl - mx * 3.5, xr + mx)
    ax.set_ylim(layers[f'bot{n_layers}'] - 1.5, ce + 4.5)
    ax.set_aspect('equal', adjustable='box')
    fig.subplots_adjust(bottom=0.22)
    return fig


def draw_caisson(p, r):
    fig, ax = plt.subplots(figsize=(10, 7), dpi=120)
    fig.patch.set_facecolor('#0d1117'); ax.set_facecolor('#0a0f16')
    B = p['B']; H_c = p['H_c']; d = p['d']
    rb_h = 1.8; rb_ext = 3.0
    rb_xs = [-rb_ext, -rb_ext*0.3, B+rb_ext*0.3, B+rb_ext, -rb_ext]
    rb_ys = [-rb_h, 0, 0, -rb_h, -rb_h]
    ax.fill(rb_xs, rb_ys, facecolor='#C8A96E', alpha=0.85, edgecolor='#7B5E3A', lw=1.2, zorder=2, label='Rubble Foundation')
    ax.axhline(y=0, color='#607d8b', lw=1.3, zorder=3)
    caisson_patch = mpatches.FancyBboxPatch((0, 0), B, H_c, boxstyle='square,pad=0',
        facecolor='#2d4a6b', alpha=0.9, edgecolor='#3d6b9e', lw=2.0, zorder=4)
    ax.add_patch(caisson_patch)
    for xi in np.linspace(B*0.2, B*0.8, 4):
        ax.plot([xi, xi], [0, H_c], color='#3a5f80', lw=0.5, alpha=0.3, zorder=5)
    for yi in [H_c*0.25, H_c*0.5, H_c*0.75]:
        ax.plot([0, B], [yi, yi], color='#3a5f80', lw=0.5, alpha=0.3, zorder=5)
    ax.text(B/2, H_c/2, 'CAISSON\n(Concrete)', ha='center', va='center',
            fontsize=11, fontweight='bold', color='#cdd9e5', zorder=6, alpha=0.9)
    water_y = d
    ax.axhline(y=water_y, color='#2f81f7', ls='--', lw=2.0, zorder=6)
    wx = -B * 0.75; wy = water_y - d * 0.35
    ax.annotate('', xy=(0, wy), xytext=(wx, wy),
                arrowprops=dict(arrowstyle='->', color='#f85149', lw=2.5), zorder=7)
    ax.text(wx - 0.5, wy + 0.3, f'P = {r["P"]:.1f} kN/m\n(Wave Force)',
            fontsize=8.5, color='#f85149', ha='right', zorder=7)
    def dim_arrow(x0, x1, y, label, color='#8b949e', vertical=False):
        if vertical:
            ax.annotate('', xy=(x0, x1), xytext=(x0, y),
                        arrowprops=dict(arrowstyle='<->', color=color, lw=0.9))
            ax.text(x0 + 0.4, (x1 + y)/2, label, fontsize=8, color=color, va='center')
        else:
            ax.annotate('', xy=(x1, y), xytext=(x0, y),
                        arrowprops=dict(arrowstyle='<->', color=color, lw=0.9))
            ax.text((x0+x1)/2, y - 0.5, label, ha='center', fontsize=8, color=color)
    dim_arrow(0, B, -rb_h - 1.2, f'B = {B:.1f} m')
    dim_arrow(B+1.2, 0, H_c, f'H_c = {H_c:.1f} m', vertical=True)
    dim_arrow(-rb_ext-1.8, 0, water_y, f'd = {d:.2f} m', color='#2f81f7', vertical=True)
    ax.text(B/2, water_y + 0.4, f'H₁% = {p["H1pct"]:.2f} m', ha='center', fontsize=8.5, color='#2f81f7')
    s_ok = r['FOS_s'] >= 1.25; o_ok = r['FOS_o'] >= 1.50; b_ok = r['q_max'] < p['q_allow']
    summary = (f"Sliding FOS:      {r['FOS_s']:.3f}  {'✓' if s_ok else '✗'}\n"
               f"Overturning FOS:  {r['FOS_o']:.3f}  {'✓' if o_ok else '✗'}\n"
               f"q_max:            {r['q_max']:.0f} kPa  {'✓' if b_ok else '✗'}")
    ax.text(0.02, 0.98, summary, transform=ax.transAxes, fontsize=9, va='top', ha='left',
            fontfamily='monospace', color='#e6edf3',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#0d1117', edgecolor='#21262d', alpha=0.95))
    handles = [
        mpatches.Patch(facecolor='#2d4a6b', alpha=0.9, edgecolor='#3d6b9e', label='Caisson (Concrete)'),
        mpatches.Patch(facecolor='#C8A96E', alpha=0.85, edgecolor='#7B5E3A', label='Rubble Foundation'),
        mlines.Line2D([], [], color='#2f81f7', ls='--', lw=2, label=f'Design Water Level (d = {d:.2f} m)'),
    ]
    legend = ax.legend(handles=handles, loc='upper right', fontsize=9, frameon=True,
                       facecolor='#0d1117', edgecolor='#21262d', framealpha=0.97)
    for t in legend.get_texts(): t.set_color('#cdd9e5')
    ax.set_xlabel('Distance  (m)', fontsize=11, color='#8b949e')
    ax.set_ylabel('Elevation  (m)', fontsize=11, color='#8b949e')
    ax.set_title('Vertical Caisson — Cross-Section & Stability', fontsize=13, fontweight='bold', color='#e6edf3', pad=12)
    ax.grid(True, alpha=0.12, color='#333d47', lw=0.5)
    ax.tick_params(colors='#8b949e', labelsize=9)
    for sp in ax.spines.values(): sp.set_color('#21262d')
    pad = B * 1.3
    ax.set_xlim(-pad, B + pad); ax.set_ylim(-rb_h - 2.5, H_c + 4.5)
    fig.tight_layout()
    return fig


# ════════════════════════════════════════════════════════════════════
#  UI HELPERS
# ════════════════════════════════════════════════════════════════════

def section(label):
    st.markdown(f'<div class="sec-lbl">{label}</div>', unsafe_allow_html=True)

def num(label, key, **kw):
    kw.setdefault('format', '%.2f')
    val = st.number_input(label, value=float(st.session_state[key]), key=f'_ni_{key}', **kw)
    st.session_state[key] = val
    return val

def txt(label, key):
    st.session_state[key] = st.text_input(label, value=st.session_state[key], key=f'_ti_{key}')
    return st.session_state[key]

def eq_block(label, formula, substitution, result_line, reference=None):
    ref_html = f'<div class="eq-sub">Reference: {reference}</div>' if reference else ''
    st.markdown(f"""
<div class="eq-block">
  <div class="eq-label">{label}</div>
  <div class="eq-main">{formula}</div>
  <div class="eq-sub">{substitution}</div>
  <div class="eq-result">{result_line}</div>
  {ref_html}
</div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
<div style="padding:18px 4px 12px 4px;">
  <div style="font-size:22px;font-weight:800;color:#e6edf3;letter-spacing:-0.5px;">HYRCAN</div>
  <div style="font-size:11px;color:#8b949e;margin-top:2px;letter-spacing:0.5px;">ENGINEERING SUITE  v4.0</div>
</div>
""", unsafe_allow_html=True)

    with st.expander("ℹ️  About", expanded=False):
        st.markdown("""
<div class="info-card" style="margin:0;">
  <div class="ic-body">
    <b style="color:#cdd9e5;">Developer</b><br>
    Mathias Adjei Tawiah<br>
    <span style="color:#8b949e;font-size:11px;">mathiasadjeitawiah@gmail.com</span><br><br>
    <b style="color:#cdd9e5;">Institution</b><br>
    Hohai University<br>
    <span style="color:#8b949e;font-size:11px;">College of Harbor, Coastal &amp; Offshore Engineering</span><br><br>
    <b style="color:#cdd9e5;">Standards</b><br>
    EurOtop 2018 · JTS 154-1-2011 · GB 50286-2013
  </div>
</div>
""", unsafe_allow_html=True)

    st.markdown('<div class="sec-lbl">Project</div>', unsafe_allow_html=True)
    proj_name = st.text_input("Save name", value="Project_001", label_visibility="collapsed",
                               placeholder="Project name…", key="_proj_name_input")
    if st.button("📌  Save to History", use_container_width=True):
        snapshot_to_history(proj_name if proj_name else f"Project_{len(st.session_state['project_history'])+1}")
        st.success("Saved to session history", icon="✅")

    history = st.session_state.get('project_history', [])
    if history:
        st.markdown('<div class="sec-lbl">Session History</div>', unsafe_allow_html=True)
        for idx, entry in enumerate(reversed(history)):
            with st.expander(f"📁  {entry['name']}", expanded=False):
                st.caption(entry['timestamp'])
                st.caption(f"Crest: {entry['summary'].get('crest_elev','—')} m  |  B: {entry['summary'].get('cs_B','—')} m")
                if st.button(f"Restore", key=f"_restore_{idx}", use_container_width=True):
                    restore_from_history(entry)
                    st.rerun()

    st.markdown('<div class="sec-lbl">File I/O</div>', unsafe_allow_html=True)
    project_json = save_project_json()
    st.download_button('⬇  Export Project (.json)', data=project_json,
                       file_name='hyrcan_project.json', mime='application/json',
                       use_container_width=True)
    uploaded = st.file_uploader('Import Project', type='json', label_visibility='collapsed')
    if uploaded:
        load_project_json(uploaded)
        st.success('Project loaded', icon='✅')
        st.rerun()

    st.markdown("""
<div style="margin-top:24px;padding-top:12px;border-top:1px solid #21262d;">
  <div style="font-size:11px;color:#484f58;line-height:2;">
    <a href="https://github.com/Mathias-lab/hyrcan-suite" target="_blank"
       style="color:#2f81f7;text-decoration:none;">⬡  GitHub Repository</a><br>
    <a href="https://linkedin.com/in/mathias-adjei-tawiah" target="_blank"
       style="color:#2f81f7;text-decoration:none;">⬡  LinkedIn</a>
  </div>
  <div style="font-size:10px;color:#30363d;margin-top:10px;">
    Coordinate logic verified against HYRCAN 3.0
  </div>
</div>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
#  HEADER
# ════════════════════════════════════════════════════════════════════

st.markdown("""
<div style="border-bottom:1px solid #21262d;padding:14px 0 14px 0;margin-bottom:4px;display:flex;align-items:center;gap:16px;">
  <span style="font-size:28px;">⚓</span>
  <div>
    <span style="font-size:20px;font-weight:800;color:#e6edf3;letter-spacing:-0.3px;">HYRCAN Engineering Suite</span>
    <span style="font-size:13px;color:#8b949e;font-weight:400;margin-left:8px;">v4.0</span>
    <div style="font-size:12px;color:#8b949e;margin-top:2px;">
      Rubble Mound Stability · Vertical Caisson Analysis · Wave Run-Up · EurOtop 2018
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
#  TABS
# ════════════════════════════════════════════════════════════════════

tab1, tab2, tab3 = st.tabs([
    "  Rubble Mound Coordinate Generator  ",
    "  Vertical Caisson Stability  ",
    "  Wave Run-Up Calculator  ",
])


# ────────────────────────────────────────────────────────────────────
#  TAB 1 — RUBBLE MOUND
# ────────────────────────────────────────────────────────────────────

with tab1:
    left_col, right_col = st.columns([1, 1.65], gap='large')

    with left_col:
        section("EMBANKMENT GEOMETRY")
        c1, c2 = st.columns(2)
        with c1:
            ce = num('Crest elevation (m)', 'rm_crest_elev')
            cw = num('Crest width (m)', 'rm_crest_width', min_value=0.5)
            uh = num('Upper section height (m)', 'rm_upper_height', min_value=0.0)
        with c2:
            se = num('Seabed elevation (m)', 'rm_seabed_elev')
            lh = num('Lower section height (m)', 'rm_lower_height', min_value=0.0)

        total_h = ce - se
        if abs((uh + lh) - total_h) > 0.01:
            st.error(f"Height mismatch: upper + lower = {uh+lh:.3f} m, expected {total_h:.3f} m")

        section("SLOPE RATIOS  (H : V)  —  Set berm = 0 for single slope")
        c1, c2, c3 = st.columns(3)
        with c1:
            sw_u = num('SW upper', 'rm_sw_upper', min_value=0.1)
            sw_l = num('SW lower', 'rm_sw_lower', min_value=0.1)
        with c2:
            lw_u = num('LW upper', 'rm_lw_upper', min_value=0.1)
            lw_l = num('LW lower', 'rm_lw_lower', min_value=0.1)
        with c3:
            sw_b = num('SW berm (m)', 'rm_sw_berm', min_value=0.0)
            lw_b = num('LW berm (m)', 'rm_lw_berm', min_value=0.0)

        section("HYDRAULIC CONDITIONS")
        c1, c2, c3 = st.columns(3)
        with c1: dhw = num('DHW level (m)', 'rm_dhw')
        with c2: q   = num('Surcharge (kN/m²)', 'rm_surcharge', min_value=0.0)
        with c3: ns  = num('Slices', 'rm_num_slices', min_value=10.0, step=5.0, format='%.0f')

        section("FOUNDATION LAYERS")
        n_layers = st.slider('Number of soil layers', min_value=3, max_value=5,
                             value=int(st.session_state['rm_n_layers']), step=1)
        st.session_state['rm_n_layers'] = n_layers

        layer_names = []; layer_thicknesses = []; layer_props = []
        header_cols = st.columns([2.2, 1.3, 1.3, 1.3, 1.3])
        for col, h in zip(header_cols, ["Layer Name", "Thickness (m)", "γ (kN/m³)", "c (kPa)", "φ (°)"]):
            col.markdown(f"<span style='font-size:11px;font-weight:600;color:#8b949e;'>{h}</span>", unsafe_allow_html=True)
        for i in range(1, n_layers + 1):
            c_name, c_t, c_g, c_c, c_phi = st.columns([2.2, 1.3, 1.3, 1.3, 1.3])
            with c_name: name = txt(' ', f'rm_n{i}')
            with c_t:    t    = num(' ', f'rm_t{i}', min_value=0.1)
            with c_g:    g_   = num(' ', f'rm_g{i}', min_value=10.0)
            with c_c:    c_   = num(' ', f'rm_c{i}', min_value=0.0)
            with c_phi:  phi  = num(' ', f'rm_phi{i}', min_value=0.0)
            layer_names.append(name); layer_thicknesses.append(t); layer_props.append((g_, c_, phi))

        section("EMBANKMENT (RUBBLE MOUND) PROPERTIES")
        c1, c2, c3 = st.columns(3)
        with c1: gr   = num('γ (kN/m³)', 'rm_gr',  min_value=10.0)
        with c2: cr_  = num('c (kPa)',   'rm_cr_', min_value=0.0)
        with c3: phir = num('φ (°)',     'rm_phir',min_value=0.0)

        layers = compute_layer_elevations(se, layer_thicknesses)

        section("LAYER ELEVATION PREVIEW")
        df_rows = {
            'Layer':           layer_names,
            'Top (m)':         [f"{layers[f'top{i+1}']:.3f}" for i in range(n_layers)],
            'Bottom (m)':      [f"{layers[f'bot{i+1}']:.3f}" for i in range(n_layers)],
            'Thickness (m)':   [f"{(layers[f'top{i+1}'] - layers[f'bot{i+1}']):.3f}" for i in range(n_layers)],
            'HYRCAN Y-top':    [f"{layers[f'Y_top{i+1}']:.3f}" for i in range(n_layers)],
            'HYRCAN Y-bot':    [f"{layers[f'Y_bot{i+1}']:.3f}" for i in range(n_layers)],
        }
        st.dataframe(pd.DataFrame(df_rows), use_container_width=True, hide_index=True)
        st.caption(f"Datum shift: +{layers['datum']:.3f} m  ·  Bottom of '{layer_names[-1]}' → Y = 0.000")

        st.markdown('<br>', unsafe_allow_html=True)
        generate = st.button('Generate HYRCAN Coordinates', type='primary', use_container_width=True)

    with right_col:
        layers = compute_layer_elevations(se, layer_thicknesses)
        valid  = abs((uh + lh) - (ce - se)) <= 0.01

        if generate and valid:
            g = compute_geometry(ce, se, cw, uh, lh, sw_u, sw_l, sw_b, lw_u, lw_l, lw_b, layers)
            st.session_state.update({
                'rm_g': g, 'rm_layers': layers, 'rm_layer_names': layer_names,
                'rm_layer_thicknesses': layer_thicknesses, 'rm_layer_props': layer_props,
                'rm_n_layers_gen': n_layers, 'rm_sw_upper_gen': sw_u, 'rm_sw_lower_gen': sw_l,
                'rm_sw_berm_gen': sw_b, 'rm_lw_upper_gen': lw_u, 'rm_lw_lower_gen': lw_l,
                'rm_lw_berm_gen': lw_b, 'rm_generated': True,
            })

        # ── Live cross-section preview ──────────────────────────────
        section("CROSS-SECTION PREVIEW")
        try:
            g_prev = compute_geometry(ce, se, cw, uh, lh, sw_u, sw_l, sw_b, lw_u, lw_l, lw_b, layers)
            fig_prev = draw_rubble_mound(g_prev, layers, dhw, ce, se, uh, lh, layer_names, n_layers)
            st.pyplot(fig_prev, use_container_width=True)
            plt.close(fig_prev)
        except Exception as e:
            st.warning(f"Preview unavailable: {e}")

        if st.session_state.get('rm_generated'):
            g      = st.session_state['rm_g']
            layers = st.session_state['rm_layers']
            lnames = st.session_state['rm_layer_names']
            lprops = st.session_state['rm_layer_props']
            nl     = st.session_state['rm_n_layers_gen']
            _sw_u  = st.session_state.get('rm_sw_upper_gen', sw_u)
            _sw_l  = st.session_state.get('rm_sw_lower_gen', sw_l)
            _sw_b  = st.session_state.get('rm_sw_berm_gen',  sw_b)
            _lw_u  = st.session_state.get('rm_lw_upper_gen', lw_u)
            _lw_l  = st.session_state.get('rm_lw_lower_gen', lw_l)
            _lw_b  = st.session_state.get('rm_lw_berm_gen',  lw_b)

            # ── Verification ────────────────────────────────────────
            section("GEOMETRY VERIFICATION")
            checks = verify_geometry(g, ce, se, cw, uh, lh, _sw_u, _sw_l, _sw_b, _lw_u, _lw_l, _lw_b)
            all_ok = all(c[3] for c in checks)
            if all_ok:
                st.success('All geometry checks passed', icon='✅')
            else:
                st.error('One or more geometry checks failed — review parameters')
            df_chk = pd.DataFrame({'Parameter': [c[0] for c in checks],
                                   'Expected':   [f'{c[1]:.4f}' for c in checks],
                                   'Calculated': [f'{c[2]:.4f}' for c in checks],
                                   'Status':     ['Pass' if c[3] else 'FAIL' for c in checks]})
            st.dataframe(df_chk, use_container_width=True, hide_index=True)

            mc1, mc2, mc3, mc4 = st.columns(4)
            mc1.metric('Model width',    f"{g['model_right']:.3f} m")
            mc2.metric('Crest left X',   f"{g['pts']['cl'][0]:.3f}")
            mc3.metric('Crest right X',  f"{g['pts']['cr'][0]:.3f}")
            mc4.metric('Datum shift',    f"+{layers['datum']:.3f} m")

            # ── Material properties table (professional) ────────────
            section("MATERIAL PROPERTIES — STEP 7 INPUT TABLE")
            all_mats_display = [("Rubble Mound (Embankment)", gr, cr_, phir, "Embankment body")]
            for i in range(nl):
                all_mats_display.append((lnames[i], lprops[i][0], lprops[i][1], lprops[i][2], f"Layer {i+1}"))
            mat_html = """
<table class="pro-table">
<thead>
<tr>
  <th>#</th>
  <th>Material Description</th>
  <th style="text-align:right;">Unit Weight<br>γ (kN/m³)</th>
  <th style="text-align:right;">Cohesion<br>c (kPa)</th>
  <th style="text-align:right;">Friction Angle<br>φ (°)</th>
  <th>Region Assignment</th>
</tr>
</thead>
<tbody>
"""
            for i, (nm, gv, cv, phiv, region) in enumerate(all_mats_display):
                mat_html += f"""<tr>
  <td class="num-cell">{i+1}</td>
  <td class="mat-name">{nm}</td>
  <td class="num-cell">{gv:.1f}</td>
  <td class="num-cell">{cv:.1f}</td>
  <td class="num-cell">{phiv:.1f}</td>
  <td style="color:#8b949e;font-size:11px;">{region}</td>
</tr>"""
            mat_html += "</tbody></table>"
            st.markdown(mat_html, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

            # ── HYRCAN instructions ────────────────────────────────
            section("HYRCAN SETUP INSTRUCTIONS")
            instructions = generate_hyrcan_instructions(
                g, layers, dhw, q, ns, ce, se, uh, lh,
                _sw_u, _sw_l, _sw_b, _lw_u, _lw_l, _lw_b, cw,
                lnames, lprops, nl, mat_rubble=(gr, cr_, phir))
            st.markdown(f'<div class="code-out">{instructions}</div>', unsafe_allow_html=True)

            # ── Export row ─────────────────────────────────────────
            section("EXPORT")

            # generate fig for export
            buf_png = io.BytesIO()
            fig_exp = draw_rubble_mound(g, layers, dhw, ce, se, uh, lh, lnames, nl)
            fig_exp.savefig(buf_png, format='png', dpi=300, bbox_inches='tight', facecolor='white')
            plt.close(fig_exp)
            fig_bytes_rm = buf_png.getvalue()

            e1, e2, e3, e4 = st.columns(4)
            with e1:
                coords_txt = generate_coordinates_txt(g, layers, dhw, q, ce, se, nl, _sw_b, _lw_b)
                st.download_button('Coordinates (.txt)', data=coords_txt,
                                   file_name='hyrcan_coordinates.txt', mime='text/plain',
                                   use_container_width=True)
            with e2:
                st.download_button('Instructions (.txt)', data=instructions,
                                   file_name='hyrcan_instructions.txt', mime='text/plain',
                                   use_container_width=True)
            with e3:
                docx_bytes = export_rubble_mound_docx(g, layers, dhw, q, ce, se, uh, lh,
                    _sw_u, _sw_l, _sw_b, _lw_u, _lw_l, _lw_b, cw,
                    lnames, lprops, nl, (gr, cr_, phir), checks, fig_bytes_rm)
                if docx_bytes:
                    st.download_button('Report (.docx)', data=docx_bytes,
                                       file_name='hyrcan_rubble_mound_report.docx',
                                       mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                                       use_container_width=True)
            with e4:
                xlsx_bytes = export_rubble_mound_xlsx(g, layers, lnames, lprops, nl, (gr, cr_, phir),
                    ce, se, cw, uh, lh, _sw_u, _sw_l, _sw_b, _lw_u, _lw_l, _lw_b, dhw, q, checks)
                if xlsx_bytes:
                    st.download_button('Workbook (.xlsx)', data=xlsx_bytes,
                                       file_name='hyrcan_rubble_mound_data.xlsx',
                                       mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                                       use_container_width=True)

            st.download_button('Cross-Section Plot (PNG 300 dpi)', data=fig_bytes_rm,
                               file_name='hyrcan_cross_section.png', mime='image/png',
                               use_container_width=True)

        elif generate and not valid:
            st.error('Correct the height mismatch before generating.')
        elif not st.session_state.get('rm_generated'):
            st.info('Enter parameters and click Generate to produce HYRCAN coordinates and export files.', icon='ℹ️')


# ────────────────────────────────────────────────────────────────────
#  TAB 2 — VERTICAL CAISSON
# ────────────────────────────────────────────────────────────────────

with tab2:
    left2, right2 = st.columns([1, 1.65], gap='large')

    with left2:
        section("CAISSON GEOMETRY")
        c1, c2 = st.columns(2)
        with c1:
            B_cs  = num('Width B (m)', 'cs_B', min_value=1.0)
            gc    = num('Concrete γ_c (kN/m³)', 'cs_gamma_c', min_value=10.0)
        with c2:
            Hc_cs = num('Height H_c (m)', 'cs_H_c', min_value=1.0)

        section("HYDRAULIC CONDITIONS")
        c1, c2, c3 = st.columns(3)
        with c1: d_cs  = num('Water depth d (m)', 'cs_d', min_value=0.1)
        with c2: H1_cs = num('Wave height H₁% (m)', 'cs_H1pct', min_value=0.1)
        with c3: gw_cs = num('Water γ_w (kN/m³)', 'cs_gamma_w', min_value=9.0)

        section("STABILITY PARAMETERS")
        c1, c2 = st.columns(2)
        with c1: mu_cs = num('Friction coefficient μ', 'cs_mu', min_value=0.1, max_value=1.0, step=0.01)
        with c2: qa_cs = num('Allowable bearing q (kPa)', 'cs_q_allow', min_value=50.0)

        st.markdown("""
<div class="info-card" style="margin-top:20px;">
  <div class="ic-title">Design Standards</div>
  <div class="ic-body">
    Wave force  · JTS 154-1-2011 Appendix A<br>
    Sliding FOS ≥ 1.25 · GB 50286-2013 §5.3.2<br>
    Overturning FOS ≥ 1.50 · GB 50286-2013 §5.3.3<br>
    Bearing: q_max &lt; q_allow · JTS 154-1-2011 §5.3.4
  </div>
</div>""", unsafe_allow_html=True)

    with right2:
        cs_p = dict(B=B_cs, H_c=Hc_cs, gamma_c=gc, d=d_cs,
                    H1pct=H1_cs, gamma_w=gw_cs, mu=mu_cs, q_allow=qa_cs)
        r = caisson_fos(**cs_p)
        s_ok = r['FOS_s'] >= 1.25; o_ok = r['FOS_o'] >= 1.50; b_ok = r['q_max'] < qa_cs

        section("STABILITY SUMMARY")
        m1, m2, m3 = st.columns(3)
        m1.metric('Sliding FOS', f"{r['FOS_s']:.3f}",
                  delta='≥ 1.25  Pass' if s_ok else '< 1.25  Fail',
                  delta_color='normal' if s_ok else 'inverse')
        m2.metric('Overturning FOS', f"{r['FOS_o']:.3f}",
                  delta='≥ 1.50  Pass' if o_ok else '< 1.50  Fail',
                  delta_color='normal' if o_ok else 'inverse')
        m3.metric('Bearing q_max', f"{r['q_max']:.1f} kPa",
                  delta=f"< {int(qa_cs)} kPa  Pass" if b_ok else f"≥ {int(qa_cs)} kPa  Fail",
                  delta_color='normal' if b_ok else 'inverse')

        if s_ok and o_ok and b_ok:
            st.success('All stability checks satisfied — design is adequate.', icon='✅')
        else:
            st.error('One or more stability checks failed — revise the design parameters.')

        section("RESULTS TABLE")
        df_res = pd.DataFrame({
            'Check':      ['Self-weight W', 'Wave Force P', 'Sliding FOS', 'Overturning FOS', 'Bearing q_max'],
            'Calculated': [f"{r['W']:,.1f} kN/m", f"{r['P']:,.3f} kN/m",
                           f"{r['FOS_s']:.3f}", f"{r['FOS_o']:.3f}", f"{r['q_max']:,.1f} kPa"],
            'Required':   ['—', '—', '≥ 1.25', '≥ 1.50', f"< {int(qa_cs)} kPa"],
            'Standard':   ['—', 'JTS 154-1-2011 App. A', 'GB 50286-2013 §5.3.2',
                           'GB 50286-2013 §5.3.3', 'JTS 154-1-2011 §5.3.4'],
            'Status':     ['—', '—',
                           'Pass' if s_ok else 'FAIL',
                           'Pass' if o_ok else 'FAIL',
                           'Pass' if b_ok else 'FAIL'],
        })
        st.dataframe(df_res, use_container_width=True, hide_index=True)

        # ── Professional equation blocks ────────────────────────────
        section("CALCULATION REPORT")

        eq_block(
            "1.  Self-Weight",
            "W = B × H_c × γ_c",
            f"W = {B_cs:.2f} m × {Hc_cs:.2f} m × {gc:.2f} kN/m³",
            f"W = {r['W']:,.2f} kN/m"
        )

        eq_block(
            "2.  Wave Force  (JTS 154-1-2011, Appendix A)",
            "P = ½ · γ_w · H₁%² + γ_w · d · H₁%",
            f"P = ½ × {gw_cs:.2f} × {H1_cs:.2f}² + {gw_cs:.2f} × {d_cs:.2f} × {H1_cs:.2f}",
            f"P = {0.5*gw_cs*H1_cs**2:.3f} + {gw_cs*d_cs*H1_cs:.3f} = {r['P']:,.3f} kN/m",
            "JTS 154-1-2011, Appendix A"
        )

        eq_block(
            "3.  Sliding Stability  (GB 50286-2013 §5.3.2)",
            "FOS_sliding = μ · W / P",
            f"FOS_sliding = {mu_cs:.2f} × {r['W']:,.2f} / {r['P']:,.3f}",
            f"FOS_sliding = {r['FOS_s']:.4f}  (required ≥ 1.25  →  {'Pass' if s_ok else 'FAIL'})",
            "GB 50286-2013 §5.3.2"
        )

        eq_block(
            "4.  Overturning Stability  (GB 50286-2013 §5.3.3)",
            "FOS_overturning = (W · B/2) / (P · arm)     where arm = d/2 + H₁%/3",
            f"arm = {d_cs:.3f}/2 + {H1_cs:.3f}/3 = {r['arm']:.4f} m\n"
            f"M_res = {r['W']:,.2f} × {B_cs/2:.3f} = {r['M_res']:,.2f} kN·m/m\n"
            f"M_ot  = {r['P']:,.3f} × {r['arm']:.4f} = {r['M_ot']:,.2f} kN·m/m",
            f"FOS_overturning = {r['M_res']:,.2f} / {r['M_ot']:,.2f} = {r['FOS_o']:.4f}  (required ≥ 1.50  →  {'Pass' if o_ok else 'FAIL'})",
            "GB 50286-2013 §5.3.3"
        )

        eq_block(
            "5.  Foundation Bearing Pressure  (JTS 154-1-2011 §5.3.4)",
            "q_max = W / B",
            f"q_max = {r['W']:,.2f} / {B_cs:.2f}",
            f"q_max = {r['q_max']:,.2f} kPa  (allowable = {int(qa_cs)} kPa  →  {'Pass' if b_ok else 'FAIL'})",
            "JTS 154-1-2011 §5.3.4"
        )

        section("CROSS-SECTION")
        fig_cs = draw_caisson(cs_p, r)
        st.pyplot(fig_cs, use_container_width=True)

        section("EXPORT")
        buf2 = io.BytesIO()
        fig_cs2 = draw_caisson(cs_p, r)
        fig_cs2.savefig(buf2, format='png', dpi=300, bbox_inches='tight', facecolor='white')
        plt.close(fig_cs2); buf2.seek(0)
        fig_bytes_cs = buf2.getvalue()

        e1, e2, e3 = st.columns(3)
        with e1:
            st.download_button('Plot (PNG 300 dpi)', data=fig_bytes_cs,
                               file_name='hyrcan_caisson.png', mime='image/png',
                               use_container_width=True)
        with e2:
            docx_cs = export_caisson_docx(cs_p, r, fig_bytes_cs)
            if docx_cs:
                st.download_button('Report (.docx)', data=docx_cs,
                                   file_name='hyrcan_caisson_report.docx',
                                   mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                                   use_container_width=True)
        with e3:
            xlsx_cs = export_caisson_xlsx(cs_p, r)
            if xlsx_cs:
                st.download_button('Workbook (.xlsx)', data=xlsx_cs,
                                   file_name='hyrcan_caisson_data.xlsx',
                                   mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                                   use_container_width=True)


# ────────────────────────────────────────────────────────────────────
#  TAB 3 — WAVE RUN-UP
# ────────────────────────────────────────────────────────────────────

with tab3:
    left3, right3 = st.columns([1, 1.5], gap='large')

    with left3:
        section("WAVE PARAMETERS")
        c1, c2 = st.columns(2)
        with c1: H_wu = num('Significant wave height H_m0 (m)', 'wu_H', min_value=0.1)
        with c2: T_wu = num('Peak wave period T_p (s)',           'wu_T', min_value=1.0)

        section("STRUCTURE GEOMETRY")
        slope_wu = num('Slope ratio (H:V)  e.g. 2.5 → slope = 1:2.5', 'wu_slope', min_value=0.1)
        Rc_wu    = num('Freeboard R_c (m) — crest height above SWL', 'wu_Rc', min_value=0.0)

        section("REDUCTION FACTORS  (EurOtop 2018)")
        c1, c2 = st.columns(2)
        with c1: gf_wu = num('Roughness γ_f', 'wu_gamma_f', min_value=0.1, max_value=1.0, step=0.01)
        with c2: gb_wu = num('Berm γ_b',       'wu_gamma_b', min_value=0.1, max_value=1.0, step=0.01)
        beta_wu = num('Wave obliquity β (°)', 'wu_beta', min_value=0.0, max_value=80.0, step=1.0, format='%.1f')

        with st.expander("Roughness Factor Reference  (EurOtop 2018, Table 5.2)"):
            rf_data = {'Structure Type': [
                'Smooth impermeable (concrete / asphalt)', 'Grass (short)',
                'Grass (long / rough)', 'Single-size rock (permeable)',
                'Double-layer rock (permeable)', 'Rock armour (rough permeable)',
                'Tetrapods', 'Accropode', 'Xbloc',
                'Cube (single layer)', 'Cube (double layer)',
            ], 'γ_f': [
                '1.00', '1.00', '0.90 – 1.00', '0.55', '0.45',
                '0.40 – 0.55', '0.38', '0.46', '0.45', '0.47', '0.50',
            ]}
            st.dataframe(pd.DataFrame(rf_data), use_container_width=True, hide_index=True)

    with right3:
        tan_alpha = 1.0 / slope_wu
        L0    = calc_wavelength(T_wu)
        xi    = calc_iribarren(tan_alpha, H_wu, L0)
        gbeta = calc_obliquity(beta_wu)
        Ru2   = calc_runup_2pct(H_wu, xi, gf_wu, gb_wu, gbeta)
        Ru1   = calc_runup_1pct(H_wu, xi, gf_wu, gb_wu, gbeta)
        Cr    = calc_reflection(xi)
        q_wu  = calc_overtopping(H_wu, L0, xi, Rc_wu, gf_wu, gbeta)
        btype = breaker_type(xi)
        q_ls  = q_wu * 1000

        section("RESULTS")
        m1, m2, m3 = st.columns(3)
        m1.metric("L₀  (m)",       f"{L0:.2f}")
        m2.metric("Iribarren  ξ₀", f"{xi:.3f}")
        m3.metric("Breaker type",  btype)
        m4, m5, m6 = st.columns(3)
        m4.metric("R_u2%  (m)", f"{Ru2:.3f}")
        m5.metric("R_u1%  (m)", f"{Ru1:.3f}")
        m6.metric("C_r (reflection)", f"{Cr:.3f}")
        m7, m8, m9 = st.columns(3)
        m7.metric("γ_β  (obliquity)", f"{gbeta:.3f}")
        m8.metric("R_c / R_u2%", f"{Rc_wu/Ru2:.3f}" if Ru2 > 0 else "—")
        m9.metric("q  (L/s/m)", f"{q_ls:.4f}" if q_ls < 1 else f"{q_ls:.3f}")

        if q_ls < 0.01:
            st.success(f"Mean overtopping = {q_ls:.4f} L/s/m — Negligible. Design is adequate.", icon='✅')
        elif q_ls < 1.0:
            st.success(f"Mean overtopping = {q_ls:.4f} L/s/m — Acceptable for most structure types.", icon='✅')
        elif q_ls < 10.0:
            st.warning(f"Mean overtopping = {q_ls:.3f} L/s/m — Verify tolerable limits for this structure type.")
        else:
            st.error(f"Mean overtopping = {q_ls:.2f} L/s/m — Excessive. Increase freeboard or armour roughness.")

        # ── Professional equation blocks ────────────────────────────
        section("CALCULATION REPORT")

        eq_block(
            "1.  Deep-Water Wavelength",
            "L₀ = g · T_p² / (2π)",
            f"L₀ = 9.81 × {T_wu:.2f}² / (2π)",
            f"L₀ = {L0:.3f} m"
        )

        eq_block(
            "2.  Iribarren Number (Surf-Similarity Parameter)",
            "ξ₀ = tan(α) / √(H_m0 / L₀)",
            f"ξ₀ = {tan_alpha:.4f} / √({H_wu:.3f} / {L0:.3f})",
            f"ξ₀ = {xi:.4f}   →   breaker class: {btype}"
        )

        eq_block(
            "3.  Obliquity Reduction Factor  (EurOtop 2018)",
            "γ_β = max(1 − 0.0033 · |β|,  0.736)   for β ≤ 80°",
            f"γ_β = max(1 − 0.0033 × {beta_wu:.1f},  0.736)",
            f"γ_β = {gbeta:.4f}",
            "EurOtop 2018, §5.1.3"
        )

        Ru_uncut = 1.65 * gb_wu * gf_wu * gbeta * xi * H_wu
        cap_val  = (4.0 - 1.5 / max(math.sqrt(gf_wu * gbeta * xi), 1e-12)) * gb_wu * H_wu
        eq_block(
            "4.  Wave Run-Up R_u2%  (EurOtop 2018, Eq. 5.2)",
            "R_u2% = min(1.65 · γ_b · γ_f · γ_β · ξ₀ · H_m0,   (4.0 − 1.5 / √(γ_f · γ_β · ξ₀)) · γ_b · H_m0)",
            f"Formula value = 1.65 × {gb_wu:.3f} × {gf_wu:.3f} × {gbeta:.4f} × {xi:.4f} × {H_wu:.3f} = {Ru_uncut:.4f} m\n"
            f"Cap value     = (4.0 − 1.5/√({gf_wu:.3f}×{gbeta:.4f}×{xi:.4f})) × {gb_wu:.3f} × {H_wu:.3f} = {cap_val:.4f} m",
            f"R_u2% = {Ru2:.4f} m   ·   R_u1% = 1.4 × R_u2% = {Ru1:.4f} m",
            "EurOtop 2018, Eq. 5.2"
        )

        eq_block(
            "5.  Reflection Coefficient  (Postma 1989)",
            "C_r = 0.1 · ξ₀²   (capped at 1.0)",
            f"C_r = 0.1 × {xi:.4f}² = {0.1*xi**2:.4f}",
            f"C_r = {Cr:.4f}",
            "Postma (1989)"
        )

        eq_block(
            "6.  Mean Overtopping Discharge  (EurOtop 2018, Eq. 5.6)",
            "q = √(g · H_m0³) / √(L₀/H_m0) · 0.2 · exp(−2.3 · R_c / (γ_f · γ_β · H_m0 · ξ₀))",
            f"q = √(9.81 × {H_wu:.3f}³) / √({L0:.3f}/{H_wu:.3f}) × 0.2 × exp(−2.3 × {Rc_wu:.3f}/({gf_wu:.3f}×{gbeta:.4f}×{H_wu:.3f}×{xi:.4f}))",
            f"q = {q_wu:.6f} m³/s/m   =   {q_ls:.5f} L/s/m",
            "EurOtop 2018, Eq. 5.6"
        )

        # ── Export ─────────────────────────────────────────────────
        section("EXPORT")
        wu_payload = {
            'inputs': {'H': H_wu, 'T': T_wu, 'slope': slope_wu, 'Rc': Rc_wu,
                       'gf': gf_wu, 'gb': gb_wu, 'beta': beta_wu},
            'results': {'L0': L0, 'xi': xi, 'btype': btype, 'gbeta': gbeta,
                        'Ru2': Ru2, 'Ru1': Ru1, 'Cr': Cr, 'q': q_wu}
        }
        e1, e2 = st.columns(2)
        with e1:
            docx_wu = export_waverunup_docx(wu_payload)
            if docx_wu:
                st.download_button('Report (.docx)', data=docx_wu,
                                   file_name='hyrcan_wave_runup_report.docx',
                                   mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                                   use_container_width=True)
        with e2:
            xlsx_wu = export_waverunup_xlsx(wu_payload)
            if xlsx_wu:
                st.download_button('Workbook (.xlsx)', data=xlsx_wu,
                                   file_name='hyrcan_wave_runup_data.xlsx',
                                   mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                                   use_container_width=True)


# ════════════════════════════════════════════════════════════════════
#  FOOTER
# ════════════════════════════════════════════════════════════════════

st.markdown("""
<div style="border-top:1px solid #21262d;margin-top:32px;padding-top:14px;
            text-align:center;font-size:11px;color:#484f58;line-height:2;">
  HYRCAN Engineering Suite v4.0  &nbsp;·&nbsp;
  Mathias Adjei Tawiah  &nbsp;·&nbsp;
  mathiasadjeitawiah@gmail.com  &nbsp;·&nbsp;
  Hohai University — College of Harbor, Coastal and Offshore Engineering<br>
  EurOtop 2018  ·  JTS 154-1-2011  ·  GB 50286-2013  ·  HYRCAN 3.0 verified
</div>
""", unsafe_allow_html=True)
