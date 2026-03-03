# dashboard/app/app.py
import os
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ----------------------------
# Page config
# ----------------------------
st.set_page_config(
    page_title="Smart Agriculture Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------
# Minimal UI styling (formal)
# ----------------------------
CSS = """
<style>
.block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 1200px; }
h1, h2, h3 { letter-spacing: -0.01em; }
.small-note { color: #6b7280; font-size: 0.9rem; }
.section-title { display: flex; align-items: center; gap: 0.6rem; margin-top: 0.2rem; }
.icon { width: 18px; height: 18px; color: #111827; }

.card {
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 12px 14px;
  background: #ffffff;
  height: 100%;
  margin-bottom: 0.75rem;
}
.card-top { display: flex; align-items: center; justify-content: space-between; gap: 0.75rem; }
.card-label { color: #6b7280; font-size: 0.85rem; margin: 0; }
.card-value { font-size: 1.35rem; font-weight: 700; margin: 0.2rem 0 0.2rem; color: #111827; }
.card-sub { color: #6b7280; font-size: 0.82rem; margin: 0; }
.badge {
  display: inline-flex; align-items: center; gap: 0.35rem;
  border-radius: 999px; padding: 0.15rem 0.5rem; font-size: 0.8rem;
  border: 1px solid #e5e7eb; background: #f9fafb; color: #374151;
}
.hr { border-top: 1px solid #eef2f7; margin: 1rem 0; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ----------------------------
# Heroicons (inline SVG)
# ----------------------------
HEROICONS = {
    "chart_bar": """<svg class="icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M3 3v18h18M9 17V9m4 8V5m4 12v-7"/>
    </svg>""",
    "droplet": """<svg class="icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M12 3s6 6 6 11a6 6 0 11-12 0c0-5 6-11 6-11z"/>
    </svg>""",
    "thermometer": """<svg class="icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M10 14.5V5a2 2 0 114 0v9.5a4 4 0 11-4 0z"/>
    </svg>""",
    "chip": """<svg class="icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M9 3v2m6-2v2M9 19v2m6-2v2M3 9h2m-2 6h2m14-6h2m-2 6h2M8 7h8a2 2 0 012 2v8a2 2 0 01-2 2H8a2 2 0 01-2-2V9a2 2 0 012-2z"/>
    </svg>""",
    "exclamation": """<svg class="icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M12 9v4m0 4h.01M10.29 3.86l-7.4 12.82A2 2 0 004.62 20h14.76a2 2 0 001.73-3.32l-7.4-12.82a2 2 0 00-3.46 0z"/>
    </svg>""",
}

def icon(name: str) -> str:
    return HEROICONS.get(name, "")

def section_header(icon_name: str, title: str, note: str | None = None):
    st.markdown(
        f"""
        <div class="section-title">
            {icon(icon_name)}
            <h3 style="margin:0;">{title}</h3>
        </div>
        {f'<div class="small-note">{note}</div>' if note else ''}
        """,
        unsafe_allow_html=True,
    )

def card_html(label: str, value: str, sub: str = "", icon_name: str = "chip") -> str:
    return f"""
    <div class="card">
      <div class="card-top">
        <div>
          <p class="card-label">{label}</p>
          <p class="card-value">{value}</p>
          <p class="card-sub">{sub}</p>
        </div>
        <div class="badge">{icon(icon_name)}<span>Metric</span></div>
      </div>
    </div>
    """

# ----------------------------
# Data path (works from dashboard/app/)
# ----------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
DATA_PATH = os.path.join(BASE_DIR, "outputs", "cleaned_data.csv")

@st.cache_data(show_spinner=False)
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

# ----------------------------
# Header
# ----------------------------
st.title("Smart Agriculture Dashboard")
st.markdown(
    '<div class="small-note">Source: cleaned dataset stored in <code>outputs/cleaned_data.csv</code></div>',
    unsafe_allow_html=True,
)

if not os.path.exists(DATA_PATH):
    st.error(f"File not found: {DATA_PATH}. Ensure it exists in the repository.")
    st.stop()

df = load_data(DATA_PATH)

required = {"crop_id", "soil_type", "seedling_stage", "moi", "temp", "humidity", "result"}
missing_cols = required - set(df.columns)
if missing_cols:
    st.error(f"Missing required columns: {sorted(list(missing_cols))}. Available: {df.columns.tolist()}")
    st.stop()

# Types
for c in ["moi", "temp", "humidity", "result"]:
    df[c] = pd.to_numeric(df[c], errors="coerce")

df["crop_id"] = df["crop_id"].astype(str).str.strip()
df["soil_type"] = df["soil_type"].astype(str).str.strip()
df["seedling_stage"] = df["seedling_stage"].astype(str).str.strip().str.lower()

# Stage ordering (time-like proxy)
stage_priority = ["germination","seedling","vegetative","budding","flowering","fruiting","harvesting","maturity"]
stages = df["seedling_stage"].unique().tolist()
order = [s for s in stage_priority if s in stages] + [s for s in sorted(stages) if s not in stage_priority]
df["seedling_stage"] = pd.Categorical(df["seedling_stage"], categories=order, ordered=True)

# ----------------------------
# Sidebar
# ----------------------------
st.sidebar.header("Filters")
crop_opt = ["All"] + sorted(df["crop_id"].unique().tolist())
soil_opt = ["All"] + sorted(df["soil_type"].unique().tolist())

selected_crop = st.sidebar.selectbox("Crop", crop_opt, index=0)
selected_soil = st.sidebar.selectbox("Soil type", soil_opt, index=0)
threshold = st.sidebar.slider("Humidity threshold (alert below)", 0, 100, 45)

dff = df.copy()
if selected_crop != "All":
    dff = dff[dff["crop_id"] == selected_crop]
if selected_soil != "All":
    dff = dff[dff["soil_type"] == selected_soil]

if dff.empty:
    st.warning("No data for the selected filters.")
    st.stop()

# Current record (no timestamp)
current = dff.iloc[-1]
current_h = float(current["humidity"]) if pd.notnull(current["humidity"]) else np.nan
current_t = float(current["temp"]) if pd.notnull(current["temp"]) else np.nan
current_m = float(current["moi"]) if pd.notnull(current["moi"]) else np.nan

# ----------------------------
# KPI (fixed layout using st.columns)
# ----------------------------
st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
section_header("chip", "Key metrics", "Metrics are computed on filtered data.")

k1, k2, k3, k4 = st.columns(4, gap="small")
with k1:
    st.markdown(card_html("Rows (filtered)", f"{len(dff):,}", "Number of records after filters.", "chip"), unsafe_allow_html=True)
with k2:
    st.markdown(card_html("Current humidity", f"{current_h:.1f}", "Last record humidity value.", "droplet"), unsafe_allow_html=True)
with k3:
    st.markdown(card_html("Current temperature", f"{current_t:.1f}", "Last record temperature value.", "thermometer"), unsafe_allow_html=True)
with k4:
    st.markdown(card_html("Current moisture index", f"{current_m:.1f}", "Last record MOI value.", "chip"), unsafe_allow_html=True)

# ----------------------------
# Alert system
# ----------------------------
section_header("exclamation", "Alert system", "Alert triggers when current humidity is below the threshold.")
if pd.notnull(current_h) and current_h < threshold:
    st.error(f"Alert: current humidity ({current_h:.1f}) is below threshold ({threshold}).")
else:
    st.success(f"Status OK: current humidity ({current_h:.1f}) is at or above threshold ({threshold}).")

# ----------------------------
# Visualizations
# ----------------------------
st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    section_header("droplet", "Gauge: current humidity")
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=current_h if pd.notnull(current_h) else 0,
        gauge={
            "axis": {"range": [0, 100]},
            "threshold": {"line": {"color": "red", "width": 3}, "value": threshold},
            "bar": {"color": "#111827"},
        },
        title={"text": "Humidity (%)"}
    ))
    fig_gauge.update_layout(margin=dict(l=10, r=10, t=50, b=10), height=340)
    st.plotly_chart(fig_gauge, use_container_width=True)

with col2:
    section_header(
        "chart_bar",
        "Trend: sensor averages by seedling stage",
        "No timestamp available; stage ordering is used as a trend proxy."
    )
    stage_means = (
        dff.groupby("seedling_stage")[["moi", "temp", "humidity"]]
        .mean()
        .reset_index()
        .dropna()
    )
    fig_trend = px.line(
        stage_means,
        x="seedling_stage",
        y=["moi", "temp", "humidity"],
        markers=True,
    )
    fig_trend.update_layout(
        xaxis_title="Seedling stage",
        yaxis_title="Mean value",
        margin=dict(l=10, r=10, t=10, b=10),
        height=340,
        legend_title_text="Sensor"
    )
    st.plotly_chart(fig_trend, use_container_width=True)

section_header("chart_bar", "Correlation heatmap", "Correlation between sensor variables and result.")
num = dff[["moi", "temp", "humidity", "result"]].dropna()
corr = num.corr(numeric_only=True)

fig_heat = px.imshow(
    corr,
    text_auto=".2f",
    aspect="auto",
)
fig_heat.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=380)
st.plotly_chart(fig_heat, use_container_width=True)

# ----------------------------
# Data preview + download
# ----------------------------
st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
section_header("chip", "Data preview", "First rows of filtered dataset.")
st.dataframe(dff.head(30), use_container_width=True)

st.download_button(
    label="Download filtered dataset (CSV)",
    data=dff.to_csv(index=False).encode("utf-8"),
    file_name="filtered_data.csv",
    mime="text/csv",
)

st.markdown(
    '<div class="small-note">Note: "current" refers to the last record due to absence of timestamp.</div>',
    unsafe_allow_html=True
)