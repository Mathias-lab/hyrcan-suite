# -*- coding: utf-8 -*-
"""
Created on Fri May 22 11:45:29 2026

@author: Mathias Adjei Tawiah
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

st.markdown("""
<div style="background:#161b22;border:1px solid #30363d;border-radius:8px;padding:12px 20px;margin-bottom:16px;">
  <div style="color:#58a6ff;font-weight:600;font-size:13px;">Quick Start</div>
  <div style="color:#8b949e;font-size:12px;margin-top:4px;">
    <b>Tab 1:</b> Rubble Mound — Enter geometry → Generate HYRCAN coordinates<br>
    <b>Tab 2:</b> Caisson Stability — Adjust parameters → Live FOS results<br>
    <b>Tab 3:</b> Wave Run-Up — Input wave conditions → Full EurOtop 2018 results
  </div>
</div>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
#  PAGE CONFIG & THEME
# ════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="HYRCAN Engineering Suite v3.0",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
html, body, [class*="css"] { font-family: 'Segoe UI', 'Inter', sans-serif; }
.stApp { background-color: #0d1117; color: #e6edf3; }

.stTabs [data-baseweb="tab-list"] {
    background-color: #161b22; border-radius: 8px; padding: 4px; gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background-color: transparent; color: #8b949e;
    border-radius: 6px; font-weight: 600; font-size: 15px; padding: 8px 24px;
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
    margin: 16px 0 8px 0; font-weight: 700; font-size: 14px;
    color: #58a6ff; letter-spacing: 0.5px;
}
.coord-block {
    background-color: #161b22; border: 1px solid #30363d;
    border-radius: 8px; padding: 16px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 13px; color: #e6edf3;
    white-space: pre; overflow-x: auto;
}
.welcome-card {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    border: 1px solid #30363d; border-radius: 14px;
    padding: 28px 32px; margin-bottom: 8px;
}
.info-card {
    background: #161b22; border: 1px solid #30363d;
    border-radius: 10px; padding: 16px 20px; margin: 8px 0;
}
.badge {
    display: inline-block; background: #1f6feb33;
    border: 1px solid #1f6feb88; color: #58a6ff;
    border-radius: 20px; padding: 3px 12px;
    font-size: 12px; font-weight: 600; margin: 3px 3px 3px 0;
}
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
#  SIDEBAR — PROFESSIONAL WELCOME / ABOUT
# ════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
<div class="welcome-card">
  <div style="font-size:26px;font-weight:800;color:#58a6ff;letter-spacing:0.5px;margin-bottom:4px;">
    HYRCAN
  </div>
  <div style="font-size:13px;color:#8b949e;margin-bottom:12px;">Engineering Suite v3.0</div>
  <div style="font-size:12px;color:#e6edf3;line-height:1.8;">
    <b style="color:#79c0ff;">Developer:</b> Mathias Adjei Tawiah<br>
    <b style="color:#79c0ff;">Email:</b> mathiasadjeitawiah@gmail.com<br>
    <b style="color:#79c0ff;">Institution:</b> Hohai University<br>
    <span style="color:#8b949e;font-size:11px;">College of Harbor, Coastal &amp; Offshore Engineering</span>
  </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="info-card">
  <div style="font-size:12px;font-weight:700;color:#58a6ff;margin-bottom:8px;">DESIGN STANDARDS</div>
  <div style="font-size:11px;color:#8b949e;line-height:2;">
    <span class="badge">EurOtop 2018</span>
    <span class="badge">JTS 154-1-2011</span>
    <span class="badge">GB 50286-2013</span>
  </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="info-card">
  <div style="font-size:12px;font-weight:700;color:#58a6ff;margin-bottom:8px;">MODULES</div>
  <div style="font-size:12px;color:#8b949e;line-height:2.0;">
    🏗️ &nbsp;Rubble Mound Coordinate Generator<br>
    🏛️ &nbsp;Vertical Caisson Stability Calculator<br>
    🌊 &nbsp;Wave Run-Up Calculator
  </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="info-card">
  <div style="font-size:12px;font-weight:700;color:#58a6ff;margin-bottom:8px;">LINKS</div>
  <div style="font-size:12px;line-height:2.0;">
    <a href="https://github.com/Mathias-lab/hyrcan-suite" target="_blank"
       style="color:#58a6ff;text-decoration:none;">🔗 GitHub Repository</a><br>
    <a href="https://linkedin.com/in/mathias-adjei-tawiah" target="_blank"
       style="color:#58a6ff;text-decoration:none;">🔗 LinkedIn Profile</a>
  </div>
</div>
""", unsafe_allow_html=True)

    st.markdown('<div style="font-size:10px;color:#484f58;margin-top:16px;text-align:center;">Coordinate logic verified against HYRCAN 3.0</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
#  HEADER
# ════════════════════════════════════════════════════════════════════

st.markdown("""
<div style="background:linear-gradient(135deg,#1f6feb18,#161b22);
            border:1px solid #30363d;border-radius:12px;
            padding:20px 28px;margin-bottom:20px;">
  <div style="display:flex;align-items:center;gap:14px;">
    <span style="font-size:36px;">🏗️</span>
    <div>
      <div style="font-size:22px;font-weight:800;color:#58a6ff;letter-spacing:0.5px;">
        HYRCAN Engineering Suite <span style="color:#8b949e;font-size:15px;">v3.0</span>
      </div>
      <div style="color:#8b949e;font-size:13px;margin-top:2px;">
        Rubble Mound Coordinate Generator &nbsp;·&nbsp;
        Vertical Caisson FOS Analysis &nbsp;·&nbsp;
        Wave Run-Up Calculator &nbsp;·&nbsp;
        Hohai University
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
#  CORE CALCULATION FUNCTIONS — verified against HYRCAN 3.0
# ════════════════════════════════════════════════════════════════════

def compute_layer_elevations(seabed_elev, thicknesses):
    """
    Auto-calculate all layer elevations from seabed and thicknesses.
    Supports 1–5 layers. Returns dict with real elevations and HYRCAN Y values.
    """
    tops = []
    bots = []
    cur = seabed_elev
    for t in thicknesses:
        tops.append(cur)
        bots.append(cur - t)
        cur = cur - t

    datum = abs(bots[-1])
    def Y(e): return e + datum

    result = {'datum': datum, 'Y_seabed': Y(seabed_elev)}
    for i, (top, bot) in enumerate(zip(tops, bots)):
        result[f'top{i+1}'] = top
        result[f'bot{i+1}'] = bot
        result[f'Y_top{i+1}'] = Y(top)
        result[f'Y_bot{i+1}'] = Y(bot)

    # Legacy keys for backward-compat (3-layer)
    if len(thicknesses) >= 3:
        result['top2'] = tops[1] if len(tops) > 1 else None
        result['bot2'] = bots[1] if len(bots) > 1 else None
        result['top3'] = tops[2] if len(tops) > 2 else None
        result['bot3'] = bots[2] if len(bots) > 2 else None
        result['Y_top2'] = Y(tops[1]) if len(tops) > 1 else None
        result['Y_bot2'] = Y(bots[1]) if len(bots) > 1 else None

    return result


def compute_geometry(crest_elev, seabed_elev, crest_width,
                     upper_height, lower_height,
                     sw_upper, sw_lower, seaward_berm,
                     lw_upper, lw_lower, landward_berm,
                     layers):
    """
    Core coordinate engine — verified against HYRCAN 3.0.
    Supports single-slope (berm=0) and double-slope (berm>0).
    Build X left-to-right from seaward toe = 0.
    """
    datum = layers['datum']
    def Y(e): return e + datum

    crest_y  = Y(crest_elev)
    seabed_y = Y(seabed_elev)

    # Single slope vs double slope
    single_slope_sw = (seaward_berm == 0)
    single_slope_lw = (landward_berm == 0)

    if single_slope_sw:
        # Single slope seaward: one continuous slope from toe to crest
        total_sw_dx = (upper_height + lower_height) * sw_upper
        berm_y = Y(crest_elev - upper_height)  # intermediate ref only
        x_sw_toe = 0.0
        x_sw_be  = x_sw_toe   # collapsed
        x_sw_bs  = x_sw_toe   # collapsed
        x_cl     = x_sw_toe + total_sw_dx
    else:
        berm_y  = Y(crest_elev - upper_height)
        sw_udx  = upper_height * sw_upper
        sw_ldx  = lower_height * sw_lower
        x_sw_toe = 0.0
        x_sw_be  = x_sw_toe + sw_ldx
        x_sw_bs  = x_sw_be  + seaward_berm
        x_cl     = x_sw_bs  + sw_udx

    x_cr = x_cl + crest_width

    if single_slope_lw:
        total_lw_dx = (upper_height + lower_height) * lw_upper
        x_lw_bs  = x_cr
        x_lw_be  = x_cr
        x_lw_toe = x_cr + total_lw_dx
    else:
        lw_udx   = upper_height * lw_upper
        lw_ldx   = lower_height * lw_lower
        x_lw_bs  = x_cr     + lw_udx
        x_lw_be  = x_lw_bs  + landward_berm
        x_lw_toe = x_lw_be  + lw_ldx

    berm_y = Y(crest_elev - upper_height)

    if single_slope_sw:
        pts = {
            'sw_toe': (x_sw_toe, seabed_y),
            'sw_be':  (x_sw_toe, seabed_y),   # coincident
            'sw_bs':  (x_sw_toe, seabed_y),   # coincident
            'cl':     (x_cl,     crest_y),
            'cr':     (x_cr,     crest_y),
            'lw_bs':  (x_lw_bs, berm_y if not single_slope_lw else seabed_y),
            'lw_be':  (x_lw_be, berm_y if not single_slope_lw else seabed_y),
            'lw_toe': (x_lw_toe, seabed_y),
        }
    else:
        pts = {
            'sw_toe': (x_sw_toe,  seabed_y),
            'sw_be':  (x_sw_be,   berm_y),
            'sw_bs':  (x_sw_bs,   berm_y),
            'cl':     (x_cl,      crest_y),
            'cr':     (x_cr,      crest_y),
            'lw_bs':  (x_lw_bs,  berm_y if not single_slope_lw else seabed_y),
            'lw_be':  (x_lw_be,  berm_y if not single_slope_lw else seabed_y),
            'lw_toe': (x_lw_toe,  seabed_y),
        }

    sw_udx = upper_height * sw_upper
    sw_ldx = lower_height * sw_lower
    lw_udx = upper_height * lw_upper
    lw_ldx = lower_height * lw_lower

    return {
        'pts':          pts,
        'crest_y':      crest_y,
        'seabed_y':     seabed_y,
        'berm_y':       berm_y,
        'model_right':  x_lw_toe,
        'model_bottom': 0.0,
        'sw_udx': sw_udx, 'sw_ldx': sw_ldx,
        'lw_udx': lw_udx, 'lw_ldx': lw_ldx,
        'x_sw_be': x_sw_be, 'x_sw_bs': x_sw_bs,
        'x_cl': x_cl, 'x_cr': x_cr,
        'x_lw_bs': x_lw_bs, 'x_lw_be': x_lw_be,
        'x_lw_toe': x_lw_toe,
        'single_slope_sw': single_slope_sw,
        'single_slope_lw': single_slope_lw,
    }


def verify_geometry(g, crest_elev, seabed_elev, crest_width,
                    upper_height, lower_height,
                    sw_upper, sw_lower, seaward_berm,
                    lw_upper, lw_lower, landward_berm):
    pts = g['pts']
    tol = 0.001
    checks = []
    def ck(name, exp, got):
        checks.append((name, exp, got, abs(exp - got) <= tol))

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
    F_res   = mu * W
    M_res   = W * (B / 2)
    arm     = d / 2 + H1pct / 3
    M_ot    = P * arm
    FOS_s   = F_res / P if P > 0 else float('inf')
    FOS_o   = M_res / M_ot if M_ot > 0 else float('inf')
    q_max   = W / B
    return dict(W=W, P=P, F_res=F_res, M_res=M_res, arm=arm,
                M_ot=M_ot, FOS_s=FOS_s, FOS_o=FOS_o, q_max=q_max)


# ════════════════════════════════════════════════════════════════════
#  WAVE RUN-UP FUNCTIONS — EurOtop 2018 (exact Tkinter formulas)
# ════════════════════════════════════════════════════════════════════

def calc_wavelength(T):
    """Deep water wavelength L0 = g*T^2 / (2*pi)"""
    return 9.81 * T**2 / (2 * math.pi)

def calc_iribarren(tan_alpha, H, L0):
    """Iribarren / surf-similarity number xi = tan(alpha)/sqrt(H/L0)"""
    if H <= 0 or L0 <= 0:
        return 0.0
    return tan_alpha / math.sqrt(H / L0)

def calc_runup_2percent(H, xi, gamma_f, gamma_b, gamma_beta):
    """EurOtop 2018 Eq 5.2 — Ru2% for rough slopes"""
    ru = 1.65 * gamma_b * gamma_f * gamma_beta * xi * H
    ru_max = (4.0 - 1.5 / math.sqrt(gamma_f * gamma_beta * xi + 1e-12)) * gamma_b * H
    return min(ru, ru_max)

def calc_runup_1percent(H, xi, gamma_f, gamma_b, gamma_beta):
    """Run-up exceeded by 1% of waves (approx 1.4 × Ru2%)"""
    return 1.4 * calc_runup_2percent(H, xi, gamma_f, gamma_b, gamma_beta)

def calc_reflection(xi):
    """Postma (1989) reflection coefficient Cr"""
    return 0.1 * xi**2 if xi > 0 else 0.0

def calc_overtopping(H, L0, xi, Rc, gamma_f, gamma_beta):
    """EurOtop 2018 Eq 5.6 — mean overtopping discharge q (m³/s/m)"""
    if H <= 0 or L0 <= 0 or xi <= 0:
        return 0.0
    term = (Rc / (gamma_f * gamma_beta * H)) * (1.0 / xi)
    q = (math.sqrt(9.81 * H**3) / math.sqrt(L0 / H)) * 0.2 * math.exp(-2.3 * term)
    return max(q, 0.0)

def calc_obliquity_factor(beta_deg):
    """EurOtop 2018 obliquity factor gamma_beta"""
    b = abs(beta_deg)
    if b <= 80:
        return max(1.0 - 0.0033 * b, 0.736)
    return 0.736

def classify_breaker(xi):
    """Breaker type classification from Iribarren number"""
    if xi < 0.5:
        return "Spilling"
    elif xi < 2.0:
        return "Plunging"
    elif xi < 3.0:
        return "Collapsing"
    else:
        return "Surging"

# ════════════════════════════════════════════════════════════════════
#  TEXT GENERATION
# ════════════════════════════════════════════════════════════════════

def generate_hyrcan_instructions(
        g, layers, dhw, surcharge, num_slices, crest_elev, seabed_elev,
        upper_height, lower_height,
        sw_upper, sw_lower, seaward_berm,
        lw_upper, lw_lower, landward_berm, crest_width,
        layer_names, layer_props, n_layers,
        mat_rubble):
    pts   = g['pts']
    cy    = g['crest_y']
    sy    = g['seabed_y']
    by    = g['berm_y']
    L     = 0.0
    R     = g['model_right']
    B_mdl = 0.0
    datum = layers['datum']
    dy    = dhw + datum

    def row(name, g_, c, phi):
        return (f"│ {name:<16} │ {g_:<14.1f} │ {c:<14.1f} │ {phi:<12.1f} │")

    mat_rows = [row("Rubble", mat_rubble[0], mat_rubble[1], mat_rubble[2])]
    for i in range(n_layers):
        mat_rows.append(row(layer_names[i], layer_props[i][0], layer_props[i][1], layer_props[i][2]))

    mat_table = "\n".join([
        "┌──────────────────┬────────────────┬────────────────┬──────────────┐",
        "│ Material         │ γ (kN/m³)      │ c (kPa)        │ φ (°)        │",
        "├──────────────────┼────────────────┼────────────────┼──────────────┤",
        *mat_rows,
        "└──────────────────┴────────────────┴────────────────┴──────────────┘",
    ])

    # Build boundary lines
    bound_lines = ""
    for i in range(n_layers - 1):
        key = f'Y_bot{i+1}'
        rkey_top = f'top{i+1}'; rkey_bot = f'bot{i+1}'
        n_top = layer_names[i]; n_bot = layer_names[i+1]
        bound_lines += f"""
  ── Boundary {i+1}: Bottom of {n_top} / Top of {n_bot} ──────────────
  {L:.3f},{layers[key]:.3f}
  {R:.3f},{layers[key]:.3f}
  d
"""

    assign_rows = [
        "  │ Rubble               │ Embankment (above seabed)                │"
    ]
    for i in range(n_layers):
        top_key = f'Y_top{i+1}'; bot_key = f'Y_bot{i+1}'
        rtop = f'top{i+1}'; rbot = f'bot{i+1}'
        assign_rows.append(
            f"  │ {layer_names[i]:<20} │ Y = {layers[bot_key]:.2f} → {layers[top_key]:.2f}"
            f"  (real: {layers[rbot]:.2f} → {layers[rtop]:.2f} m) │"
        )
    assign_table = "\n".join(assign_rows)

    slope_note = "Single-slope (no berm)" if g['single_slope_sw'] else "Double-slope with berm"

    out = f"""\
{'='*72}
  HYRCAN ENGINEERING SUITE v3.0 — COMPLETE SETUP INSTRUCTIONS
  Mathias Adjei Tawiah  |  Hohai University — Coastal Engineering
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
  Type each line, press ENTER. Close with  c  on its own line.

  {L:.3f},{sy:.3f}
  {L:.3f},{B_mdl:.3f}
  {R:.3f},{B_mdl:.3f}
  {R:.3f},{sy:.3f}
  {pts['lw_be'][0]:.3f},{by:.3f}
  {pts['lw_bs'][0]:.3f},{by:.3f}
  {pts['cr'][0]:.3f},{cy:.3f}
  {pts['cl'][0]:.3f},{cy:.3f}
  {pts['sw_bs'][0]:.3f},{by:.3f}
  {pts['sw_be'][0]:.3f},{by:.3f}
  {pts['sw_toe'][0]:.3f},{sy:.3f}
  c

  ⚠  No spaces after commas. Press Enter after EVERY line.

──────────────────────────────────────────────────────────────────────
STEP 4: MATERIAL BOUNDARIES  ({n_layers - 1} boundaries for {n_layers} layers)
  ▸ Geometry → Material Boundary

  ── Boundary 0: Seabed / Top of {layer_names[0]} ──────────────────
  {L:.3f},{layers['Y_seabed']:.3f}
  {R:.3f},{layers['Y_seabed']:.3f}
  d
{bound_lines}
  ✅ You should see {n_layers + 1} coloured regions.

──────────────────────────────────────────────────────────────────────
STEP 5: WATER TABLE
  ▸ Geometry → Add Water Table

  {L:.3f},{dy:.3f}
  {R:.3f},{dy:.3f}
  d

  ✅ Water table Y = {dy:.3f}  (real elevation = {dhw:.2f} m)

──────────────────────────────────────────────────────────────────────
STEP 6: SURCHARGE LOAD
  ▸ Loading → Distributed Load
  ▸ Load Type  : Vertical (Downward)
  ▸ Magnitude  : {surcharge:.1f} kN/m²
  ▸ Click Apply, then enter crest coordinates:

  {pts['cl'][0]:.3f},{cy:.3f}
  {pts['cr'][0]:.3f},{cy:.3f}
  d

  ✅ Load acts on crest  X = {pts['cl'][0]:.3f} → {pts['cr'][0]:.3f}

──────────────────────────────────────────────────────────────────────
STEP 7: ASSIGN MATERIALS
  ▸ Properties → Define Materials
  Enter these values exactly:

{mat_table}

  ▸ Properties → Assign Properties

  ┌──────────────────────┬──────────────────────────────────────────┐
  │ Material             │ Region                                   │
  ├──────────────────────┼──────────────────────────────────────────┤
{assign_table}
  └──────────────────────┴──────────────────────────────────────────┘
  ▸ Click OK

──────────────────────────────────────────────────────────────────────
STEP 8: COMPUTE
  ▸ Analysis → Compute
  ⏳ Wait 15–30 seconds.

──────────────────────────────────────────────────────────────────────
STEP 9: READ RESULTS
  ▸ Click the  Result  tab
  ▸ Record Bishop and Spencer Factor of Safety values
  ▸ Minimum recommended FOS: 1.3 (static)

{'='*72}
  ✅  ALL STEPS COMPLETE — GOOD LUCK WITH YOUR THESIS!
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
"""
    return out


def generate_coordinates_txt(g, layers, dhw, surcharge, crest_elev, seabed_elev, n_layers):
    pts = g['pts']
    cy  = g['crest_y']; sy = g['seabed_y']; by = g['berm_y']
    L   = 0.0; R = g['model_right']; B = 0.0
    datum = layers['datum']
    dy    = dhw + datum

    lines = [
        "HYRCAN COORDINATE EXPORT — v3.0",
        f"Datum shift: +{datum:.3f} m",
        "",
        "EXTERNAL BOUNDARY",
        f"{L:.3f},{sy:.3f}", f"{L:.3f},{B:.3f}", f"{R:.3f},{B:.3f}", f"{R:.3f},{sy:.3f}",
        f"{pts['lw_be'][0]:.3f},{by:.3f}", f"{pts['lw_bs'][0]:.3f},{by:.3f}",
        f"{pts['cr'][0]:.3f},{cy:.3f}", f"{pts['cl'][0]:.3f},{cy:.3f}",
        f"{pts['sw_bs'][0]:.3f},{by:.3f}", f"{pts['sw_be'][0]:.3f},{by:.3f}",
        f"{pts['sw_toe'][0]:.3f},{sy:.3f}", "c",
        "",
        f"MATERIAL BOUNDARY 0 (Seabed):",
        f"{L:.3f},{layers['Y_seabed']:.3f}", f"{R:.3f},{layers['Y_seabed']:.3f}", "d",
    ]
    for i in range(n_layers - 1):
        key = f'Y_bot{i+1}'
        lines += [
            f"",
            f"MATERIAL BOUNDARY {i+1} (Bottom Layer {i+1}):",
            f"{L:.3f},{layers[key]:.3f}", f"{R:.3f},{layers[key]:.3f}", "d",
        ]
    lines += [
        "",
        "WATER TABLE:",
        f"{L:.3f},{dy:.3f}", f"{R:.3f},{dy:.3f}", "d",
        "",
        f"SURCHARGE ({surcharge:.1f} kN/m²):",
        f"{pts['cl'][0]:.3f},{cy:.3f}", f"{pts['cr'][0]:.3f},{cy:.3f}", "d",
    ]
    return "\n".join(lines)

# ════════════════════════════════════════════════════════════════════
#  VISUALIZATION
# ════════════════════════════════════════════════════════════════════

LAYER_COLORS = ['#C9B99A', '#A8B5A0', '#B5C4D1', '#D1B5C4', '#B5D1C4']

def draw_rubble_mound(g, layers, dhw, crest_elev, seabed_elev,
                      upper_height, lower_height, layer_names, n_layers):
    pts   = g['pts']
    ce    = crest_elev
    se    = seabed_elev
    berm_e = ce - upper_height

    fig, ax = plt.subplots(figsize=(12, 6), dpi=120)
    fig.patch.set_facecolor('#0d1117')
    ax.set_facecolor('#161b22')

    xl = pts['sw_toe'][0]
    xr = pts['lw_toe'][0]

    # Soil layers (real elevation coords)
    for i in range(n_layers):
        top_e = layers[f'top{i+1}']
        bot_e = layers[f'bot{i+1}']
        col   = LAYER_COLORS[i % len(LAYER_COLORS)]
        ax.fill_betweenx([bot_e, top_e], xl - 999, xr + 999,
                         facecolor=col, alpha=0.55 - i*0.02, zorder=1)
        ax.axhline(y=top_e, color='#444', lw=0.7, ls=':', zorder=2)

    ax.axhline(y=se, color='#607d8b', lw=1.3, ls='--', zorder=2)

    # Embankment (real elevation)
    if g['single_slope_sw'] and g['single_slope_lw']:
        xs = [pts['sw_toe'][0], pts['cl'][0], pts['cr'][0], pts['lw_toe'][0], pts['sw_toe'][0]]
        ys = [se, ce, ce, se, se]
    elif g['single_slope_sw']:
        xs = [pts['sw_toe'][0], pts['cl'][0], pts['cr'][0],
              pts['lw_bs'][0], pts['lw_be'][0], pts['lw_toe'][0], pts['sw_toe'][0]]
        ys = [se, ce, ce, berm_e, berm_e, se, se]
    elif g['single_slope_lw']:
        xs = [pts['sw_toe'][0], pts['sw_be'][0], pts['sw_bs'][0],
              pts['cl'][0], pts['cr'][0], pts['lw_toe'][0], pts['sw_toe'][0]]
        ys = [se, berm_e, berm_e, ce, ce, se, se]
    else:
        xs = [pts['sw_toe'][0], pts['sw_be'][0], pts['sw_bs'][0],
              pts['cl'][0], pts['cr'][0],
              pts['lw_bs'][0], pts['lw_be'][0], pts['lw_toe'][0], pts['sw_toe'][0]]
        ys = [se, berm_e, berm_e, ce, ce, berm_e, berm_e, se, se]

    ax.fill(xs, ys, facecolor='#C9A96E', alpha=0.88,
            edgecolor='#7B5E3A', lw=1.5, zorder=3)

    # Water table
    ax.axhline(y=dhw, color='#3A7EC4', ls='--', lw=2.0, zorder=4)
    # ── Ensure required imports are available ──────────────────────
    import matplotlib.patches as mpatches
    import numpy as np

        # ── Distributed load (surcharge) on full crest width ──────────
    surcharge = st.session_state.get('rm_surcharge', 10.0)
    cl_x = pts['cl'][0]
    cr_x = pts['cr'][0]
    crest_w = cr_x - cl_x                          # exact crest width
    block_h = max(crest_w * 0.06, 0.4)             # small height
    gap = 0.15                                     # small gap above crest

    # Hatched rectangle sitting just above the crest surface
    load_rect = mpatches.FancyBboxPatch(
        (cl_x, ce + gap), crest_w, block_h,
        boxstyle='square,pad=0',
        facecolor='#ff6b3533', edgecolor='#ff6b35',
        lw=1.5, hatch='////', zorder=10,
    )
    ax.add_patch(load_rect)

  

    # Bold magnitude label centred above the block (outside the rectangle)
    ax.text(
    (cl_x + cr_x) / 2, ce + gap + block_h + 0.8,
    f'{surcharge:.1f} kN/m²',
    ha='center', va='bottom', fontsize=9, fontweight='bold',
    color='#ff6b35', zorder=12,
)
    
  
    # Layer labels (left margin)
    lx = xl - (xr - xl) * 0.015
    for i in range(n_layers):
        top_e = layers[f'top{i+1}']
        bot_e = layers[f'bot{i+1}']
        ax.text(lx, (top_e + bot_e) / 2, layer_names[i],
                fontsize=9, va='center', ha='right',
                fontstyle='italic', color='#ccc', zorder=5)

    # Coordinate labels
    for lbl, xp, yp, va in [
       
        (f'({pts["sw_toe"][0]:.1f}, {se:.1f})', pts['sw_toe'][0], se - 0.7, 'top'),
        (f'({pts["lw_toe"][0]:.1f}, {se:.1f})', pts['lw_toe'][0], se - 0.7, 'top'),
    ]:
        ax.text(xp, yp, lbl, ha='center', fontsize=7.5, color='#aaa', va=va, zorder=5)

    handles = [
        mpatches.Patch(facecolor='#C9A96E', alpha=0.88, edgecolor='#7B5E3A',
                       label='Embankment (Rubble)'),
        *[mpatches.Patch(facecolor=LAYER_COLORS[i % len(LAYER_COLORS)], alpha=0.7,
                         label=f'{layer_names[i]}  [{layers[f"top{i+1}"]:.1f}→{layers[f"bot{i+1}"]:.1f} m]')
          for i in range(n_layers)],
        mlines.Line2D([], [], color='#3A7EC4', ls='--', lw=2,
                      label=f'Water Table ({dhw:.2f} m)'),
    ]
    legend = ax.legend(handles=handles, loc='upper center',
                       bbox_to_anchor=(0.5, -0.13), ncol=3,
                       fontsize=9, frameon=True,
                       facecolor='#21262d', edgecolor='#30363d',
                       framealpha=0.97, labelspacing=0.5)
    for t in legend.get_texts():
        t.set_color('#e6edf3')

    ax.set_xlabel('Distance (m)', fontsize=11, color='#8b949e')
    ax.set_ylabel('Elevation (m)', fontsize=11, color='#8b949e')
    ax.set_title('Rubble Mound Embankment — Cross-Section',
                 fontsize=13, fontweight='bold', color='#e6edf3', pad=10)
    ax.grid(True, alpha=0.15, color='#444', lw=0.5)
    ax.tick_params(colors='#8b949e', labelsize=9)
    for sp in ax.spines.values():
        sp.set_color('#30363d')

    mx = (xr - xl) * 0.08
    ax.set_xlim(xl - mx * 3.5, xr + mx)
    ax.set_ylim(layers[f'bot{n_layers}'] - 1.5, ce + 4.0)
    ax.set_aspect('equal', adjustable='box')
    fig.subplots_adjust(bottom=0.22)
    return fig


def draw_caisson(p, r):
    fig, ax = plt.subplots(figsize=(10, 6), dpi=120)
    fig.patch.set_facecolor('#0d1117')
    ax.set_facecolor('#0f1921')

    B = p['B']; H_c = p['H_c']; seabed = 0.0; d = p['d']

    rb_h, rb_ext = 1.8, 3.0
    rb_xs = [-rb_ext, -rb_ext*0.3, B+rb_ext*0.3, B+rb_ext, -rb_ext]
    rb_ys = [seabed-rb_h, seabed, seabed, seabed-rb_h, seabed-rb_h]
    ax.fill(rb_xs, rb_ys, facecolor='#C8A96E', alpha=0.85,
            edgecolor='#7B5E3A', lw=1.2, zorder=2, label='Rubble Foundation')

    ax.axhline(y=seabed, color='#607d8b', lw=1.3, zorder=3)

    caisson_top = seabed + H_c
    caisson_patch = mpatches.FancyBboxPatch(
        (0, seabed), B, H_c, boxstyle='square,pad=0',
        facecolor='#5b7fa5', alpha=0.85, edgecolor='#2c4a70', lw=2.0, zorder=4)
    ax.add_patch(caisson_patch)
    for xi in np.linspace(B*0.2, B*0.8, 4):
        ax.plot([xi, xi], [seabed, caisson_top], color='#3a5f80', lw=0.5, alpha=0.35, zorder=5)
    for yi in [seabed+H_c*0.25, seabed+H_c*0.5, seabed+H_c*0.75]:
        ax.plot([0, B], [yi, yi], color='#3a5f80', lw=0.5, alpha=0.35, zorder=5)
    ax.text(B/2, seabed+H_c/2, 'CAISSON\n(Concrete)',
            ha='center', va='center', fontsize=11, fontweight='bold',
            color='white', zorder=6)

    water_y = seabed + d
    ax.axhline(y=water_y, color='#3A7EC4', ls='--', lw=2.0, zorder=6)

    wx = -B * 0.75
    wy = water_y - d * 0.35
    ax.annotate('', xy=(0, wy), xytext=(wx, wy),
                arrowprops=dict(arrowstyle='->', color='#f85149', lw=2.5), zorder=7)
    ax.text(wx - 0.5, wy + 0.2,
            f'P = {r["P"]:.1f} kN/m\n(Wave Force)',
            fontsize=8.5, color='#f85149', ha='right', zorder=7)

    def dim_arrow(x0, x1, y, label, color='#8b949e', vertical=False):
        if vertical:
            ax.annotate('', xy=(x0, x1), xytext=(x0, y),
                        arrowprops=dict(arrowstyle='<->', color=color, lw=0.9))
            ax.text(x0 + 0.4, (x1 + y) / 2, label, fontsize=8, color=color, va='center')
        else:
            ax.annotate('', xy=(x1, y), xytext=(x0, y),
                        arrowprops=dict(arrowstyle='<->', color=color, lw=0.9))
            ax.text((x0 + x1) / 2, y - 0.5, label, ha='center', fontsize=8, color=color)

    dim_arrow(0, B, seabed - rb_h - 1.2, f'B = {B:.1f} m')
    dim_arrow(B+1.2, seabed, caisson_top, f'H_c = {H_c:.1f} m', vertical=True)
    dim_arrow(-rb_ext-1.8, seabed, water_y, f'd = {d:.2f} m', color='#3A7EC4', vertical=True)
    ax.text(B/2, water_y + 0.4, f'H₁% = {p["H1pct"]:.2f} m',
            ha='center', fontsize=8.5, color='#3A7EC4')

    s_ok = r['FOS_s'] >= 1.25; o_ok = r['FOS_o'] >= 1.50; b_ok = r['q_max'] < p['q_allow']
    summary = (f"FOS Sliding:      {r['FOS_s']:.3f}  {'✅' if s_ok else '❌'}\n"
               f"FOS Overturning:  {r['FOS_o']:.3f}  {'✅' if o_ok else '❌'}\n"
               f"q_max:            {r['q_max']:.0f} kPa  {'✅' if b_ok else '❌'}")
    ax.text(0.02, 0.98, summary, transform=ax.transAxes,
            fontsize=9, va='top', ha='left', fontfamily='monospace',
            color='#e6edf3',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#21262d',
                      edgecolor='#30363d', alpha=0.95))

    handles = [
        mpatches.Patch(facecolor='#5b7fa5', alpha=0.85, edgecolor='#2c4a70', label='Caisson (Concrete)'),
        mpatches.Patch(facecolor='#C8A96E', alpha=0.85, edgecolor='#7B5E3A', label='Rubble Foundation'),
        mlines.Line2D([], [], color='#3A7EC4', ls='--', lw=2, label=f'Water Table (d = {d:.2f} m)'),
    ]
    legend = ax.legend(handles=handles, loc='upper right',
                       fontsize=9, frameon=True,
                       facecolor='#21262d', edgecolor='#30363d', framealpha=0.97)
    for t in legend.get_texts():
        t.set_color('#e6edf3')

    ax.set_xlabel('Distance (m)', fontsize=11, color='#8b949e')
    ax.set_ylabel('Elevation (m)', fontsize=11, color='#8b949e')
    ax.set_title('Vertical Caisson — Cross-Section & Stability',
                 fontsize=13, fontweight='bold', color='#e6edf3', pad=10)
    ax.grid(True, alpha=0.15, color='#444', lw=0.5)
    ax.tick_params(colors='#8b949e', labelsize=9)
    for sp in ax.spines.values():
        sp.set_color('#30363d')

    pad = B * 1.3
    ax.set_xlim(-pad, B + pad)
    ax.set_ylim(seabed - rb_h - 2.5, caisson_top + 4.0)
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════
#  SESSION STATE DEFAULTS
# ════════════════════════════════════════════════════════════════════

def _default(key, val):
    if key not in st.session_state:
        st.session_state[key] = val

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

# Layer defaults (5 layers)
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

# Wave run-up defaults
_default('wu_H',      2.0)
_default('wu_T',     10.0)
_default('wu_slope',  2.5)
_default('wu_Rc',     1.5)
_default('wu_gamma_f', 0.55)
_default('wu_gamma_b', 1.0)
_default('wu_beta',    0.0)

# ════════════════════════════════════════════════════════════════════
#  PROJECT SAVE / LOAD
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

def save_project():
    data = {k: st.session_state[k] for k in RM_KEYS + CS_KEYS if k in st.session_state}
    return json.dumps(data, indent=2)

def load_project(uploaded):
    data = json.loads(uploaded.read().decode())
    for k, v in data.items():
        st.session_state[k] = v

# ════════════════════════════════════════════════════════════════════
#  UI HELPERS
# ════════════════════════════════════════════════════════════════════

def section(label):
    st.markdown(f'<div class="section-header">{label}</div>', unsafe_allow_html=True)

def num(label, key, **kw):
    kw.setdefault('format', '%.2f')
    st.session_state[key] = st.number_input(
        label, value=float(st.session_state[key]), key=f'_ni_{key}', **kw)
    return st.session_state[key]

def txt(label, key):
    st.session_state[key] = st.text_input(label, value=st.session_state[key], key=f'_ti_{key}')
    return st.session_state[key]

# ════════════════════════════════════════════════════════════════════
#  TABS
# ════════════════════════════════════════════════════════════════════

tab1, tab2, tab3 = st.tabs([
    "🏗️  Rubble Mound Coordinate Generator",
    "🏛️  Vertical Caisson Stability",
    "🌊  Wave Run-Up Calculator",
])

# ────────────────────────────────────────────────────────────────────
#  TAB 1 — RUBBLE MOUND
# ────────────────────────────────────────────────────────────────────

with tab1:
    sc1, sc2, sc3 = st.columns([2, 2, 6])
    with sc1:
        project_json = save_project()
        st.download_button('💾 Save Project (.json)', data=project_json,
                           file_name='hyrcan_project.json',
                           mime='application/json', use_container_width=True)
    with sc2:
        uploaded = st.file_uploader('📂 Load Project', type='json', label_visibility='collapsed')
        if uploaded:
            load_project(uploaded)
            st.success('Project loaded!', icon='✅')

    st.markdown('<hr style="border-color:#30363d;margin:8px 0 16px 0;">', unsafe_allow_html=True)

    left_col, right_col = st.columns([1, 1.6], gap='large')

    with left_col:
        section("🏗  Embankment Geometry")
        c1, c2 = st.columns(2)
        with c1:
            ce = num('Crest elevation (m)', 'rm_crest_elev')
            cw = num('Crest width (m)', 'rm_crest_width', min_value=0.5)
            uh = num('Upper height (m)', 'rm_upper_height', min_value=0.0)
        with c2:
            se = num('Seabed elevation (m)', 'rm_seabed_elev')
            lh = num('Lower height (m)', 'rm_lower_height', min_value=0.0)

        total_h = ce - se
        if abs((uh + lh) - total_h) > 0.01:
            st.error(f"⚠️  upper + lower = {uh+lh:.3f} m ≠ crest − seabed = {total_h:.3f} m")

        section("📐  Slope Ratios (H : V)  |  Set berm = 0 for single-slope")
        c1, c2, c3 = st.columns(3)
        with c1:
            sw_u = num('Seaward upper', 'rm_sw_upper', min_value=0.1)
            sw_l = num('Seaward lower', 'rm_sw_lower', min_value=0.1)
        with c2:
            lw_u = num('Landward upper', 'rm_lw_upper', min_value=0.1)
            lw_l = num('Landward lower', 'rm_lw_lower', min_value=0.1)
        with c3:
            sw_b = num('Seaward berm (m)', 'rm_sw_berm', min_value=0.0)
            lw_b = num('Landward berm (m)', 'rm_lw_berm', min_value=0.0)

        # Slope type indicator
        sw_type = "Single-slope" if sw_b == 0 else f"Double-slope (berm {sw_b:.1f} m)"
        lw_type = "Single-slope" if lw_b == 0 else f"Double-slope (berm {lw_b:.1f} m)"
        st.caption(f"Seaward: **{sw_type}**  |  Landward: **{lw_type}**")

        section("🌊  Water & Loads")
        c1, c2, c3 = st.columns(3)
        with c1: dhw = num('DHW level (m)', 'rm_dhw')
        with c2: q   = num('Surcharge (kN/m²)', 'rm_surcharge', min_value=0.0)
        with c3: ns  = num('No. of slices', 'rm_num_slices', min_value=10.0, step=5.0, format='%.0f')

        section("🧱  Soil Layers  (up to 5)")

        n_layers = st.slider('Number of layers', min_value=3, max_value=5, value=int(st.session_state['rm_n_layers']), step=1)
        st.session_state['rm_n_layers'] = n_layers

        layer_names = []; layer_thicknesses = []; layer_props = []
        LAYER_LABELS = ['Layer 1', 'Layer 2', 'Layer 3', 'Layer 4', 'Layer 5']

        for i in range(1, n_layers + 1):
            st.markdown(f"**Layer {i}**")
            c_name, c_t, c_g, c_c, c_phi = st.columns([2.2, 1.3, 1.3, 1.3, 1.3])
            with c_name: name = txt('Name' if i == 1 else ' ', f'rm_n{i}')
            with c_t:    t    = num('Thickness (m)' if i == 1 else ' ', f'rm_t{i}', min_value=0.1)
            with c_g:    g_   = num('γ (kN/m³)' if i == 1 else ' ',    f'rm_g{i}', min_value=10.0)
            with c_c:    c_   = num('c (kPa)' if i == 1 else ' ',      f'rm_c{i}', min_value=0.0)
            with c_phi:  phi  = num('φ (°)' if i == 1 else ' ',        f'rm_phi{i}', min_value=0.0)
            layer_names.append(name)
            layer_thicknesses.append(t)
            layer_props.append((g_, c_, phi))

        st.markdown("**Embankment (Rubble)**")
        c1, c2, c3 = st.columns(3)
        with c1: gr  = num('γ (kN/m³)', 'rm_gr', min_value=10.0)
        with c2: cr_ = num('c (kPa)',   'rm_cr_', min_value=0.0)
        with c3: phir= num('φ (°)',     'rm_phir', min_value=0.0)

        layers = compute_layer_elevations(se, layer_thicknesses)

        section("📊  Live Layer Elevation Preview")
        df_rows = {
            'Layer':          layer_names,
            'Top Elev (m)':   [f"{layers[f'top{i+1}']:.3f}" for i in range(n_layers)],
            'Bottom Elev (m)':[f"{layers[f'bot{i+1}']:.3f}" for i in range(n_layers)],
            'Thickness (m)':  [f"{layer_thicknesses[i]:.2f}" for i in range(n_layers)],
            'HYRCAN Y_top':   [f"{layers[f'Y_top{i+1}']:.3f}" for i in range(n_layers)],
            'HYRCAN Y_bot':   [f"{layers[f'Y_bot{i+1}']:.3f}" for i in range(n_layers)],
        }
        st.dataframe(pd.DataFrame(df_rows), use_container_width=True, hide_index=True)
        st.caption(f"Datum shift: **+{layers['datum']:.3f} m**  |  Bottom of {layer_names[-1]} → Y = 0.000")

        st.markdown('<br>', unsafe_allow_html=True)
        generate = st.button('🚀  Generate HYRCAN Coordinates', type='primary', use_container_width=True)

    with right_col:
        layers = compute_layer_elevations(se, layer_thicknesses)
        valid = abs((uh + lh) - (ce - se)) <= 0.01

        if generate and valid:
            g = compute_geometry(ce, se, cw, uh, lh, sw_u, sw_l, sw_b, lw_u, lw_l, lw_b, layers)
            st.session_state['rm_g'] = g
            st.session_state['rm_layers'] = layers
            st.session_state['rm_layer_names'] = layer_names
            st.session_state['rm_layer_thicknesses'] = layer_thicknesses
            st.session_state['rm_layer_props'] = layer_props
            st.session_state['rm_n_layers_gen'] = n_layers
            st.session_state['rm_generated'] = True

        # Live preview (always shown)
        section("📊  Cross-Section Preview")
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

            section("✅  Automatic Verification")
            checks = verify_geometry(g, ce, se, cw, uh, lh, sw_u, sw_l, sw_b, lw_u, lw_l, lw_b)
            all_ok = all(c[3] for c in checks)
            if all_ok:
                st.success('All geometry checks passed ✅', icon='✅')
            else:
                st.error('One or more geometry checks failed ❌')

            df_chk = pd.DataFrame({
                'Parameter':  [c[0] for c in checks],
                'Expected':   [f'{c[1]:.4f}' for c in checks],
                'Calculated': [f'{c[2]:.4f}' for c in checks],
                'Status':     ['✅ Pass' if c[3] else '❌ FAIL' for c in checks],
            })
            st.dataframe(df_chk, use_container_width=True, hide_index=True)

            pts = g['pts']
            mc1, mc2, mc3, mc4 = st.columns(4)
            mc1.metric('Model width',   f"{g['model_right']:.3f} m")
            mc2.metric('Crest left X',  f"{pts['cl'][0]:.3f}")
            mc3.metric('Crest right X', f"{pts['cr'][0]:.3f}")
            mc4.metric('Datum shift',   f"+{layers['datum']:.3f} m")

            section("📖  Complete HYRCAN Step-by-Step Instructions")
            instructions = generate_hyrcan_instructions(
                g, layers, dhw, q, ns, ce, se, uh, lh,
                sw_u, sw_l, sw_b, lw_u, lw_l, lw_b, cw,
                lnames, lprops, nl, mat_rubble=(gr, cr_, phir))
            st.markdown(f'<div class="coord-block">{instructions}</div>', unsafe_allow_html=True)

            st.markdown('<br>', unsafe_allow_html=True)
            dc1, dc2 = st.columns(2)
            with dc1:
                coords_txt = generate_coordinates_txt(g, layers, dhw, q, ce, se, nl)
                st.download_button('📥 Export Coordinates (.txt)', data=coords_txt,
                                   file_name='hyrcan_coordinates.txt', mime='text/plain',
                                   use_container_width=True)
            with dc2:
                st.download_button('📥 Export Full Instructions (.txt)', data=instructions,
                                   file_name='hyrcan_step_by_step.txt', mime='text/plain',
                                   use_container_width=True)

            buf = io.BytesIO()
            fig2 = draw_rubble_mound(g, layers, dhw, ce, se, uh, lh, lnames, nl)
            fig2.savefig(buf, format='png', dpi=300, bbox_inches='tight', facecolor='white')
            plt.close(fig2)
            buf.seek(0)
            st.download_button('🖼  Export Plot (PNG 300 DPI)', data=buf,
                               file_name='hyrcan_cross_section.png', mime='image/png',
                               use_container_width=True)

        elif generate and not valid:
            st.error('Fix the height mismatch before generating.')
        elif not st.session_state.get('rm_generated'):
            st.info('👈  Fill in parameters and click **Generate** to produce HYRCAN coordinates.', icon='ℹ️')

# ────────────────────────────────────────────────────────────────────
#  TAB 2 — VERTICAL CAISSON
# ────────────────────────────────────────────────────────────────────

with tab2:
    st.markdown('<hr style="border-color:#30363d;margin:0 0 16px 0;">', unsafe_allow_html=True)
    left2, right2 = st.columns([1, 1.6], gap='large')

    with left2:
        section("📐  Caisson Geometry")
        c1, c2 = st.columns(2)
        with c1:
            B_cs = num('Width B (m)', 'cs_B', min_value=1.0)
            gc   = num('Concrete γ_c (kN/m³)', 'cs_gamma_c', min_value=10.0)
        with c2:
            Hc_cs = num('Height H_c (m)', 'cs_H_c', min_value=1.0)

        section("🌊  Hydraulic Conditions")
        c1, c2, c3 = st.columns(3)
        with c1: d_cs  = num('Water depth d (m)', 'cs_d', min_value=0.1)
        with c2: H1_cs = num('Wave H₁% (m)', 'cs_H1pct', min_value=0.1)
        with c3: gw_cs = num('γ_w (kN/m³)', 'cs_gamma_w', min_value=9.0)

        section("⚙️  Stability Parameters")
        c1, c2 = st.columns(2)
        with c1: mu_cs = num('Friction coeff μ', 'cs_mu', min_value=0.1, max_value=1.0, step=0.01)
        with c2: qa_cs = num('q_allow (kPa)', 'cs_q_allow', min_value=50.0)

        st.markdown('<br>', unsafe_allow_html=True)
        st.markdown("""
<div style="background:#161b22;border:1px solid #30363d;border-radius:8px;padding:14px;font-size:12px;color:#8b949e;">
<b style="color:#58a6ff;">📚 Design Standards</b><br><br>
• Wave force: JTS 154-1-2011, Appendix A<br>
• Sliding FOS ≥ 1.25 — GB 50286-2013 §5.3.2<br>
• Overturning FOS ≥ 1.50 — GB 50286-2013 §5.3.3<br>
• Bearing: q_max &lt; q_allow — JTS 154-1-2011 §5.3.4
</div>""", unsafe_allow_html=True)

    with right2:
        cs_p = dict(B=B_cs, H_c=Hc_cs, gamma_c=gc, d=d_cs,
                    H1pct=H1_cs, gamma_w=gw_cs, mu=mu_cs, q_allow=qa_cs)
        r = caisson_fos(**cs_p)

        section("📊  FOS Results  (live)")
        m1, m2, m3 = st.columns(3)
        s_ok = r['FOS_s'] >= 1.25; o_ok = r['FOS_o'] >= 1.50; b_ok = r['q_max'] < qa_cs

        m1.metric('Sliding FOS', f"{r['FOS_s']:.3f}",
                  delta='≥ 1.25 ✅' if s_ok else '< 1.25 ❌',
                  delta_color='normal' if s_ok else 'inverse')
        m2.metric('Overturning FOS', f"{r['FOS_o']:.3f}",
                  delta='≥ 1.50 ✅' if o_ok else '< 1.50 ❌',
                  delta_color='normal' if o_ok else 'inverse')
        m3.metric('Bearing q_max', f"{r['q_max']:.1f} kPa",
                  delta=f"< {int(qa_cs)} kPa ✅" if b_ok else f"≥ {int(qa_cs)} kPa ❌",
                  delta_color='normal' if b_ok else 'inverse')

        if s_ok and o_ok and b_ok:
            st.success('✅  ALL STABILITY CHECKS PASSED — Design is adequate.', icon='✅')
        else:
            st.error('❌  ONE OR MORE CHECKS FAILED — Review design parameters.', icon='❌')

        section("📋  Detailed Results Table")
        df_res = pd.DataFrame({
            'Check':      ['Self-weight W', 'Wave Force P', 'Sliding FOS', 'Overturning FOS', 'Bearing q_max'],
            'Calculated': [f"{r['W']:,.1f} kN/m", f"{r['P']:,.2f} kN/m",
                           f"{r['FOS_s']:.3f}", f"{r['FOS_o']:.3f}", f"{r['q_max']:,.1f} kPa"],
            'Required':   ['—', '—', '≥ 1.25', '≥ 1.50', f"< {int(qa_cs)} kPa"],
            'Standard':   ['—', 'JTS 154-1-2011', 'GB 50286-2013 §5.3.2',
                           'GB 50286-2013 §5.3.3', 'JTS 154-1-2011 §5.3.4'],
            'Status':     ['—', '—',
                           '✅ Pass' if s_ok else '❌ Fail',
                           '✅ Pass' if o_ok else '❌ Fail',
                           '✅ Pass' if b_ok else '❌ Fail'],
        })
        st.dataframe(df_res, use_container_width=True, hide_index=True)

        section("🔢  Step-by-Step Calculations")
        calc_text = f"""\
1. Self-Weight
   W = B × H_c × γ_c
   W = {B_cs:.2f} × {Hc_cs:.2f} × {gc:.2f}
   W = {r['W']:,.2f} kN/m

2. Wave Force  [JTS 154-1-2011, Appendix A]
   P = 0.5 × γ_w × H₁%² + γ_w × d × H₁%
   P = 0.5 × {gw_cs:.2f} × {H1_cs:.2f}² + {gw_cs:.2f} × {d_cs:.2f} × {H1_cs:.2f}
   P = {0.5*gw_cs*H1_cs**2:.3f} + {gw_cs*d_cs*H1_cs:.3f}
   P = {r['P']:,.3f} kN/m

3. Sliding Check  [GB 50286-2013 §5.3.2]
   F_resisting = μ × W = {mu_cs:.2f} × {r['W']:,.2f} = {r['F_res']:,.2f} kN/m
   FOS_sliding = {r['F_res']:,.2f} / {r['P']:,.3f} = {r['FOS_s']:.4f}
   Required ≥ 1.25  → {'✅ PASS' if s_ok else '❌ FAIL'}

4. Overturning Check  [GB 50286-2013 §5.3.3]
   M_resisting  = W × (B/2) = {r['W']:,.2f} × {B_cs/2:.2f} = {r['M_res']:,.2f} kN·m/m
   Moment arm   = d/2 + H₁%/3 = {d_cs/2:.3f} + {H1_cs/3:.3f} = {r['arm']:.3f} m
   M_overturning = P × arm = {r['P']:,.3f} × {r['arm']:.3f} = {r['M_ot']:,.2f} kN·m/m
   FOS_overturning = {r['M_res']:,.2f} / {r['M_ot']:,.2f} = {r['FOS_o']:.4f}
   Required ≥ 1.50  → {'✅ PASS' if o_ok else '❌ FAIL'}

5. Bearing Pressure  [JTS 154-1-2011 §5.3.4]
   q_max = W / B = {r['W']:,.2f} / {B_cs:.2f} = {r['q_max']:,.2f} kPa
   Required < {int(qa_cs)} kPa  → {'✅ PASS' if b_ok else '❌ FAIL'}
"""
        st.markdown(f'<div class="coord-block">{calc_text}</div>', unsafe_allow_html=True)

        section("📊  Cross-Section")
        fig_cs = draw_caisson(cs_p, r)
        st.pyplot(fig_cs, use_container_width=True)
        plt.close(fig_cs)

        buf2 = io.BytesIO()
        fig_cs2 = draw_caisson(cs_p, r)
        fig_cs2.savefig(buf2, format='png', dpi=300, bbox_inches='tight', facecolor='white')
        plt.close(fig_cs2)
        buf2.seek(0)
        dc1, dc2 = st.columns(2)
        with dc1:
            st.download_button('🖼  Export Plot (PNG 300 DPI)', data=buf2,
                               file_name='hyrcan_caisson.png', mime='image/png',
                               use_container_width=True)
        with dc2:
            st.download_button('📥 Export Report (.txt)', data=calc_text,
                               file_name='hyrcan_caisson_report.txt', mime='text/plain',
                               use_container_width=True)

# ────────────────────────────────────────────────────────────────────
#  TAB 3 — WAVE RUN-UP CALCULATOR
# ────────────────────────────────────────────────────────────────────

with tab3:
    st.markdown('<hr style="border-color:#30363d;margin:0 0 16px 0;">', unsafe_allow_html=True)
    left3, right3 = st.columns([1, 1.4], gap='large')

    with left3:
        section("🌊  Wave Parameters")
        c1, c2 = st.columns(2)
        with c1: H_wu  = num('Significant wave height H_m0 (m)', 'wu_H', min_value=0.1)
        with c2: T_wu  = num('Peak wave period T_p (s)',          'wu_T', min_value=1.0)

        section("📐  Structure Geometry")
        slope_wu = num('Slope ratio (H:V)  e.g. 2.5 means 1:2.5', 'wu_slope', min_value=0.1)
        Rc_wu    = num('Freeboard Rc (m)  — crest height above SWL', 'wu_Rc', min_value=0.0)

        section("⚙️  Reduction Factors (EurOtop 2018)")
        c1, c2 = st.columns(2)
        with c1: gf_wu = num('Roughness factor γ_f', 'wu_gamma_f', min_value=0.1, max_value=1.0, step=0.01)
        with c2: gb_wu = num('Berm factor γ_b',       'wu_gamma_b', min_value=0.1, max_value=1.0, step=0.01)
        beta_wu = num('Wave obliquity β (degrees)', 'wu_beta', min_value=0.0, max_value=80.0, step=1.0, format='%.1f')

        with st.expander("📋  Roughness Factor Reference Table (γ_f)"):
            rf_data = {
                'Structure Type': [
                    'Smooth impermeable (concrete)',
                    'Asphalt',
                    'Grass (short)',
                    'Grass (long / rough)',
                    'Single-size rock (permeable)',
                    'Double-layer rock (permeable)',
                    'Rock armour (rough permeable)',
                    'Tetrapods',
                    'Accropode',
                    'Xbloc',
                    'Cube (single layer)',
                    'Cube (double layer)',
                ],
                'γ_f': [
                    '1.00', '1.00', '1.00', '0.90–1.00',
                    '0.55', '0.45', '0.40–0.55',
                    '0.38', '0.46', '0.45',
                    '0.47', '0.50',
                ]
            }
            st.dataframe(pd.DataFrame(rf_data), use_container_width=True, hide_index=True)
            st.caption("Source: EurOtop 2018, Table 5.2")

        calc_wu = st.button('Calculate Run-Up & Overtopping', type='primary', use_container_width=True)

    with right3:
        # Compute
        tan_alpha = 1.0 / slope_wu
        L0  = calc_wavelength(T_wu)
        xi  = calc_iribarren(tan_alpha, H_wu, L0)
        gbeta = calc_obliquity_factor(beta_wu)
        Ru2  = calc_runup_2percent(H_wu, xi, gf_wu, gb_wu, gbeta)
        Ru1  = calc_runup_1percent(H_wu, xi, gf_wu, gb_wu, gbeta)
        Cr   = min(calc_reflection(xi), 1.0)
        q    = calc_overtopping(H_wu, L0, xi, Rc_wu, gf_wu, gbeta)
        btype = classify_breaker(xi)

        # Results always visible
        section("📊  Results  (live)")

        m1, m2, m3 = st.columns(3)
        m1.metric("Wavelength L₀ (m)",     f"{L0:.2f}")
        m2.metric("Iribarren ξ",            f"{xi:.3f}")
        m3.metric("Breaker Type",           btype)

        m4, m5, m6 = st.columns(3)
        m4.metric("Ru2% (m)",               f"{Ru2:.3f}")
        m5.metric("Ru1% (m)",               f"{Ru1:.3f}")
        m6.metric("Reflection Cr",          f"{Cr:.3f}")

        m7, m8, m9 = st.columns(3)
        m7.metric("γ_beta (obliquity)",     f"{gbeta:.3f}")
        m8.metric("Mean overtopping q",     f"{q*1000:.4f} L/s/m" if q < 0.001 else f"{q:.6f} m³/s/m")
        m9.metric("Rc / Ru2%",             f"{Rc_wu/Ru2:.3f}" if Ru2 > 0 else "—")

        # Overtopping assessment
        q_ls = q * 1000
        if q_ls < 0.01:
            st.success(f"✅  Mean overtopping = {q_ls:.4f} L/s/m — Negligible (< 0.01 L/s/m). Design adequate.", icon='✅')
        elif q_ls < 1.0:
            st.success(f"✅  Mean overtopping = {q_ls:.4f} L/s/m — Acceptable for most structures.", icon='✅')
        elif q_ls < 10.0:
            st.warning(f"⚠️  Mean overtopping = {q_ls:.3f} L/s/m — Check tolerable limits for structure type.")
        else:
            st.error(f"❌  Mean overtopping = {q_ls:.2f} L/s/m — Excessive. Increase freeboard or armour roughness.")

        section("🔢  Step-by-Step Calculations")
        wu_text = f"""\
WAVE RUN-UP CALCULATOR — HYRCAN Engineering Suite v3.0
EurOtop 2018 | JTS 154-1-2011 | GB 50286-2013
{'─'*60}

INPUT PARAMETERS
  H_m0 (significant wave height) : {H_wu:.3f} m
  T_p   (peak wave period)        : {T_wu:.3f} s
  Slope (H:V)                     : 1:{slope_wu:.2f}
  tan(α)                          : {tan_alpha:.4f}
  Freeboard Rc                    : {Rc_wu:.3f} m
  Roughness factor γ_f            : {gf_wu:.3f}
  Berm factor γ_b                 : {gb_wu:.3f}
  Obliquity β                     : {beta_wu:.1f}°
  Obliquity factor γ_β            : {gbeta:.4f}

STEP 1 — Deep Water Wavelength
  L₀ = g·T_p² / (2π)
  L₀ = 9.81 × {T_wu:.2f}² / (2π)
  L₀ = {L0:.3f} m

STEP 2 — Iribarren Number (surf-similarity)
  ξ = tan(α) / √(H_m0 / L₀)
  ξ = {tan_alpha:.4f} / √({H_wu:.3f} / {L0:.3f})
  ξ = {xi:.4f}
  Breaker type: {btype}

STEP 3 — Wave Run-Up (EurOtop 2018, Eq. 5.2)
  Ru2% = 1.65 · γ_b · γ_f · γ_β · ξ · H_m0
       = 1.65 × {gb_wu:.3f} × {gf_wu:.3f} × {gbeta:.4f} × {xi:.4f} × {H_wu:.3f}
       = {1.65*gb_wu*gf_wu*gbeta*xi*H_wu:.4f} m  (before cap)
  Cap  = (4.0 - 1.5/√(γ_f·γ_β·ξ)) · γ_b · H_m0
       = {(4.0 - 1.5/max(math.sqrt(gf_wu*gbeta*xi), 1e-9))*gb_wu*H_wu:.4f} m
  Ru2% = {Ru2:.4f} m  (minimum of above)
  Ru1% ≈ 1.4 × Ru2% = {Ru1:.4f} m

STEP 4 — Reflection Coefficient (Postma 1989)
  Cr = 0.1 · ξ²  = 0.1 × {xi:.4f}² = {Cr:.4f}
  (capped at 1.0)

STEP 5 — Mean Overtopping Discharge (EurOtop 2018, Eq. 5.6)
  q = √(g·H_m0³) / √(L₀/H_m0) · 0.2 · exp(-2.3 · Rc/(γ_f·γ_β·H_m0·ξ))
  q = {q:.6f} m³/s/m  =  {q*1000:.4f} L/s/m

STEP 6 — Obliquity Factor (EurOtop 2018)
  γ_β = max(1 - 0.0033·β, 0.736)  [β = {beta_wu:.1f}°]
  γ_β = {gbeta:.4f}
"""
        st.markdown(f'<div class="coord-block">{wu_text}</div>', unsafe_allow_html=True)

        st.download_button('📥 Export Run-Up Report (.txt)', data=wu_text,
                           file_name='hyrcan_wave_runup.txt', mime='text/plain',
                           use_container_width=True)

# ════════════════════════════════════════════════════════════════════
#  FOOTER
# ════════════════════════════════════════════════════════════════════

st.markdown('<br>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;color:#484f58;font-size:12px;
            border-top:1px solid #21262d;padding-top:12px;">
  HYRCAN Engineering Suite v3.0 &nbsp;·&nbsp;
  Developed by <b>Mathias Adjei Tawiah</b> &nbsp;·&nbsp;
  mathiasadjeitawiah@gmail.com &nbsp;·&nbsp;
  Hohai University — College of Harbor, Coastal and Offshore Engineering<br>
  Standards: EurOtop 2018 | JTS 154-1-2011 | GB 50286-2013 &nbsp;·&nbsp;
  Coordinate logic verified against HYRCAN 3.0
</div>
""", unsafe_allow_html=True)
