"""
HYRCAN Engineering Suite v8.0 — Streamlit Web Application
Module 1: Rubble Mound Embankment — HYRCAN Coordinate Generator
Module 2: Vertical Caisson — Direct FOS Stability Analysis

Developed by: Makson
Email: onlyupwardandforward@gmail.com
Hohai University — Coastal Engineering

Coordinate logic verified against HYRCAN 3.0.
DO NOT modify the core calculation functions.
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

# ════════════════════════════════════════════════════════════════════
#  PAGE CONFIG & THEME
# ════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="HYRCAN Engineering Suite v8.0",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS — dark professional theme
st.markdown("""
<style>
/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Segoe UI', 'Inter', sans-serif;
}
.stApp {
    background-color: #0d1117;
    color: #e6edf3;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background-color: #161b22;
    border-radius: 8px;
    padding: 4px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background-color: transparent;
    color: #8b949e;
    border-radius: 6px;
    font-weight: 600;
    font-size: 15px;
    padding: 8px 24px;
}
.stTabs [aria-selected="true"] {
    background-color: #21262d !important;
    color: #58a6ff !important;
}

/* ── Inputs ── */
.stNumberInput input, .stTextInput input {
    background-color: #21262d;
    border: 1px solid #30363d;
    color: #e6edf3;
    border-radius: 6px;
}
.stSelectbox select {
    background-color: #21262d;
    color: #e6edf3;
}

/* ── Buttons ── */
.stButton > button {
    background-color: #238636;
    color: white;
    border: none;
    border-radius: 6px;
    font-weight: 600;
    padding: 8px 20px;
    transition: background 0.2s;
}
.stButton > button:hover {
    background-color: #2ea043;
}

/* ── Metric cards ── */
[data-testid="metric-container"] {
    background-color: #21262d;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 12px;
}

/* ── DataFrames / Tables ── */
.stDataFrame { border-radius: 8px; overflow: hidden; }

/* ── Info/success/error boxes ── */
.stAlert { border-radius: 8px; }

/* ── Section headers ── */
.section-header {
    background: linear-gradient(90deg, #1f6feb22, transparent);
    border-left: 3px solid #58a6ff;
    padding: 8px 14px;
    border-radius: 0 6px 6px 0;
    margin: 16px 0 8px 0;
    font-weight: 700;
    font-size: 14px;
    color: #58a6ff;
    letter-spacing: 0.5px;
}
.pass-badge {
    color: #3fb950; font-weight: 700;
}
.fail-badge {
    color: #f85149; font-weight: 700;
}
.coord-block {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 16px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 13px;
    color: #e6edf3;
    white-space: pre;
    overflow-x: auto;
}
</style>
""", unsafe_allow_html=True)

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
        HYRCAN Engineering Suite <span style="color:#8b949e;font-size:15px;">v8.0</span>
      </div>
      <div style="color:#8b949e;font-size:13px;margin-top:2px;">
        Rubble Mound Coordinate Generator &nbsp;·&nbsp; Vertical Caisson FOS Analysis
        &nbsp;·&nbsp; Hohai University — Coastal Engineering
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
#  CORE CALCULATION FUNCTIONS  (verified against HYRCAN 3.0)
# ════════════════════════════════════════════════════════════════════

def compute_layer_elevations(seabed_elev, t1, t2, t3):
    """
    Auto-calculate all layer elevations from seabed and thicknesses.
    Returns dict with real elevations and datum-shifted HYRCAN Y values.
    """
    top1  = seabed_elev
    bot1  = top1 - t1
    top2  = bot1
    bot2  = top2 - t2
    top3  = bot2
    bot3  = top3 - t3
    datum = abs(bot3)          # HYRCAN Y = real_elev + datum

    def Y(e): return e + datum

    return {
        'top1': top1,  'bot1': bot1,
        'top2': bot1,  'bot2': bot2,
        'top3': bot2,  'bot3': bot3,
        'datum': datum,
        'Y_top1': Y(top1), 'Y_bot1': Y(bot1),
        'Y_top2': Y(bot1), 'Y_bot2': Y(bot2),
        'Y_top3': Y(bot2), 'Y_bot3': Y(bot3),
        'Y_seabed': Y(seabed_elev),
    }


def compute_geometry(crest_elev, seabed_elev, crest_width,
                     upper_height, lower_height,
                     sw_upper, sw_lower, seaward_berm,
                     lw_upper, lw_lower, landward_berm,
                     layers):
    """
    Core coordinate engine — verified against HYRCAN 3.0 and DeepSeek.
    Build X left-to-right from seaward toe = 0.
    Crest left is placed at top of seaward upper slope (NOT centered).
    """
    datum    = layers['datum']
    def Y(e): return e + datum

    crest_y  = Y(crest_elev)
    seabed_y = Y(seabed_elev)
    berm_y   = Y(crest_elev - upper_height)
    dhw_y    = None   # set by caller

    # Horizontal distances per segment
    sw_udx = upper_height * sw_upper
    sw_ldx = lower_height * sw_lower
    lw_udx = upper_height * lw_upper
    lw_ldx = lower_height * lw_lower

    # X from seaward toe = 0, left → right
    x_sw_toe  = 0.0
    x_sw_be   = x_sw_toe + sw_ldx              # seaward berm end (berm level)
    x_sw_bs   = x_sw_be  + seaward_berm        # seaward berm start (berm level)
    x_cl      = x_sw_bs  + sw_udx              # crest left
    x_cr      = x_cl     + crest_width         # crest right
    x_lw_bs   = x_cr     + lw_udx             # landward berm start
    x_lw_be   = x_lw_bs  + landward_berm       # landward berm end
    x_lw_toe  = x_lw_be  + lw_ldx             # landward toe

    pts = {
        'sw_toe':  (x_sw_toe,  seabed_y),
        'sw_be':   (x_sw_be,   berm_y),
        'sw_bs':   (x_sw_bs,   berm_y),
        'cl':      (x_cl,      crest_y),
        'cr':      (x_cr,      crest_y),
        'lw_bs':   (x_lw_bs,   berm_y),
        'lw_be':   (x_lw_be,   berm_y),
        'lw_toe':  (x_lw_toe,  seabed_y),
    }

    return {
        'pts':         pts,
        'crest_y':     crest_y,
        'seabed_y':    seabed_y,
        'berm_y':      berm_y,
        'model_right': x_lw_toe,
        'model_bottom': 0.0,
        'sw_udx': sw_udx, 'sw_ldx': sw_ldx,
        'lw_udx': lw_udx, 'lw_ldx': lw_ldx,
        'x_sw_be': x_sw_be, 'x_sw_bs': x_sw_bs,
        'x_cl': x_cl, 'x_cr': x_cr,
        'x_lw_bs': x_lw_bs, 'x_lw_be': x_lw_be,
        'x_lw_toe': x_lw_toe,
    }


def verify_geometry(g, crest_elev, seabed_elev, crest_width,
                    upper_height, lower_height,
                    sw_upper, sw_lower, seaward_berm,
                    lw_upper, lw_lower, landward_berm):
    """Self-check all coordinates against inputs. Returns list of (name, expected, got, pass)."""
    pts = g['pts']
    tol = 0.001
    checks = []
    def ck(name, exp, got):
        checks.append((name, exp, got, abs(exp - got) <= tol))

    ck('Crest width',          crest_width,   pts['cr'][0] - pts['cl'][0])
    ck('Upper slope height',   upper_height,  (crest_elev - (seabed_elev + lower_height)))
    ck('Total height',         crest_elev - seabed_elev,
                               upper_height + lower_height)
    ck('Seaward lower ΔX',     lower_height * sw_lower,   g['sw_ldx'])
    ck('Seaward berm width',   seaward_berm,  g['x_sw_bs'] - g['x_sw_be'])
    ck('Seaward upper ΔX',     upper_height * sw_upper,   g['sw_udx'])
    ck('Landward upper ΔX',    upper_height * lw_upper,   g['lw_udx'])
    ck('Landward berm width',  landward_berm, g['x_lw_be'] - g['x_lw_bs'])
    ck('Landward lower ΔX',    lower_height * lw_lower,   g['lw_ldx'])
    return checks


def caisson_fos(B, H_c, gamma_c, d, H1pct, gamma_w, mu, q_allow):
    """
    Caisson FOS calculations per GB 50286-2013 and JTS 154-1-2011.
    Returns dict of all intermediate and final values.
    """
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
#  TEXT GENERATION
# ════════════════════════════════════════════════════════════════════

def generate_hyrcan_instructions(
        g, layers, dhw, surcharge, num_slices, crest_elev, seabed_elev,
        upper_height, lower_height,
        sw_upper, sw_lower, seaward_berm,
        lw_upper, lw_lower, landward_berm, crest_width,
        n1, n2, n3, mat_rubble, mat_l1, mat_l2, mat_l3,
        ):
    """Build the complete HYRCAN step-by-step instruction block."""
    pts   = g['pts']
    cy    = g['crest_y']
    sy    = g['seabed_y']
    by    = g['berm_y']
    L     = 0.0
    R     = g['model_right']
    B_mdl = 0.0
    datum = layers['datum']
    dy    = dhw + datum   # HYRCAN Y for water table

    # Material table (text-art, for Step 7)
    def row(name, g_, c, phi):
        return (f"│ {name:<16} │ {g_:<14.1f} │ {c:<14.1f} │ {phi:<12.1f} │")

    mat_table = "\n".join([
        "┌──────────────────┬────────────────┬────────────────┬──────────────┐",
        "│ Material         │ γ (kN/m³)      │ c (kPa)        │ φ (°)        │",
        "├──────────────────┼────────────────┼────────────────┼──────────────┤",
        row("Rubble",  mat_rubble[0], mat_rubble[1], mat_rubble[2]),
        row(n1,        mat_l1[0],     mat_l1[1],     mat_l1[2]),
        row(n2,        mat_l2[0],     mat_l2[1],     mat_l2[2]),
        row(n3,        mat_l3[0],     mat_l3[1],     mat_l3[2]),
        "└──────────────────┴────────────────┴────────────────┴──────────────┘",
    ])

    out = f"""\
{'='*72}
  HYRCAN ENGINEERING SUITE v8.0 — COMPLETE SETUP INSTRUCTIONS
  Hohai University — Coastal Engineering  |  Developed by Makson
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
STEP 4: MATERIAL BOUNDARIES
  ▸ Geometry → Material Boundary

  ── Boundary 1: Seabed / Top of {n1} ───────────────────────
  {L:.3f},{layers['Y_seabed']:.3f}
  {R:.3f},{layers['Y_seabed']:.3f}
  d

  ── Boundary 2: Bottom of {n1} / Top of {n2} ──────────────
  {L:.3f},{layers['Y_bot1']:.3f}
  {R:.3f},{layers['Y_bot1']:.3f}
  d

  ── Boundary 3: Bottom of {n2} / Top of {n3} ──────────────
  {L:.3f},{layers['Y_bot2']:.3f}
  {R:.3f},{layers['Y_bot2']:.3f}
  d

  ✅ You should see 4 coloured regions.

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
  Click each material, then click its region:

  ┌──────────────────────┬──────────────────────────────────────────┐
  │ Material             │ Region                                   │
  ├──────────────────────┼──────────────────────────────────────────┤
  │ Rubble               │ Embankment (above seabed)                │
  │ {n1:<20} │ Y = {layers['Y_bot1']:.2f} → {layers['Y_top1']:.2f}  (real: {layers['bot1']:.2f} → {layers['top1']:.2f} m)       │
  │ {n2:<20} │ Y = {layers['Y_bot2']:.2f} → {layers['Y_bot1']:.2f}  (real: {layers['bot2']:.2f} → {layers['bot1']:.2f} m)      │
  │ {n3:<20} │ Y = {layers['Y_bot3']:.2f} → {layers['Y_bot2']:.2f}  (real: {layers['bot3']:.2f} → {layers['bot2']:.2f} m)      │
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
  Bottom of {n3} = {layers['bot3']:.2f} m (real) → Y = 0.000 (HYRCAN)
  Datum shift applied: +{datum:.3f} m to all elevations

MODEL DIMENSIONS
  Total width  : {R:.3f} m
  Total height : {g['crest_y']:.3f} m  (HYRCAN Y)
  Seaward toe  : X = {pts['sw_toe'][0]:.3f}
  Landward toe : X = {pts['lw_toe'][0]:.3f}
  Crest        : X = {pts['cl'][0]:.3f} → {pts['cr'][0]:.3f}  (width = {pts['cr'][0]-pts['cl'][0]:.3f} m)
"""
    return out


def generate_coordinates_txt(g, layers, dhw, surcharge, crest_elev, seabed_elev):
    """Minimal coordinate-only export."""
    pts = g['pts']
    cy  = g['crest_y']; sy = g['seabed_y']; by = g['berm_y']
    L   = 0.0; R = g['model_right']; B = 0.0
    datum = layers['datum']
    dy    = dhw + datum

    lines = [
        "HYRCAN COORDINATE EXPORT — v8.0",
        f"Datum shift: +{datum:.3f} m",
        "",
        "EXTERNAL BOUNDARY",
        f"{L:.3f},{sy:.3f}", f"{L:.3f},{B:.3f}", f"{R:.3f},{B:.3f}", f"{R:.3f},{sy:.3f}",
        f"{pts['lw_be'][0]:.3f},{by:.3f}", f"{pts['lw_bs'][0]:.3f},{by:.3f}",
        f"{pts['cr'][0]:.3f},{cy:.3f}", f"{pts['cl'][0]:.3f},{cy:.3f}",
        f"{pts['sw_bs'][0]:.3f},{by:.3f}", f"{pts['sw_be'][0]:.3f},{by:.3f}",
        f"{pts['sw_toe'][0]:.3f},{sy:.3f}", "c",
        "",
        f"MATERIAL BOUNDARY 1 (Seabed):",
        f"{L:.3f},{layers['Y_seabed']:.3f}", f"{R:.3f},{layers['Y_seabed']:.3f}", "d",
        "",
        f"MATERIAL BOUNDARY 2 (Bottom Layer 1):",
        f"{L:.3f},{layers['Y_bot1']:.3f}", f"{R:.3f},{layers['Y_bot1']:.3f}", "d",
        "",
        f"MATERIAL BOUNDARY 3 (Bottom Layer 2):",
        f"{L:.3f},{layers['Y_bot2']:.3f}", f"{R:.3f},{layers['Y_bot2']:.3f}", "d",
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

LAYER_COLORS = ['#C9B99A', '#A8B5A0', '#B5C4D1']

def draw_rubble_mound(g, layers, dhw, crest_elev, seabed_elev,
                      upper_height, lower_height, n1, n2, n3):
    pts = g['pts']
    lh  = lower_height
    ce  = crest_elev
    se  = seabed_elev
    berm_e = ce - upper_height

    fig, ax = plt.subplots(figsize=(12, 6), dpi=120)
    fig.patch.set_facecolor('#0d1117')
    ax.set_facecolor('#161b22')

    xl = pts['sw_toe'][0]
    xr = pts['lw_toe'][0]

    # Soil layers
    layer_defs = [
        (layers['top1'], layers['bot1'], LAYER_COLORS[0], 0.55, n1),
        (layers['bot1'], layers['bot2'], LAYER_COLORS[1], 0.50, n2),
        (layers['bot2'], layers['bot3'], LAYER_COLORS[2], 0.45, n3),
    ]
    for top_e, bot_e, col, alp, lbl in layer_defs:
        ax.fill_betweenx([bot_e, top_e], xl - 999, xr + 999,
                         facecolor=col, alpha=alp, zorder=1)
        ax.axhline(y=top_e, color='#444', lw=0.7, ls=':', zorder=2)

    ax.axhline(y=se, color='#607d8b', lw=1.3, ls='--', zorder=2)

    # Embankment
    xs = [pts['sw_toe'][0], pts['sw_be'][0], pts['sw_bs'][0],
          pts['cl'][0], pts['cr'][0],
          pts['lw_bs'][0], pts['lw_be'][0], pts['lw_toe'][0],
          pts['sw_toe'][0]]
    ys = [se, berm_e, berm_e, ce, ce, berm_e, berm_e, se, se]
    ax.fill(xs, ys, facecolor='#C9A96E', alpha=0.88,
            edgecolor='#7B5E3A', lw=1.5, zorder=3)

    # Water table
    ax.axhline(y=dhw, color='#3A7EC4', ls='--', lw=2.0, zorder=4)

    # Surcharge arrows on crest
    arrow_xs = np.linspace(pts['cl'][0] + 1, pts['cr'][0] - 1, 4)
    for ax_x in arrow_xs:
        ax.annotate('', xy=(ax_x, ce), xytext=(ax_x, ce + 1.8),
                    arrowprops=dict(arrowstyle='->', color='#ff6b35', lw=1.5),
                    zorder=5)
    ax.text((pts['cl'][0] + pts['cr'][0]) / 2, ce + 2.0,
            f'q = {10:.0f} kN/m²', ha='center', fontsize=8,
            color='#ff6b35', zorder=5)

    # Layer labels
    lx = xl - (xr - xl) * 0.015
    for top_e, bot_e, col, alp, lbl in layer_defs:
        ax.text(lx, (top_e + bot_e) / 2, lbl,
                fontsize=9, va='center', ha='right',
                fontstyle='italic', color='#ccc', zorder=5)

    # ── Distributed load (surcharge) on full crest width ──────────
    surcharge = st.session_state.get('rm_surcharge', 10.0)
    cl_x    = pts['cl'][0]
    cr_x    = pts['cr'][0]
    crest_w = cr_x - cl_x                       # exact crest width (6.0 m)
    block_h = max(crest_w * 0.12, 0.6)          # hatched block height

    # Hatched rectangle sitting directly on the crest surface
    load_rect = mpatches.FancyBboxPatch(
        (cl_x, ce), crest_w, block_h,
        boxstyle='square,pad=0',
        facecolor='#ff6b3533', edgecolor='#ff6b35',
        lw=1.5, hatch='////', zorder=6,
    )
    ax.add_patch(load_rect)

    # Downward arrows evenly spaced across the full crest width
    n_arrows  = max(3, int(crest_w / 1.5))
    arrow_xs  = np.linspace(cl_x + crest_w * 0.1, cr_x - crest_w * 0.1, n_arrows)
    arrow_top = ce + block_h
    for ax_x in arrow_xs:
        ax.annotate(
            '', xy=(ax_x, ce), xytext=(ax_x, arrow_top),
            arrowprops=dict(arrowstyle='->', color='#ff6b35', lw=1.8),
            zorder=7,
        )

    # Bold magnitude label centred above the block
    ax.text(
        (cl_x + cr_x) / 2, arrow_top + block_h * 0.3,
        f'Distributed Load = {surcharge:.1f} kN/m²',
        ha='center', va='bottom', fontsize=9, fontweight='bold',
        color='#ff6b35', zorder=7,
    )

    # ── Toe coordinate labels only (crest labels removed) ───────────
    for lbl, xp, yp, va in [
        (f'({pts["sw_toe"][0]:.1f}, {se:.1f})', pts['sw_toe'][0], se - 0.7, 'top'),
        (f'({pts["lw_toe"][0]:.1f}, {se:.1f})', pts['lw_toe'][0], se - 0.7, 'top'),
    ]:
        ax.text(xp, yp, lbl, ha='center', fontsize=7.5, color='#aaa',
                va=va, zorder=5)

    # Legend
    handles = [
        mpatches.Patch(facecolor='#C9A96E', alpha=0.88, edgecolor='#7B5E3A',
                       label='Embankment (Rubble)'),
        *[mpatches.Patch(facecolor=LAYER_COLORS[i], alpha=0.7,
                         label=f'{nm}  [{layer_defs[i][0]:.1f}→{layer_defs[i][1]:.1f} m]')
          for i, nm in enumerate([n1, n2, n3])],
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
    ax.set_ylim(layers['bot3'] - 1.5, ce + 4.0)
    ax.set_aspect('equal', adjustable='box')
    fig.subplots_adjust(bottom=0.22)
    return fig


def draw_caisson(p, r):
    fig, ax = plt.subplots(figsize=(10, 6), dpi=120)
    fig.patch.set_facecolor('#0d1117')
    ax.set_facecolor('#0f1921')

    B = p['B']; H_c = p['H_c']; seabed = 0.0; d = p['d']

    # Rubble foundation
    rb_h, rb_ext = 1.8, 3.0
    rb_xs = [-rb_ext, -rb_ext*0.3, B+rb_ext*0.3, B+rb_ext, -rb_ext]
    rb_ys = [seabed-rb_h, seabed, seabed, seabed-rb_h, seabed-rb_h]
    ax.fill(rb_xs, rb_ys, facecolor='#C8A96E', alpha=0.85,
            edgecolor='#7B5E3A', lw=1.2, zorder=2, label='Rubble Foundation')

    ax.axhline(y=seabed, color='#607d8b', lw=1.3, zorder=3)

    # Caisson block
    caisson_top = seabed + H_c
    caisson_patch = mpatches.FancyBboxPatch(
        (0, seabed), B, H_c, boxstyle='square,pad=0',
        facecolor='#5b7fa5', alpha=0.85,
        edgecolor='#2c4a70', lw=2.0, zorder=4)
    ax.add_patch(caisson_patch)
    for xi in np.linspace(B*0.2, B*0.8, 4):
        ax.plot([xi,xi],[seabed,caisson_top], color='#3a5f80', lw=0.5, alpha=0.35, zorder=5)
    for yi in [seabed+H_c*0.25, seabed+H_c*0.5, seabed+H_c*0.75]:
        ax.plot([0,B],[yi,yi], color='#3a5f80', lw=0.5, alpha=0.35, zorder=5)

    ax.text(B/2, seabed+H_c/2, 'CAISSON\n(Concrete)',
            ha='center', va='center', fontsize=11, fontweight='bold',
            color='white', zorder=6)

    # Water table
    water_y = seabed + d
    ax.axhline(y=water_y, color='#3A7EC4', ls='--', lw=2.0, zorder=6)

    # Wave force arrow
    wx = -B * 0.75
    wy = water_y - d * 0.35
    ax.annotate('', xy=(0, wy), xytext=(wx, wy),
                arrowprops=dict(arrowstyle='->', color='#f85149', lw=2.5), zorder=7)
    ax.text(wx - 0.5, wy + 0.2,
            f'P = {r["P"]:.1f} kN/m\n(Wave Force)',
            fontsize=8.5, color='#f85149', ha='right', zorder=7)

    # Dimension arrows
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
    dim_arrow(-rb_ext-1.8, seabed, water_y, f'd = {d:.2f} m',
              color='#3A7EC4', vertical=True)
    ax.text(B/2, water_y + 0.4, f'H₁% = {p["H1pct"]:.2f} m',
            ha='center', fontsize=8.5, color='#3A7EC4')

    # FOS summary
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
        mpatches.Patch(facecolor='#5b7fa5', alpha=0.85, edgecolor='#2c4a70',
                       label='Caisson (Concrete)'),
        mpatches.Patch(facecolor='#C8A96E', alpha=0.85, edgecolor='#7B5E3A',
                       label='Rubble Foundation'),
        mlines.Line2D([], [], color='#3A7EC4', ls='--', lw=2,
                      label=f'Water Table (d = {d:.2f} m)'),
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

# Rubble Mound defaults
_default('rm_crest_elev',    14.55)
_default('rm_seabed_elev',   -3.30)
_default('rm_crest_width',    6.0)
_default('rm_upper_height',   4.85)
_default('rm_lower_height',  13.0)
_default('rm_sw_upper',       2.5)
_default('rm_sw_lower',       2.5)
_default('rm_sw_berm',        6.5)
_default('rm_lw_upper',       1.5)
_default('rm_lw_lower',       1.5)
_default('rm_lw_berm',        2.0)
_default('rm_dhw',            4.99)
_default('rm_surcharge',     10.0)
_default('rm_num_slices',    50.0)

_default('rm_n1',   'Soft Silt')
_default('rm_t1',    7.8)
_default('rm_g1',   16.5); _default('rm_c1',  6.0); _default('rm_phi1',  8.0)
_default('rm_n2',   'Silty Clay')
_default('rm_t2',   10.2)
_default('rm_g2',   19.0); _default('rm_c2', 20.0); _default('rm_phi2', 18.0)
_default('rm_n3',   'Fine Sand')
_default('rm_t3',   10.0)
_default('rm_g3',   19.5); _default('rm_c3',  0.0); _default('rm_phi3', 30.0)
_default('rm_gr',   19.0); _default('rm_cr_',  0.0); _default('rm_phir', 38.0)

# Caisson defaults
_default('cs_generated', False)
_default('cs_B',       16.0)
_default('cs_H_c',     14.0)
_default('cs_gamma_c', 24.0)
_default('cs_d',        4.59)
_default('cs_H1pct',    2.71)
_default('cs_gamma_w', 10.25)
_default('cs_mu',       0.60)
_default('cs_q_allow', 500.0)

# ════════════════════════════════════════════════════════════════════
#  PROJECT SAVE / LOAD
# ════════════════════════════════════════════════════════════════════

RM_KEYS = ['rm_crest_elev','rm_seabed_elev','rm_crest_width','rm_upper_height',
           'rm_lower_height','rm_sw_upper','rm_sw_lower','rm_sw_berm',
           'rm_lw_upper','rm_lw_lower','rm_lw_berm','rm_dhw','rm_surcharge',
           'rm_num_slices','rm_n1','rm_t1','rm_g1','rm_c1','rm_phi1',
           'rm_n2','rm_t2','rm_g2','rm_c2','rm_phi2',
           'rm_n3','rm_t3','rm_g3','rm_c3','rm_phi3',
           'rm_gr','rm_cr_','rm_phir']
CS_KEYS = ['cs_B','cs_H_c','cs_gamma_c','cs_d','cs_H1pct',
           'cs_gamma_w','cs_mu','cs_q_allow']

def save_project():
    data = {k: st.session_state[k] for k in RM_KEYS + CS_KEYS if k in st.session_state}
    return json.dumps(data, indent=2)

def load_project(uploaded):
    data = json.loads(uploaded.read().decode())
    for k, v in data.items():
        st.session_state[k] = v

# ════════════════════════════════════════════════════════════════════
#  UI HELPER
# ════════════════════════════════════════════════════════════════════

def section(label):
    st.markdown(f'<div class="section-header">{label}</div>', unsafe_allow_html=True)

def num(label, key, **kw):
    st.session_state[key] = st.number_input(label, value=st.session_state[key],
                                             key=f'_ni_{key}', **kw)
    return st.session_state[key]

def txt(label, key):
    st.session_state[key] = st.text_input(label, value=st.session_state[key],
                                           key=f'_ti_{key}')
    return st.session_state[key]

# ════════════════════════════════════════════════════════════════════
#  TABS
# ════════════════════════════════════════════════════════════════════

tab1, tab2 = st.tabs(["🏗️  Rubble Mound Coordinate Generator",
                       "🏛️  Vertical Caisson Stability"])

# ────────────────────────────────────────────────────────────────────
#  TAB 1 — RUBBLE MOUND
# ────────────────────────────────────────────────────────────────────

with tab1:
    # Top row: Save/Load
    sc1, sc2, sc3 = st.columns([2, 2, 6])
    with sc1:
        project_json = save_project()
        st.download_button('💾 Save Project (.json)', data=project_json,
                           file_name='hyrcan_project.json',
                           mime='application/json', use_container_width=True)
    with sc2:
        uploaded = st.file_uploader('📂 Load Project', type='json',
                                    label_visibility='collapsed')
        if uploaded:
            load_project(uploaded)
            st.success('Project loaded! Re-run to apply.', icon='✅')

    st.markdown('<hr style="border-color:#30363d;margin:8px 0 16px 0;">', unsafe_allow_html=True)

    left_col, right_col = st.columns([1, 1.6], gap='large')

    # ── INPUTS ──────────────────────────────────────────────────────
    with left_col:
        section("🏗  Embankment Geometry")
        c1, c2 = st.columns(2)
        with c1:
            ce  = num('Crest elevation (m)',  'rm_crest_elev')
            cw  = num('Crest width (m)',       'rm_crest_width', min_value=0.5)
            uh  = num('Upper height (m)',      'rm_upper_height', min_value=0.0)
        with c2:
            se  = num('Seabed elevation (m)', 'rm_seabed_elev')
            lh  = num('Lower height (m)',     'rm_lower_height', min_value=0.0)

        # Height check
        total_h = ce - se
        if abs((uh + lh) - total_h) > 0.01:
            st.error(f"⚠️  upper + lower = {uh+lh:.3f} m ≠ crest − seabed = {total_h:.3f} m")

        section("📐  Slope Ratios (H : V)")
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

        section("🌊  Water & Loads")
        c1, c2, c3 = st.columns(3)
        with c1:
            dhw = num('DHW level (m)', 'rm_dhw')
        with c2:
            q   = num('Surcharge (kN/m²)', 'rm_surcharge', min_value=0.0)
        with c3:
            ns  = num('No. of slices', 'rm_num_slices', min_value=10.0, step=5.0)

        section("🧱  Soil Layers  (enter thickness — elevations auto-calculated)")

        # Layer 1
        st.markdown("**Layer 1**")
        c1, c2, c3, c4, c5 = st.columns([2, 1.2, 1.2, 1.2, 1.2])
        with c1: n1 = txt('Name', 'rm_n1')
        with c2: t1 = num('Thickness (m)', 'rm_t1', min_value=0.1)
        with c3: g1 = num('γ (kN/m³)', 'rm_g1', min_value=10.0)
        with c4: c1_ = num('c (kPa)', 'rm_c1', min_value=0.0)
        with c5: phi1 = num('φ (°)', 'rm_phi1', min_value=0.0)

        st.markdown("**Layer 2**")
        c1, c2, c3, c4, c5 = st.columns([2, 1.2, 1.2, 1.2, 1.2])
        with c1: n2 = txt('Name', 'rm_n2')
        with c2: t2 = num('Thickness (m)', 'rm_t2', min_value=0.1)
        with c3: g2 = num('γ (kN/m³)', 'rm_g2', min_value=10.0)
        with c4: c2_ = num('c (kPa)', 'rm_c2', min_value=0.0)
        with c5: phi2 = num('φ (°)', 'rm_phi2', min_value=0.0)

        st.markdown("**Layer 3**")
        c1, c2, c3, c4, c5 = st.columns([2, 1.2, 1.2, 1.2, 1.2])
        with c1: n3 = txt('Name', 'rm_n3')
        with c2: t3 = num('Thickness (m)', 'rm_t3', min_value=0.1)
        with c3: g3 = num('γ (kN/m³)', 'rm_g3', min_value=10.0)
        with c4: c3_ = num('c (kPa)', 'rm_c3', min_value=0.0)
        with c5: phi3 = num('φ (°)', 'rm_phi3', min_value=0.0)

        st.markdown("**Embankment (Rubble)**")
        c1, c2, c3 = st.columns(3)
        with c1: gr  = num('γ (kN/m³)', 'rm_gr', min_value=10.0)
        with c2: cr_ = num('c (kPa)',    'rm_cr_', min_value=0.0)
        with c3: phir= num('φ (°)',      'rm_phir', min_value=0.0)

        # Live layer elevation table
        layers = compute_layer_elevations(se, t1, t2, t3)

        section("📊  Live Layer Elevation Preview")
        import pandas as pd
        df_layers = pd.DataFrame({
            'Layer':          [n1, n2, n3],
            'Top Elev (m)':   [f"{layers['top1']:.3f}", f"{layers['top2']:.3f}", f"{layers['top3']:.3f}"],
            'Bottom Elev (m)':[f"{layers['bot1']:.3f}", f"{layers['bot2']:.3f}", f"{layers['bot3']:.3f}"],
            'Thickness (m)':  [f"{t1:.2f}", f"{t2:.2f}", f"{t3:.2f}"],
            'HYRCAN Y_top':   [f"{layers['Y_top1']:.3f}", f"{layers['Y_top2']:.3f}", f"{layers['Y_top3']:.3f}"],
            'HYRCAN Y_bot':   [f"{layers['Y_bot1']:.3f}", f"{layers['Y_bot2']:.3f}", f"{layers['Y_bot3']:.3f}"],
        })
        st.dataframe(df_layers, use_container_width=True, hide_index=True)
        st.caption(f"Datum shift: **+{layers['datum']:.3f} m**  |  Bottom of {n3} → Y = 0.000")

        st.markdown('<br>', unsafe_allow_html=True)
        generate = st.button('🚀  Generate HYRCAN Coordinates', type='primary',
                             use_container_width=True)

    # ── OUTPUTS ─────────────────────────────────────────────────────
    with right_col:
        # Always recompute geometry so preview is live
        layers = compute_layer_elevations(se, t1, t2, t3)

        valid = abs((uh + lh) - (ce - se)) <= 0.01

        if generate and valid:
            g = compute_geometry(ce, se, cw, uh, lh,
                                 sw_u, sw_l, sw_b, lw_u, lw_l, lw_b, layers)

            # Store in session
            st.session_state['rm_g'] = g
            st.session_state['rm_layers'] = layers
            st.session_state['rm_generated'] = True

        if st.session_state.get('rm_generated'):
            g = st.session_state['rm_g']
            layers = st.session_state['rm_layers']

            # ── Cross-section plot ──────────────────────────────────
            section("📊  Cross-Section")
            fig = draw_rubble_mound(g, layers, dhw, ce, se, uh, lh, n1, n2, n3)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

            # ── Verification table ──────────────────────────────────
            section("✅  Automatic Verification")
            checks = verify_geometry(g, ce, se, cw, uh, lh,
                                     sw_u, sw_l, sw_b, lw_u, lw_l, lw_b)
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

            # ── Key dimensions metrics ──────────────────────────────
            pts = g['pts']
            mc1, mc2, mc3, mc4 = st.columns(4)
            mc1.metric('Model width',    f"{g['model_right']:.3f} m")
            mc2.metric('Crest left X',   f"{pts['cl'][0]:.3f}")
            mc3.metric('Crest right X',  f"{pts['cr'][0]:.3f}")
            mc4.metric('Datum shift',    f"+{layers['datum']:.3f} m")

            # ── Instructions ────────────────────────────────────────
            section("📖  Complete HYRCAN Step-by-Step Instructions")
            instructions = generate_hyrcan_instructions(
                g, layers, dhw, q, ns, ce, se, uh, lh,
                sw_u, sw_l, sw_b, lw_u, lw_l, lw_b, cw,
                n1, n2, n3,
                mat_rubble=(gr, cr_, phir),
                mat_l1=(g1, c1_, phi1),
                mat_l2=(g2, c2_, phi2),
                mat_l3=(g3, c3_, phi3),
            )
            st.markdown(f'<div class="coord-block">{instructions}</div>',
                        unsafe_allow_html=True)

            # ── Download buttons ────────────────────────────────────
            st.markdown('<br>', unsafe_allow_html=True)
            dc1, dc2 = st.columns(2)
            with dc1:
                coords_txt = generate_coordinates_txt(g, layers, dhw, q, ce, se)
                st.download_button('📥 Export Coordinates (.txt)',
                                   data=coords_txt,
                                   file_name='hyrcan_coordinates.txt',
                                   mime='text/plain',
                                   use_container_width=True)
            with dc2:
                st.download_button('📥 Export Full Instructions (.txt)',
                                   data=instructions,
                                   file_name='hyrcan_step_by_step.txt',
                                   mime='text/plain',
                                   use_container_width=True)

            # Export plot
            buf = io.BytesIO()
            fig2 = draw_rubble_mound(g, layers, dhw, ce, se, uh, lh, n1, n2, n3)
            fig2.savefig(buf, format='png', dpi=300, bbox_inches='tight',
                         facecolor='white')
            plt.close(fig2)
            buf.seek(0)
            st.download_button('🖼  Export Plot (PNG 300 DPI)',
                               data=buf, file_name='hyrcan_cross_section.png',
                               mime='image/png', use_container_width=True)

        elif generate and not valid:
            st.error('Fix the height mismatch before generating.')
        else:
            st.info('👈  Fill in parameters and click **Generate** to produce coordinates.',
                    icon='ℹ️')

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
            B_cs  = num('Width B (m)',        'cs_B',       min_value=1.0)
            gc    = num('Concrete γ_c (kN/m³)', 'cs_gamma_c', min_value=10.0)
        with c2:
            Hc_cs = num('Height H_c (m)',     'cs_H_c',     min_value=1.0)

        section("🌊  Hydraulic Conditions")
        c1, c2, c3 = st.columns(3)
        with c1: d_cs  = num('Water depth d (m)', 'cs_d',      min_value=0.1)
        with c2: H1_cs = num('Wave H₁% (m)',       'cs_H1pct',  min_value=0.1)
        with c3: gw_cs = num('γ_w (kN/m³)',        'cs_gamma_w',min_value=9.0)

        section("⚙️  Stability Parameters")
        c1, c2 = st.columns(2)
        with c1: mu_cs = num('Friction coeff μ', 'cs_mu', min_value=0.1, max_value=1.0, step=0.01)
        with c2: qa_cs = num('q_allow (kPa)',    'cs_q_allow', min_value=50.0)

        st.markdown('<br>', unsafe_allow_html=True)

        # Reference card
        st.markdown("""
<div style="background:#161b22;border:1px solid #30363d;border-radius:8px;padding:14px;font-size:12px;color:#8b949e;">
<b style="color:#58a6ff;">📚 Design Standards</b><br><br>
• Wave force: JTS 154-1-2011, Appendix A<br>
• Sliding FOS ≥ 1.25 — GB 50286-2013 §5.3.2<br>
• Overturning FOS ≥ 1.50 — GB 50286-2013 §5.3.3<br>
• Bearing: q_max &lt; q_allow — JTS 154-1-2011 §5.3.4
</div>""", unsafe_allow_html=True)

    with right2:
        if st.button('⚡  Generate Stability Results', type='primary', use_container_width=True):
            st.session_state['cs_generated'] = True

        if st.session_state.get('cs_generated'):
            cs_p = dict(B=B_cs, H_c=Hc_cs, gamma_c=gc, d=d_cs,
                        H1pct=H1_cs, gamma_w=gw_cs, mu=mu_cs, q_allow=qa_cs)
            r = caisson_fos(**cs_p)

            # ── Metrics row ──────────────────────────────────────────
            section("📊  FOS Results")
            m1, m2, m3 = st.columns(3)
            s_ok = r['FOS_s'] >= 1.25
            o_ok = r['FOS_o'] >= 1.50
            b_ok = r['q_max'] < qa_cs

            m1.metric('Sliding FOS',     f"{r['FOS_s']:.3f}",
                      delta='≥ 1.25 ✅' if s_ok else '< 1.25 ❌',
                      delta_color='normal' if s_ok else 'inverse')
            m2.metric('Overturning FOS', f"{r['FOS_o']:.3f}",
                      delta='≥ 1.50 ✅' if o_ok else '< 1.50 ❌',
                      delta_color='normal' if o_ok else 'inverse')
            m3.metric('Bearing q_max',   f"{r['q_max']:.1f} kPa",
                      delta=f"< {int(qa_cs)} kPa ✅" if b_ok else f"≥ {int(qa_cs)} kPa ❌",
                      delta_color='normal' if b_ok else 'inverse')

            overall = s_ok and o_ok and b_ok
            if overall:
                st.success('✅  ALL STABILITY CHECKS PASSED — Design is adequate.', icon='✅')
            else:
                st.error('❌  ONE OR MORE CHECKS FAILED — Review design parameters.', icon='❌')

            # ── Results table ─────────────────────────────────────────
            section("📋  Detailed Results Table")
            df_res = pd.DataFrame({
                'Check':       ['Self-weight W', 'Wave Force P', 'Sliding FOS', 'Overturning FOS', 'Bearing q_max'],
                'Calculated':  [f"{r['W']:,.1f} kN/m", f"{r['P']:,.2f} kN/m",
                                f"{r['FOS_s']:.3f}", f"{r['FOS_o']:.3f}",
                                f"{r['q_max']:,.1f} kPa"],
                'Required':    ['—', '—', '≥ 1.25', '≥ 1.50', f"< {int(qa_cs)} kPa"],
                'Standard':    ['—', 'JTS 154-1-2011', 'GB 50286-2013 §5.3.2',
                                'GB 50286-2013 §5.3.3', 'JTS 154-1-2011 §5.3.4'],
                'Status':      ['—', '—',
                                '✅ Pass' if s_ok else '❌ Fail',
                                '✅ Pass' if o_ok else '❌ Fail',
                                '✅ Pass' if b_ok else '❌ Fail'],
            })
            st.dataframe(df_res, use_container_width=True, hide_index=True)

            # ── Calculation steps ─────────────────────────────────────
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
            st.markdown(f'<div class="coord-block">{calc_text}</div>',
                        unsafe_allow_html=True)

            # ── Cross-section plot ────────────────────────────────────
            section("📊  Cross-Section")
            fig_cs = draw_caisson(cs_p, r)
            st.pyplot(fig_cs, use_container_width=True)
            plt.close(fig_cs)

            # Export
            buf2 = io.BytesIO()
            fig_cs2 = draw_caisson(cs_p, r)
            fig_cs2.savefig(buf2, format='png', dpi=300, bbox_inches='tight',
                            facecolor='white')
            plt.close(fig_cs2)
            buf2.seek(0)
            dc1, dc2 = st.columns(2)
            with dc1:
                st.download_button('🖼  Export Plot (PNG 300 DPI)', data=buf2,
                                   file_name='hyrcan_caisson.png',
                                   mime='image/png', use_container_width=True)
            with dc2:
                st.download_button('📥 Export Report (.txt)',
                                   data=calc_text,
                                   file_name='hyrcan_caisson_report.txt',
                                   mime='text/plain', use_container_width=True)
        else:
            st.info('👈  Adjust parameters then click **Generate Stability Results**.', icon='ℹ️')

# ════════════════════════════════════════════════════════════════════
#  FOOTER
# ════════════════════════════════════════════════════════════════════

st.markdown('<br>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;color:#484f58;font-size:12px;
            border-top:1px solid #21262d;padding-top:12px;">
  HYRCAN Engineering Suite v8.0 &nbsp;·&nbsp;
  Developed by <b>Makson</b> &nbsp;·&nbsp;
  onlyupwardandforward@gmail.com &nbsp;·&nbsp;
  Hohai University — Coastal Engineering<br>
  Coordinate logic verified against HYRCAN 3.0
</div>
""", unsafe_allow_html=True)
