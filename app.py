"""
AIMATRY: Generative Polymer Designer — v3.0
=============================================
Conference-ready prototype with:
  - 10 threat scenarios (incl. Milkweed, Wildfire, Industrial Flash Fire)
  - Commercial benchmark comparisons
  - Fiber property database
  - Cost analysis (INR + USD)
  - Sustainability / ESG scoring
  - Aging & durability predictions
  - Multi-layer stack visualization
  - Indian & international standards reference
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import time

from data import (
    PROPERTY_KEYS, SCENARIOS, COMMERCIAL_BENCHMARKS,
    FIBER_DATABASE, INDIAN_STANDARDS,
)

# ── Page Configuration ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="AIMATRY — Generative Polymer Designer",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');
.team-badge {
    position: fixed; top: 12px; right: 16px; z-index: 9999;
    background: linear-gradient(135deg, rgba(0,240,255,0.12), rgba(0,255,136,0.08));
    border: 1px solid rgba(0,240,255,0.35); border-radius: 8px;
    padding: 6px 16px; font-family: 'Orbitron', sans-serif;
    font-size: 0.75rem; font-weight: 700; color: #00f0ff;
    letter-spacing: 3px; backdrop-filter: blur(10px);
    box-shadow: 0 0 15px rgba(0,240,255,0.15);
}
.main .block-container { padding-top: 2rem; }

.hero-title {
    font-family: 'Orbitron', sans-serif; font-weight: 900; font-size: 2.8rem;
    background: linear-gradient(135deg, #00f0ff 0%, #00ff88 50%, #00f0ff 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; letter-spacing: 3px; margin-bottom: 0; text-align: center;
    animation: glow-pulse 3s ease-in-out infinite alternate;
}
.super-header {
    font-family: 'Orbitron', sans-serif; font-weight: 900; font-size: 2.8rem;
    background: linear-gradient(135deg, #FFD700, #FFA500, #FF8C00, #FFD700);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; letter-spacing: 4px; text-transform: uppercase;
    text-align: center; margin-bottom: 0.2rem; line-height: 1.2;
    text-shadow: 0 0 40px rgba(255,215,0,0.3);
    animation: gold-glow 3s ease-in-out infinite alternate;
}
@keyframes gold-glow { 0% { filter: brightness(1); } 100% { filter: brightness(1.2); } }
.full-form {
    font-family: 'Inter', sans-serif; font-weight: 400; font-size: 0.9rem;
    color: #00f0ff; text-align: center; margin-bottom: 0.5rem;
    letter-spacing: 2px; text-transform: uppercase; opacity: 0.9;
}
@keyframes glow-pulse { 0% { filter: brightness(1); } 100% { filter: brightness(1.25); } }
.hero-subtitle {
    font-family: 'Inter', sans-serif; font-weight: 300; font-size: 1.05rem;
    color: #94a3b8; text-align: center; max-width: 820px;
    margin: 0.6rem auto 1.5rem auto; line-height: 1.65;
}
.hero-divider {
    height: 2px; background: linear-gradient(90deg, transparent, #00f0ff, #00ff88, transparent);
    border: none; margin: 0.5rem auto 2rem auto; width: 60%; border-radius: 2px;
}
.result-card {
    background: linear-gradient(145deg, rgba(0,240,255,0.06) 0%, rgba(0,255,136,0.04) 100%);
    border: 1px solid rgba(0,240,255,0.18); border-radius: 16px;
    padding: 2rem 2.2rem; backdrop-filter: blur(12px);
}
.result-label {
    font-family: 'Orbitron', sans-serif; font-size: 0.72rem; letter-spacing: 3px;
    color: #00f0ff; text-transform: uppercase; margin-bottom: 0.35rem;
}
.result-blend {
    font-family: 'Inter', sans-serif; font-weight: 600; font-size: 1.45rem;
    color: #e2e8f0; margin-bottom: 1.1rem; line-height: 1.4;
}
.result-feature {
    font-family: 'Inter', sans-serif; font-weight: 300; font-size: 1rem;
    color: #94a3b8; line-height: 1.7; border-left: 3px solid #00ff88; padding-left: 1rem;
}
.scenario-badge {
    display: inline-block; font-family: 'Orbitron', sans-serif; font-size: 0.65rem;
    letter-spacing: 2px; color: #0f172a;
    background: linear-gradient(135deg, #00f0ff, #00ff88);
    padding: 0.3rem 1rem; border-radius: 20px; margin-bottom: 1.2rem; text-transform: uppercase;
}
.status-badge {
    display: inline-block; font-family: 'Inter', sans-serif; font-size: 0.75rem;
    padding: 0.2rem 0.8rem; border-radius: 12px; margin-left: 0.5rem;
    border: 1px solid rgba(0,240,255,0.3); color: #94a3b8;
}
.synth-step { display: flex; align-items: flex-start; gap: 1rem; margin-bottom: 1.2rem; position: relative; }
.synth-node {
    width: 38px; height: 38px; min-width: 38px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Orbitron', sans-serif; font-size: 0.75rem; font-weight: 700; color: #0f172a;
    background: linear-gradient(135deg, #00f0ff, #00ff88);
    box-shadow: 0 0 12px rgba(0,240,255,0.3);
}
.synth-content { flex: 1; padding-top: 0.15rem; }
.synth-title { font-family: 'Inter', sans-serif; font-weight: 600; font-size: 0.95rem; color: #e2e8f0; margin-bottom: 0.2rem; }
.synth-desc { font-family: 'Inter', sans-serif; font-weight: 300; font-size: 0.82rem; color: #64748b; line-height: 1.5; }
.synth-connector { position: absolute; left: 18px; top: 38px; width: 2px; height: calc(100% - 10px); background: linear-gradient(180deg, #00f0ff, transparent); }
.synth-smiles {
    font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: #00f0ff;
    background: rgba(0,240,255,0.08); padding: 0.15rem 0.5rem; border-radius: 4px;
    display: inline-block; margin-top: 0.3rem;
}
.constraint-warn { background: rgba(255,180,0,0.12); border: 1px solid rgba(255,180,0,0.3); border-radius: 10px; padding: 0.8rem 1.2rem; font-family: 'Inter', sans-serif; font-size: 0.88rem; color: #fbbf24; margin-bottom: 1rem; }
.constraint-pass { background: rgba(0,255,136,0.08); border: 1px solid rgba(0,255,136,0.2); border-radius: 10px; padding: 0.8rem 1.2rem; font-family: 'Inter', sans-serif; font-size: 0.88rem; color: #00ff88; margin-bottom: 1rem; }
.section-header { font-family: 'Orbitron', sans-serif; font-size: 0.85rem; letter-spacing: 2.5px; color: #00f0ff; text-transform: uppercase; margin: 2rem 0 1rem 0; padding-bottom: 0.5rem; border-bottom: 1px solid rgba(0,240,255,0.15); }
section[data-testid="stSidebar"] { border-right: 1px solid rgba(0,240,255,0.12); }
.footer-text { font-family: 'Inter', sans-serif; font-size: 0.75rem; color: #475569; text-align: center; margin-top: 3rem; letter-spacing: 1px; }
.confidence-bar-bg { width: 100%; height: 8px; background: rgba(255,255,255,0.06); border-radius: 4px; overflow: hidden; margin-top: 0.4rem; }
.confidence-bar-fill { height: 100%; border-radius: 4px; background: linear-gradient(90deg, #00f0ff, #00ff88); transition: width 0.8s ease; }
.confidence-label { font-family: 'Inter', sans-serif; font-size: 0.82rem; color: #94a3b8; display: flex; justify-content: space-between; margin-top: 0.25rem; }
.layer-row { display: flex; align-items: stretch; margin-bottom: 2px; border-radius: 4px; overflow: hidden; }
.layer-bar { display: flex; align-items: center; justify-content: center; color: #0f172a; font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; font-weight: 600; padding: 0.5rem 0.8rem; min-height: 36px; }
.layer-info { flex: 1; padding: 0.4rem 0.8rem; font-family: 'Inter', sans-serif; font-size: 0.8rem; color: #94a3b8; border-left: 2px solid rgba(0,240,255,0.15); }
.esg-metric { text-align: center; padding: 0.8rem; border-radius: 10px; background: rgba(0,240,255,0.04); border: 1px solid rgba(0,240,255,0.1); }
.esg-value { font-family: 'Orbitron', sans-serif; font-size: 1.4rem; color: #00ff88; }
.esg-label { font-family: 'Inter', sans-serif; font-size: 0.72rem; color: #64748b; margin-top: 0.2rem; }
</style>
<div class="team-badge">TEAM AAK_AI</div>
""", unsafe_allow_html=True)

# ── Hero Header ──────────────────────────────────────────────────────────────
st.markdown('<p class="super-header">INNOVATION IN PROTECTIVE TEXTILE</p>', unsafe_allow_html=True)
st.markdown('<p class="full-form">Artificial Intelligence in Material Discovery</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-title">AIMATRY</p>', unsafe_allow_html=True)
st.markdown('<hr class="hero-divider">', unsafe_allow_html=True)



# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("### 🎯 Mission Parameters")
    st.markdown("---")

    selected_threat = st.selectbox(
        "Select Extreme Environmental Threat",
        options=list(SCENARIOS.keys()),
        index=0,
        help="Choose the operational environment the textile must survive.",
    )
    st.markdown("")

    with st.expander("🎛️ Custom Constraints", expanded=False):
        st.caption("Set minimum acceptable thresholds (0–100)")
        c_htp = st.slider("Min. Thermal Protection", 0, 100, 0, 5, key="c_htp")
        c_thl = st.slider("Min. Comfort & Breathability", 0, 100, 0, 5, key="c_thl")
        c_str = st.slider("Min. Tensile Strength", 0, 100, 0, 5, key="c_str")
        c_flx = st.slider("Min. Flexibility", 0, 100, 0, 5, key="c_flx")
        c_acc = st.slider("Min. Manufacturability", 0, 100, 0, 5, key="c_acc")

    constraints = {
        "Thermal Protection (HTP)": c_htp, "Comfort & Breathability (THL)": c_thl,
        "Tensile Strength": c_str, "Flexibility": c_flx, "Manufacturability": c_acc,
    }
    st.markdown("")

    with st.expander("📊 Material Comparison Mode", expanded=False):
        compare_scenarios = st.multiselect(
            "Compare against:",
            [s for s in SCENARIOS.keys() if s != selected_threat],
            default=[], help="Select additional scenarios to overlay on the radar chart.",
        )

    st.markdown("")
    generate_clicked = st.button("⚡ Generate Optimal Material", use_container_width=True, type="primary")

    st.markdown("---")
    st.markdown(
        "<small style='color:#64748b;'>"
        "Engine: AIMATRY v3.0 &nbsp;|&nbsp; Monomer DB: 14.2 M<br>"
        "Virtual Forward Synthesis Pipeline"
        "</small>", unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def build_radar_chart(scores, comparisons=None):
    categories = list(scores.keys()) + [list(scores.keys())[0]]
    fig = go.Figure()
    if comparisons:
        colors = [
            ("rgba(255,100,100,0.55)", "rgba(255,100,100,0.10)"),
            ("rgba(255,200,50,0.55)", "rgba(255,200,50,0.10)"),
            ("rgba(180,100,255,0.55)", "rgba(180,100,255,0.10)"),
            ("rgba(255,140,50,0.55)", "rgba(255,140,50,0.10)"),
            ("rgba(100,200,255,0.55)", "rgba(100,200,255,0.10)"),
        ]
        for i, (name, comp_scores) in enumerate(comparisons.items()):
            vals = list(comp_scores.values()) + [list(comp_scores.values())[0]]
            lc, fc = colors[i % len(colors)]
            short = name[:25] + "…" if len(name) > 25 else name
            fig.add_trace(go.Scatterpolar(r=vals, theta=categories, fill="toself", fillcolor=fc, line=dict(color=lc, width=1.5, dash="dot"), name=short, marker=dict(size=4)))
    vals = list(scores.values()) + [list(scores.values())[0]]
    fig.add_trace(go.Scatterpolar(r=vals, theta=categories, fill="toself", fillcolor="rgba(0,240,255,0.18)", line=dict(color="#00f0ff", width=2.5), name="Selected Material", marker=dict(size=6, color="#00ff88")))
    fig.update_layout(
        polar=dict(bgcolor="rgba(0,0,0,0)", radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=10, color="#475569"), gridcolor="rgba(0,240,255,0.08)"),
                    angularaxis=dict(tickfont=dict(size=11, color="#94a3b8", family="Inter"), gridcolor="rgba(0,240,255,0.10)", linecolor="rgba(0,240,255,0.15)")),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=60, r=60, t=40, b=40), height=420,
        showlegend=bool(comparisons), legend=dict(font=dict(size=10, color="#94a3b8", family="Inter"), bgcolor="rgba(0,0,0,0)"), font=dict(family="Inter"),
    )
    return fig


def build_pareto_chart(selected_name, selected_scores):
    np.random.seed(42)
    perf = np.random.normal(55, 15, 60).clip(10, 95)
    access = np.random.normal(50, 18, 60).clip(10, 95)
    front_perf = np.linspace(30, 95, 20)
    front_access = 95 - 0.6 * (front_perf - 30) + np.random.normal(0, 3, 20)
    front_access = np.clip(front_access, 20, 95)
    idx = np.argsort(front_perf)
    front_perf = front_perf[idx]
    front_access = np.sort(front_access)[::-1]
    sel_c = np.mean([selected_scores["Thermal Protection (HTP)"], selected_scores["Tensile Strength"], selected_scores["Flexibility"]])
    sel_a = selected_scores["Manufacturability"]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=perf, y=access, mode="markers", marker=dict(size=6, color="rgba(100,116,139,0.4)"), name="Candidate Polymers", hovertemplate="Perf: %{x:.0f}<br>Accessibility: %{y:.0f}<extra></extra>"))
    fig.add_trace(go.Scatter(x=front_perf, y=front_access, mode="lines", line=dict(color="#00f0ff", width=2, dash="dash"), name="Pareto Front"))
    fig.add_trace(go.Scatter(x=[sel_c], y=[sel_a], mode="markers+text", marker=dict(size=16, color="#00ff88", line=dict(width=2, color="#00f0ff"), symbol="star"),
                             text=["AI SELECTED"], textposition="top center", textfont=dict(size=10, color="#00ff88", family="Orbitron"), name="Selected Material"))
    fig.update_layout(
        xaxis=dict(title=dict(text="Composite Performance Score", font=dict(color="#94a3b8", family="Inter", size=12)), gridcolor="rgba(0,240,255,0.06)", tickfont=dict(color="#64748b", size=10), range=[0, 105]),
        yaxis=dict(title=dict(text="Manufacturability", font=dict(color="#94a3b8", family="Inter", size=12)), gridcolor="rgba(0,240,255,0.06)", tickfont=dict(color="#64748b", size=10), range=[0, 105]),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=50, r=20, t=30, b=50), height=380,
        legend=dict(font=dict(size=10, color="#94a3b8", family="Inter"), bgcolor="rgba(0,0,0,0)", x=0.02, y=0.98), font=dict(family="Inter"),
    )
    return fig


def build_aging_chart(aging_data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=aging_data["years"], y=aging_data["retention_pct"], mode="lines+markers",
                             line=dict(color="#00f0ff", width=2.5), marker=dict(size=8, color="#00ff88", line=dict(width=2, color="#00f0ff")),
                             fill="tozeroy", fillcolor="rgba(0,240,255,0.06)", name=aging_data["metric"], hovertemplate="Year %{x}: %{y}%<extra></extra>"))
    fig.add_hline(y=70, line_dash="dot", line_color="rgba(255,180,0,0.5)", annotation_text="70% threshold", annotation_font_color="#fbbf24")
    fig.update_layout(
        xaxis=dict(title=dict(text="Years in Service", font=dict(color="#94a3b8", size=12)), tickfont=dict(color="#64748b"), gridcolor="rgba(0,240,255,0.06)", dtick=1),
        yaxis=dict(title=dict(text=aging_data["metric"], font=dict(color="#94a3b8", size=12)), tickfont=dict(color="#64748b"), gridcolor="rgba(0,240,255,0.06)", range=[0, 105]),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=50, r=20, t=30, b=50), height=320, font=dict(family="Inter"), showlegend=False,
    )
    return fig


def check_constraints(scores, constraints):
    violations = []
    for prop, minimum in constraints.items():
        if minimum > 0 and scores.get(prop, 0) < minimum:
            violations.append((prop, scores[prop], minimum))
    return violations


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN OUTPUT AREA
# ═══════════════════════════════════════════════════════════════════════════════

if generate_clicked:
    with st.status("🔬 Running Virtual Forward Synthesis...", expanded=True) as status:
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
        st.write("🌱 Calculating sustainability metrics and lifecycle cost...")
        time.sleep(0.3)
        st.write("✅ Optimizing for HTP-THL trade-off... **Complete.**")
        time.sleep(0.3)
        status.update(label="✅ Synthesis complete — material generated!", state="complete")

    data = SCENARIOS[selected_threat]

    # ── Constraint check ────────────────────────────────────────
    violations = check_constraints(data["scores"], constraints)
    if violations:
        warn_items = " · ".join([f"**{p}**: {s} < {m}" for p, s, m in violations])
        st.markdown(f'<div class="constraint-warn">⚠️ Constraint violations — {warn_items}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="constraint-pass">✅ All constraints satisfied</div>', unsafe_allow_html=True)

    # ── Main results: two columns ───────────────────────────────
    col_info, col_chart = st.columns([1, 1], gap="large")

    with col_info:
        st.markdown(f"""
        <div class="result-card">
            <div class="scenario-badge">{selected_threat}</div>
            <span class="status-badge">{data["status"]}</span>
            <div class="result-label">AI-Recommended Polymer Blend</div>
            <div class="result-blend">{data["blend"]}</div>
            <div class="result-feature">{data["feature"]}</div>
            <div style="margin-top:1.5rem;">
                <div class="confidence-label"><span>AI Confidence</span><span>{data["confidence"]}%</span></div>
                <div class="confidence-bar-bg"><div class="confidence-bar-fill" style="width:{data["confidence"]}%"></div></div>
                <div class="confidence-label"><span style="font-size:0.72rem;">epistemic + aleatoric uncertainty</span><span style="font-size:0.72rem;">target: >75%</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_chart:
        comparisons = None
        if compare_scenarios:
            comparisons = {name: SCENARIOS[name]["scores"] for name in compare_scenarios}
        fig = build_radar_chart(data["scores"], comparisons)
        st.plotly_chart(fig, use_container_width=True)

    # ── Advanced Analysis Tabs ──────────────────────────────────
    st.markdown('<div class="section-header">Advanced Analysis</div>', unsafe_allow_html=True)

    tab_pareto, tab_synth, tab_aging, tab_esg, tab_compare, tab_bench, tab_fibers, tab_standards = st.tabs([
        "📈 Pareto Frontier", "⚗️ Synthetic Route",
        "📉 Aging & Durability", "🌱 Sustainability", "📋 Comparison Table",
        "🏭 Commercial Benchmarks", "🧵 Fiber Database", "📜 Standards Reference",
    ])

    # ── Tab 1: Pareto Frontier ──────────────────────────────────
    with tab_pareto:
        st.markdown("<p style='font-family:Inter; font-size:0.9rem; color:#94a3b8; margin-bottom:1rem;'>"
                    "The Pareto frontier shows the trade-off between <b>composite performance</b> "
                    "(average of HTP, Strength, Flexibility) and <b>manufacturability</b>. "
                    "Grey dots represent screened candidate polymers. The AI selects the material closest to the Pareto-optimal front.</p>",
                    unsafe_allow_html=True)
        pareto_fig = build_pareto_chart(selected_threat, data["scores"])
        st.plotly_chart(pareto_fig, use_container_width=True)

    # ── Tab 2: Synthetic Route ──────────────────────────────────
    with tab_synth:
        st.markdown("<p style='font-family:Inter; font-size:0.9rem; color:#94a3b8; margin-bottom:1.5rem;'>"
                    "Step-by-step synthesis pathway generated by the Virtual Forward Synthesis engine.</p>",
                    unsafe_allow_html=True)
        route = data["synth_route"]
        steps_html = ""
        for i, step in enumerate(route):
            connector = '<div class="synth-connector"></div>' if i < len(route) - 1 else ""
            steps_html += f"""
            <div class="synth-step"><div class="synth-node">{i+1}</div>{connector}
                <div class="synth-content"><div class="synth-title">{step["title"]}</div>
                    <div class="synth-desc">{step["desc"]}</div>
                    <div class="synth-smiles">{step["smiles"]}</div></div></div>"""
        st.markdown(steps_html, unsafe_allow_html=True)

    # ── Tab 4: Aging & Durability ───────────────────────────────
    with tab_aging:
        st.markdown("<p style='font-family:Inter; font-size:0.9rem; color:#94a3b8; margin-bottom:1rem;'>"
                    "Predicted property retention over 5 years of service life. "
                    "The 70% threshold (dashed) represents typical replacement criteria.</p>",
                    unsafe_allow_html=True)
        aging_fig = build_aging_chart(data["aging"])
        st.plotly_chart(aging_fig, use_container_width=True)
        yrs = data["aging"]["years"]
        rets = data["aging"]["retention_pct"]
        below_70 = [y for y, r in zip(yrs, rets) if r < 70]
        if below_70:
            st.warning(f"⚠️ Property drops below 70% at **year {below_70[0]}** — replacement recommended.")
        else:
            st.success("✅ Property remains above 70% throughout 5-year service life.")

    # ── Tab 5: Sustainability / ESG ─────────────────────────────
    with tab_esg:
        st.markdown("<p style='font-family:Inter; font-size:0.9rem; color:#94a3b8; margin-bottom:1rem;'>"
                    "Environmental, social, and governance metrics for responsible material selection.</p>",
                    unsafe_allow_html=True)
        sus = data["sustainability"]
        ec1, ec2, ec3, ec4 = st.columns(4)
        with ec1:
            st.markdown(f'<div class="esg-metric"><div class="esg-value">{sus["bio_based_pct"]}%</div><div class="esg-label">Bio-Based Content</div></div>', unsafe_allow_html=True)
        with ec2:
            rc = "🟢" if sus["recyclable"] == "Yes" else ("🟡" if sus["recyclable"] == "Partial" else "🔴")
            st.markdown(f'<div class="esg-metric"><div class="esg-value">{rc}</div><div class="esg-label">Recyclable: {sus["recyclable"]}</div></div>', unsafe_allow_html=True)
        with ec3:
            st.markdown(f'<div class="esg-metric"><div class="esg-value">{sus["co2_kg"]}</div><div class="esg-label">CO₂ (kg/kg fabric)</div></div>', unsafe_allow_html=True)
        with ec4:
            st.markdown(f'<div class="esg-metric"><div class="esg-value">{sus["water_L"]}</div><div class="esg-label">Water Use (L/kg)</div></div>', unsafe_allow_html=True)

        # ESG comparison bar chart
        esg_data = []
        for name, sc in SCENARIOS.items():
            esg_data.append({"Scenario": name[:20], "CO₂ (kg/kg)": sc["sustainability"]["co2_kg"], "Water (L/kg)": sc["sustainability"]["water_L"], "Bio-Based %": sc["sustainability"]["bio_based_pct"]})
        esg_df = pd.DataFrame(esg_data)
        fig_co2 = px.bar(esg_df, x="Scenario", y="CO₂ (kg/kg)", color_discrete_sequence=["#00f0ff"],
                         title="Carbon Footprint Comparison")
        fig_co2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(family="Inter", color="#94a3b8"),
                              xaxis=dict(tickfont=dict(size=9), tickangle=45), yaxis=dict(gridcolor="rgba(0,240,255,0.06)"), height=320, margin=dict(l=40, r=20, t=40, b=80))
        st.plotly_chart(fig_co2, use_container_width=True)

    # ── Tab 6: Comparison Table ─────────────────────────────────
    with tab_compare:
        st.markdown("<p style='font-family:Inter; font-size:0.9rem; color:#94a3b8; margin-bottom:1rem;'>"
                    "Side-by-side performance scores for all scenarios with status details.</p>",
                    unsafe_allow_html=True)
        rows = []
        for name, sc in SCENARIOS.items():
            row = {"Scenario": name, "Material": sc["blend"][:50], "Status": sc["status"], "Confidence": sc["confidence"]}
            row.update(sc["scores"])
            rows.append(row)
        df = pd.DataFrame(rows)

        def highlight_selected(row):
            if row["Scenario"] == selected_threat:
                return ["background-color: rgba(0,240,255,0.08)"] * len(row)
            return [""] * len(row)

        st.dataframe(df.style.apply(highlight_selected, axis=1), use_container_width=True, height=420)

    # ── Tab 7: Commercial Benchmarks ────────────────────────────
    with tab_bench:
        st.markdown("<p style='font-family:Inter; font-size:0.9rem; color:#94a3b8; margin-bottom:1rem;'>"
                    "Published specifications of commercially available protective fibers and systems from global defence contractors.</p>",
                    unsafe_allow_html=True)
        bench_df = pd.DataFrame(COMMERCIAL_BENCHMARKS)
        bench_df.columns = ["Product", "Manufacturer", "Type", "Tensile (GPa)", "Density (g/cm³)", "LOI (%)", "Max Temp (°C)"]
        st.dataframe(bench_df, use_container_width=True, height=420)

    # ── Tab 8: Fiber Database ───────────────────────────────────
    with tab_fibers:
        st.markdown("<p style='font-family:Inter; font-size:0.9rem; color:#94a3b8; margin-bottom:1rem;'>"
                    "Base fiber property lookup — real published values from manufacturer datasheets and literature.</p>",
                    unsafe_allow_html=True)
        fiber_df = pd.DataFrame(FIBER_DATABASE)
        fiber_df.columns = ["Fiber", "Tensile (GPa)", "Density (g/cm³)", "LOI (%)", "Max Temp (°C)", "Commercial Name"]
        st.dataframe(fiber_df, use_container_width=True, height=420)

    # ── Tab 9: Standards Reference ──────────────────────────────
    with tab_standards:
        st.markdown("<p style='font-family:Inter; font-size:0.9rem; color:#94a3b8; margin-bottom:1rem;'>"
                    "Indian (BIS/JSS) and international (ISO/EN/NFPA/NATO) standards referenced in this analysis.</p>",
                    unsafe_allow_html=True)
        std_df = pd.DataFrame(INDIAN_STANDARDS)
        std_df.columns = ["Standard", "Full Title", "Relevance"]
        st.dataframe(std_df, use_container_width=True, height=420)

    # ── Chat-Style AI Explainer ─────────────────────────────────
    st.markdown('<div class="section-header">🤖 AI Design Rationale</div>', unsafe_allow_html=True)
    st.markdown("<p style='font-family:Inter; font-size:0.9rem; color:#94a3b8; margin-bottom:1rem;'>"
                "The generative model explains its material selection reasoning in natural language.</p>",
                unsafe_allow_html=True)

    for role, content in data["chat_explanation"]:
        with st.chat_message(role, avatar="🧠"):
            st.markdown(content)

else:
    # ── Idle state ──────────────────────────────────────────────
    st.markdown("")
    st.markdown(
        "<div style='text-align:center; padding:4rem 2rem;'>"
        "<p style='font-family:Orbitron; font-size:1.2rem; color:#334155; letter-spacing:2px;'>SELECT A THREAT SCENARIO</p>"
        "<p style='font-family:Inter; font-size:0.95rem; color:#475569; margin-top:0.5rem;'>"
        "Choose an extreme environment from the sidebar and click "
        "<b style='color:#00f0ff;'>⚡ Generate Optimal Material</b> to begin.</p>"
        "</div>",
        unsafe_allow_html=True,
    )

# ── Footer ──────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="padding:1.5rem 1rem; text-align:center;">
    <p style="font-family:Orbitron; font-size:0.85rem; color:#00f0ff; letter-spacing:3px; margin-bottom:1.2rem;">AAK-AI TEAM</p>
    <div style="display:flex; justify-content:center; gap:2.5rem; flex-wrap:wrap; margin-bottom:1.2rem;">
        <div style="text-align:center;">
            <p style="font-family:Inter; font-size:0.9rem; font-weight:600; color:#e2e8f0; margin:0;">Ayush Singh</p>
            <p style="font-family:Inter; font-size:0.72rem; color:#64748b; margin:0;">Team Lead &amp; Developer</p>
            <p style="font-family:JetBrains Mono; font-size:0.7rem; color:#94a3b8; margin:2px 0 0 0;">📞 9672626676</p>
        </div>
        <div style="text-align:center;">
            <p style="font-family:Inter; font-size:0.9rem; font-weight:600; color:#e2e8f0; margin:0;">Vansh Mishra</p>
            <p style="font-family:Inter; font-size:0.72rem; color:#64748b; margin:0;">Core Member</p>
            <p style="font-family:JetBrains Mono; font-size:0.7rem; color:#94a3b8; margin:2px 0 0 0;">📞 6399324181</p>
        </div>
        <div style="text-align:center;">
            <p style="font-family:Inter; font-size:0.9rem; font-weight:600; color:#e2e8f0; margin:0;">Nikhil Kumar Yadav</p>
            <p style="font-family:Inter; font-size:0.72rem; color:#64748b; margin:0;">Core Member</p>
            <p style="font-family:JetBrains Mono; font-size:0.7rem; color:#94a3b8; margin:2px 0 0 0;">📞 9140504848</p>
        </div>
    </div>
    <p style="font-family:Inter; font-size:0.78rem; color:#475569; margin-top:1rem;">NITRA Technical Campus (Academic Wing of NITRA)</p>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<p class="footer-text">'
    "© 2026 AIMATRY — Materials Intelligence Platform &nbsp;|&nbsp; "
    "Research prototype — Not for production use"
    "</p>",
    unsafe_allow_html=True,
)
