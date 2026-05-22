# HYRCAN Engineering Suite v3.0

**Professional Edition — Coastal Structure Analysis**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://hyrcan-suite-geotf68jxfjqcrnp5rbvbv.streamlit.app)

---

## About

HYRCAN Engineering Suite is a self-initiated Python-based engineering software suite developed alongside my undergraduate thesis on rubble-mound embankment design for land reclamation at **Hohai University**.

The suite automates key calculations for coastal structure analysis, implementing international standards:

- **EurOtop 2018** — European Overtopping Manual
- **JTS 154-1-2011** — Chinese Technical Standard for Port Engineering
- **GB 50286-2013** — Chinese National Standard for Seawall Engineering

Built with Python Tkinter GUI framework and deployed as an interactive **Streamlit** web application for remote access from any device.

---

## Developer

- **Name:** Mathias Adjei Tawiah
- **Email:** mathiasadjeitawiah@gmail.com
- **Institution:** Hohai University — College of Harbor, Coastal, and Offshore Engineering
- **GitHub:** [github.com/Mathias-lab](https://github.com/Mathias-lab)
- **LinkedIn:** [linkedin.com/in/mathias-adjei-tawiah](https://linkedin.com/in/mathias-adjei-tawiah)

---

## Modules

### Module 1: Rubble Mound Coordinate Generator
- Automates HYRCAN 3.0 model geometry setup for complex embankment profiles
- Supports single-slope and double-slope geometries (with berm)
- Generates complete slope coordinate tables automatically
- Step-by-step workflow guidance for first-time users
- Reduces manual pre-processing time from hours to minutes
- Live cross-section preview visualization

### Module 2: Vertical Caisson Stability Calculator
- Computes sliding, overturning, and bearing capacity factors of safety
- Real-time calculation with professional cross-section visualization
- Pass/fail indicators against standard safety thresholds
- Full step-by-step calculation breakdown
- Exportable plots and reports

### Module 3: Wave Run-Up Calculator v3.0
- Full implementation of EurOtop 2018, JTS 154-1-2011, and GB 50286-2013
- Calculates Ru2%, Ru1%, wave reflection coefficient (Cr)
- Calculates mean overtopping discharge (q)
- Classifies breaker type (Spilling, Plunging, Collapsing, Surging)
- Built-in roughness factor reference library
- Obliquity factor calculation for angled wave attack

---

## Live App

**[Launch HYRCAN Engineering Suite](https://hyrcan-suite-geotf68jxfjqcrnp5rbvbv.streamlit.app)**

---

## Installation (Local)

```bash
git clone https://github.com/Mathias-lab/hyrcan-suite.git
cd hyrcan-suite
pip install -r requirements.txt
streamlit run "HYRCAN_Engineering_Suite v3.0.py"
