"""
GuardianAI X — Disaster Intelligence & Response Demo
Run with: streamlit run guardianai_x_hackathon.py

All figures, sensor readings, forecasts, locations, and response outcomes in this
hackathon demo are illustrative simulations, not live emergency-service data.
"""

import math
from datetime import datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ---------------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------------
st.set_page_config(
    page_title="GuardianAI X | Disaster Command",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------
# THEME
# ---------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    :root {
        --bg: #07111f;
        --panel: #0d1b2b;
        --panel-2: #102238;
        --line: rgba(148, 178, 207, .16);
        --muted: #91a5bb;
        --text: #eef6ff;
        --cyan: #45d6e8;
        --blue: #5b8cff;
        --amber: #ffbf69;
        --red: #ff6577;
        --green: #48d6a0;
    }
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }
    .stApp {
        background:
            radial-gradient(900px 500px at 12% -10%, rgba(42, 108, 160, .24), transparent 60%),
            radial-gradient(700px 450px at 100% 0%, rgba(42, 77, 145, .16), transparent 55%),
            var(--bg);
        color: var(--text);
    }
    [data-testid="stHeader"] { background: rgba(7,17,31,.72); }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0b1929 0%, #081321 100%);
        border-right: 1px solid var(--line);
    }
    [data-testid="stSidebar"] * { color: #dceafa; }
    #MainMenu, footer { visibility: hidden; }
    h1, h2, h3, h4 { font-family: 'Space Grotesk', sans-serif !important; letter-spacing: -.03em; }
    h1 { color: var(--text); }
    p, label, .stMarkdown { color: #d7e5f3; }
    .block-container { padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1600px; }
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, rgba(17,39,61,.95), rgba(12,28,44,.92));
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 16px 18px;
        box-shadow: 0 12px 35px rgba(0,0,0,.12);
    }
    div[data-testid="stMetric"] label { color: var(--muted) !important; }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: var(--text) !important;
        font-family: 'Space Grotesk', sans-serif;
    }
    .brand {
        display:flex; align-items:center; gap:12px;
        padding: 8px 4px 22px 4px;
    }
    .brand-mark {
        width:42px; height:42px; border-radius:13px;
        display:flex; align-items:center; justify-content:center;
        background:linear-gradient(135deg, #1d9db5, #4968d8);
        box-shadow:0 8px 25px rgba(69,214,232,.2);
        font-size:21px;
    }
    .brand-name { font-family:'Space Grotesk'; font-size:19px; font-weight:700; color:#f4f9ff; }
    .brand-sub { font-size:10px; color:#8da7c1; letter-spacing:.16em; text-transform:uppercase; }
    .eyebrow {
        color:var(--cyan); font-size:11px; font-weight:700;
        letter-spacing:.18em; text-transform:uppercase; margin-bottom:8px;
    }
    .hero {
        position:relative; overflow:hidden;
        padding:30px 32px; border-radius:22px;
        background:linear-gradient(115deg, rgba(16,48,73,.98), rgba(17,34,62,.95) 58%, rgba(30,43,83,.92));
        border:1px solid rgba(105,185,220,.24);
        box-shadow:0 22px 60px rgba(0,0,0,.2);
        margin-bottom:22px;
    }
    .hero:after {
        content:""; position:absolute; width:330px; height:330px; right:-95px; top:-170px;
        border:1px solid rgba(69,214,232,.18); border-radius:50%;
        box-shadow:0 0 0 35px rgba(69,214,232,.035), 0 0 0 75px rgba(69,214,232,.025);
    }
    .hero h1 { font-size: clamp(28px, 4vw, 43px); margin:0 0 7px 0; }
    .hero p { color:#afc4d9; margin:0; max-width:720px; font-size:15px; }
    .hero-meta { display:flex; gap:10px; flex-wrap:wrap; margin-top:22px; }
    .pill {
        display:inline-flex; align-items:center; gap:7px;
        padding:7px 11px; border-radius:999px; font-size:11px;
        border:1px solid rgba(255,255,255,.13); background:rgba(255,255,255,.06);
        color:#d8eafa;
    }
    .live-dot { width:7px; height:7px; border-radius:50%; background:var(--green); display:inline-block; box-shadow:0 0 10px var(--green); }
    .section-head { display:flex; align-items:center; justify-content:space-between; margin:24px 0 12px; }
    .section-head h3 { margin:0; font-size:19px; }
    .section-note { color:var(--muted); font-size:12px; }
    .panel {
        background:linear-gradient(145deg, rgba(15,34,53,.96), rgba(11,26,42,.96));
        border:1px solid var(--line); border-radius:18px; padding:19px 20px;
        box-shadow:0 14px 35px rgba(0,0,0,.12);
    }
    .panel-title { color:#f0f7ff; font-family:'Space Grotesk'; font-weight:600; font-size:16px; margin-bottom:4px; }
    .panel-sub { color:var(--muted); font-size:12px; margin-bottom:14px; }
    .risk-number { font-family:'Space Grotesk'; font-size:54px; line-height:1; font-weight:700; color:#ff7885; }
    .risk-caption { color:#a9bbcd; font-size:12px; margin-top:7px; }
    .status-row { display:flex; justify-content:space-between; gap:12px; padding:10px 0; border-bottom:1px solid var(--line); font-size:13px; }
    .status-row:last-child { border-bottom:0; }
    .status-good { color:var(--green); font-weight:600; }
    .status-warn { color:var(--amber); font-weight:600; }
    .status-critical { color:var(--red); font-weight:600; }
    .callout {
        border:1px solid rgba(255,191,105,.24);
        border-left:4px solid var(--amber);
        border-radius:13px; padding:15px 17px;
        background:rgba(255,191,105,.07); color:#f4dfbf;
    }
    .callout strong { color:#ffd08b; }
    .success-panel {
        border:1px solid rgba(72,214,160,.25); border-radius:16px;
        background:rgba(72,214,160,.07); padding:18px;
    }
    .step {
        display:flex; gap:12px; align-items:flex-start; padding:12px 0;
        border-bottom:1px solid var(--line);
    }
    .step:last-child { border-bottom:0; }
    .step-no {
        min-width:28px; height:28px; border-radius:9px; display:flex;
        align-items:center; justify-content:center; background:rgba(69,214,232,.12);
        color:var(--cyan); font-weight:700; font-size:12px;
    }
    .step-title { color:#edf6ff; font-weight:600; font-size:13px; }
    .step-desc { color:var(--muted); font-size:12px; margin-top:2px; }
    .small-muted { color:var(--muted); font-size:11px; }
    .stButton > button {
        border:1px solid rgba(69,214,232,.35); border-radius:11px;
        background:linear-gradient(135deg, #147f9a, #3457bd);
        color:white; font-weight:700; min-height:43px;
        box-shadow:0 8px 20px rgba(24,116,160,.18);
    }
    .stButton > button:hover { border-color:#7ce8f3; color:white; }
    .stSelectbox > div > div, .stSlider, .stNumberInput input {
        background-color:#102238 !important;
    }
    [data-testid="stDataFrame"] { border:1px solid var(--line); border-radius:12px; overflow:hidden; }
    .footer-note { color:#6f879f; font-size:10px; text-align:center; margin-top:28px; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------
# DEMO DATA — ILLUSTRATIVE ONLY
# ---------------------------------------------------------------------
SCENARIOS = {
    "Urban flooding · Chennai": {
        "type": "Flood",
        "risk": 91,
        "people": 142000,
        "rainfall": 186,
        "wind": 34,
        "zones": ["North Chennai", "Central Chennai", "South Chennai", "West Chennai"],
        "zone_risk": [91, 76, 58, 43],
        "forecast": [64, 73, 84, 91, 94],
        "advice": "Prioritise low-lying communities, verify shelter capacity, and stage water-rescue teams near the highest-risk corridors.",
        "hazard": "Heavy rainfall and waterlogging",
    },
    "Cyclone landfall · Bay of Bengal": {
        "type": "Cyclone",
        "risk": 86,
        "people": 98000,
        "rainfall": 142,
        "wind": 118,
        "zones": ["Coastal North", "Harbour Belt", "River Delta", "Inland West"],
        "zone_risk": [86, 82, 71, 39],
        "forecast": [48, 61, 74, 86, 90],
        "advice": "Prioritise coastal advisories, confirm evacuation transport, and keep response teams clear of exposed shoreline areas.",
        "hazard": "Cyclonic winds and coastal surge",
    },
    "Industrial incident · Simulated site": {
        "type": "Industrial",
        "risk": 78,
        "people": 26500,
        "rainfall": 12,
        "wind": 21,
        "zones": ["Plant perimeter", "Residential east", "Transit corridor", "Outer zone"],
        "zone_risk": [78, 73, 49, 25],
        "forecast": [32, 46, 59, 71, 78],
        "advice": "Coordinate with site safety officers, validate the affected-area assessment, and route public updates through authorised agencies.",
        "hazard": "Potential hazardous-material release",
    },
    "Landslide early warning · Nilgiris": {
        "type": "Landslide",
        "risk": 83,
        "people": 18400,
        "rainfall": 214,
        "wind": 28,
        "zones": ["Steep-slope settlements", "Hill roads", "Valley communities", "Town centre"],
        "zone_risk": [91, 84, 63, 34],
        "forecast": [46, 59, 72, 83, 88],
        "advice": "Prioritise review of slope-monitoring reports, rainfall advisories, road status, and community access needs with local authorities.",
        "hazard": "Slope instability after intense rainfall",
    },
    "Extreme heatwave · Tamil Nadu": {
        "type": "Heatwave",
        "risk": 79,
        "people": 216000,
        "rainfall": 0,
        "wind": 16,
        "zones": ["Dense urban wards", "Outdoor work areas", "Low-tree-cover zones", "Peri-urban areas"],
        "zone_risk": [88, 82, 73, 48],
        "forecast": [42, 55, 66, 79, 84],
        "advice": "Coordinate public-health messaging, check on people who may need assistance, and review access to cooling and hydration support through local services.",
        "hazard": "Prolonged high-temperature exposure",
    },
}

BASE_RESOURCES = {"Rescue boats": 21, "Drones": 14, "Ambulances": 34, "Medical teams": 12}


def risk_color(score: int) -> str:
    if score >= 80:
        return "#ff6577"
    if score >= 60:
        return "#ffbf69"
    return "#48d6a0"


def section(title: str, note: str = ""):
    st.markdown(
        f'<div class="section-head"><h3>{title}</h3><span class="section-note">{note}</span></div>',
        unsafe_allow_html=True,
    )


def metric_card(label: str, value: str, delta: str, icon: str):
    st.markdown(
        f"""
        <div class="panel" style="padding:16px 18px; min-height:112px;">
          <div style="display:flex;justify-content:space-between;align-items:center;">
            <span class="small-muted">{label}</span><span style="font-size:18px">{icon}</span>
          </div>
          <div style="font-family:'Space Grotesk';font-size:27px;font-weight:700;color:#f1f7ff;margin-top:8px;">{value}</div>
          <div class="small-muted" style="margin-top:2px;">{delta}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def chart_layout(fig, height=320):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color="#b9cadd", size=11),
        margin=dict(l=12, r=12, t=36, b=12),
        height=height,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
    )
    fig.update_xaxes(showgrid=False, zeroline=False, linecolor="rgba(148,178,207,.15)")
    fig.update_yaxes(gridcolor="rgba(148,178,207,.10)", zeroline=False)
    return fig


# ---------------------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div class="brand">
          <div class="brand-mark">🛰️</div>
          <div><div class="brand-name">GuardianAI X</div><div class="brand-sub">Disaster intelligence</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="eyebrow">Workspace</div>', unsafe_allow_html=True)
    page = st.radio(
        "Navigation",
        ["Command Center", "Risk Intelligence", "Multi-Hazard Intelligence", "Response Operations", "Judge Demo"],
        label_visibility="collapsed",
        format_func=lambda x: {
            "Command Center": "◈  Command Center",
            "Risk Intelligence": "⌁  Risk Intelligence",
            "Multi-Hazard Intelligence": "⟷  Multi-Hazard Intelligence",
            "Response Operations": "✣  Response Operations",
            "Judge Demo": "▶  Judge Demo",
        }[x],
    )
    st.markdown("---")
    st.markdown('<div class="eyebrow">Simulation controls</div>', unsafe_allow_html=True)
    scenario_name = st.selectbox("Active scenario", list(SCENARIOS.keys()), index=0)
    rainfall_adjust = st.slider("Hazard intensity", 0, 100, 70, help="Adjusts the illustrative scenario risk score.")
    st.markdown("---")
    st.markdown(
        """
        <div class="panel" style="padding:13px;">
          <div class="small-muted">SYSTEM STATUS</div>
          <div style="margin-top:9px;font-size:13px;"><span class="live-dot"></span> &nbsp;Simulation engine ready</div>
          <div class="small-muted" style="margin-top:7px;">Demo environment · No live emergency connection</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

scenario = SCENARIOS[scenario_name]
adjusted_risk = max(5, min(99, round(scenario["risk"] * (0.55 + rainfall_adjust / 155))))
risk_tint = risk_color(adjusted_risk)
now_label = datetime.now().strftime("%d %b %Y · %H:%M")


# ---------------------------------------------------------------------
# GLOBAL HERO
# ---------------------------------------------------------------------
st.markdown(
    f"""
    <div class="hero">
      <div class="eyebrow">Disaster response operating picture · Demo environment</div>
      <h1>See the signal. Coordinate the response.</h1>
      <p>One operational view for hazard intelligence, community impact, and coordinated emergency response.</p>
      <div class="hero-meta">
        <span class="pill"><span class="live-dot"></span> SIMULATION ONLINE</span>
        <span class="pill">◷ {now_label}</span>
        <span class="pill">⌖ {scenario_name}</span>
        <span class="pill">⚑ {scenario['type'].upper()} SCENARIO</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------
# COMMAND CENTER
# ---------------------------------------------------------------------
if page == "Command Center":
    st.markdown('<div class="eyebrow">01 / Situational awareness</div>', unsafe_allow_html=True)
    st.title("Command Center")
    st.caption("A consolidated view of the active scenario. All values below are simulated for demonstration.")
    st.info("Expanded scenario library: flooding, cyclone, industrial incident, landslide, and extreme heatwave. Open **Multi-Hazard Intelligence** to explore cascading impacts.")

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        metric_card("Composite risk index", f"{adjusted_risk}/100", "Illustrative model output", "◉")
    with k2:
        metric_card("Population in focus", f"{scenario['people']:,}", "Scenario planning estimate", "⌂")
    with k3:
        metric_card("Monitoring nodes", "1,284", "Synthetic sensor network", "⌁")
    with k4:
        metric_card("Response assets", f"{sum(BASE_RESOURCES.values())}", "Illustrative available units", "✣")

    section("Operational picture", "Risk distribution across monitored zones")
    left, right = st.columns([1.05, 1.95], gap="large")
    with left:
        st.markdown(
            f"""
            <div class="panel" style="height:100%;">
              <div class="panel-title">Current threat index</div>
              <div class="panel-sub">Composite scenario severity</div>
              <div class="risk-number" style="color:{risk_tint};">{adjusted_risk}<span style="font-size:20px;color:#9db2c7;"> / 100</span></div>
              <div class="risk-caption">Elevated risk · validate with official local advisories</div>
              <div style="height:10px;background:#1d3044;border-radius:20px;margin:20px 0 12px;overflow:hidden;">
                <div style="height:100%;width:{adjusted_risk}%;background:linear-gradient(90deg,#ffbf69,#ff6577);border-radius:20px;"></div>
              </div>
              <div class="status-row"><span>Hazard profile</span><strong>{scenario['hazard']}</strong></div>
              <div class="status-row"><span>Rainfall input</span><strong>{scenario['rainfall']} mm / 24h*</strong></div>
              <div class="status-row"><span>Wind input</span><strong>{scenario['wind']} km/h*</strong></div>
              <div class="status-row"><span>Confidence</span><strong class="status-warn">Not validated</strong></div>
              <div class="small-muted" style="margin-top:12px;">*Scenario inputs are illustrative, not measured observations.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        df = pd.DataFrame({"Zone": scenario["zones"], "Risk index": scenario["zone_risk"]})
        fig = px.bar(
            df, x="Zone", y="Risk index", color="Risk index",
            color_continuous_scale=["#48d6a0", "#ffbf69", "#ff6577"], range_color=(0, 100),
            text="Risk index",
        )
        fig.update_traces(marker_line_width=0, textposition="outside", textfont_color="#dceafa")
        fig.update_yaxes(range=[0, 112], title=None)
        fig.update_xaxes(title=None)
        fig.update_coloraxes(showscale=False)
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Zone-level exposure</div><div class="panel-sub">Relative prioritisation score · illustrative</div>', unsafe_allow_html=True)
        st.plotly_chart(chart_layout(fig, 300), use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    section("Recommended next actions", "Decision support · human approval required")
    a, b = st.columns([1.35, 1], gap="large")
    with a:
        st.markdown(
            f"""
            <div class="callout">
              <strong>Priority recommendation</strong><br><br>
              {scenario['advice']}
              <div class="small-muted" style="margin-top:10px;">Generated from the selected demo scenario. Confirm with authorised incident command before acting.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with b:
        st.markdown(
            """
            <div class="panel">
              <div class="panel-title">Readiness checklist</div>
              <div class="status-row"><span>Scenario loaded</span><span class="status-good">READY</span></div>
              <div class="status-row"><span>Risk zones ranked</span><span class="status-good">READY</span></div>
              <div class="status-row"><span>Resource plan drafted</span><span class="status-warn">REVIEW</span></div>
              <div class="status-row"><span>Official alert verified</span><span class="status-warn">PENDING</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------------------
# RISK INTELLIGENCE
# ---------------------------------------------------------------------
elif page == "Risk Intelligence":
    st.markdown('<div class="eyebrow">02 / Predictive intelligence</div>', unsafe_allow_html=True)
    st.title("Risk Intelligence")
    st.caption("Explore how changing scenario intensity affects the illustrative risk outlook.")

    c1, c2 = st.columns([1.4, 1], gap="large")
    with c1:
        hours = [0, 3, 6, 12, 18]
        forecast = scenario["forecast"]
        # Scale the illustrative curve based on the intensity control.
        scaled = [max(1, min(99, round(v * (0.65 + rainfall_adjust / 200)))) for v in forecast]
        forecast_df = pd.DataFrame({"Hours from now": hours, "Risk index": scaled})
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=hours, y=scaled, mode="lines+markers",
            line=dict(color="#45d6e8", width=4, shape="spline"),
            marker=dict(size=9, color="#45d6e8", line=dict(color="#d9fbff", width=2)),
            fill="tozeroy", fillcolor="rgba(69,214,232,.10)",
            hovertemplate="T+%{x}h<br>Risk: %{y}/100<extra></extra>",
        ))
        fig.add_hrect(y0=80, y1=100, fillcolor="rgba(255,101,119,.08)", line_width=0)
        fig.add_hline(y=80, line_dash="dot", line_color="#ff6577", annotation_text="High-risk threshold")
        fig.update_xaxes(title="Forecast horizon", tickvals=hours, ticktext=["Now", "+3h", "+6h", "+12h", "+18h"])
        fig.update_yaxes(title="Illustrative risk index", range=[0, 105])
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Scenario risk trajectory</div><div class="panel-sub">Illustrative trend, not a validated forecast</div>', unsafe_allow_html=True)
        st.plotly_chart(chart_layout(fig, 360), use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown(
            f"""
            <div class="panel">
              <div class="panel-title">Model interpretation</div>
              <div class="panel-sub">Selected scenario · {scenario['type']}</div>
              <div style="font-family:'Space Grotesk';font-size:38px;font-weight:700;color:{risk_tint};">{scaled[-1]}<span style="font-size:15px;color:#9db2c7;"> / 100</span></div>
              <div class="small-muted">Illustrative risk at T+18h</div>
              <div class="status-row" style="margin-top:14px;"><span>Primary hazard</span><strong>{scenario['hazard']}</strong></div>
              <div class="status-row"><span>Scenario intensity</span><strong>{rainfall_adjust}%</strong></div>
              <div class="status-row"><span>Escalation threshold</span><strong>80 / 100</strong></div>
              <div class="status-row"><span>Model status</span><strong class="status-warn">Demo simulation</strong></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class="callout">
              <strong>Interpretation guardrail</strong><br>
              This screen demonstrates a possible risk-scoring workflow. Real deployment requires validated data, calibrated models, uncertainty estimates, and review by emergency-management experts.
            </div>
            """,
            unsafe_allow_html=True,
        )

    section("Zone prioritisation", "Use this view to support planning discussions")
    zone_df = pd.DataFrame({
        "Priority": ["P1", "P2", "P3", "P4"],
        "Zone": scenario["zones"],
        "Risk index": scenario["zone_risk"],
        "Suggested review": ["Immediate", "High", "Monitor", "Routine"],
    })
    st.dataframe(
        zone_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Risk index": st.column_config.ProgressColumn("Risk index", min_value=0, max_value=100, format="%d"),
        },
    )


# ---------------------------------------------------------------------
# MULTI-HAZARD INTELLIGENCE
# ---------------------------------------------------------------------
elif page == "Multi-Hazard Intelligence":
    st.markdown('<div class="eyebrow">03 / Cascading impact analysis</div>', unsafe_allow_html=True)
    st.title("Multi-Hazard Intelligence")
    st.caption(
        "Explore how one hazard can create secondary pressures across infrastructure and public services. "
        "This is a conceptual simulation, not a predictive model."
    )

    st.markdown(
        """
        <div class="callout">
          <strong>Scenario chain</strong><br>
          Intense rainfall → urban flooding → transport disruption → possible power interruptions
          → increased pressure on healthcare and response resources.
          <div class="small-muted" style="margin-top:8px;">
            The links are illustrative dependencies for a hackathon demonstration; they are not verified causal forecasts.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    mh1, mh2, mh3 = st.columns(3)
    with mh1:
        rainfall_pressure = st.slider("Rainfall pressure", 0, 100, 72, key="mh_rain")
    with mh2:
        infrastructure_vulnerability = st.slider("Infrastructure vulnerability", 0, 100, 58, key="mh_infra")
    with mh3:
        response_capacity = st.slider("Response capacity", 0, 100, 64, key="mh_capacity")

    # Transparent toy scoring: each downstream score is a weighted combination,
    # deliberately labelled as illustrative rather than an operational forecast.
    flood_pressure = round(0.72 * rainfall_pressure + 0.28 * infrastructure_vulnerability)
    transport_pressure = round(0.58 * flood_pressure + 0.42 * infrastructure_vulnerability)
    power_pressure = round(0.48 * flood_pressure + 0.52 * infrastructure_vulnerability)
    health_pressure = round(0.45 * flood_pressure + 0.30 * transport_pressure + 0.25 * (100 - response_capacity))
    resource_pressure = round(0.55 * health_pressure + 0.45 * (100 - response_capacity))

    cascade = pd.DataFrame({
        "System": ["Rainfall input", "Flood pressure", "Transport disruption", "Power interruption", "Healthcare pressure", "Resource pressure"],
        "Illustrative index": [rainfall_pressure, flood_pressure, transport_pressure, power_pressure, health_pressure, resource_pressure],
        "Stage": ["Primary hazard", "Direct impact", "Secondary impact", "Secondary impact", "Service impact", "Response impact"],
    })

    section("Cascading impact pathway", "Illustrative indices · 0–100")
    left, right = st.columns([1.55, 1], gap="large")
    with left:
        fig = px.bar(
            cascade, x="Illustrative index", y="System", color="Illustrative index",
            orientation="h", range_color=(0, 100), color_continuous_scale=["#48d6a0", "#ffbf69", "#ff6577"],
            text="Illustrative index",
        )
        fig.update_traces(textposition="outside", textfont_color="#dceafa", cliponaxis=False)
        fig.update_xaxes(range=[0, 112], title=None)
        fig.update_yaxes(title=None, autorange="reversed")
        fig.update_coloraxes(showscale=False)
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">System pressure profile</div><div class="panel-sub">The selected assumptions flow through a simple dependency model</div>', unsafe_allow_html=True)
        st.plotly_chart(chart_layout(fig, 390), use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        overall_pressure = round(
            (flood_pressure + transport_pressure + power_pressure + health_pressure + resource_pressure) / 5
        )
        pressure_color = risk_color(overall_pressure)
        st.markdown(
            f"""
            <div class="panel">
              <div class="panel-title">Cascade pressure index</div>
              <div class="panel-sub">Average of simulated downstream system indices</div>
              <div class="risk-number" style="color:{pressure_color};">{overall_pressure}<span style="font-size:20px;color:#9db2c7;"> / 100</span></div>
              <div class="risk-caption">Scenario exploration metric · not a warning level</div>
              <div class="status-row"><span>Flood pressure</span><strong>{flood_pressure}/100</strong></div>
              <div class="status-row"><span>Transport pressure</span><strong>{transport_pressure}/100</strong></div>
              <div class="status-row"><span>Power pressure</span><strong>{power_pressure}/100</strong></div>
              <div class="status-row"><span>Healthcare pressure</span><strong>{health_pressure}/100</strong></div>
              <div class="status-row"><span>Response capacity input</span><strong>{response_capacity}/100</strong></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    section("Dependency sequence", "Discussion prompts for incident planners")
    stages = [
        ("01", "Primary hazard", "Rainfall pressure is the initiating scenario input."),
        ("02", "Direct impact", "Flood pressure combines the hazard input with infrastructure vulnerability."),
        ("03", "Infrastructure effects", "Transport and power indices illustrate possible knock-on service pressures."),
        ("04", "Community services", "Healthcare pressure combines flood, transport, and response-capacity assumptions."),
        ("05", "Response demand", "Resource pressure highlights where planners may want to validate capacity and coordination needs."),
    ]
    for number, title, detail in stages:
        st.markdown(
            f'<div class="step"><div class="step-no">{number}</div><div><div class="step-title">{title}</div><div class="step-desc">{detail}</div></div></div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="callout" style="margin-top:16px;">
          <strong>Human-review checkpoint</strong><br>
          Use this view to structure questions, not to issue alerts or direct operations. Validate each dependency with current official information,
          local infrastructure operators, public-health teams, and authorised incident command.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.dataframe(cascade, use_container_width=True, hide_index=True)


# ---------------------------------------------------------------------
# RESPONSE OPERATIONS
# ---------------------------------------------------------------------
elif page == "Response Operations":
    st.markdown('<div class="eyebrow">04 / Coordinated response</div>', unsafe_allow_html=True)
    st.title("Response Operations")
    st.caption("Plan a response package and review the proposed allocation before any real-world action.")

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Resource allocation planner</div><div class="panel-sub">Adjust the illustrative units assigned to this scenario.</div>', unsafe_allow_html=True)
    r1, r2, r3, r4 = st.columns(4)
    with r1:
        boats = st.number_input("Rescue boats", 0, 100, 21)
    with r2:
        drones = st.number_input("Assessment drones", 0, 100, 14)
    with r3:
        ambulances = st.number_input("Ambulances", 0, 100, 34)
    with r4:
        medical = st.number_input("Medical teams", 0, 100, 12)
    st.markdown("</div>", unsafe_allow_html=True)

    allocations = {"Rescue boats": boats, "Drones": drones, "Ambulances": ambulances, "Medical teams": medical}
    total_units = sum(allocations.values())
    col_a, col_b = st.columns([1.1, 1], gap="large")
    with col_a:
        fig = px.pie(
            names=list(allocations.keys()), values=list(allocations.values()), hole=.66,
            color_discrete_sequence=["#45d6e8", "#668cff", "#ffbf69", "#48d6a0"],
        )
        fig.update_traces(textposition="outside", textinfo="label+value", marker=dict(line=dict(color="#0d1b2b", width=3)))
        fig.add_annotation(text=f"<b>{total_units}</b><br><span style='font-size:11px'>TOTAL UNITS</span>", x=.5, y=.5, showarrow=False, font=dict(color="#eef6ff", size=20))
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Proposed resource mix</div><div class="panel-sub">Distribution of the current planning package</div>', unsafe_allow_html=True)
        st.plotly_chart(chart_layout(fig, 330), use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
    with col_b:
        st.markdown(
            """
            <div class="panel">
              <div class="panel-title">Deployment workflow</div>
              <div class="step"><div class="step-no">01</div><div><div class="step-title">Validate the incident picture</div><div class="step-desc">Confirm conditions with authorised field teams and official sources.</div></div></div>
              <div class="step"><div class="step-no">02</div><div><div class="step-title">Approve resource assignments</div><div class="step-desc">Incident command reviews availability, safety, and coverage.</div></div></div>
              <div class="step"><div class="step-no">03</div><div><div class="step-title">Coordinate dispatch</div><div class="step-desc">Use established emergency channels and local operating procedures.</div></div></div>
              <div class="step"><div class="step-no">04</div><div><div class="step-title">Track and reassess</div><div class="step-desc">Update the situation picture as verified information arrives.</div></div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    section("Proposed allocation summary", "Planning draft only")
    allocation_df = pd.DataFrame({
        "Resource": list(allocations.keys()),
        "Proposed units": list(allocations.values()),
        "Planning status": ["Draft allocation"] * 4,
    })
    st.dataframe(allocation_df, use_container_width=True, hide_index=True)
    if st.button("Generate response plan", use_container_width=True):
        st.session_state["plan_generated"] = True
    if st.session_state.get("plan_generated"):
        st.markdown(
            f"""
            <div class="success-panel">
              <strong style="color:#70e7b5;">Response plan drafted</strong><br>
              <span style="color:#c5d9e8;font-size:13px;">A planning draft for {scenario_name} has been prepared with {total_units} total units. This is not a dispatch order and requires review by authorised incident command.</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------------------
# JUDGE DEMO
# ---------------------------------------------------------------------
elif page == "Judge Demo":
    st.markdown('<div class="eyebrow">05 / Guided product walkthrough</div>', unsafe_allow_html=True)
    st.title("Judge Demo")
    st.caption("A concise end-to-end story: detect → understand cascading impacts → prioritise → coordinate.")

    st.markdown(
        f"""
        <div class="panel" style="padding:24px;">
          <div class="eyebrow">Live scenario playback · simulated</div>
          <div style="font-family:'Space Grotesk';font-size:26px;font-weight:700;color:#f3f8ff;">{scenario_name}</div>
          <div style="color:#a9bfd3;font-size:13px;margin-top:5px;">{scenario['hazard']} · Risk index {adjusted_risk}/100 · {scenario['people']:,} people in the scenario planning area</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")
    if "demo_stage" not in st.session_state:
        st.session_state.demo_stage = 0

    stages = [
        ("Signal detected", "The simulated monitoring layer flags a changing hazard pattern.", "Synthetic sensor events received and grouped."),
        ("Risk assessed", "The intelligence layer scores zones and estimates potential exposure.", "Zone prioritisation and scenario trajectory generated."),
        ("Cascading impacts explored", "The multi-hazard view explores possible knock-on pressures across transport, power, healthcare, and response capacity.", "Dependency pathway and illustrative system-pressure indices displayed."),
        ("Response coordinated", "The operations layer prepares a resource plan for human review.", "Draft response package assembled; no dispatch action taken."),
        ("Situation brief ready", "A concise operational picture is ready for the incident team.", "Key risk, cascading impacts, and response decisions are presented together."),
    ]
    stage = st.session_state.demo_stage
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Walkthrough sequence</div><div class="panel-sub">Advance one stage at a time while presenting to judges.</div>', unsafe_allow_html=True)
    for idx, (name, desc, detail) in enumerate(stages):
        active = idx == stage
        complete = idx < stage
        color = "#48d6a0" if complete else ("#45d6e8" if active else "#61768b")
        icon = "✓" if complete else (str(idx + 1) if not active else "●")
        st.markdown(
            f"""
            <div style="display:flex;gap:13px;align-items:flex-start;padding:13px 0;border-bottom:1px solid rgba(148,178,207,.12);">
              <div style="width:29px;height:29px;border-radius:9px;display:flex;align-items:center;justify-content:center;background:{color}22;color:{color};font-weight:700;">{icon}</div>
              <div style="flex:1;">
                <div style="font-weight:700;color:{'#f2f8ff' if active or complete else '#91a5bb'};">{name}</div>
                <div style="font-size:12px;color:#9db2c7;margin-top:3px;">{desc}</div>
                {f'<div style="font-size:11px;color:#48d6a0;margin-top:5px;">{detail}</div>' if active or complete else ''}
              </div>
              <div style="font-size:10px;color:{color};font-weight:700;">{'DONE' if complete else ('NOW' if active else 'NEXT')}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

    b1, b2, b3 = st.columns([1, 1, 2])
    with b1:
        if st.button("← Previous", disabled=stage == 0, use_container_width=True):
            st.session_state.demo_stage = max(0, stage - 1)
            st.rerun()
    with b2:
        if st.button("Next stage →", disabled=stage == len(stages) - 1, use_container_width=True):
            st.session_state.demo_stage = min(len(stages) - 1, stage + 1)
            st.rerun()
    with b3:
        if st.button("↺ Restart walkthrough", use_container_width=True):
            st.session_state.demo_stage = 0
            st.session_state.pop("plan_generated", None)
            st.rerun()

    if stage == len(stages) - 1:
        st.markdown(
            """
            <div class="success-panel" style="margin-top:18px;">
              <div style="font-family:'Space Grotesk';font-size:23px;font-weight:700;color:#70e7b5;">Operational brief assembled</div>
              <div style="color:#c5d9e8;font-size:13px;margin-top:5px;">GuardianAI X brings hazard context, risk prioritisation, and response planning into one demonstrable workflow.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ---------------------------------------------------------------------
# FOOTER
# ---------------------------------------------------------------------
st.markdown(
    """
    <div class="footer-note">
      GUARDIANAI X · EXPANDED HACKATHON DEMONSTRATION BUILD · SIMULATED DATA ONLY<br>
      Not an operational emergency system. Do not use for real-world dispatch, evacuation, or safety decisions.
    </div>
    """,
    unsafe_allow_html=True,
)
