# -*- coding: utf-8 -*-
"""
HYRCAN Engineering Suite v4.0
Developer: Mathias Adjei Tawiah
Institution: Hohai University — College of Harbor, Coastal & Offshore Engineering
Standards: EurOtop 2018 | JTS 154-1-2011 | GB 50286-2013

Enhancements in v4.0:
  - Word (.docx) export for all three modules
  - Excel (.xlsx) export for all three modules
  - Project History & Session Manager (save, reload, compare sessions)
  - Removed all informal language; fully professional tone
  - Refined UI: status badges, audit trail, timestamped records
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
import os
import datetime
import pandas as pd

# ── Word export ──────────────────────────────────────────────────────
from docx import Document
from docx.shared import Pt, RGBColor, Cm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ── Excel export ─────────────────────────────────────────────────────
import openpyxl
from openpyxl.styles import (Font, PatternFill, Alignment, Border, Side,
                              numbers as xl_numbers)
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, Reference

# ════════════════════════════════════════════════════════════════════
#  PAGE CONFIG  (must be first Streamlit call)
# ════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="HYRCAN Engineering Suite v4.0",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ════════════════════════════════════════════════════════════════════
#  GLOBAL STYLE
# ════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
html, body, [class*="css"] { font-family: 'Segoe UI', 'Inter', sans-serif; }
.stApp { background-color: #0d1117; color: #e6edf3; }

.stTabs [data-baseweb="tab-list"] {
    background-color: #161b22; border-radius: 8px; padding: 4px; gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background-color: transparent; color: #8b949e;
    border-radius: 6px; font-weight: 600; font-size: 14px; padding: 8px 20px;
}
.stTabs [aria-selected="true"] {
    background-color: #21262d !important; color: #58a6ff !important;
}
.stNumberInput input, .stTextInput input {
    background-color: #21262d; border: 1px solid #30363d;
    color: #e6edf3; border-radius: 6px; min-width: 90px;
}
.stSelectbox select { background-color: #21262d; color: #e6edf3; }
.stButton > button {
    background-color: #238636; color: white; border: none;
    border-radius: 6px; font-weight: 600; padding: 8px 20px; transition: background 0.2s;
}
.stButton > button:hover { background-color: #2ea043; }
[data-testid="metric-container"] {
    background-color: #21262d; border: 1px solid #30363d;
    border-radius: 8px; padding: 12px;
}
.stDataFrame { border-radius: 8px; overflow: hidden; }
.stAlert { border-radius: 8px; }
.section-header {
    background: linear-gradient(90deg, #1f6feb22, transparent);
    border-left: 3px solid #58a6ff;
    padding: 8px 14px; border-radius: 0 6px 6px 0;
    margin: 16px 0 8px 0; font-weight: 700; font-size: 13px;
    color: #58a6ff; letter-spacing: 0.5px; text-transform: uppercase;
}
.coord-block {
    background-color: #161b22; border: 1px solid #30363d;
    border-radius: 8px; padding: 16px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 12px; color: #e6edf3;
    white-space: pre; overflow-x: auto;
}
.welcome-card {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    border: 1px solid #30363d; border-radius: 14px;
    padding: 24px 28px; margin-bottom: 8px;
}
.info-card {
    background: #161b22; border: 1px solid #30363d;
    border-radius: 10px; padding: 14px 18px; margin: 8px 0;
}
.badge {
    display: inline-block; background: #1f6feb33;
    border: 1px solid #1f6feb88; color: #58a6ff;
    border-radius: 20px; padding: 3px 10px;
    font-size: 11px; font-weight: 600; margin: 2px;
}
.history-card {
    background: #161b22; border: 1px solid #30363d;
    border-radius: 8px; padding: 12px 16px; margin: 6px 0;
    cursor: pointer; transition: border-color 0.2s;
}
.history-card:hover { border-color: #58a6ff; }
.pass-badge {
    display: inline-block; background: #23863633; border: 1px solid #2ea04388;
    color: #3fb950; border-radius: 4px; padding: 2px 8px; font-size: 11px; font-weight: 700;
}
.fail-badge {
    display: inline-block; background: #da363333; border: 1px solid #f8514988;
    color: #f85149; border-radius: 4px; padding: 2px 8px; font-size: 11px; font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
#  PROJECT HISTORY STORAGE
# ════════════════════════════════════════════════════════════════════

HISTORY_FILE = "/tmp/hyrcan_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def add_to_history(module: str, label: str, params: dict, results: dict):
    history = load_history()
    entry = {
        "id": datetime.datetime.now().strftime("%Y%m%d_%H%M%S"),
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "module": module,
        "label": label,
        "params": params,
        "results": results,
    }
    history.insert(0, entry)
    history = history[:50]   # keep last 50 records
    save_history(history)
    return entry["id"]

# ════════════════════════════════════════════════════════════════════
#  CORE CALCULATION FUNCTIONS
# ════════════════════════════════════════════════════════════════════

def compute_layer_elevations(seabed_elev, thicknesses):
    tops, bots = [], []
    cur = seabed_elev
    for t in thicknesses:
        tops.append(cur); bots.append(cur - t); cur -= t
    datum = abs(bots[-1])
    def Y(e): return e + datum
    result = {'datum': datum, 'Y_seabed': Y(seabed_elev)}
    for i, (top, bot) in enumerate(zip(tops, bots)):
        result[f'top{i+1}'] = top; result[f'bot{i+1}'] = bot
        result[f'Y_top{i+1}'] = Y(top); result[f'Y_bot{i+1}'] = Y(bot)
    return result


def compute_geometry(crest_elev, seabed_elev, crest_width,
                     upper_height, lower_height,
                     sw_upper, sw_lower, seaward_berm,
                     lw_upper, lw_lower, landward_berm, layers):
    datum = layers['datum']
    def Y(e): return e + datum
    crest_y  = Y(crest_elev); seabed_y = Y(seabed_elev)
    single_slope_sw = (seaward_berm == 0); single_slope_lw = (landward_berm == 0)

    if single_slope_sw:
        total_sw_dx = (upper_height + lower_height) * sw_upper
        x_sw_toe = 0.0; x_sw_be = x_sw_toe; x_sw_bs = x_sw_toe
        x_cl = x_sw_toe + total_sw_dx
    else:
        sw_udx = upper_height * sw_upper; sw_ldx = lower_height * sw_lower
        x_sw_toe = 0.0; x_sw_be = x_sw_toe + sw_ldx
        x_sw_bs  = x_sw_be + seaward_berm; x_cl = x_sw_bs + sw_udx
    x_cr = x_cl + crest_width

    if single_slope_lw:
        total_lw_dx = (upper_height + lower_height) * lw_upper
        x_lw_bs = x_cr; x_lw_be = x_cr; x_lw_toe = x_cr + total_lw_dx
    else:
        lw_udx = upper_height * lw_upper; lw_ldx = lower_height * lw_lower
        x_lw_bs = x_cr + lw_udx; x_lw_be = x_lw_bs + landward_berm
        x_lw_toe = x_lw_be + lw_ldx

    berm_y = Y(crest_elev - upper_height)

    if single_slope_sw:
        pts = {'sw_toe': (x_sw_toe, seabed_y), 'sw_be': (x_sw_toe, seabed_y),
               'sw_bs':  (x_sw_toe, seabed_y), 'cl':    (x_cl, crest_y),
               'cr':     (x_cr,     crest_y),
               'lw_bs':  (x_lw_bs,  berm_y if not single_slope_lw else seabed_y),
               'lw_be':  (x_lw_be,  berm_y if not single_slope_lw else seabed_y),
               'lw_toe': (x_lw_toe, seabed_y)}
    else:
        pts = {'sw_toe': (x_sw_toe, seabed_y), 'sw_be': (x_sw_be, berm_y),
               'sw_bs':  (x_sw_bs,  berm_y),   'cl':    (x_cl, crest_y),
               'cr':     (x_cr,     crest_y),
               'lw_bs':  (x_lw_bs,  berm_y if not single_slope_lw else seabed_y),
               'lw_be':  (x_lw_be,  berm_y if not single_slope_lw else seabed_y),
               'lw_toe': (x_lw_toe, seabed_y)}

    sw_udx = upper_height * sw_upper; sw_ldx = lower_height * sw_lower
    lw_udx = upper_height * lw_upper; lw_ldx = lower_height * lw_lower

    return {
        'pts': pts, 'crest_y': crest_y, 'seabed_y': seabed_y, 'berm_y': berm_y,
        'model_right': x_lw_toe, 'model_bottom': 0.0,
        'sw_udx': sw_udx, 'sw_ldx': sw_ldx, 'lw_udx': lw_udx, 'lw_ldx': lw_ldx,
        'x_sw_be': x_sw_be if not single_slope_sw else x_sw_toe,
        'x_sw_bs': x_sw_bs if not single_slope_sw else x_sw_toe,
        'x_cl': x_cl, 'x_cr': x_cr,
        'x_lw_bs': x_lw_bs, 'x_lw_be': x_lw_be, 'x_lw_toe': x_lw_toe,
        'single_slope_sw': single_slope_sw, 'single_slope_lw': single_slope_lw,
    }


def verify_geometry(g, crest_elev, seabed_elev, crest_width,
                    upper_height, lower_height,
                    sw_upper, sw_lower, seaward_berm,
                    lw_upper, lw_lower, landward_berm):
    pts = g['pts']; tol = 0.001; checks = []
    def ck(name, exp, got): checks.append((name, exp, got, abs(exp - got) <= tol))
    ck('Crest width', crest_width, pts['cr'][0] - pts['cl'][0])
    ck('Total height', crest_elev - seabed_elev, upper_height + lower_height)
    if not g['single_slope_sw']:
        ck('Seaward lower ΔX', lower_height * sw_lower, g['sw_ldx'])
        ck('Seaward berm width', seaward_berm, g['x_sw_bs'] - g['x_sw_be'])
        ck('Seaward upper ΔX', upper_height * sw_upper, g['sw_udx'])
    else:
        total_sw = (upper_height + lower_height) * sw_upper
        ck('Seaward single-slope ΔX', total_sw, g['x_cl'] - pts['sw_toe'][0])
    if not g['single_slope_lw']:
        ck('Landward upper ΔX', upper_height * lw_upper, g['lw_udx'])
        ck('Landward berm width', landward_berm, g['x_lw_be'] - g['x_lw_bs'])
        ck('Landward lower ΔX', lower_height * lw_lower, g['lw_ldx'])
    else:
        total_lw = (upper_height + lower_height) * lw_upper
        ck('Landward single-slope ΔX', total_lw, g['x_lw_toe'] - g['x_cr'])
    return checks


def caisson_fos(B, H_c, gamma_c, d, H1pct, gamma_w, mu, q_allow):
    W       = B * H_c * gamma_c
    P       = 0.5 * gamma_w * H1pct**2 + gamma_w * d * H1pct
    F_res   = mu * W; M_res = W * (B / 2)
    arm     = d / 2 + H1pct / 3; M_ot = P * arm
    FOS_s   = F_res / P if P > 0 else float('inf')
    FOS_o   = M_res / M_ot if M_ot > 0 else float('inf')
    q_max   = W / B
    return dict(W=W, P=P, F_res=F_res, M_res=M_res, arm=arm,
                M_ot=M_ot, FOS_s=FOS_s, FOS_o=FOS_o, q_max=q_max)


# ════════════════════════════════════════════════════════════════════
#  WAVE RUN-UP — EurOtop 2018
# ════════════════════════════════════════════════════════════════════

def calc_wavelength(T): return 9.81 * T**2 / (2 * math.pi)

def calc_iribarren(tan_alpha, H, L0):
    if H <= 0 or L0 <= 0: return 0.0
    return tan_alpha / math.sqrt(H / L0)

def calc_runup_2percent(H, xi, gamma_f, gamma_b, gamma_beta):
    ru     = 1.65 * gamma_b * gamma_f * gamma_beta * xi * H
    ru_max = (4.0 - 1.5 / math.sqrt(gamma_f * gamma_beta * xi + 1e-12)) * gamma_b * H
    return min(ru, ru_max)

def calc_runup_1percent(H, xi, gamma_f, gamma_b, gamma_beta):
    return 1.4 * calc_runup_2percent(H, xi, gamma_f, gamma_b, gamma_beta)

def calc_reflection(xi): return min(0.1 * xi**2, 1.0) if xi > 0 else 0.0

def calc_overtopping(H, L0, xi, Rc, gamma_f, gamma_beta):
    if H <= 0 or L0 <= 0 or xi <= 0: return 0.0
    term = (Rc / (gamma_f * gamma_beta * H)) * (1.0 / xi)
    return max(math.sqrt(9.81 * H**3) / math.sqrt(L0 / H) * 0.2 * math.exp(-2.3 * term), 0.0)

def calc_obliquity_factor(beta_deg):
    b = abs(beta_deg)
    return max(1.0 - 0.0033 * b, 0.736) if b <= 80 else 0.736

def classify_breaker(xi):
    if xi < 0.5: return "Spilling"
    elif xi < 2.0: return "Plunging"
    elif xi < 3.0: return "Collapsing"
    else: return "Surging"

# ════════════════════════════════════════════════════════════════════
#  BOUNDARY BUILDER
# ════════════════════════════════════════════════════════════════════

def build_clean_boundary(g, pts, L, R, B_mdl, sy, cy, by, seaward_berm, landward_berm):
    raw = [(L,sy),(L,B_mdl),(R,B_mdl),(R,sy)]
    if not g['single_slope_lw']:
        if g['lw_ldx'] > 0.001: raw.append((pts['lw_be'][0], by))
        if landward_berm > 0.001: raw.append((pts['lw_bs'][0], by))
    raw.append((pts['cr'][0], cy)); raw.append((pts['cl'][0], cy))
    if not g['single_slope_sw']:
        if g['sw_udx'] > 0.001: raw.append((pts['sw_bs'][0], by))
        if seaward_berm > 0.001: raw.append((pts['sw_be'][0], by))
    raw.append((pts['sw_toe'][0], sy))
    clean = []
    for pt in raw:
        if not clean or abs(pt[0]-clean[-1][0])>0.001 or abs(pt[1]-clean[-1][1])>0.001:
            clean.append(pt)
    return clean

# ════════════════════════════════════════════════════════════════════
#  TEXT GENERATION
# ════════════════════════════════════════════════════════════════════

def generate_hyrcan_instructions(
        g, layers, dhw, surcharge, num_slices, crest_elev, seabed_elev,
        upper_height, lower_height,
        sw_upper, sw_lower, seaward_berm,
        lw_upper, lw_lower, landward_berm, crest_width,
        layer_names, layer_props, n_layers, mat_rubble):
    pts = g['pts']; cy=g['crest_y']; sy=g['seabed_y']; by=g['berm_y']
    L=0.0; R=g['model_right']; B_mdl=0.0; datum=layers['datum']
    dy = dhw + datum

    def row(name,g_,c,phi):
        return f"│ {name:<16} │ {g_:<14.1f} │ {c:<14.1f} │ {phi:<12.1f} │"
    mat_rows = [row("Rubble",mat_rubble[0],mat_rubble[1],mat_rubble[2])]
    for i in range(n_layers):
        mat_rows.append(row(layer_names[i],layer_props[i][0],layer_props[i][1],layer_props[i][2]))
    mat_table = "\n".join([
        "┌──────────────────┬────────────────┬────────────────┬──────────────┐",
        "│ Material         │ γ (kN/m³)      │ c (kPa)        │ φ (°)        │",
        "├──────────────────┼────────────────┼────────────────┼──────────────┤",
        *mat_rows,
        "└──────────────────┴────────────────┴────────────────┴──────────────┘",
    ])

    bound_lines = ""
    for i in range(n_layers - 1):
        key=f'Y_bot{i+1}'; n_top=layer_names[i]; n_bot=layer_names[i+1]
        bound_lines += f"""
  ── Boundary {i+1}: Bottom of {n_top} / Top of {n_bot} ─────────────
  {L:.3f},{layers[key]:.3f}
  {R:.3f},{layers[key]:.3f}
  d
"""
    assign_rows = ["  │ Rubble               │ Embankment body (above seabed)           │"]
    for i in range(n_layers):
        assign_rows.append(
            f"  │ {layer_names[i]:<20} │ Y = {layers[f'Y_bot{i+1}']:.2f} → "
            f"{layers[f'Y_top{i+1}']:.2f}  (real: {layers[f'bot{i+1}']:.2f} → {layers[f'top{i+1}']:.2f} m) │")
    assign_table = "\n".join(assign_rows)
    slope_note = "Single-slope" if g['single_slope_sw'] else "Double-slope with berm"
    clean_pts = build_clean_boundary(g, pts, L, R, B_mdl, sy, cy, by, seaward_berm, landward_berm)
    boundary_lines = "\n".join([f"  {x:.3f},{y:.3f}" for x,y in clean_pts]) + "\n  c"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M UTC")

    return f"""\
{'='*72}
  HYRCAN ENGINEERING SUITE v4.0 — COMPLETE SETUP INSTRUCTIONS
  Mathias Adjei Tawiah  |  Hohai University — Coastal Engineering
  Generated: {timestamp}
  Slope geometry: {slope_note}  |  Soil layers: {n_layers}
{'='*72}

STEP 1: NEW PROJECT
  ▸ File → New Project
  ▸ Name : Embankment_Stability
  ▸ Units: SI  (kN, m, degrees)
  ▸ Click OK

──────────────────────────────────────────────────────────────────────
STEP 2: PROJECT SETTINGS
  ▸ Analysis → Project Settings

  [ General ]
    Failure Direction : Left to Right
    Surface Type      : Circular
    Search Method     : Slope Search

  [ Methods ]
    ☑ Bishop Simplified
    ☑ Spencer
    ☑ GLE / Morgenstern-Price
    Number of slices  : {int(num_slices)}
  ▸ Apply → OK

──────────────────────────────────────────────────────────────────────
STEP 3: EXTERNAL BOUNDARY
  ▸ Geometry → External Boundary

{boundary_lines}

  Note: No spaces after commas. Press Enter after every line.

──────────────────────────────────────────────────────────────────────
STEP 4: MATERIAL BOUNDARIES  ({n_layers - 1} boundaries for {n_layers} layers)
  ▸ Geometry → Material Boundary

  ── Boundary 0: Seabed / Top of {layer_names[0]} ────────────────────
  {L:.3f},{layers['Y_seabed']:.3f}
  {R:.3f},{layers['Y_seabed']:.3f}
  d
{bound_lines}
  Verify {n_layers + 1} coloured regions are visible.

──────────────────────────────────────────────────────────────────────
STEP 5: WATER TABLE
  ▸ Geometry → Add Water Table

  {L:.3f},{dy:.3f}
  {R:.3f},{dy:.3f}
  d

  Water table Y = {dy:.3f}  (design high water = {dhw:.2f} m)

──────────────────────────────────────────────────────────────────────
STEP 6: SURCHARGE LOAD
  ▸ Loading → Distributed Load
  ▸ Load Type  : Vertical (Downward)
  ▸ Magnitude  : {surcharge:.1f} kN/m²
  ▸ Crest coordinates:

  {pts['cl'][0]:.3f},{cy:.3f}
  {pts['cr'][0]:.3f},{cy:.3f}
  d

  Load acts on crest  X = {pts['cl'][0]:.3f} → {pts['cr'][0]:.3f}

──────────────────────────────────────────────────────────────────────
STEP 7: ASSIGN MATERIALS
  ▸ Properties → Define Materials

{mat_table}

  ▸ Properties → Assign Properties

  ┌──────────────────────┬──────────────────────────────────────────┐
  │ Material             │ Region                                   │
  ├──────────────────────┼──────────────────────────────────────────┤
{assign_table}
  └──────────────────────┴──────────────────────────────────────────┘

──────────────────────────────────────────────────────────────────────
STEP 8: COMPUTE
  ▸ Analysis → Compute

──────────────────────────────────────────────────────────────────────
STEP 9: RESULTS
  ▸ Result tab → Record Bishop and Spencer FOS values
  ▸ Minimum recommended FOS: 1.3 (static load case)

{'='*72}
  DATUM SHIFT REFERENCE
  Bottom of {layer_names[-1]} = {layers[f'bot{n_layers}']:.2f} m (real) → Y = 0.000 (HYRCAN)
  Datum shift applied: +{datum:.3f} m to all elevations

  MODEL DIMENSIONS
  Total width  : {R:.3f} m
  Total height : {g['crest_y']:.3f} m  (HYRCAN Y)
  Seaward toe  : X = {pts['sw_toe'][0]:.3f}
  Landward toe : X = {pts['lw_toe'][0]:.3f}
  Crest        : X = {pts['cl'][0]:.3f} → {pts['cr'][0]:.3f}  (width = {pts['cr'][0]-pts['cl'][0]:.3f} m)
{'='*72}
"""


def generate_coordinates_txt(g, layers, dhw, surcharge, crest_elev, seabed_elev,
                              n_layers, seaward_berm=0, landward_berm=0):
    pts=g['pts']; cy=g['crest_y']; sy=g['seabed_y']; by=g['berm_y']
    L=0.0; R=g['model_right']; B=0.0; datum=layers['datum']; dy=dhw+datum
    clean_pts = build_clean_boundary(g, pts, L, R, B, sy, cy, by, seaward_berm, landward_berm)
    clean_lines = [f"{x:.3f},{y:.3f}" for x,y in clean_pts]+["c"]
    lines = [
        "HYRCAN COORDINATE EXPORT — v4.0",
        f"Datum shift: +{datum:.3f} m",
        "", "EXTERNAL BOUNDARY", *clean_lines,
        f"", f"MATERIAL BOUNDARY 0 (Seabed):",
        f"{L:.3f},{layers['Y_seabed']:.3f}", f"{R:.3f},{layers['Y_seabed']:.3f}", "d",
    ]
    for i in range(n_layers-1):
        lines += ["", f"MATERIAL BOUNDARY {i+1} (Bottom Layer {i+1}):",
                  f"{L:.3f},{layers[f'Y_bot{i+1}']:.3f}",
                  f"{R:.3f},{layers[f'Y_bot{i+1}']:.3f}", "d"]
    lines += ["", "WATER TABLE:", f"{L:.3f},{dy:.3f}", f"{R:.3f},{dy:.3f}", "d",
              "", f"SURCHARGE ({surcharge:.1f} kN/m²):",
              f"{pts['cl'][0]:.3f},{cy:.3f}", f"{pts['cr'][0]:.3f},{cy:.3f}", "d"]
    return "\n".join(lines)

# ════════════════════════════════════════════════════════════════════
#  WORD EXPORT HELPERS
# ════════════════════════════════════════════════════════════════════

def _style_heading(run, size=14, bold=True, color=(0, 82, 165)):
    run.font.size = Pt(size); run.font.bold = bold
    run.font.color.rgb = RGBColor(*color)

def _add_table_row(table, cells, bold=False, header=False):
    row = table.add_row()
    for i, val in enumerate(cells):
        cell = row.cells[i]; cell.text = str(val)
        para = cell.paragraphs[0]
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = para.runs[0] if para.runs else para.add_run(str(val))
        run.font.size = Pt(9); run.font.bold = bold or header
        if header:
            shading = OxmlElement('w:shd')
            shading.set(qn('w:fill'), '003366')
            shading.set(qn('w:color'), 'FFFFFF')
            cell._tc.get_or_add_tcPr().append(shading)
            run.font.color.rgb = RGBColor(255, 255, 255)
    return row

def _set_col_widths(table, widths_cm):
    for row in table.rows:
        for i, cell in enumerate(row.cells):
            if i < len(widths_cm):
                cell.width = Cm(widths_cm[i])

def build_word_rubble(g, layers, dhw, surcharge, checks, crest_elev, seabed_elev,
                      layer_names, layer_props, n_layers, mat_rubble, fig_bytes=None):
    doc = Document()
    # Margins
    for sec in doc.sections:
        sec.left_margin = Cm(2); sec.right_margin = Cm(2)
        sec.top_margin = Cm(2.5); sec.bottom_margin = Cm(2.5)

    # Title block
    p = doc.add_paragraph()
    run = p.add_run("HYRCAN Engineering Suite v4.0")
    run.font.size = Pt(18); run.font.bold = True
    run.font.color.rgb = RGBColor(0, 82, 165)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p2 = doc.add_paragraph()
    p2.add_run("Module 1: Rubble Mound Coordinate Generator — Technical Report").font.size = Pt(11)
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
                      f"  |  Developer: Mathias Adjei Tawiah  |  Hohai University").alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph("Standards: EurOtop 2018 | JTS 154-1-2011 | GB 50286-2013").alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph()

    # Section 1 — Geometry
    doc.add_heading("1. Embankment Geometry Parameters", level=1)
    tbl = doc.add_table(rows=1, cols=2); tbl.style = 'Table Grid'
    _add_table_row(tbl, ["Parameter", "Value"], header=True)
    for param, val in [
        ("Crest Elevation", f"{crest_elev:.3f} m"),
        ("Seabed Elevation", f"{seabed_elev:.3f} m"),
        ("Total Height", f"{crest_elev-seabed_elev:.3f} m"),
        ("Design High Water Level", f"{dhw:.3f} m"),
        ("Surcharge Load", f"{surcharge:.1f} kN/m²"),
        ("Datum Shift", f"+{layers['datum']:.3f} m"),
    ]:
        _add_table_row(tbl, [param, val])

    doc.add_paragraph()
    doc.add_heading("2. Soil Layer Properties", level=1)
    tbl2 = doc.add_table(rows=1, cols=5); tbl2.style = 'Table Grid'
    _add_table_row(tbl2, ["Layer", "γ (kN/m³)", "c (kPa)", "φ (°)", "Thickness (m)"], header=True)
    _add_table_row(tbl2, ["Rubble (Embankment)", mat_rubble[0], mat_rubble[1], mat_rubble[2], "—"])
    for i in range(n_layers):
        t = layers[f'top{i+1}'] - layers[f'bot{i+1}']
        _add_table_row(tbl2, [layer_names[i], layer_props[i][0], layer_props[i][1], layer_props[i][2], f"{t:.2f}"])

    doc.add_paragraph()
    doc.add_heading("3. Layer Elevation Schedule (HYRCAN Coordinate System)", level=1)
    tbl3 = doc.add_table(rows=1, cols=5); tbl3.style = 'Table Grid'
    _add_table_row(tbl3, ["Layer", "Top Elev (m)", "Bot Elev (m)", "HYRCAN Y_top", "HYRCAN Y_bot"], header=True)
    for i in range(n_layers):
        _add_table_row(tbl3, [
            layer_names[i],
            f"{layers[f'top{i+1}']:.3f}", f"{layers[f'bot{i+1}']:.3f}",
            f"{layers[f'Y_top{i+1}']:.3f}", f"{layers[f'Y_bot{i+1}']:.3f}",
        ])

    doc.add_paragraph()
    doc.add_heading("4. Geometry Verification Checks", level=1)
    tbl4 = doc.add_table(rows=1, cols=4); tbl4.style = 'Table Grid'
    _add_table_row(tbl4, ["Parameter", "Expected", "Calculated", "Status"], header=True)
    for name, exp, got, ok in checks:
        _add_table_row(tbl4, [name, f"{exp:.4f}", f"{got:.4f}", "PASS" if ok else "FAIL"],
                       bold=not ok)

    # Cross-section figure
    if fig_bytes:
        doc.add_paragraph()
        doc.add_heading("5. Cross-Section Diagram", level=1)
        doc.add_picture(io.BytesIO(fig_bytes), width=Cm(16))

    # Footer note
    doc.add_paragraph()
    p_foot = doc.add_paragraph(
        "This report was generated automatically by HYRCAN Engineering Suite v4.0. "
        "All coordinates are referenced to the internal datum (HYRCAN Y-system). "
        "Verify input parameters against project drawings before use in analysis software.")
    p_foot.runs[0].font.size = Pt(8); p_foot.runs[0].font.italic = True

    buf = io.BytesIO(); doc.save(buf); buf.seek(0)
    return buf


def build_word_caisson(B, H_c, gamma_c, d, H1pct, gamma_w, mu, q_allow, r, fig_bytes=None):
    doc = Document()
    for sec in doc.sections:
        sec.left_margin = Cm(2); sec.right_margin = Cm(2)
        sec.top_margin = Cm(2.5); sec.bottom_margin = Cm(2.5)

    p = doc.add_paragraph()
    p.add_run("HYRCAN Engineering Suite v4.0").font.size = Pt(18)
    p.runs[0].font.bold = True; p.runs[0].font.color.rgb = RGBColor(0,82,165)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p2 = doc.add_paragraph(); p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p2.add_run("Module 2: Vertical Caisson Stability Analysis — Technical Report").font.size = Pt(11)
    doc.add_paragraph(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
                      f"  |  Mathias Adjei Tawiah  |  Hohai University").alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph()

    doc.add_heading("1. Input Parameters", level=1)
    tbl = doc.add_table(rows=1, cols=2); tbl.style = 'Table Grid'
    _add_table_row(tbl, ["Parameter", "Value"], header=True)
    for param, val in [
        ("Caisson Width B", f"{B:.2f} m"), ("Caisson Height H_c", f"{H_c:.2f} m"),
        ("Concrete Unit Weight γ_c", f"{gamma_c:.2f} kN/m³"),
        ("Water Depth d", f"{d:.3f} m"), ("Design Wave H₁%", f"{H1pct:.3f} m"),
        ("Water Unit Weight γ_w", f"{gamma_w:.2f} kN/m³"),
        ("Friction Coefficient μ", f"{mu:.3f}"),
        ("Allowable Bearing q_allow", f"{q_allow:.0f} kPa"),
    ]:
        _add_table_row(tbl, [param, val])

    doc.add_paragraph()
    doc.add_heading("2. Stability Analysis Results", level=1)
    s_ok = r['FOS_s'] >= 1.25; o_ok = r['FOS_o'] >= 1.50; b_ok = r['q_max'] < q_allow
    tbl2 = doc.add_table(rows=1, cols=5); tbl2.style = 'Table Grid'
    _add_table_row(tbl2, ["Check", "Calculated", "Required", "Standard", "Status"], header=True)
    _add_table_row(tbl2, ["Self-Weight W", f"{r['W']:,.1f} kN/m", "—", "—", "—"])
    _add_table_row(tbl2, ["Wave Force P", f"{r['P']:,.2f} kN/m", "—", "JTS 154-1-2011 App. A", "—"])
    _add_table_row(tbl2, ["Sliding FOS", f"{r['FOS_s']:.3f}", "≥ 1.25",
                          "GB 50286-2013 §5.3.2", "PASS" if s_ok else "FAIL"])
    _add_table_row(tbl2, ["Overturning FOS", f"{r['FOS_o']:.3f}", "≥ 1.50",
                          "GB 50286-2013 §5.3.3", "PASS" if o_ok else "FAIL"])
    _add_table_row(tbl2, ["Bearing q_max", f"{r['q_max']:,.0f} kPa", f"< {q_allow:.0f} kPa",
                          "JTS 154-1-2011 §5.3.4", "PASS" if b_ok else "FAIL"])

    doc.add_paragraph()
    overall = "DESIGN ADEQUATE — All stability criteria satisfied." if (s_ok and o_ok and b_ok) \
              else "DESIGN DEFICIENT — One or more stability criteria not met. Review parameters."
    p_ov = doc.add_paragraph(overall)
    p_ov.runs[0].font.bold = True
    p_ov.runs[0].font.color.rgb = RGBColor(0,128,0) if (s_ok and o_ok and b_ok) else RGBColor(192,0,0)

    if fig_bytes:
        doc.add_paragraph()
        doc.add_heading("3. Cross-Section Diagram", level=1)
        doc.add_picture(io.BytesIO(fig_bytes), width=Cm(14))

    buf = io.BytesIO(); doc.save(buf); buf.seek(0)
    return buf


def build_word_runup(H, T, slope, Rc, gf, gb, beta, xi, L0, Ru2, Ru1, Cr, q_wu, gbeta, btype):
    doc = Document()
    for sec in doc.sections:
        sec.left_margin = Cm(2); sec.right_margin = Cm(2)
        sec.top_margin = Cm(2.5); sec.bottom_margin = Cm(2.5)

    p = doc.add_paragraph()
    p.add_run("HYRCAN Engineering Suite v4.0").font.size = Pt(18)
    p.runs[0].font.bold = True; p.runs[0].font.color.rgb = RGBColor(0,82,165)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p2 = doc.add_paragraph(); p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p2.add_run("Module 3: Wave Run-Up & Overtopping Calculator — Technical Report").font.size = Pt(11)
    doc.add_paragraph(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
                      f"  |  Mathias Adjei Tawiah  |  Hohai University").alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph()

    doc.add_heading("1. Input Parameters", level=1)
    tbl = doc.add_table(rows=1, cols=2); tbl.style = 'Table Grid'
    _add_table_row(tbl, ["Parameter", "Value"], header=True)
    for param, val in [
        ("Significant Wave Height H_m0", f"{H:.3f} m"),
        ("Peak Wave Period T_p", f"{T:.2f} s"),
        ("Slope Ratio (H:V)", f"1:{slope:.2f}"),
        ("Freeboard R_c", f"{Rc:.3f} m"),
        ("Roughness Factor γ_f", f"{gf:.3f}"),
        ("Berm Factor γ_b", f"{gb:.3f}"),
        ("Wave Obliquity β", f"{beta:.1f}°"),
    ]:
        _add_table_row(tbl, [param, val])

    doc.add_paragraph()
    doc.add_heading("2. Computed Results (EurOtop 2018)", level=1)
    tbl2 = doc.add_table(rows=1, cols=2); tbl2.style = 'Table Grid'
    _add_table_row(tbl2, ["Result", "Value"], header=True)
    q_ls = q_wu * 1000
    for res, val in [
        ("Deep Water Wavelength L₀", f"{L0:.3f} m"),
        ("Iribarren Number ξ", f"{xi:.4f}"),
        ("Breaker Classification", btype),
        ("Obliquity Factor γ_β", f"{gbeta:.4f}"),
        ("Wave Run-Up Ru2%", f"{Ru2:.4f} m"),
        ("Wave Run-Up Ru1%", f"{Ru1:.4f} m"),
        ("Reflection Coefficient Cr", f"{Cr:.4f}"),
        ("Mean Overtopping Discharge q", f"{q_ls:.4f} L/s/m  ({q_wu:.6f} m³/s/m)"),
        ("Rc / Ru2%", f"{Rc/Ru2:.3f}" if Ru2 > 0 else "—"),
    ]:
        _add_table_row(tbl2, [res, val])

    doc.add_paragraph()
    status = ("Negligible overtopping (< 0.01 L/s/m)" if q_ls < 0.01 else
              "Acceptable overtopping for most structures" if q_ls < 1.0 else
              "Elevated overtopping — verify tolerable limits" if q_ls < 10.0 else
              "Excessive overtopping — increase freeboard or roughness")
    p_s = doc.add_paragraph(f"Overtopping Assessment: {status}")
    p_s.runs[0].font.bold = True

    buf = io.BytesIO(); doc.save(buf); buf.seek(0)
    return buf

# ════════════════════════════════════════════════════════════════════
#  EXCEL EXPORT HELPERS
# ════════════════════════════════════════════════════════════════════

def _xl_header_style():
    return {
        'font': Font(name='Calibri', bold=True, color='FFFFFF', size=10),
        'fill': PatternFill('solid', fgColor='003366'),
        'align': Alignment(horizontal='center', vertical='center', wrap_text=True),
        'border': Border(
            left=Side(style='thin'), right=Side(style='thin'),
            top=Side(style='thin'), bottom=Side(style='thin'))
    }

def _xl_data_style(alt=False):
    return {
        'font': Font(name='Calibri', size=10),
        'fill': PatternFill('solid', fgColor='E8EFF7' if alt else 'FFFFFF'),
        'align': Alignment(horizontal='center', vertical='center'),
        'border': Border(
            left=Side(style='thin'), right=Side(style='thin'),
            top=Side(style='thin'), bottom=Side(style='thin'))
    }

def _apply_styles(cell, styles):
    if 'font' in styles: cell.font = styles['font']
    if 'fill' in styles: cell.fill = styles['fill']
    if 'align' in styles: cell.alignment = styles['align']
    if 'border' in styles: cell.border = styles['border']

def _write_xl_table(ws, headers, rows, start_row=1, start_col=1):
    hs = _xl_header_style()
    for j, h in enumerate(headers, start_col):
        c = ws.cell(row=start_row, column=j, value=h)
        _apply_styles(c, hs)
    for i, row in enumerate(rows, start_row+1):
        ds = _xl_data_style(alt=(i % 2 == 0))
        for j, val in enumerate(row, start_col):
            c = ws.cell(row=i, column=j, value=val)
            _apply_styles(c, ds)
    return start_row + len(rows) + 2


def build_excel_rubble(g, layers, dhw, surcharge, checks, crest_elev, seabed_elev,
                       layer_names, layer_props, n_layers, mat_rubble):
    wb = openpyxl.Workbook()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    # ── Sheet 1: Summary ────────────────────────────────────────────
    ws = wb.active; ws.title = "Summary"
    ws.column_dimensions['A'].width = 32; ws.column_dimensions['B'].width = 20

    title_font = Font(name='Calibri', bold=True, size=14, color='003366')
    ws['A1'] = "HYRCAN Engineering Suite v4.0 — Rubble Mound Module"
    ws['A1'].font = title_font; ws.merge_cells('A1:D1')
    ws['A2'] = f"Generated: {timestamp}  |  Mathias Adjei Tawiah  |  Hohai University"
    ws['A2'].font = Font(name='Calibri', italic=True, size=9)
    ws.merge_cells('A2:D2')

    _write_xl_table(ws, ["Parameter", "Value"], [
        ["Crest Elevation (m)", crest_elev],
        ["Seabed Elevation (m)", seabed_elev],
        ["Total Height (m)", round(crest_elev-seabed_elev, 3)],
        ["Design High Water (m)", dhw],
        ["Surcharge (kN/m²)", surcharge],
        ["Datum Shift (m)", round(layers['datum'], 3)],
    ], start_row=4)

    # ── Sheet 2: Layer Schedule ──────────────────────────────────────
    ws2 = wb.create_sheet("Layer Schedule")
    ws2.column_dimensions['A'].width = 20
    for col in ['B','C','D','E','F','G','H']: ws2.column_dimensions[col].width = 16
    ws2['A1'] = "HYRCAN Layer Elevation Schedule"
    ws2['A1'].font = Font(name='Calibri', bold=True, size=13, color='003366')
    ws2.merge_cells('A1:H1')

    rows_lyr = []
    for i in range(n_layers):
        rows_lyr.append([
            layer_names[i],
            round(layer_props[i][0], 2), round(layer_props[i][1], 2), round(layer_props[i][2], 2),
            round(layers[f'top{i+1}'], 3), round(layers[f'bot{i+1}'], 3),
            round(layers[f'Y_top{i+1}'], 3), round(layers[f'Y_bot{i+1}'], 3),
        ])
    _write_xl_table(ws2,
        ["Layer Name", "γ (kN/m³)", "c (kPa)", "φ (°)",
         "Top Elev (m)", "Bot Elev (m)", "HYRCAN Y_top", "HYRCAN Y_bot"],
        rows_lyr, start_row=3)

    # ── Sheet 3: Verification ────────────────────────────────────────
    ws3 = wb.create_sheet("Verification")
    ws3.column_dimensions['A'].width = 30
    for col in ['B','C','D']: ws3.column_dimensions[col].width = 18
    ws3['A1'] = "Geometry Verification Checks"
    ws3['A1'].font = Font(name='Calibri', bold=True, size=13, color='003366')
    ws3.merge_cells('A1:D1')

    check_rows = [[name, round(exp,4), round(got,4), "PASS" if ok else "FAIL"]
                  for name, exp, got, ok in checks]
    _write_xl_table(ws3, ["Parameter", "Expected", "Calculated", "Status"], check_rows, start_row=3)

    # Colour status cells
    pass_fill = PatternFill('solid', fgColor='C6EFCE')
    fail_fill = PatternFill('solid', fgColor='FFC7CE')
    for i, (_, _, _, ok) in enumerate(checks, 4):
        c = ws3.cell(row=i, column=4)
        c.fill = pass_fill if ok else fail_fill
        c.font = Font(name='Calibri', bold=True, color='006100' if ok else '9C0006', size=10)

    # ── Sheet 4: HYRCAN Coordinates ─────────────────────────────────
    ws4 = wb.create_sheet("Coordinates")
    ws4.column_dimensions['A'].width = 22; ws4.column_dimensions['B'].width = 22
    ws4['A1'] = "HYRCAN Coordinate Export"; ws4['A1'].font = Font(name='Calibri', bold=True, size=13, color='003366')
    ws4.merge_cells('A1:B1')

    pts = g['pts']; cy=g['crest_y']; sy=g['seabed_y']; by=g['berm_y']
    clean_pts = build_clean_boundary(g, pts, 0.0, g['model_right'], 0.0, sy, cy, by, 0, 0)
    _write_xl_table(ws4, ["X (m)", "Y (m)"], [[round(x,3), round(y,3)] for x,y in clean_pts], start_row=3)

    buf = io.BytesIO(); wb.save(buf); buf.seek(0)
    return buf


def build_excel_caisson(B, H_c, gamma_c, d, H1pct, gamma_w, mu, q_allow, r):
    wb = openpyxl.Workbook()
    ws = wb.active; ws.title = "Caisson Stability"
    ws.column_dimensions['A'].width = 30
    for col in ['B','C','D','E']: ws.column_dimensions[col].width = 22
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    ws['A1'] = "HYRCAN Engineering Suite v4.0 — Vertical Caisson Module"
    ws['A1'].font = Font(name='Calibri', bold=True, size=14, color='003366')
    ws.merge_cells('A1:E1')
    ws['A2'] = f"Generated: {timestamp}  |  Mathias Adjei Tawiah  |  Hohai University"
    ws['A2'].font = Font(name='Calibri', italic=True, size=9); ws.merge_cells('A2:E2')

    _write_xl_table(ws, ["Parameter", "Value"], [
        ["Caisson Width B (m)", B], ["Caisson Height H_c (m)", H_c],
        ["Concrete γ_c (kN/m³)", gamma_c], ["Water Depth d (m)", d],
        ["Design Wave H₁% (m)", H1pct], ["Water γ_w (kN/m³)", gamma_w],
        ["Friction Coefficient μ", mu], ["Allowable Bearing (kPa)", q_allow],
    ], start_row=4)

    s_ok = r['FOS_s'] >= 1.25; o_ok = r['FOS_o'] >= 1.50; b_ok = r['q_max'] < q_allow
    res_rows = [
        ["Self-Weight W (kN/m)", round(r['W'],2), "—", "—", "—"],
        ["Wave Force P (kN/m)", round(r['P'],3), "—", "JTS 154-1-2011 App. A", "—"],
        ["Sliding FOS", round(r['FOS_s'],4), "≥ 1.25", "GB 50286-2013 §5.3.2", "PASS" if s_ok else "FAIL"],
        ["Overturning FOS", round(r['FOS_o'],4), "≥ 1.50", "GB 50286-2013 §5.3.3", "PASS" if o_ok else "FAIL"],
        ["Bearing q_max (kPa)", round(r['q_max'],1), f"< {q_allow:.0f}", "JTS 154-1-2011 §5.3.4", "PASS" if b_ok else "FAIL"],
    ]
    end_row = _write_xl_table(ws, ["Check", "Calculated", "Required", "Standard", "Status"],
                               res_rows, start_row=14)

    pass_fill = PatternFill('solid', fgColor='C6EFCE'); fail_fill = PatternFill('solid', fgColor='FFC7CE')
    status_col = 18  # row 14 header → data starts at 15
    for i, (_, _, _, _, status) in enumerate(res_rows, 15):
        if status in ("PASS","FAIL"):
            c = ws.cell(row=i, column=5)
            c.fill = pass_fill if status=="PASS" else fail_fill
            c.font = Font(name='Calibri', bold=True, color='006100' if status=="PASS" else '9C0006', size=10)

    buf = io.BytesIO(); wb.save(buf); buf.seek(0)
    return buf


def build_excel_runup(H, T, slope, Rc, gf, gb, beta, xi, L0, Ru2, Ru1, Cr, q_wu, gbeta, btype):
    wb = openpyxl.Workbook()
    ws = wb.active; ws.title = "Wave Run-Up"
    ws.column_dimensions['A'].width = 36; ws.column_dimensions['B'].width = 28
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    ws['A1'] = "HYRCAN Engineering Suite v4.0 — Wave Run-Up Module"
    ws['A1'].font = Font(name='Calibri', bold=True, size=14, color='003366')
    ws.merge_cells('A1:B1')
    ws['A2'] = f"Generated: {timestamp}  |  Mathias Adjei Tawiah  |  Hohai University"
    ws['A2'].font = Font(name='Calibri', italic=True, size=9); ws.merge_cells('A2:B2')

    _write_xl_table(ws, ["Input Parameter", "Value"], [
        ["Significant Wave Height H_m0 (m)", H],
        ["Peak Wave Period T_p (s)", T],
        ["Slope Ratio H:V", f"1:{slope:.2f}"],
        ["Freeboard Rc (m)", Rc],
        ["Roughness Factor γ_f", gf],
        ["Berm Factor γ_b", gb],
        ["Wave Obliquity β (°)", beta],
    ], start_row=4)

    _write_xl_table(ws, ["Computed Result", "Value"], [
        ["Deep Water Wavelength L₀ (m)", round(L0, 3)],
        ["Iribarren Number ξ", round(xi, 4)],
        ["Breaker Classification", btype],
        ["Obliquity Factor γ_β", round(gbeta, 4)],
        ["Wave Run-Up Ru2% (m)", round(Ru2, 4)],
        ["Wave Run-Up Ru1% (m)", round(Ru1, 4)],
        ["Reflection Coefficient Cr", round(Cr, 4)],
        ["Mean Overtopping q (L/s/m)", round(q_wu*1000, 5)],
        ["Mean Overtopping q (m³/s/m)", round(q_wu, 7)],
        ["Rc / Ru2%", round(Rc/Ru2, 3) if Ru2 > 0 else "—"],
    ], start_row=13)

    buf = io.BytesIO(); wb.save(buf); buf.seek(0)
    return buf

# ════════════════════════════════════════════════════════════════════
#  VISUALIZATION
# ════════════════════════════════════════════════════════════════════

LAYER_COLORS = ['#C9B99A','#A8B5A0','#B5C4D1','#D1B5C4','#B5D1C4']

def draw_rubble_mound(g, layers, dhw, crest_elev, seabed_elev,
                      upper_height, lower_height, layer_names, n_layers,
                      surcharge_val=10.0):
    pts=g['pts']; ce=crest_elev; se=seabed_elev; berm_e=ce-upper_height
    fig, ax = plt.subplots(figsize=(12,6), dpi=120)
    fig.patch.set_facecolor('#0d1117'); ax.set_facecolor('#161b22')
    xl=pts['sw_toe'][0]; xr=pts['lw_toe'][0]

    for i in range(n_layers):
        top_e=layers[f'top{i+1}']; bot_e=layers[f'bot{i+1}']
        col=LAYER_COLORS[i%len(LAYER_COLORS)]
        ax.fill_betweenx([bot_e,top_e], xl-999, xr+999,
                         facecolor=col, alpha=0.55-i*0.02, zorder=1)
        ax.axhline(y=top_e, color='#444', lw=0.7, ls=':', zorder=2)
    ax.axhline(y=se, color='#607d8b', lw=1.3, ls='--', zorder=2)

    if g['single_slope_sw'] and g['single_slope_lw']:
        xs=[pts['sw_toe'][0],pts['cl'][0],pts['cr'][0],pts['lw_toe'][0],pts['sw_toe'][0]]
        ys=[se,ce,ce,se,se]
    elif g['single_slope_sw']:
        xs=[pts['sw_toe'][0],pts['cl'][0],pts['cr'][0],pts['lw_bs'][0],pts['lw_be'][0],pts['lw_toe'][0],pts['sw_toe'][0]]
        ys=[se,ce,ce,berm_e,berm_e,se,se]
    elif g['single_slope_lw']:
        xs=[pts['sw_toe'][0],pts['sw_be'][0],pts['sw_bs'][0],pts['cl'][0],pts['cr'][0],pts['lw_toe'][0],pts['sw_toe'][0]]
        ys=[se,berm_e,berm_e,ce,ce,se,se]
    else:
        xs=[pts['sw_toe'][0],pts['sw_be'][0],pts['sw_bs'][0],pts['cl'][0],pts['cr'][0],
            pts['lw_bs'][0],pts['lw_be'][0],pts['lw_toe'][0],pts['sw_toe'][0]]
        ys=[se,berm_e,berm_e,ce,ce,berm_e,berm_e,se,se]
    ax.fill(xs,ys,facecolor='#C9A96E',alpha=0.88,edgecolor='#7B5E3A',lw=1.5,zorder=3)
    ax.axhline(y=dhw,color='#3A7EC4',ls='--',lw=2.0,zorder=4)

    cl_x=pts['cl'][0]; cr_x=pts['cr'][0]; crest_w=cr_x-cl_x
    block_h=max(crest_w*0.06,0.4)
    load_rect = mpatches.FancyBboxPatch((cl_x,ce+0.15),crest_w,block_h,
        boxstyle='square,pad=0',facecolor='#ff6b3533',edgecolor='#ff6b35',lw=1.5,hatch='////',zorder=10)
    ax.add_patch(load_rect)
    ax.text((cl_x+cr_x)/2,ce+0.15+block_h+0.6,f'{surcharge_val:.1f} kN/m²',
            ha='center',va='bottom',fontsize=9,fontweight='bold',color='#ff6b35',zorder=12)

    lx=xl-(xr-xl)*0.015
    for i in range(n_layers):
        ax.text(lx,(layers[f'top{i+1}']+layers[f'bot{i+1}'])/2,layer_names[i],
                fontsize=9,va='center',ha='right',fontstyle='italic',color='#ccc',zorder=5)
    for xp,yp in [(pts['sw_toe'][0],se),(pts['lw_toe'][0],se)]:
        ax.text(xp,yp-0.7,f'({xp:.1f}, {yp:.1f})',ha='center',fontsize=7.5,color='#aaa',va='top',zorder=5)

    handles=[mpatches.Patch(facecolor='#C9A96E',alpha=0.88,edgecolor='#7B5E3A',label='Embankment (Rubble)'),
             *[mpatches.Patch(facecolor=LAYER_COLORS[i%len(LAYER_COLORS)],alpha=0.7,
                label=f'{layer_names[i]}  [{layers[f"top{i+1}"]:.1f}→{layers[f"bot{i+1}"]:.1f} m]')
               for i in range(n_layers)],
             mlines.Line2D([],[],color='#3A7EC4',ls='--',lw=2,label=f'DHW ({dhw:.2f} m)')]
    legend=ax.legend(handles=handles,loc='upper center',bbox_to_anchor=(0.5,-0.13),ncol=3,
                     fontsize=9,frameon=True,facecolor='#21262d',edgecolor='#30363d',framealpha=0.97)
    for t in legend.get_texts(): t.set_color('#e6edf3')
    ax.set_xlabel('Distance (m)',fontsize=11,color='#8b949e')
    ax.set_ylabel('Elevation (m)',fontsize=11,color='#8b949e')
    ax.set_title('Rubble Mound Embankment — Cross-Section',fontsize=13,fontweight='bold',color='#e6edf3',pad=10)
    ax.grid(True,alpha=0.15,color='#444',lw=0.5)
    ax.tick_params(colors='#8b949e',labelsize=9)
    for sp in ax.spines.values(): sp.set_color('#30363d')
    mx=(xr-xl)*0.08; ax.set_xlim(xl-mx*3.5,xr+mx)
    ax.set_ylim(layers[f'bot{n_layers}']-1.5,ce+4.0); ax.set_aspect('equal',adjustable='box')
    fig.subplots_adjust(bottom=0.22)
    return fig


def draw_caisson(p, r):
    fig,ax=plt.subplots(figsize=(10,6),dpi=120)
    fig.patch.set_facecolor('#0d1117'); ax.set_facecolor('#0f1921')
    B=p['B']; H_c=p['H_c']; seabed=0.0; d=p['d']
    rb_h,rb_ext=1.8,3.0
    rb_xs=[-rb_ext,-rb_ext*0.3,B+rb_ext*0.3,B+rb_ext,-rb_ext]
    rb_ys=[seabed-rb_h,seabed,seabed,seabed-rb_h,seabed-rb_h]
    ax.fill(rb_xs,rb_ys,facecolor='#C8A96E',alpha=0.85,edgecolor='#7B5E3A',lw=1.2,zorder=2,label='Rubble Foundation')
    ax.axhline(y=seabed,color='#607d8b',lw=1.3,zorder=3)
    caisson_top=seabed+H_c
    caisson_patch=mpatches.FancyBboxPatch((0,seabed),B,H_c,boxstyle='square,pad=0',
        facecolor='#5b7fa5',alpha=0.85,edgecolor='#2c4a70',lw=2.0,zorder=4)
    ax.add_patch(caisson_patch)
    for xi in np.linspace(B*0.2,B*0.8,4):
        ax.plot([xi,xi],[seabed,caisson_top],color='#3a5f80',lw=0.5,alpha=0.35,zorder=5)
    for yi in [seabed+H_c*0.25,seabed+H_c*0.5,seabed+H_c*0.75]:
        ax.plot([0,B],[yi,yi],color='#3a5f80',lw=0.5,alpha=0.35,zorder=5)
    ax.text(B/2,seabed+H_c/2,'CAISSON\n(Concrete)',ha='center',va='center',
            fontsize=11,fontweight='bold',color='white',zorder=6)
    water_y=seabed+d; ax.axhline(y=water_y,color='#3A7EC4',ls='--',lw=2.0,zorder=6)
    wx=-B*0.75; wy=water_y-d*0.35
    ax.annotate('',xy=(0,wy),xytext=(wx,wy),
                arrowprops=dict(arrowstyle='->',color='#f85149',lw=2.5),zorder=7)
    ax.text(wx-0.5,wy+0.2,f'P = {r["P"]:.1f} kN/m\n(Wave Force)',
            fontsize=8.5,color='#f85149',ha='right',zorder=7)
    def dim_arrow(x0,x1,y,label,color='#8b949e',vertical=False):
        if vertical:
            ax.annotate('',xy=(x0,x1),xytext=(x0,y),
                        arrowprops=dict(arrowstyle='<->',color=color,lw=0.9))
            ax.text(x0+0.4,(x1+y)/2,label,fontsize=8,color=color,va='center')
        else:
            ax.annotate('',xy=(x1,y),xytext=(x0,y),
                        arrowprops=dict(arrowstyle='<->',color=color,lw=0.9))
            ax.text((x0+x1)/2,y-0.5,label,ha='center',fontsize=8,color=color)
    dim_arrow(0,B,seabed-rb_h-1.2,f'B = {B:.1f} m')
    dim_arrow(B+1.2,seabed,caisson_top,f'H_c = {H_c:.1f} m',vertical=True)
    dim_arrow(-rb_ext-1.8,seabed,water_y,f'd = {d:.2f} m',color='#3A7EC4',vertical=True)
    ax.text(B/2,water_y+0.4,f'H₁% = {p["H1pct"]:.2f} m',ha='center',fontsize=8.5,color='#3A7EC4')
    s_ok=r['FOS_s']>=1.25; o_ok=r['FOS_o']>=1.50; b_ok=r['q_max']<p['q_allow']
    summary=(f"FOS Sliding:      {r['FOS_s']:.3f}  {'✓' if s_ok else '✗'}\n"
             f"FOS Overturning:  {r['FOS_o']:.3f}  {'✓' if o_ok else '✗'}\n"
             f"q_max:            {r['q_max']:.0f} kPa  {'✓' if b_ok else '✗'}")
    ax.text(0.02,0.98,summary,transform=ax.transAxes,fontsize=9,va='top',ha='left',
            fontfamily='monospace',color='#e6edf3',
            bbox=dict(boxstyle='round,pad=0.5',facecolor='#21262d',edgecolor='#30363d',alpha=0.95))
    handles=[mpatches.Patch(facecolor='#5b7fa5',alpha=0.85,edgecolor='#2c4a70',label='Caisson (Concrete)'),
             mpatches.Patch(facecolor='#C8A96E',alpha=0.85,edgecolor='#7B5E3A',label='Rubble Foundation'),
             mlines.Line2D([],[],color='#3A7EC4',ls='--',lw=2,label=f'Water Table (d = {d:.2f} m)')]
    legend=ax.legend(handles=handles,loc='upper right',fontsize=9,frameon=True,
                     facecolor='#21262d',edgecolor='#30363d',framealpha=0.97)
    for t in legend.get_texts(): t.set_color('#e6edf3')
    ax.set_xlabel('Distance (m)',fontsize=11,color='#8b949e')
    ax.set_ylabel('Elevation (m)',fontsize=11,color='#8b949e')
    ax.set_title('Vertical Caisson — Cross-Section & Stability',fontsize=13,fontweight='bold',color='#e6edf3',pad=10)
    ax.grid(True,alpha=0.15,color='#444',lw=0.5)
    ax.tick_params(colors='#8b949e',labelsize=9)
    for sp in ax.spines.values(): sp.set_color('#30363d')
    pad=B*1.3; ax.set_xlim(-pad,B+pad); ax.set_ylim(seabed-rb_h-2.5,caisson_top+4.0)
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════
#  SESSION STATE DEFAULTS
# ════════════════════════════════════════════════════════════════════

def _default(key, val):
    if key not in st.session_state: st.session_state[key] = val

_default('rm_crest_elev',   14.55); _default('rm_seabed_elev', -3.30)
_default('rm_crest_width',   6.0);  _default('rm_upper_height',  4.85)
_default('rm_lower_height', 13.0);  _default('rm_sw_upper',      2.5)
_default('rm_sw_lower',      2.5);  _default('rm_sw_berm',       6.5)
_default('rm_lw_upper',      1.5);  _default('rm_lw_lower',      1.5)
_default('rm_lw_berm',       2.0);  _default('rm_dhw',           4.99)
_default('rm_surcharge',    10.0);  _default('rm_num_slices',   50.0)
_default('rm_n_layers',      3)

_default('rm_n1','Soft Silt');  _default('rm_t1',7.8)
_default('rm_g1',16.5); _default('rm_c1',6.0); _default('rm_phi1',8.0)
_default('rm_n2','Silty Clay'); _default('rm_t2',10.2)
_default('rm_g2',19.0); _default('rm_c2',20.0); _default('rm_phi2',18.0)
_default('rm_n3','Fine Sand');  _default('rm_t3',10.0)
_default('rm_g3',19.5); _default('rm_c3',0.0); _default('rm_phi3',30.0)
_default('rm_n4','Dense Sand'); _default('rm_t4',8.0)
_default('rm_g4',20.0); _default('rm_c4',0.0); _default('rm_phi4',35.0)
_default('rm_n5','Gravel');     _default('rm_t5',6.0)
_default('rm_g5',21.0); _default('rm_c5',0.0); _default('rm_phi5',40.0)
_default('rm_gr',19.0); _default('rm_cr_',0.0); _default('rm_phir',38.0)

_default('cs_B',16.0); _default('cs_H_c',14.0); _default('cs_gamma_c',24.0)
_default('cs_d',4.59); _default('cs_H1pct',2.71); _default('cs_gamma_w',10.25)
_default('cs_mu',0.60); _default('cs_q_allow',500.0)

_default('wu_H',2.0); _default('wu_T',10.0); _default('wu_slope',2.5)
_default('wu_Rc',1.5); _default('wu_gamma_f',0.55); _default('wu_gamma_b',1.0)
_default('wu_beta',0.0)

# ════════════════════════════════════════════════════════════════════
#  PROJECT SAVE / LOAD
# ════════════════════════════════════════════════════════════════════

RM_KEYS=['rm_crest_elev','rm_seabed_elev','rm_crest_width','rm_upper_height',
         'rm_lower_height','rm_sw_upper','rm_sw_lower','rm_sw_berm',
         'rm_lw_upper','rm_lw_lower','rm_lw_berm','rm_dhw','rm_surcharge',
         'rm_num_slices','rm_n_layers',
         'rm_n1','rm_t1','rm_g1','rm_c1','rm_phi1',
         'rm_n2','rm_t2','rm_g2','rm_c2','rm_phi2',
         'rm_n3','rm_t3','rm_g3','rm_c3','rm_phi3',
         'rm_n4','rm_t4','rm_g4','rm_c4','rm_phi4',
         'rm_n5','rm_t5','rm_g5','rm_c5','rm_phi5',
         'rm_gr','rm_cr_','rm_phir']
CS_KEYS=['cs_B','cs_H_c','cs_gamma_c','cs_d','cs_H1pct','cs_gamma_w','cs_mu','cs_q_allow']
WU_KEYS=['wu_H','wu_T','wu_slope','wu_Rc','wu_gamma_f','wu_gamma_b','wu_beta']

def save_project():
    data={k: st.session_state[k] for k in RM_KEYS+CS_KEYS+WU_KEYS if k in st.session_state}
    data['__version__'] = '4.0'
    data['__saved__'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return json.dumps(data, indent=2)

def load_project(uploaded):
    data=json.loads(uploaded.read().decode())
    for k,v in data.items():
        if not k.startswith('__'): st.session_state[k]=v

# ════════════════════════════════════════════════════════════════════
#  UI HELPERS
# ════════════════════════════════════════════════════════════════════

def section(label):
    st.markdown(f'<div class="section-header">{label}</div>', unsafe_allow_html=True)

def num(label, key, **kw):
    kw.setdefault('format','%.2f')
    val=st.number_input(label, value=float(st.session_state[key]), key=f'_ni_{key}', **kw)
    st.session_state[key]=val; return val

def txt(label, key):
    st.session_state[key]=st.text_input(label, value=st.session_state[key], key=f'_ti_{key}')
    return st.session_state[key]

# ════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
<div class="welcome-card">
  <div style="font-size:24px;font-weight:800;color:#58a6ff;letter-spacing:0.5px;margin-bottom:2px;">HYRCAN</div>
  <div style="font-size:12px;color:#8b949e;margin-bottom:12px;">Engineering Suite v4.0</div>
  <div style="font-size:11px;color:#e6edf3;line-height:2.0;">
    <b style="color:#79c0ff;">Developer:</b> Mathias Adjei Tawiah<br>
    <b style="color:#79c0ff;">Email:</b> mathiasadjeitawiah@gmail.com<br>
    <b style="color:#79c0ff;">Institution:</b> Hohai University<br>
    <span style="color:#8b949e;">College of Harbor, Coastal &amp; Offshore Engineering</span>
  </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="info-card">
  <div style="font-size:11px;font-weight:700;color:#58a6ff;margin-bottom:6px;letter-spacing:0.5px;">DESIGN STANDARDS</div>
  <span class="badge">EurOtop 2018</span>
  <span class="badge">JTS 154-1-2011</span>
  <span class="badge">GB 50286-2013</span>
</div>""", unsafe_allow_html=True)

    st.markdown("""
<div class="info-card">
  <div style="font-size:11px;font-weight:700;color:#58a6ff;margin-bottom:6px;letter-spacing:0.5px;">MODULES</div>
  <div style="font-size:11px;color:#8b949e;line-height:2.2;">
    🏗️ &nbsp;Rubble Mound Coordinate Generator<br>
    🏛️ &nbsp;Vertical Caisson Stability Calculator<br>
    🌊 &nbsp;Wave Run-Up & Overtopping Calculator<br>
    📁 &nbsp;Project History Manager
  </div>
</div>""", unsafe_allow_html=True)

    st.markdown("""
<div class="info-card">
  <div style="font-size:11px;font-weight:700;color:#58a6ff;margin-bottom:6px;letter-spacing:0.5px;">REPOSITORY</div>
  <div style="font-size:11px;line-height:2.0;">
    <a href="https://github.com/Mathias-lab/hyrcan-suite" target="_blank"
       style="color:#58a6ff;text-decoration:none;">🔗 GitHub Repository</a><br>
    <a href="https://linkedin.com/in/mathias-adjei-tawiah" target="_blank"
       style="color:#58a6ff;text-decoration:none;">🔗 LinkedIn Profile</a>
  </div>
</div>""", unsafe_allow_html=True)

    st.markdown('<div style="font-size:10px;color:#484f58;margin-top:12px;text-align:center;">Coordinate logic verified against HYRCAN 3.0 reference output</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
#  HEADER
# ════════════════════════════════════════════════════════════════════

st.markdown("""
<div style="background:linear-gradient(135deg,#1f6feb18,#161b22);
            border:1px solid #30363d;border-radius:12px;
            padding:18px 26px;margin-bottom:20px;">
  <div style="display:flex;align-items:center;gap:14px;">
    <span style="font-size:34px;">🏗️</span>
    <div>
      <div style="font-size:20px;font-weight:800;color:#58a6ff;letter-spacing:0.5px;">
        HYRCAN Engineering Suite <span style="color:#8b949e;font-size:14px;">v4.0</span>
      </div>
      <div style="color:#8b949e;font-size:12px;margin-top:3px;">
        Rubble Mound Coordinate Generator &nbsp;·&nbsp;
        Vertical Caisson FOS Analysis &nbsp;·&nbsp;
        Wave Run-Up & Overtopping &nbsp;·&nbsp;
        Project History Manager
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
#  TABS
# ════════════════════════════════════════════════════════════════════

tab1, tab2, tab3, tab4 = st.tabs([
    "🏗️  Rubble Mound",
    "🏛️  Vertical Caisson",
    "🌊  Wave Run-Up",
    "📁  Project History",
])

# ────────────────────────────────────────────────────────────────────
#  TAB 1 — RUBBLE MOUND
# ────────────────────────────────────────────────────────────────────

with tab1:
    sc1, sc2, sc3 = st.columns([2,2,5])
    with sc1:
        st.download_button('💾 Save Project', data=save_project(),
                           file_name='hyrcan_project.json', mime='application/json',
                           use_container_width=True)
    with sc2:
        uploaded=st.file_uploader('📂 Load Project', type='json', label_visibility='collapsed')
        if uploaded:
            load_project(uploaded); st.success('Project loaded.', icon='✅')

    st.markdown('<hr style="border-color:#30363d;margin:8px 0 16px 0;">', unsafe_allow_html=True)
    left_col, right_col = st.columns([1,1.6], gap='large')

    with left_col:
        section("Embankment Geometry")
        c1,c2=st.columns(2)
        with c1:
            ce=num('Crest elevation (m)','rm_crest_elev')
            cw=num('Crest width (m)','rm_crest_width',min_value=0.5)
            uh=num('Upper height (m)','rm_upper_height',min_value=0.0)
        with c2:
            se=num('Seabed elevation (m)','rm_seabed_elev')
            lh=num('Lower height (m)','rm_lower_height',min_value=0.0)

        total_h=ce-se
        if abs((uh+lh)-total_h)>0.01:
            st.error(f"Height mismatch: upper + lower = {uh+lh:.3f} m  ≠  crest − seabed = {total_h:.3f} m")

        section("Slope Ratios (H : V)  —  Set berm = 0 for single-slope")
        c1,c2,c3=st.columns(3)
        with c1: sw_u=num('Seaward upper','rm_sw_upper',min_value=0.1); sw_l=num('Seaward lower','rm_sw_lower',min_value=0.1)
        with c2: lw_u=num('Landward upper','rm_lw_upper',min_value=0.1); lw_l=num('Landward lower','rm_lw_lower',min_value=0.1)
        with c3: sw_b=num('Seaward berm (m)','rm_sw_berm',min_value=0.0); lw_b=num('Landward berm (m)','rm_lw_berm',min_value=0.0)

        sw_type="Single-slope" if sw_b==0 else f"Double-slope (berm {sw_b:.1f} m)"
        lw_type="Single-slope" if lw_b==0 else f"Double-slope (berm {lw_b:.1f} m)"
        st.caption(f"Seaward: **{sw_type}**  |  Landward: **{lw_type}**")

        section("Hydraulic Conditions & Loads")
        c1,c2,c3=st.columns(3)
        with c1: dhw=num('DHW level (m)','rm_dhw')
        with c2: q=num('Surcharge (kN/m²)','rm_surcharge',min_value=0.0)
        with c3: ns=num('No. of slices','rm_num_slices',min_value=10.0,step=5.0,format='%.0f')

        section("Soil Layers  (up to 5)")
        n_layers=st.slider('Number of layers',min_value=3,max_value=5,
                           value=int(st.session_state['rm_n_layers']),step=1)
        st.session_state['rm_n_layers']=n_layers

        layer_names=[]; layer_thicknesses=[]; layer_props=[]
        for i in range(1,n_layers+1):
            st.markdown(f"**Layer {i}**")
            c_name,c_t,c_g,c_c,c_phi=st.columns([2.2,1.3,1.3,1.3,1.3])
            with c_name: name=txt('Name' if i==1 else ' ',f'rm_n{i}')
            with c_t:    t=num('Thickness (m)' if i==1 else ' ',f'rm_t{i}',min_value=0.1)
            with c_g:    g_=num('γ (kN/m³)' if i==1 else ' ',f'rm_g{i}',min_value=10.0)
            with c_c:    c_=num('c (kPa)' if i==1 else ' ',f'rm_c{i}',min_value=0.0)
            with c_phi:  phi=num('φ (°)' if i==1 else ' ',f'rm_phi{i}',min_value=0.0)
            layer_names.append(name); layer_thicknesses.append(t); layer_props.append((g_,c_,phi))

        st.markdown("**Embankment (Rubble)**")
        c1,c2,c3=st.columns(3)
        with c1: gr=num('γ (kN/m³)','rm_gr',min_value=10.0)
        with c2: cr_=num('c (kPa)','rm_cr_',min_value=0.0)
        with c3: phir=num('φ (°)','rm_phir',min_value=0.0)

        layers=compute_layer_elevations(se,layer_thicknesses)

        section("Layer Elevation Preview")
        df_rows={
            'Layer': layer_names,
            'Top Elev (m)':    [f"{layers[f'top{i+1}']:.3f}" for i in range(n_layers)],
            'Bottom Elev (m)': [f"{layers[f'bot{i+1}']:.3f}" for i in range(n_layers)],
            'Thickness (m)':   [f"{layer_thicknesses[i]:.2f}" for i in range(n_layers)],
            'HYRCAN Y_top':    [f"{layers[f'Y_top{i+1}']:.3f}" for i in range(n_layers)],
            'HYRCAN Y_bot':    [f"{layers[f'Y_bot{i+1}']:.3f}" for i in range(n_layers)],
        }
        st.dataframe(pd.DataFrame(df_rows), use_container_width=True, hide_index=True)
        st.caption(f"Datum shift: **+{layers['datum']:.3f} m**  |  Bottom of {layer_names[-1]} → Y = 0.000")

        st.markdown('<br>', unsafe_allow_html=True)
        generate=st.button('Generate HYRCAN Coordinates',type='primary',use_container_width=True)

    with right_col:
        layers=compute_layer_elevations(se,layer_thicknesses)
        valid=abs((uh+lh)-(ce-se))<=0.01

        if generate and valid:
            g=compute_geometry(ce,se,cw,uh,lh,sw_u,sw_l,sw_b,lw_u,lw_l,lw_b,layers)
            st.session_state.update({
                'rm_g':g,'rm_layers':layers,'rm_layer_names':layer_names,
                'rm_layer_thicknesses':layer_thicknesses,'rm_layer_props':layer_props,
                'rm_n_layers_gen':n_layers,'rm_sw_upper_gen':sw_u,'rm_sw_lower_gen':sw_l,
                'rm_sw_berm_gen':sw_b,'rm_lw_upper_gen':lw_u,'rm_lw_lower_gen':lw_l,
                'rm_lw_berm_gen':lw_b,'rm_generated':True,
            })
            checks=verify_geometry(g,ce,se,cw,uh,lh,sw_u,sw_l,sw_b,lw_u,lw_l,lw_b)
            all_ok=all(c[3] for c in checks)
            add_to_history("Rubble Mound", f"Crest={ce}m / Seabed={se}m",
                params={'crest_elev':ce,'seabed_elev':se,'crest_width':cw,
                        'upper_height':uh,'lower_height':lh,'dhw':dhw,'surcharge':q},
                results={'all_checks_passed':all_ok,'datum_shift':layers['datum'],
                         'model_width':g['model_right']})

        section("Cross-Section Preview")
        try:
            g_prev=compute_geometry(ce,se,cw,uh,lh,sw_u,sw_l,sw_b,lw_u,lw_l,lw_b,layers)
            fig_prev=draw_rubble_mound(g_prev,layers,dhw,ce,se,uh,lh,layer_names,n_layers,
                                       surcharge_val=q)
            st.pyplot(fig_prev,use_container_width=True); plt.close(fig_prev)
        except Exception as e:
            st.warning(f"Preview unavailable: {e}")

        if st.session_state.get('rm_generated'):
            g=st.session_state['rm_g']; layers=st.session_state['rm_layers']
            lnames=st.session_state['rm_layer_names']; lprops=st.session_state['rm_layer_props']
            nl=st.session_state['rm_n_layers_gen']
            _sw_u=st.session_state.get('rm_sw_upper_gen',sw_u)
            _sw_l=st.session_state.get('rm_sw_lower_gen',sw_l)
            _sw_b=st.session_state.get('rm_sw_berm_gen',sw_b)
            _lw_u=st.session_state.get('rm_lw_upper_gen',lw_u)
            _lw_l=st.session_state.get('rm_lw_lower_gen',lw_l)
            _lw_b=st.session_state.get('rm_lw_berm_gen',lw_b)

            section("Geometry Verification")
            checks=verify_geometry(g,ce,se,cw,uh,lh,_sw_u,_sw_l,_sw_b,_lw_u,_lw_l,_lw_b)
            all_ok=all(c[3] for c in checks)
            if all_ok: st.success('All geometry checks passed.', icon='✅')
            else: st.error('One or more geometry checks failed.')
            df_chk=pd.DataFrame({
                'Parameter':[c[0] for c in checks],
                'Expected':[f'{c[1]:.4f}' for c in checks],
                'Calculated':[f'{c[2]:.4f}' for c in checks],
                'Status':['Pass' if c[3] else 'FAIL' for c in checks],
            })
            st.dataframe(df_chk,use_container_width=True,hide_index=True)

            pts=g['pts']
            mc1,mc2,mc3,mc4=st.columns(4)
            mc1.metric('Model Width', f"{g['model_right']:.3f} m")
            mc2.metric('Crest Left X', f"{pts['cl'][0]:.3f}")
            mc3.metric('Crest Right X', f"{pts['cr'][0]:.3f}")
            mc4.metric('Datum Shift', f"+{layers['datum']:.3f} m")

            section("HYRCAN Step-by-Step Instructions")
            instructions=generate_hyrcan_instructions(
                g,layers,dhw,q,ns,ce,se,uh,lh,_sw_u,_sw_l,_sw_b,_lw_u,_lw_l,_lw_b,cw,
                lnames,lprops,nl,mat_rubble=(gr,cr_,phir))
            st.markdown(f'<div class="coord-block">{instructions}</div>',unsafe_allow_html=True)

            # ── Export block ─────────────────────────────────────────
            section("Export Results")
            st.caption("Download results in multiple formats for documentation and reporting.")

            fig_bytes_buf=io.BytesIO()
            fig_export=draw_rubble_mound(g,layers,dhw,ce,se,uh,lh,lnames,nl,surcharge_val=q)
            fig_export.savefig(fig_bytes_buf,format='png',dpi=300,bbox_inches='tight',facecolor='white')
            plt.close(fig_export)
            fig_bytes_buf.seek(0); fig_bytes=fig_bytes_buf.read()

            coords_txt=generate_coordinates_txt(g,layers,dhw,q,ce,se,nl,_sw_b,_lw_b)
            word_buf=build_word_rubble(g,layers,dhw,q,checks,ce,se,lnames,lprops,nl,
                                       mat_rubble=(gr,cr_,phir),fig_bytes=fig_bytes)
            excel_buf=build_excel_rubble(g,layers,dhw,q,checks,ce,se,lnames,lprops,nl,
                                         mat_rubble=(gr,cr_,phir))

            e1,e2,e3,e4,e5=st.columns(5)
            with e1:
                st.download_button('📄 Coordinates (.txt)', data=coords_txt,
                                   file_name='hyrcan_coordinates.txt',mime='text/plain',
                                   use_container_width=True)
            with e2:
                st.download_button('📋 Instructions (.txt)', data=instructions,
                                   file_name='hyrcan_instructions.txt',mime='text/plain',
                                   use_container_width=True)
            with e3:
                st.download_button('📝 Report (.docx)', data=word_buf,
                                   file_name='hyrcan_rubble_report.docx',
                                   mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                                   use_container_width=True)
            with e4:
                st.download_button('📊 Data (.xlsx)', data=excel_buf,
                                   file_name='hyrcan_rubble_data.xlsx',
                                   mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                                   use_container_width=True)
            with e5:
                st.download_button('🖼 Plot (PNG)', data=fig_bytes,
                                   file_name='hyrcan_cross_section.png',mime='image/png',
                                   use_container_width=True)

        elif generate and not valid:
            st.error('Correct the height mismatch before generating coordinates.')
        elif not st.session_state.get('rm_generated'):
            st.info('Enter parameters and click **Generate HYRCAN Coordinates** to produce output.', icon='ℹ️')


# ────────────────────────────────────────────────────────────────────
#  TAB 2 — VERTICAL CAISSON
# ────────────────────────────────────────────────────────────────────

with tab2:
    st.markdown('<hr style="border-color:#30363d;margin:0 0 16px 0;">', unsafe_allow_html=True)
    left2, right2 = st.columns([1,1.6], gap='large')

    with left2:
        section("Caisson Geometry")
        c1,c2=st.columns(2)
        with c1: B_cs=num('Width B (m)','cs_B',min_value=1.0); gc=num('Concrete γ_c (kN/m³)','cs_gamma_c',min_value=10.0)
        with c2: Hc_cs=num('Height H_c (m)','cs_H_c',min_value=1.0)

        section("Hydraulic Conditions")
        c1,c2,c3=st.columns(3)
        with c1: d_cs=num('Water depth d (m)','cs_d',min_value=0.1)
        with c2: H1_cs=num('Wave H₁% (m)','cs_H1pct',min_value=0.1)
        with c3: gw_cs=num('γ_w (kN/m³)','cs_gamma_w',min_value=9.0)

        section("Stability Parameters")
        c1,c2=st.columns(2)
        with c1: mu_cs=num('Friction coeff μ','cs_mu',min_value=0.1,max_value=1.0,step=0.01)
        with c2: qa_cs=num('q_allow (kPa)','cs_q_allow',min_value=50.0)

        st.markdown("""
<div class="info-card" style="margin-top:16px;">
  <div style="font-size:11px;font-weight:700;color:#58a6ff;margin-bottom:6px;letter-spacing:0.5px;">DESIGN STANDARDS</div>
  <div style="font-size:11px;color:#8b949e;line-height:2.0;">
    Wave force: JTS 154-1-2011, Appendix A<br>
    Sliding FOS ≥ 1.25 — GB 50286-2013 §5.3.2<br>
    Overturning FOS ≥ 1.50 — GB 50286-2013 §5.3.3<br>
    Bearing: q_max &lt; q_allow — JTS 154-1-2011 §5.3.4
  </div>
</div>""", unsafe_allow_html=True)

    with right2:
        cs_p=dict(B=B_cs,H_c=Hc_cs,gamma_c=gc,d=d_cs,H1pct=H1_cs,gamma_w=gw_cs,mu=mu_cs,q_allow=qa_cs)
        r=caisson_fos(**cs_p)
        s_ok=r['FOS_s']>=1.25; o_ok=r['FOS_o']>=1.50; b_ok=r['q_max']<qa_cs

        section("FOS Results (live)")
        m1,m2,m3=st.columns(3)
        m1.metric('Sliding FOS',f"{r['FOS_s']:.3f}",
                  delta='≥ 1.25  Pass' if s_ok else '< 1.25  Fail',
                  delta_color='normal' if s_ok else 'inverse')
        m2.metric('Overturning FOS',f"{r['FOS_o']:.3f}",
                  delta='≥ 1.50  Pass' if o_ok else '< 1.50  Fail',
                  delta_color='normal' if o_ok else 'inverse')
        m3.metric('Bearing q_max',f"{r['q_max']:.1f} kPa",
                  delta=f"< {int(qa_cs)} kPa  Pass" if b_ok else f"≥ {int(qa_cs)} kPa  Fail",
                  delta_color='normal' if b_ok else 'inverse')

        if s_ok and o_ok and b_ok:
            st.success('All stability criteria satisfied — design is adequate.', icon='✅')
        else:
            st.error('One or more stability criteria not met — review design parameters.', icon='❌')

        # Save to history
        add_to_history("Vertical Caisson", f"B={B_cs}m / H_c={Hc_cs}m",
            params={'B':B_cs,'H_c':Hc_cs,'gamma_c':gc,'d':d_cs,'H1pct':H1_cs,'mu':mu_cs},
            results={'FOS_s':round(r['FOS_s'],4),'FOS_o':round(r['FOS_o'],4),
                     'q_max':round(r['q_max'],2),
                     'all_pass':bool(s_ok and o_ok and b_ok)})

        section("Detailed Results")
        df_res=pd.DataFrame({
            'Check':['Self-weight W','Wave Force P','Sliding FOS','Overturning FOS','Bearing q_max'],
            'Calculated':[f"{r['W']:,.1f} kN/m",f"{r['P']:,.2f} kN/m",
                          f"{r['FOS_s']:.3f}",f"{r['FOS_o']:.3f}",f"{r['q_max']:,.1f} kPa"],
            'Required':['—','—','≥ 1.25','≥ 1.50',f"< {int(qa_cs)} kPa"],
            'Standard':['—','JTS 154-1-2011 App. A','GB 50286-2013 §5.3.2',
                        'GB 50286-2013 §5.3.3','JTS 154-1-2011 §5.3.4'],
            'Status':['—','—',
                      'Pass' if s_ok else 'FAIL',
                      'Pass' if o_ok else 'FAIL',
                      'Pass' if b_ok else 'FAIL'],
        })
        st.dataframe(df_res,use_container_width=True,hide_index=True)

        section("Step-by-Step Calculations")
        calc_text=f"""\
VERTICAL CAISSON STABILITY ANALYSIS — HYRCAN v4.0
Standards: JTS 154-1-2011 | GB 50286-2013
{'─'*60}

1. SELF-WEIGHT
   W = B × H_c × γ_c
   W = {B_cs:.2f} × {Hc_cs:.2f} × {gc:.2f}
   W = {r['W']:,.2f} kN/m

2. WAVE FORCE  [JTS 154-1-2011, Appendix A]
   P = 0.5 × γ_w × H₁%² + γ_w × d × H₁%
   P = 0.5 × {gw_cs:.2f} × {H1_cs:.2f}² + {gw_cs:.2f} × {d_cs:.2f} × {H1_cs:.2f}
   P = {0.5*gw_cs*H1_cs**2:.3f} + {gw_cs*d_cs*H1_cs:.3f}
   P = {r['P']:,.3f} kN/m

3. SLIDING CHECK  [GB 50286-2013 §5.3.2]
   F_resisting = μ × W = {mu_cs:.2f} × {r['W']:,.2f} = {r['F_res']:,.2f} kN/m
   FOS_sliding = {r['F_res']:,.2f} / {r['P']:,.3f} = {r['FOS_s']:.4f}
   Required ≥ 1.25  →  {'PASS' if s_ok else 'FAIL'}

4. OVERTURNING CHECK  [GB 50286-2013 §5.3.3]
   M_resisting  = W × (B/2) = {r['W']:,.2f} × {B_cs/2:.2f} = {r['M_res']:,.2f} kN·m/m
   Moment arm   = d/2 + H₁%/3 = {d_cs/2:.3f} + {H1_cs/3:.3f} = {r['arm']:.3f} m
   M_overturning = P × arm = {r['P']:,.3f} × {r['arm']:.3f} = {r['M_ot']:,.2f} kN·m/m
   FOS_overturning = {r['M_res']:,.2f} / {r['M_ot']:,.2f} = {r['FOS_o']:.4f}
   Required ≥ 1.50  →  {'PASS' if o_ok else 'FAIL'}

5. BEARING PRESSURE  [JTS 154-1-2011 §5.3.4]
   q_max = W / B = {r['W']:,.2f} / {B_cs:.2f} = {r['q_max']:,.2f} kPa
   Required < {int(qa_cs)} kPa  →  {'PASS' if b_ok else 'FAIL'}
"""
        st.markdown(f'<div class="coord-block">{calc_text}</div>',unsafe_allow_html=True)

        section("Cross-Section")
        fig_cs=draw_caisson(cs_p,r)
        st.pyplot(fig_cs,use_container_width=True); plt.close(fig_cs)

        # ── Export block ──────────────────────────────────────────────
        section("Export Results")
        fig_cs2_buf=io.BytesIO()
        fig_cs2=draw_caisson(cs_p,r)
        fig_cs2.savefig(fig_cs2_buf,format='png',dpi=300,bbox_inches='tight',facecolor='white')
        plt.close(fig_cs2); fig_cs2_buf.seek(0); cs_fig_bytes=fig_cs2_buf.read()

        word_cs=build_word_caisson(B_cs,Hc_cs,gc,d_cs,H1_cs,gw_cs,mu_cs,qa_cs,r,fig_bytes=cs_fig_bytes)
        excel_cs=build_excel_caisson(B_cs,Hc_cs,gc,d_cs,H1_cs,gw_cs,mu_cs,qa_cs,r)

        e1,e2,e3,e4=st.columns(4)
        with e1:
            st.download_button('📝 Report (.docx)', data=word_cs,
                               file_name='hyrcan_caisson_report.docx',
                               mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                               use_container_width=True)
        with e2:
            st.download_button('📊 Data (.xlsx)', data=excel_cs,
                               file_name='hyrcan_caisson_data.xlsx',
                               mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                               use_container_width=True)
        with e3:
            st.download_button('📋 Calculations (.txt)', data=calc_text,
                               file_name='hyrcan_caisson_calcs.txt',mime='text/plain',
                               use_container_width=True)
        with e4:
            st.download_button('🖼 Plot (PNG)', data=cs_fig_bytes,
                               file_name='hyrcan_caisson.png',mime='image/png',
                               use_container_width=True)


# ────────────────────────────────────────────────────────────────────
#  TAB 3 — WAVE RUN-UP
# ────────────────────────────────────────────────────────────────────

with tab3:
    st.markdown('<hr style="border-color:#30363d;margin:0 0 16px 0;">', unsafe_allow_html=True)
    left3,right3=st.columns([1,1.4],gap='large')

    with left3:
        section("Wave Parameters")
        c1,c2=st.columns(2)
        with c1: H_wu=num('H_m0 (m)','wu_H',min_value=0.1)
        with c2: T_wu=num('T_p (s)','wu_T',min_value=1.0)

        section("Structure Geometry")
        slope_wu=num('Slope ratio H:V  (e.g. 2.5 = 1:2.5)','wu_slope',min_value=0.1)
        Rc_wu=num('Freeboard Rc (m)','wu_Rc',min_value=0.0)

        section("Reduction Factors  (EurOtop 2018)")
        c1,c2=st.columns(2)
        with c1: gf_wu=num('Roughness factor γ_f','wu_gamma_f',min_value=0.1,max_value=1.0,step=0.01)
        with c2: gb_wu=num('Berm factor γ_b','wu_gamma_b',min_value=0.1,max_value=1.0,step=0.01)
        beta_wu=num('Wave obliquity β (°)','wu_beta',min_value=0.0,max_value=80.0,step=1.0,format='%.1f')

        with st.expander("Roughness Factor Reference  (EurOtop 2018, Table 5.2)"):
            rf_data={'Structure Type':[
                'Smooth impermeable (concrete)','Asphalt','Grass (short)','Grass (long/rough)',
                'Single-size rock (permeable)','Double-layer rock (permeable)',
                'Rock armour (rough permeable)','Tetrapods','Accropode','Xbloc',
                'Cube (single layer)','Cube (double layer)'],
                'γ_f':['1.00','1.00','1.00','0.90–1.00','0.55','0.45','0.40–0.55',
                       '0.38','0.46','0.45','0.47','0.50']}
            st.dataframe(pd.DataFrame(rf_data),use_container_width=True,hide_index=True)

    with right3:
        tan_alpha=1.0/slope_wu
        L0=calc_wavelength(T_wu)
        xi=calc_iribarren(tan_alpha,H_wu,L0)
        gbeta=calc_obliquity_factor(beta_wu)
        Ru2=calc_runup_2percent(H_wu,xi,gf_wu,gb_wu,gbeta)
        Ru1=calc_runup_1percent(H_wu,xi,gf_wu,gb_wu,gbeta)
        Cr=calc_reflection(xi)
        q_wu=calc_overtopping(H_wu,L0,xi,Rc_wu,gf_wu,gbeta)
        btype=classify_breaker(xi)

        add_to_history("Wave Run-Up", f"H={H_wu}m / T={T_wu}s / Rc={Rc_wu}m",
            params={'H':H_wu,'T':T_wu,'slope':slope_wu,'Rc':Rc_wu,'gamma_f':gf_wu,'beta':beta_wu},
            results={'Ru2':round(Ru2,4),'Ru1':round(Ru1,4),'xi':round(xi,4),
                     'q_L_s_m':round(q_wu*1000,5),'breaker':btype})

        section("Results  (live)")
        m1,m2,m3=st.columns(3)
        m1.metric("Wavelength L₀",f"{L0:.2f} m")
        m2.metric("Iribarren ξ",f"{xi:.3f}")
        m3.metric("Breaker Type",btype)
        m4,m5,m6=st.columns(3)
        m4.metric("Ru2% (m)",f"{Ru2:.3f}")
        m5.metric("Ru1% (m)",f"{Ru1:.3f}")
        m6.metric("Reflection Cr",f"{Cr:.3f}")
        m7,m8,m9=st.columns(3)
        m7.metric("γ_β (obliquity)",f"{gbeta:.3f}")
        m8.metric("Overtopping q",
                  f"{q_wu*1000:.4f} L/s/m" if q_wu<0.001 else f"{q_wu*1000:.3f} L/s/m")
        m9.metric("Rc / Ru2%",f"{Rc_wu/Ru2:.3f}" if Ru2>0 else "—")

        q_ls=q_wu*1000
        if q_ls<0.01:    st.success(f"Mean overtopping = {q_ls:.4f} L/s/m — Negligible (< 0.01 L/s/m).", icon='✅')
        elif q_ls<1.0:   st.success(f"Mean overtopping = {q_ls:.4f} L/s/m — Within acceptable limits.", icon='✅')
        elif q_ls<10.0:  st.warning(f"Mean overtopping = {q_ls:.3f} L/s/m — Verify tolerable limits for structure type.")
        else:            st.error(f"Mean overtopping = {q_ls:.2f} L/s/m — Excessive. Increase freeboard or armour roughness.")

        section("Step-by-Step Calculations")
        wu_text=f"""\
WAVE RUN-UP & OVERTOPPING CALCULATOR — HYRCAN v4.0
EurOtop 2018 | JTS 154-1-2011
{'─'*60}

INPUT PARAMETERS
  H_m0 (significant wave height) : {H_wu:.3f} m
  T_p  (peak wave period)         : {T_wu:.3f} s
  Slope (H:V)                     : 1:{slope_wu:.2f}
  tan(α)                          : {tan_alpha:.4f}
  Freeboard Rc                    : {Rc_wu:.3f} m
  Roughness factor γ_f            : {gf_wu:.3f}
  Berm factor γ_b                 : {gb_wu:.3f}
  Obliquity β                     : {beta_wu:.1f}°
  Obliquity factor γ_β            : {gbeta:.4f}

STEP 1 — Deep Water Wavelength
  L₀ = g·T_p² / (2π) = 9.81 × {T_wu:.2f}² / (2π) = {L0:.3f} m

STEP 2 — Iribarren Number
  ξ = tan(α) / √(H_m0 / L₀)
  ξ = {tan_alpha:.4f} / √({H_wu:.3f} / {L0:.3f}) = {xi:.4f}
  Breaker classification: {btype}

STEP 3 — Wave Run-Up (EurOtop 2018, Eq. 5.2)
  Ru2% = 1.65 · γ_b · γ_f · γ_β · ξ · H_m0
       = 1.65 × {gb_wu:.3f} × {gf_wu:.3f} × {gbeta:.4f} × {xi:.4f} × {H_wu:.3f}
       = {1.65*gb_wu*gf_wu*gbeta*xi*H_wu:.4f} m  (before upper limit)
  Upper limit = (4.0 - 1.5/√(γ_f·γ_β·ξ)) · γ_b · H_m0
              = {(4.0 - 1.5/max(math.sqrt(gf_wu*gbeta*xi),1e-9))*gb_wu*H_wu:.4f} m
  Ru2% = {Ru2:.4f} m  (governing value)
  Ru1% ≈ 1.4 × Ru2% = {Ru1:.4f} m

STEP 4 — Reflection Coefficient (Postma 1989)
  Cr = 0.1 · ξ² = 0.1 × {xi:.4f}² = {Cr:.4f}  (capped at 1.0)

STEP 5 — Mean Overtopping Discharge (EurOtop 2018, Eq. 5.6)
  q = √(g·H³) / √(L₀/H) · 0.2 · exp(−2.3 · Rc / (γ_f·γ_β·H·ξ))
  q = {q_wu:.6f} m³/s/m  =  {q_wu*1000:.4f} L/s/m

STEP 6 — Obliquity Factor (EurOtop 2018)
  γ_β = max(1 − 0.0033·β, 0.736)  [β = {beta_wu:.1f}°]
  γ_β = {gbeta:.4f}
"""
        st.markdown(f'<div class="coord-block">{wu_text}</div>',unsafe_allow_html=True)

        section("Export Results")
        word_wu=build_word_runup(H_wu,T_wu,slope_wu,Rc_wu,gf_wu,gb_wu,beta_wu,
                                  xi,L0,Ru2,Ru1,Cr,q_wu,gbeta,btype)
        excel_wu=build_excel_runup(H_wu,T_wu,slope_wu,Rc_wu,gf_wu,gb_wu,beta_wu,
                                    xi,L0,Ru2,Ru1,Cr,q_wu,gbeta,btype)
        e1,e2,e3=st.columns(3)
        with e1:
            st.download_button('📝 Report (.docx)', data=word_wu,
                               file_name='hyrcan_runup_report.docx',
                               mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                               use_container_width=True)
        with e2:
            st.download_button('📊 Data (.xlsx)', data=excel_wu,
                               file_name='hyrcan_runup_data.xlsx',
                               mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                               use_container_width=True)
        with e3:
            st.download_button('📋 Calculations (.txt)', data=wu_text,
                               file_name='hyrcan_runup_calcs.txt',mime='text/plain',
                               use_container_width=True)


# ────────────────────────────────────────────────────────────────────
#  TAB 4 — PROJECT HISTORY
# ────────────────────────────────────────────────────────────────────

with tab4:
    st.markdown('<hr style="border-color:#30363d;margin:0 0 16px 0;">', unsafe_allow_html=True)

    history=load_history()

    hdr_col, btn_col=st.columns([4,1])
    with hdr_col:
        st.markdown(f"""
<div style="font-size:13px;color:#8b949e;margin-bottom:12px;">
  Session log — last <b style="color:#e6edf3;">{len(history)}</b> calculations recorded
  (capacity: 50). Records persist for the duration of the server session.
</div>""", unsafe_allow_html=True)
    with btn_col:
        if st.button('Clear History', use_container_width=True):
            save_history([]); st.rerun()

    if not history:
        st.info('No records yet. Run a calculation in any module to begin logging.', icon='ℹ️')
    else:
        # Filter
        modules=["All Modules"]+list({e['module'] for e in history})
        sel_module=st.selectbox('Filter by module', modules)

        filtered=[e for e in history if sel_module=="All Modules" or e['module']==sel_module]

        for entry in filtered:
            mod=entry['module']; ts=entry['timestamp']; lbl=entry['label']
            res=entry.get('results',{})

            # Status badge
            if 'all_checks_passed' in res or 'all_pass' in res:
                ok=res.get('all_checks_passed', res.get('all_pass', False))
                badge=f'<span class="pass-badge">PASS</span>' if ok else '<span class="fail-badge">FAIL</span>'
            elif 'Ru2' in res:
                badge=f'<span class="badge">{res["breaker"]}</span>'
            else:
                badge=""

            with st.expander(f"**[{mod}]**  {lbl}  —  {ts}  {badge}", expanded=False):
                c1,c2=st.columns(2)
                with c1:
                    st.markdown("**Parameters**")
                    param_rows=[[k,str(v)] for k,v in entry.get('params',{}).items()]
                    st.dataframe(pd.DataFrame(param_rows,columns=['Key','Value']),
                                 use_container_width=True,hide_index=True)
                with c2:
                    st.markdown("**Results**")
                    res_rows=[[k,str(v)] for k,v in res.items()]
                    st.dataframe(pd.DataFrame(res_rows,columns=['Key','Value']),
                                 use_container_width=True,hide_index=True)

                # Export this history entry
                entry_json=json.dumps(entry,indent=2)
                st.download_button(
                    f'Export Record ({entry["id"]}) as JSON',
                    data=entry_json,
                    file_name=f'hyrcan_record_{entry["id"]}.json',
                    mime='application/json',
                    key=f'dl_{entry["id"]}',
                )

        # Aggregate export
        st.markdown('<br>', unsafe_allow_html=True)
        section("Batch Export")
        all_json=json.dumps(history,indent=2)
        # Build summary Excel
        wb_hist=openpyxl.Workbook()
        ws_hist=wb_hist.active; ws_hist.title="History"
        ws_hist.column_dimensions['A'].width=22; ws_hist.column_dimensions['B'].width=18
        ws_hist.column_dimensions['C'].width=30; ws_hist.column_dimensions['D'].width=40
        ws_hist.column_dimensions['E'].width=40
        _write_xl_table(ws_hist,
            ["Timestamp","Module","Label","Parameters","Results"],
            [[e['timestamp'],e['module'],e['label'],
              json.dumps(e.get('params',{})),json.dumps(e.get('results',{}))]
             for e in history], start_row=1)
        hist_excel_buf=io.BytesIO(); wb_hist.save(hist_excel_buf); hist_excel_buf.seek(0)

        bc1,bc2=st.columns(2)
        with bc1:
            st.download_button('Export All Records (.json)', data=all_json,
                               file_name='hyrcan_history.json',mime='application/json',
                               use_container_width=True)
        with bc2:
            st.download_button('Export All Records (.xlsx)', data=hist_excel_buf,
                               file_name='hyrcan_history.xlsx',
                               mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                               use_container_width=True)


# ════════════════════════════════════════════════════════════════════
#  FOOTER
# ════════════════════════════════════════════════════════════════════

st.markdown('<br>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;color:#484f58;font-size:11px;
            border-top:1px solid #21262d;padding-top:12px;">
  HYRCAN Engineering Suite v4.0 &nbsp;·&nbsp;
  Developed by <b>Mathias Adjei Tawiah</b> &nbsp;·&nbsp;
  mathiasadjeitawiah@gmail.com &nbsp;·&nbsp;
  Hohai University — College of Harbor, Coastal and Offshore Engineering<br>
  Standards: EurOtop 2018 | JTS 154-1-2011 | GB 50286-2013 &nbsp;·&nbsp;
  Coordinate logic verified against HYRCAN 3.0 reference output
</div>
""", unsafe_allow_html=True)
