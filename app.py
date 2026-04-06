"""
AIMATRY: Generative Polymer Designer — v2.0
=============================================
A "Wizard of Oz" UI prototype for conference demonstrations.
Features:
  1. AI Material Recommendation + Radar Chart
  2. Custom Constraint Sliders
  3. Multi-Objective Pareto Frontier
  4. Material Comparison Mode (overlay radar)
  5. Synthetic Route Flowchart
  6. Chat-Style AI Explainer

No real ML backend — all outputs are expertly hardcoded.
"""

# ── Imports ──────────────────────────────────────────────────────────────────
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import time
import random

# ── Page Configuration ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="AIMATRY — Generative Polymer Designer",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

    .main .block-container { padding-top: 2rem; }

    /* ── Hero ────────────────────────────────────────────────────── */
    .hero-title {
        font-family: 'Orbitron', sans-serif;
        font-weight: 900; font-size: 2.8rem;
        background: linear-gradient(135deg, #00f0ff 0%, #00ff88 50%, #00f0ff 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-clip: text; letter-spacing: 3px;
        margin-bottom: 0; text-align: center;
        animation: glow-pulse 3s ease-in-out infinite alternate;
    }
    @keyframes glow-pulse {
        0%   { filter: brightness(1); }
        100% { filter: brightness(1.25); }
    }
    .hero-subtitle {
        font-family: 'Inter', sans-serif; font-weight: 300;
        font-size: 1.05rem; color: #94a3b8; text-align: center;
        max-width: 820px; margin: 0.6rem auto 1.5rem auto; line-height: 1.65;
    }
    .hero-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #00f0ff, #00ff88, transparent);
        border: none; margin: 0.5rem auto 2rem auto; width: 60%; border-radius: 2px;
    }

    /* ── Result card ─────────────────────────────────────────────── */
    .result-card {
        background: linear-gradient(145deg, rgba(0,240,255,0.06) 0%, rgba(0,255,136,0.04) 100%);
        border: 1px solid rgba(0,240,255,0.18);
        border-radius: 16px; padding: 2rem 2.2rem; backdrop-filter: blur(12px);
    }
    .result-label {
        font-family: 'Orbitron', sans-serif; font-size: 0.72rem;
        letter-spacing: 3px; color: #00f0ff; text-transform: uppercase;
        margin-bottom: 0.35rem;
    }
    .result-blend {
        font-family: 'Inter', sans-serif; font-weight: 600;
        font-size: 1.45rem; color: #e2e8f0;
        margin-bottom: 1.1rem; line-height: 1.4;
    }
    .result-feature {
        font-family: 'Inter', sans-serif; font-weight: 300;
        font-size: 1rem; color: #94a3b8; line-height: 1.7;
        border-left: 3px solid #00ff88; padding-left: 1rem;
    }
    .scenario-badge {
        display: inline-block; font-family: 'Orbitron', sans-serif;
        font-size: 0.65rem; letter-spacing: 2px; color: #0f172a;
        background: linear-gradient(135deg, #00f0ff, #00ff88);
        padding: 0.3rem 1rem; border-radius: 20px;
        margin-bottom: 1.2rem; text-transform: uppercase;
    }

    /* ── Synthesis route steps ───────────────────────────────────── */
    .synth-step {
        display: flex; align-items: flex-start; gap: 1rem;
        margin-bottom: 1.2rem; position: relative;
    }
    .synth-node {
        width: 38px; height: 38px; min-width: 38px;
        border-radius: 50%; display: flex; align-items: center;
        justify-content: center; font-family: 'Orbitron', sans-serif;
        font-size: 0.75rem; font-weight: 700; color: #0f172a;
        background: linear-gradient(135deg, #00f0ff, #00ff88);
        box-shadow: 0 0 12px rgba(0,240,255,0.3);
    }
    .synth-content {
        flex: 1; padding-top: 0.15rem;
    }
    .synth-title {
        font-family: 'Inter', sans-serif; font-weight: 600;
        font-size: 0.95rem; color: #e2e8f0; margin-bottom: 0.2rem;
    }
    .synth-desc {
        font-family: 'Inter', sans-serif; font-weight: 300;
        font-size: 0.82rem; color: #64748b; line-height: 1.5;
    }
    .synth-connector {
        position: absolute; left: 18px; top: 38px;
        width: 2px; height: calc(100% - 10px);
        background: linear-gradient(180deg, #00f0ff, transparent);
    }
    .synth-smiles {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem; color: #00f0ff;
        background: rgba(0,240,255,0.08);
        padding: 0.15rem 0.5rem; border-radius: 4px;
        display: inline-block; margin-top: 0.3rem;
    }

    /* ── Constraint warning badge ────────────────────────────────── */
    .constraint-warn {
        background: rgba(255,180,0,0.12); border: 1px solid rgba(255,180,0,0.3);
        border-radius: 10px; padding: 0.8rem 1.2rem;
        font-family: 'Inter', sans-serif; font-size: 0.88rem; color: #fbbf24;
        margin-bottom: 1rem;
    }
    .constraint-pass {
        background: rgba(0,255,136,0.08); border: 1px solid rgba(0,255,136,0.2);
        border-radius: 10px; padding: 0.8rem 1.2rem;
        font-family: 'Inter', sans-serif; font-size: 0.88rem; color: #00ff88;
        margin-bottom: 1rem;
    }

    /* ── Section headers ─────────────────────────────────────────── */
    .section-header {
        font-family: 'Orbitron', sans-serif; font-size: 0.85rem;
        letter-spacing: 2.5px; color: #00f0ff; text-transform: uppercase;
        margin: 2rem 0 1rem 0; padding-bottom: 0.5rem;
        border-bottom: 1px solid rgba(0,240,255,0.15);
    }

    /* ── Sidebar polish ──────────────────────────────────────────── */
    section[data-testid="stSidebar"] {
        border-right: 1px solid rgba(0,240,255,0.12);
    }

    /* ── Footer ──────────────────────────────────────────────────── */
    .footer-text {
        font-family: 'Inter', sans-serif; font-size: 0.75rem;
        color: #475569; text-align: center;
        margin-top: 3rem; letter-spacing: 1px;
    }

    /* ── Confidence meter ────────────────────────────────────────── */
    .confidence-bar-bg {
        width: 100%; height: 8px; background: rgba(255,255,255,0.06);
        border-radius: 4px; overflow: hidden; margin-top: 0.4rem;
    }
    .confidence-bar-fill {
        height: 100%; border-radius: 4px;
        background: linear-gradient(90deg, #00f0ff, #00ff88);
        transition: width 0.8s ease;
    }
    .confidence-label {
        font-family: 'Inter', sans-serif; font-size: 0.82rem;
        color: #94a3b8; display: flex; justify-content: space-between;
        margin-top: 0.25rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Hero Header ──────────────────────────────────────────────────────────────
st.markdown('<p class="hero-title">AIMATRY</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-subtitle">'
    "<b>Generative Polymer Designer</b> — Powered by Virtual Forward Synthesis "
    "and Foundational Chemical Language Models (e.g., <em>POLYT5</em>) to "
    "autonomously generate synthetically accessible polymers for next-generation "
    "protective textiles."
    "</p>",
    unsafe_allow_html=True,
)
st.markdown('<hr class="hero-divider">', unsafe_allow_html=True)

# ── Research Prototype Disclaimer ────────────────────────────────────────────
st.info(
    "🔬 **Research Prototype — Conference Demonstration** · "
    "All property scores (HTP, THL, Tensile Strength, Flexibility, Synthetic Accessibility) "
    "are illustrative and normalized on a 0–100 comparative scale for visualization purposes. "
    "Metrics are aligned with ISO 11612 (thermal protection), ISO 13934 (tensile), "
    "and EN ISO 9151 (HTP) frameworks. "
    "This application demonstrates AI-assisted materials discovery workflows and does not "
    "constitute validated experimental data. POLYT5 is a conceptual generative model "
    "for demonstration purposes.",
    icon="ℹ️",
)


# ═══════════════════════════════════════════════════════════════════════════════
# HARDCODED DATA STORE
# ═══════════════════════════════════════════════════════════════════════════════

PROPERTY_KEYS = [
    "Thermal Protection (HTP)",
    "Comfort & Breathability (THL)",
    "Tensile Strength",
    "Flexibility",
    "Synthetic Accessibility",
]

SCENARIOS = {
    "-40°C Arctic Combat": {
        "blend": "Meta-aramid / Aerogel Nanoporous Composite",
        "feature": (
            "Maximizes thermal insulation while retaining high "
            "thermo-physiological comfort (THL)."
        ),
        "scores": {
            "Thermal Protection (HTP)": 85,
            "Comfort & Breathability (THL)": 70,
            "Tensile Strength": 60,
            "Flexibility": 80,
            "Synthetic Accessibility": 90,
        },
        "confidence": 92,
        "synth_route": [
            {
                "title": "Monomer Selection",
                "desc": "Select isophthaloyl chloride and m-phenylenediamine from curated library.",
                "smiles": "c1cc(N)cccc1N + ClC(=O)c1cccc(C(=O)Cl)c1",
            },
            {
                "title": "Interfacial Polycondensation",
                "desc": "Perform step-growth polymerization at aqueous-organic interface (25°C, 2h).",
                "smiles": "→ [—NH-C₆H₄-NH-CO-C₆H₄-CO—]ₙ",
            },
            {
                "title": "Aerogel Nanocomposite Infusion",
                "desc": "Infuse silica aerogel precursor (TEOS) via supercritical CO₂ drying.",
                "smiles": "Si(OC₂H₅)₄ → SiO₂ aerogel matrix",
            },
            {
                "title": "Lamination & Finishing",
                "desc": "Hot-press laminate with PTFE moisture barrier. Apply DWR treatment.",
                "smiles": "Final composite: 420 g/m², λ = 0.018 W/mK",
            },
        ],
        "chat_explanation": [
            ("assistant", "I selected **Meta-aramid** as the base fiber for its excellent inherent flame resistance (LOI > 28%) and thermal stability up to 370°C — critical for Arctic combat where flash fires from equipment are a risk."),
            ("assistant", "The **aerogel nanoporous composite** layer provides a thermal conductivity of just 0.018 W/mK — roughly 3× better than standard batting insulation — while adding only 15% to the total weight."),
            ("assistant", "I specifically optimized for the **HTP-THL trade-off**: most insulating materials trap moisture and reduce comfort. By using a nanoporous structure with 95% porosity, we maintain vapor permeability at 28 m²Pa/W, keeping the THL score at 70."),
            ("assistant", "⚡ Synthetic accessibility score is **90/100** — all monomers are commercially available and the process uses standard interfacial polycondensation. Scale-up risk is minimal."),
        ],
    },
    "High Ballistic Threat": {
        "blend": "Para-aramid / Carbon Nanotube (CNT) Matrix",
        "feature": (
            "Extreme tensile strength and shear thickening "
            "properties upon impact."
        ),
        "scores": {
            "Thermal Protection (HTP)": 50,
            "Comfort & Breathability (THL)": 40,
            "Tensile Strength": 95,
            "Flexibility": 45,
            "Synthetic Accessibility": 75,
        },
        "confidence": 88,
        "synth_route": [
            {
                "title": "Monomer Selection",
                "desc": "Select p-phenylenediamine and terephthaloyl chloride for para-aramid backbone.",
                "smiles": "H₂N-C₆H₄-NH₂ + ClOC-C₆H₄-COCl",
            },
            {
                "title": "Solution Polymerization",
                "desc": "Low-temperature polycondensation in NMP/CaCl₂ solvent system (−10°C, 4h).",
                "smiles": "→ [—NH-C₆H₄-NH-CO-C₆H₄-CO—]ₙ (PPTA)",
            },
            {
                "title": "CNT Doping & Wet Spinning",
                "desc": "Disperse MWCNTs (0.5 wt%) in dope solution. Wet-spin through air-gap into fibers.",
                "smiles": "PPTA/CNT → 12 μm filaments, σ = 3.8 GPa",
            },
            {
                "title": "Weave & STF Impregnation",
                "desc": "2D plain-weave at 34 threads/cm. Impregnate with colloidal silica STF.",
                "smiles": "STF: SiO₂ (450 nm) in PEG-200, φ = 0.61",
            },
        ],
        "chat_explanation": [
            ("assistant", "**Para-aramid (PPTA)** was chosen as the primary fiber because of its exceptional specific strength — 5× stronger than steel per unit weight. It's the gold standard for ballistic protection."),
            ("assistant", "Adding **multi-wall carbon nanotubes (0.5 wt%)** into the fiber spinning dope increases tensile modulus by ~22% and improves energy absorption during high-velocity impact."),
            ("assistant", "The **shear thickening fluid (STF)** is the key innovation: at low strain rates the fabric remains flexible, but upon bullet impact the colloidal suspension immediately rigidifies, distributing energy across a much larger area."),
            ("assistant", "⚠️ Trade-off: comfort and breathability score is **40/100** — this is a rigid, tightly woven system. For prolonged wear, I recommend pairing with a separate comfort liner."),
        ],
    },
    "40% Oxygen-Enriched Lunar Environment": {
        "blend": "Polyimide / Aluminized Mylar Laminate with Auxetic Weave",
        "feature": (
            "Maximum radiation shielding and extreme temperature "
            "variance tolerance."
        ),
        "scores": {
            "Thermal Protection (HTP)": 95,
            "Comfort & Breathability (THL)": 20,
            "Tensile Strength": 80,
            "Flexibility": 60,
            "Synthetic Accessibility": 50,
        },
        "confidence": 79,
        "synth_route": [
            {
                "title": "Monomer Selection",
                "desc": "Select pyromellitic dianhydride (PMDA) and 4,4'-oxydianiline (ODA) for polyimide.",
                "smiles": "PMDA + ODA → Polyamic acid precursor",
            },
            {
                "title": "Thermal Imidization",
                "desc": "Stepwise thermal cure (100°C → 200°C → 350°C) to form rigid polyimide film.",
                "smiles": "→ Kapton-type PI, Tg > 360°C",
            },
            {
                "title": "Auxetic Geometry Patterning",
                "desc": "Laser-cut re-entrant honeycomb pattern for negative Poisson's ratio behavior.",
                "smiles": "ν = −0.7, impact energy absorption ↑ 40%",
            },
            {
                "title": "Aluminized Mylar Integration",
                "desc": "Vacuum-deposit 100 nm Al on PET substrate. Bond to PI layer via plasma activation.",
                "smiles": "Final: ε_IR = 0.04, α_solar = 0.12",
            },
        ],
        "chat_explanation": [
            ("assistant", "The **lunar environment** poses a triple threat: extreme temperature swings (−180°C to +120°C), unfiltered UV/cosmic radiation, and a hyper-oxygenated atmosphere that makes most organics flammable."),
            ("assistant", "**Polyimide (Kapton-type)** was selected for its unmatched thermal stability — it retains mechanical properties from −269°C to +400°C with an LOI > 36% even in oxygen-enriched atmospheres."),
            ("assistant", "The **auxetic weave** is a unique design choice: when stretched, it expands laterally instead of contracting. This means micrometeorite impacts cause the fabric to *thicken* around the puncture, self-sealing the breach."),
            ("assistant", "⚠️ Synthetic accessibility is only **50/100** — the auxetic laser-cutting step requires specialized equipment. This is the primary bottleneck for mass production."),
        ],
    },
    "Deep-Sea Pressure (1000 m Depth)": {
        "blend": "Ultra-High-Molecular-Weight Polyethylene (UHMWPE) / Graphene Oxide Laminate",
        "feature": (
            "Exceptional compressive strength and hydrostatic pressure resistance "
            "while maintaining neutral buoyancy and diver mobility."
        ),
        "scores": {
            "Thermal Protection (HTP)": 55,
            "Comfort & Breathability (THL)": 35,
            "Tensile Strength": 90,
            "Flexibility": 50,
            "Synthetic Accessibility": 65,
        },
        "confidence": 85,
        "synth_route": [
            {
                "title": "Catalytic Polymerization",
                "desc": "Ziegler-Natta catalysis of ethylene to UHMWPE (Mw > 3.5 × 10⁶ g/mol).",
                "smiles": "CH₂=CH₂ →[TiCl₄/Al(C₂H₅)₃] [—CH₂—CH₂—]ₙ",
            },
            {
                "title": "Gel Spinning",
                "desc": "Dissolve in decalin at 150°C, gel-spin and hot-draw at 120°C (draw ratio 80×).",
                "smiles": "→ Dyneema-class fiber, σ = 3.5 GPa",
            },
            {
                "title": "Graphene Oxide Coating",
                "desc": "Layer-by-layer electrostatic deposition of GO nanosheets onto fiber surface.",
                "smiles": "GO + PAH/PSS → 200 nm barrier coating",
            },
            {
                "title": "Pressure Suit Assembly",
                "desc": "Multi-axis braid over rigid joint elements. Seal with vulcanized neoprene gaskets.",
                "smiles": "Rated to 100 bar, neutral buoyancy achieved",
            },
        ],
        "chat_explanation": [
            ("assistant", "At **1000 m depth**, the suit must resist 100 atmospheres of hydrostatic pressure while allowing enough mobility for technical operations — a severe engineering constraint."),
            ("assistant", "**UHMWPE** was selected for its extraordinary specific strength (15× steel) *and* its density of just 0.97 g/cm³ — it actually floats. This is critical for achieving neutral buoyancy without excessive ballast."),
            ("assistant", "The **graphene oxide laminate** serves a dual purpose: it creates an impermeable barrier to water ingress, and it increases compressive stiffness by 35% through inter-layer load transfer."),
            ("assistant", "🔬 The tensile strength score of **90/100** reflects the gel-spun fiber's crystal orientation — over 95% crystallinity along the chain axis."),
        ],
    },
    "Chemical / Biological Warfare (CBRN)": {
        "blend": "Activated Carbon Fiber (ACF) / Selectively Permeable PTFE Membrane",
        "feature": (
            "Multi-spectrum chemical agent adsorption with one-way moisture "
            "vapor transport for sustained wear under full CBRN protocols."
        ),
        "scores": {
            "Thermal Protection (HTP)": 40,
            "Comfort & Breathability (THL)": 60,
            "Tensile Strength": 55,
            "Flexibility": 75,
            "Synthetic Accessibility": 85,
        },
        "confidence": 94,
        "synth_route": [
            {
                "title": "Precursor Fiber Preparation",
                "desc": "Stabilize PAN (polyacrylonitrile) fibers in air at 250°C for 2h.",
                "smiles": "[—CH₂-CH(CN)—]ₙ → cyclized ladder polymer",
            },
            {
                "title": "Activation & Carbonization",
                "desc": "Carbonize at 800°C under N₂, then steam-activate at 900°C.",
                "smiles": "→ ACF, SBET = 1800 m²/g, micropore vol = 0.65 cm³/g",
            },
            {
                "title": "PTFE Membrane Lamination",
                "desc": "Expand PTFE film biaxially (400% stretch). Bond to ACF via dot adhesive.",
                "smiles": "Pore size: 0.2 μm (blocks agents, passes H₂O vapor)",
            },
            {
                "title": "Impregnation & QA Testing",
                "desc": "Impregnate ACF with ASZM-TEDA catalyst for CWA neutralization. LIVE agent test.",
                "smiles": "Breakthrough time: HD mustard > 24h, GB sarin > 24h",
            },
        ],
        "chat_explanation": [
            ("assistant", "The CBRN scenario uniquely demands **selective permeability** — the suit must block chemical warfare agents (molecules ~0.5 nm) while allowing water vapor (~0.27 nm) to escape for wearer comfort."),
            ("assistant", "**Activated carbon fiber** with 1800 m²/g surface area provides massive adsorption capacity. Unlike granular carbon, ACF's micro-pore structure captures agents in < 5 milliseconds of contact."),
            ("assistant", "The **PTFE membrane** acts as the selectivity layer — its 0.2 μm pores are large enough for vapor but block all liquid and aerosol threats. This is the same Gore-Tex principle, military-hardened."),
            ("assistant", "✅ Synthetic accessibility score is **85/100** — this is one of the most manufacturable designs. All components are in active military supply chains, reducing adoption risk significantly."),
        ],
    },
    "Volcanic Proximity (1200°C Radiant Heat)": {
        "blend": "Basalt Fiber / Silica Aerogel Quilted Panel with Zirconia Coating",
        "feature": (
            "Extreme radiant-heat reflection and multi-layer ablative protection "
            "for sustained operations within 10 m of active lava flows."
        ),
        "scores": {
            "Thermal Protection (HTP)": 98,
            "Comfort & Breathability (THL)": 15,
            "Tensile Strength": 70,
            "Flexibility": 30,
            "Synthetic Accessibility": 45,
        },
        "confidence": 76,
        "synth_route": [
            {
                "title": "Basalt Fiber Extrusion",
                "desc": "Melt crushed basalt rock at 1450°C, extrude through platinum-rhodium bushings.",
                "smiles": "SiO₂·Al₂O₃·Fe₂O₃·CaO → 13 μm continuous filament",
            },
            {
                "title": "Aerogel Blanket Preparation",
                "desc": "Cast silica sol-gel into fiber blanket, age, and supercritical-dry.",
                "smiles": "TEOS → SiO₂ aerogel, λ = 0.015 W/mK, ρ = 120 kg/m³",
            },
            {
                "title": "Zirconia Plasma Spray",
                "desc": "Apply 250 μm yttria-stabilized zirconia (YSZ) thermal barrier coating via APS.",
                "smiles": "ZrO₂-8%Y₂O₃, melting point: 2715°C",
            },
            {
                "title": "Quilted Panel Assembly",
                "desc": "Quilt aerogel between basalt-fabric face and aluminized fiberglass lining.",
                "smiles": "Total thickness: 12 mm, mass: 3.2 kg/m²",
            },
        ],
        "chat_explanation": [
            ("assistant", "At **1200°C radiant heat**, ordinary protective fabrics fail within seconds. This design uses three independent thermal defense mechanisms for redundancy."),
            ("assistant", "**Basalt fiber** is nature's fireproof material — it's literally made from volcanic rock. It retains 90% of its strength at 600°C and doesn't melt until 1450°C."),
            ("assistant", "The **YSZ zirconia coating** reflects >85% of infrared radiation and has the lowest thermal conductivity of any known ceramic (~2.0 W/mK). It's the same material used on jet turbine blades."),
            ("assistant", "⚠️ The major trade-off is **flexibility (30/100)** and **comfort (15/100)**. This is essentially a rigid panel system, not a wearable garment. Recommended for proximity suits with exoskeleton support."),
        ],
    },
    "Hypersonic Re-entry (Mach 25+)": {
        "blend": "Carbon-Carbon (C/C) Composite / Phenolic-Impregnated Ablative Layer",
        "feature": (
            "Ultra-high-temperature oxidation resistance with controlled ablation "
            "rate, engineered for thermal shock tolerance above 2500°C."
        ),
        "scores": {
            "Thermal Protection (HTP)": 99,
            "Comfort & Breathability (THL)": 10,
            "Tensile Strength": 85,
            "Flexibility": 15,
            "Synthetic Accessibility": 30,
        },
        "confidence": 71,
        "synth_route": [
            {
                "title": "Carbon Fiber Preform",
                "desc": "3D needle-punch PAN-based carbon fiber felt (density: 0.4 g/cm³).",
                "smiles": "PAN → 1400°C carbonization → 2200°C graphitization",
            },
            {
                "title": "CVI Densification",
                "desc": "Chemical vapor infiltration with methane at 1100°C (6 cycles, ~800h total).",
                "smiles": "CH₄ → C (pyrolytic) + 2H₂, final density: 1.75 g/cm³",
            },
            {
                "title": "Phenolic Ablative Layer",
                "desc": "Impregnate silica-fiber cloth with SC-1008 phenolic resin. Autoclave cure.",
                "smiles": "Ablation rate: 0.05 mm/s at q = 1.5 MW/m²",
            },
            {
                "title": "SiC Oxidation Barrier",
                "desc": "Pack cementation SiC coating at 1650°C to prevent C/C oxidation below 1500°C.",
                "smiles": "Si(g) + C(s) → SiC(s), thickness: 100 μm",
            },
        ],
        "chat_explanation": [
            ("assistant", "**Mach 25+ re-entry** generates surface temperatures exceeding 2500°C — hotter than most materials' melting points. This is the most extreme thermal scenario in the database."),
            ("assistant", "**Carbon-carbon composites** are one of the few materials that actually get *stronger* as temperature increases (up to 2200°C). They were used on the Space Shuttle nose cone for this reason."),
            ("assistant", "The **phenolic ablative layer** is a sacrificial shield — it intentionally decomposes, and the endothermic decomposition reaction absorbs enormous amounts of heat, keeping the inner surface below 200°C."),
            ("assistant", "⚠️ Synthetic accessibility is only **30/100** — CVI densification alone takes 800+ hours per batch. This material costs ~$50,000/kg and is practical only for aerospace applications."),
        ],
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("### 🎯 Mission Parameters")
    st.markdown("---")

    # ── Threat selector ──────────────────────────────────────────
    selected_threat = st.selectbox(
        "Select Extreme Environmental Threat",
        options=list(SCENARIOS.keys()),
        index=0,
        help="Choose the operational environment the textile must survive.",
    )

    st.markdown("")

    # ── Custom Constraint Sliders (Feature 1) ────────────────────
    with st.expander("🎛️ Custom Constraints", expanded=False):
        st.caption("Set minimum acceptable thresholds (0–100)")
        c_htp = st.slider("Min. Thermal Protection", 0, 100, 0, 5, key="c_htp")
        c_thl = st.slider("Min. Comfort & Breathability", 0, 100, 0, 5, key="c_thl")
        c_str = st.slider("Min. Tensile Strength", 0, 100, 0, 5, key="c_str")
        c_flx = st.slider("Min. Flexibility", 0, 100, 0, 5, key="c_flx")
        c_acc = st.slider("Min. Synthetic Accessibility", 0, 100, 0, 5, key="c_acc")

    constraints = {
        "Thermal Protection (HTP)": c_htp,
        "Comfort & Breathability (THL)": c_thl,
        "Tensile Strength": c_str,
        "Flexibility": c_flx,
        "Synthetic Accessibility": c_acc,
    }

    st.markdown("")

    # ── Comparison Mode (Feature 3) ──────────────────────────────
    with st.expander("📊 Material Comparison Mode", expanded=False):
        compare_scenarios = st.multiselect(
            "Compare against:",
            [s for s in SCENARIOS.keys() if s != selected_threat],
            default=[],
            help="Select additional scenarios to overlay on the radar chart.",
        )

    st.markdown("")

    # ── Generate button ──────────────────────────────────────────
    generate_clicked = st.button(
        "⚡ Generate Optimal Material",
        use_container_width=True,
        type="primary",
    )

    st.markdown("---")
    st.markdown(
        "<small style='color:#64748b;'>"
        "Engine: POLYT5 v3.2 &nbsp;|&nbsp; Monomer DB: 14.2 M<br>"
        "Virtual Forward Synthesis Pipeline"
        "</small>",
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def build_radar_chart(scores: dict, comparisons: dict = None) -> go.Figure:
    """Build a radar chart, optionally overlaying comparison traces."""
    categories = list(scores.keys()) + [list(scores.keys())[0]]

    fig = go.Figure()

    # If comparisons exist, draw them first (behind the primary)
    if comparisons:
        comparison_colors = [
            ("rgba(255,100,100,0.55)", "rgba(255,100,100,0.10)"),
            ("rgba(255,200,50,0.55)", "rgba(255,200,50,0.10)"),
            ("rgba(180,100,255,0.55)", "rgba(180,100,255,0.10)"),
            ("rgba(255,140,50,0.55)", "rgba(255,140,50,0.10)"),
            ("rgba(100,200,255,0.55)", "rgba(100,200,255,0.10)"),
        ]
        for i, (name, comp_scores) in enumerate(comparisons.items()):
            vals = list(comp_scores.values()) + [list(comp_scores.values())[0]]
            line_col, fill_col = comparison_colors[i % len(comparison_colors)]
            # Shorten name for legend
            short_name = name[:25] + "…" if len(name) > 25 else name
            fig.add_trace(go.Scatterpolar(
                r=vals, theta=categories, fill="toself",
                fillcolor=fill_col,
                line=dict(color=line_col, width=1.5, dash="dot"),
                name=short_name,
                marker=dict(size=4),
            ))

    # Primary trace
    primary_vals = list(scores.values()) + [list(scores.values())[0]]
    fig.add_trace(go.Scatterpolar(
        r=primary_vals, theta=categories, fill="toself",
        fillcolor="rgba(0, 240, 255, 0.18)",
        line=dict(color="#00f0ff", width=2.5),
        name="Selected Material",
        marker=dict(size=6, color="#00ff88"),
    ))

    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True, range=[0, 100],
                tickfont=dict(size=10, color="#475569"),
                gridcolor="rgba(0,240,255,0.08)",
            ),
            angularaxis=dict(
                tickfont=dict(size=11, color="#94a3b8", family="Inter"),
                gridcolor="rgba(0,240,255,0.10)",
                linecolor="rgba(0,240,255,0.15)",
            ),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=60, r=60, t=40, b=40),
        height=420,
        showlegend=bool(comparisons),
        legend=dict(
            font=dict(size=10, color="#94a3b8", family="Inter"),
            bgcolor="rgba(0,0,0,0)",
        ),
        font=dict(family="Inter"),
    )
    return fig


def build_pareto_chart(selected_name: str, selected_scores: dict) -> go.Figure:
    """
    Build a fake Pareto frontier scatter plot.
    X-axis = Composite Performance, Y-axis = Synthetic Accessibility.
    Shows ~50 candidate materials as grey dots, a Pareto front curve,
    and the selected material highlighted.
    """
    np.random.seed(42)
    n_candidates = 60

    # Generate fake candidate cloud
    perf = np.random.normal(55, 15, n_candidates).clip(10, 95)
    access = np.random.normal(50, 18, n_candidates).clip(10, 95)

    # Pareto front (upper-right envelope)
    # Sort by perf and keep running max of accessibility
    front_perf = np.linspace(30, 95, 20)
    front_access = 95 - 0.6 * (front_perf - 30) + np.random.normal(0, 3, 20)
    front_access = np.clip(front_access, 20, 95)
    # Make it a proper decreasing front
    sort_idx = np.argsort(front_perf)
    front_perf = front_perf[sort_idx]
    front_access = np.sort(front_access)[::-1]

    # Selected material point
    sel_composite = np.mean([
        selected_scores["Thermal Protection (HTP)"],
        selected_scores["Tensile Strength"],
        selected_scores["Flexibility"],
    ])
    sel_access = selected_scores["Synthetic Accessibility"]

    fig = go.Figure()

    # Candidate cloud
    fig.add_trace(go.Scatter(
        x=perf, y=access, mode="markers",
        marker=dict(size=6, color="rgba(100,116,139,0.4)", line=dict(width=0)),
        name="Candidate Polymers",
        hovertemplate="Perf: %{x:.0f}<br>Accessibility: %{y:.0f}<extra></extra>",
    ))

    # Pareto front line
    fig.add_trace(go.Scatter(
        x=front_perf, y=front_access, mode="lines",
        line=dict(color="#00f0ff", width=2, dash="dash"),
        name="Pareto Front",
    ))

    # Selected point (large, glowing)
    fig.add_trace(go.Scatter(
        x=[sel_composite], y=[sel_access], mode="markers+text",
        marker=dict(
            size=16, color="#00ff88",
            line=dict(width=2, color="#00f0ff"),
            symbol="star",
        ),
        text=["AI SELECTED"], textposition="top center",
        textfont=dict(size=10, color="#00ff88", family="Orbitron"),
        name="Selected Material",
        hovertemplate=(
            f"<b>{selected_name[:30]}</b><br>"
            "Composite Perf: %{x:.0f}<br>"
            "Accessibility: %{y:.0f}<extra></extra>"
        ),
    ))

    fig.update_layout(
        xaxis=dict(
            title=dict(
                text="Composite Performance Score",
                font=dict(color="#94a3b8", family="Inter", size=12),
            ),
            gridcolor="rgba(0,240,255,0.06)",
            tickfont=dict(color="#64748b", size=10),
            range=[0, 105],
        ),
        yaxis=dict(
            title=dict(
                text="Synthetic Accessibility",
                font=dict(color="#94a3b8", family="Inter", size=12),
            ),
            gridcolor="rgba(0,240,255,0.06)",
            tickfont=dict(color="#64748b", size=10),
            range=[0, 105],
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=50, r=20, t=30, b=50),
        height=380,
        legend=dict(
            font=dict(size=10, color="#94a3b8", family="Inter"),
            bgcolor="rgba(0,0,0,0)",
            x=0.02, y=0.98,
        ),
        font=dict(family="Inter"),
    )
    return fig


def check_constraints(scores: dict, constraints: dict) -> list:
    """Return list of (property, score, minimum) for any violated constraints."""
    violations = []
    for prop, minimum in constraints.items():
        if minimum > 0 and scores.get(prop, 0) < minimum:
            violations.append((prop, scores[prop], minimum))
    return violations


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN OUTPUT AREA
# ═══════════════════════════════════════════════════════════════════════════════

if generate_clicked:
    # ── Simulated loading with detailed status ───────────────────
    with st.status(
        "🔬 Running Virtual Forward Synthesis...", expanded=True
    ) as status:
        st.write("📂 Loading monomer database (14.2 M entries)...")
        time.sleep(0.7)
        st.write("🧪 Screening monomers for target properties...")
        time.sleep(0.6)
        st.write("⚗️ Running retrosynthetic feasibility analysis...")
        time.sleep(0.5)
        st.write("📊 Evaluating 2,847 viable candidates on Pareto frontier...")
        time.sleep(0.5)
        st.write("🏆 Selecting optimal material from 12 Pareto-dominant solutions...")
        time.sleep(0.4)
        st.write("✅ Optimizing for HTP and THL trade-off... **Complete.**")
        time.sleep(0.3)
        status.update(label="✅ Synthesis complete — material generated!", state="complete")

    # ── Load data ────────────────────────────────────────────────
    data = SCENARIOS[selected_threat]

    # ── Constraint check (Feature 1) ─────────────────────────────
    violations = check_constraints(data["scores"], constraints)

    if violations:
        warn_items = " / ".join(
            f"**{p}** ({s} < {m})" for p, s, m in violations
        )
        st.markdown(
            f'<div class="constraint-warn">'
            f"⚠️ Constraint violation: {warn_items} — "
            f"consider adjusting requirements or exploring alternative threats."
            f"</div>",
            unsafe_allow_html=True,
        )
    else:
        has_active = any(v > 0 for v in constraints.values())
        if has_active:
            st.markdown(
                '<div class="constraint-pass">'
                "✅ All custom constraints satisfied."
                "</div>",
                unsafe_allow_html=True,
            )

    # ══════════════════════════════════════════════════════════════
    # Row 1: Recommendation Card + Radar Chart
    # ══════════════════════════════════════════════════════════════
    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        # Confidence meter
        conf = data["confidence"]
        st.markdown(
            f"""
            <div class="result-card">
                <div class="scenario-badge">{selected_threat}</div>
                <div class="result-label">AI-Generated Material Recommendation</div>
                <div class="result-blend">🧪 {data["blend"]}</div>
                <div class="result-label" style="margin-top:1rem;">Key Performance Feature</div>
                <div class="result-feature">{data["feature"]}</div>
                <div style="margin-top:1.3rem;">
                    <div class="result-label">AI Confidence</div>
                    <div class="confidence-bar-bg">
                        <div class="confidence-bar-fill" style="width:{conf}%;"></div>
                    </div>
                    <div class="confidence-label">
                        <span>Epistemic + Aleatoric</span>
                        <span style="color:#00ff88; font-weight:600;">{conf}%</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_right:
        st.markdown(
            '<p class="result-label" style="margin-bottom:0.5rem;">'
            "Material Property Profile (0-100)</p>",
            unsafe_allow_html=True,
        )
        # Build comparisons dict if any selected
        comp_data = {}
        for comp_name in compare_scenarios:
            comp_data[comp_name] = SCENARIOS[comp_name]["scores"]

        radar_fig = build_radar_chart(
            data["scores"],
            comparisons=comp_data if comp_data else None,
        )
        st.plotly_chart(radar_fig, use_container_width=True)

    # ══════════════════════════════════════════════════════════════
    # Row 2: Tabbed Advanced Features
    # ══════════════════════════════════════════════════════════════
    st.markdown(
        '<div class="section-header">Advanced Analysis</div>',
        unsafe_allow_html=True,
    )

    tab_pareto, tab_synth, tab_compare = st.tabs([
        "📈 Pareto Frontier",
        "⚗️ Synthetic Route",
        "🔄 Comparison Table",
    ])

    # ── Tab 1: Pareto Frontier (Feature 2) ───────────────────────
    with tab_pareto:
        st.markdown(
            "<p style='font-family:Inter; font-size:0.9rem; color:#94a3b8;'>"
            "The Pareto frontier shows the trade-off between <b>composite performance</b> "
            "(average of HTP, Strength, Flexibility) and <b>synthetic accessibility</b>. "
            "Grey dots represent screened candidate polymers. The AI selects the material "
            "closest to the Pareto-optimal front."
            "</p>",
            unsafe_allow_html=True,
        )
        pareto_fig = build_pareto_chart(selected_threat, data["scores"])
        st.plotly_chart(pareto_fig, use_container_width=True)

    # ── Tab 2: Synthetic Route (Feature 4) ───────────────────────
    with tab_synth:
        st.markdown(
            "<p style='font-family:Inter; font-size:0.9rem; color:#94a3b8; "
            "margin-bottom:1.5rem;'>"
            "Step-by-step synthesis pathway generated by the Virtual Forward Synthesis engine. "
            "Each step shows the reaction or process along with key molecular identifiers."
            "</p>",
            unsafe_allow_html=True,
        )

        route = data["synth_route"]
        # Build all steps as ONE html string — avoids Streamlit's per-call
        # rendering bug inside tabs where the last markdown block shows raw HTML.
        steps_html = ""
        for i, step in enumerate(route):
            connector_html = (
                '<div class="synth-connector"></div>' if i < len(route) - 1 else ""
            )
            steps_html += f"""
            <div class="synth-step">
                <div class="synth-node">{i + 1}</div>
                {connector_html}
                <div class="synth-content">
                    <div class="synth-title">{step["title"]}</div>
                    <div class="synth-desc">{step["desc"]}</div>
                    <div class="synth-smiles">{step["smiles"]}</div>
                </div>
            </div>
            """
        st.markdown(steps_html, unsafe_allow_html=True)

    # ── Tab 3: Comparison Table (Feature 3 extended) ─────────────
    with tab_compare:
        st.markdown(
            "<p style='font-family:Inter; font-size:0.9rem; color:#94a3b8; "
            "margin-bottom:1rem;'>"
            "Side-by-side property comparison across all available scenarios. "
            "Use the sidebar <b>Material Comparison Mode</b> to overlay selected "
            "materials on the radar chart."
            "</p>",
            unsafe_allow_html=True,
        )

        # Build comparison dataframe
        comp_rows = []
        for name, sdata in SCENARIOS.items():
            row = {"Scenario": name, "Material Blend": sdata["blend"]}
            row.update(sdata["scores"])
            row["Confidence"] = sdata["confidence"]
            comp_rows.append(row)

        comp_df = pd.DataFrame(comp_rows)
        # Highlight the selected row
        st.dataframe(
            comp_df.style.apply(
                lambda row: [
                    "background-color: rgba(0,240,255,0.1)"
                    if row["Scenario"] == selected_threat
                    else "" for _ in row
                ],
                axis=1,
            ),
            use_container_width=True,
            hide_index=True,
            height=340,
        )

    # ══════════════════════════════════════════════════════════════
    # Row 3: Chat-Style AI Explainer (Feature 5)
    # ══════════════════════════════════════════════════════════════
    st.markdown(
        '<div class="section-header">🤖 AI Design Rationale</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='font-family:Inter; font-size:0.9rem; color:#94a3b8; "
        "margin-bottom:1rem;'>"
        "The POLYT5 model explains its material selection reasoning in natural language."
        "</p>",
        unsafe_allow_html=True,
    )

    for role, message in data["chat_explanation"]:
        with st.chat_message(role, avatar="🧠"):
            st.markdown(message)

else:
    # ── Idle state ───────────────────────────────────────────────
    st.markdown(
        """
        <div style="text-align:center; padding:4rem 1rem;">
            <p style="font-size:3rem; margin-bottom:0.5rem;">🧬</p>
            <p style="font-family:'Inter',sans-serif; font-size:1.1rem;
                      color:#64748b; max-width:500px; margin:0 auto;">
                Select an <b>extreme environmental threat</b> from the
                sidebar, then click <b>⚡ Generate Optimal Material</b>
                to begin autonomous polymer design.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown(
    '<p class="footer-text">'
    "© 2026 AIMATRY Inc. &nbsp;·&nbsp; Generative Polymer Designer "
    "&nbsp;·&nbsp; For demonstration purposes only"
    "</p>",
    unsafe_allow_html=True,
)
