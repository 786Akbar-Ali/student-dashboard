"""
====================================================
  Student Exam Score Dashboard — Streamlit App
  Run:  streamlit run app.py
====================================================
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0f1117; }
    .metric-card {
        background: linear-gradient(135deg, #1e2130, #2a2d3e);
        border-radius: 12px;
        padding: 18px 22px;
        border-left: 4px solid #4fc3f7;
        margin-bottom: 10px;
    }
    .metric-value { font-size: 2rem; font-weight: 700; color: #4fc3f7; }
    .metric-label { font-size: 0.85rem; color: #9e9e9e; margin-top: 4px; }
    h1, h2, h3 { color: #e8eaf6 !important; }
    .stSelectbox label, .stSlider label, .stMultiSelect label { color: #b0bec5 !important; }
</style>
""", unsafe_allow_html=True)

COLORS = ["#4fc3f7", "#81c784", "#ffb74d", "#e57373", "#ce93d8", "#80cbc4"]

# ─── Load & Enrich Data ───────────────────────────────────────────────────────
@st.cache_data
def load_data():
    import os
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), "17_student_exam_scores.csv"))

    df["performance_grade"] = pd.cut(
        df["exam_score"],
        bins=[0, 25, 30, 35, 40, 100],
        labels=["F (<25)", "D (25-30)", "C (30-35)", "B (35-40)", "A (40+)"],
    )
    df["study_category"] = pd.cut(
        df["hours_studied"],
        bins=[0, 4, 8, 13],
        labels=["Low (0-4h)", "Medium (4-8h)", "High (8+h)"],
    )
    df["sleep_quality"] = pd.cut(
        df["sleep_hours"],
        bins=[0, 5.5, 7.5, 10],
        labels=["Poor", "Fair", "Good"],
    )
    df["pass_fail"] = df["exam_score"].apply(lambda x: "Pass" if x >= 30 else "Fail")
    df["improvement_gap"] = df["exam_score"] - df["previous_scores"]
    df["attendance_band"] = pd.cut(
        df["attendance_percent"],
        bins=[0, 60, 75, 90, 101],
        labels=["Low", "Average", "Good", "Excellent"],
    )
    return df


df = load_data()

# ─── Sidebar Filters ─────────────────────────────────────────────────────────
st.sidebar.image(
    "https://img.icons8.com/fluency/96/graduation-cap.png", width=70
)
st.sidebar.title("🎓 Dashboard Filters")

study_filter = st.sidebar.multiselect(
    "Study Category",
    options=df["study_category"].dropna().unique().tolist(),
    default=df["study_category"].dropna().unique().tolist(),
)
sleep_filter = st.sidebar.multiselect(
    "Sleep Quality",
    options=df["sleep_quality"].dropna().unique().tolist(),
    default=df["sleep_quality"].dropna().unique().tolist(),
)
score_range = st.sidebar.slider(
    "Exam Score Range",
    min_value=int(df["exam_score"].min()),
    max_value=int(df["exam_score"].max()),
    value=(int(df["exam_score"].min()), int(df["exam_score"].max())),
)
pass_filter = st.sidebar.radio("Show", ["All", "Pass Only", "Fail Only"], horizontal=True)

# ─── Apply Filters ───────────────────────────────────────────────────────────
fdf = df[
    df["study_category"].isin(study_filter)
    & df["sleep_quality"].isin(sleep_filter)
    & df["exam_score"].between(*score_range)
]
if pass_filter == "Pass Only":
    fdf = fdf[fdf["pass_fail"] == "Pass"]
elif pass_filter == "Fail Only":
    fdf = fdf[fdf["pass_fail"] == "Fail"]

# ─── Title ───────────────────────────────────────────────────────────────────
st.title("🎓 Student Performance Dashboard")
st.caption(f"Showing **{len(fdf)}** of **{len(df)}** students after filters")
st.divider()

# ─── KPI Row ─────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
kpi_style = "background:linear-gradient(135deg,#1e2130,#2a2d3e);border-radius:12px;padding:16px;border-left:4px solid {c};text-align:center;"

k1.markdown(
    f'<div style="{kpi_style.format(c="#4fc3f7")}">'
    f'<div style="font-size:1.9rem;font-weight:700;color:#4fc3f7">{len(fdf)}</div>'
    f'<div style="color:#9e9e9e;font-size:0.8rem">Total Students</div></div>',
    unsafe_allow_html=True,
)
k2.markdown(
    f'<div style="{kpi_style.format(c="#81c784")}">'
    f'<div style="font-size:1.9rem;font-weight:700;color:#81c784">{fdf["exam_score"].mean():.1f}</div>'
    f'<div style="color:#9e9e9e;font-size:0.8rem">Avg Exam Score</div></div>',
    unsafe_allow_html=True,
)
pass_rate = (fdf["pass_fail"] == "Pass").mean() * 100
k3.markdown(
    f'<div style="{kpi_style.format(c="#ffb74d")}">'
    f'<div style="font-size:1.9rem;font-weight:700;color:#ffb74d">{pass_rate:.1f}%</div>'
    f'<div style="color:#9e9e9e;font-size:0.8rem">Pass Rate</div></div>',
    unsafe_allow_html=True,
)
k4.markdown(
    f'<div style="{kpi_style.format(c="#ce93d8")}">'
    f'<div style="font-size:1.9rem;font-weight:700;color:#ce93d8">{fdf["hours_studied"].mean():.1f}h</div>'
    f'<div style="color:#9e9e9e;font-size:0.8rem">Avg Study Hours</div></div>',
    unsafe_allow_html=True,
)
top_student = fdf.loc[fdf["exam_score"].idxmax(), "student_id"] if len(fdf) else "—"
k5.markdown(
    f'<div style="{kpi_style.format(c="#e57373")}">'
    f'<div style="font-size:1.9rem;font-weight:700;color:#e57373">{top_student}</div>'
    f'<div style="color:#9e9e9e;font-size:0.8rem">Top Student</div></div>',
    unsafe_allow_html=True,
)

st.divider()

# ─── Row 1: Grade Pie + Study Bar ────────────────────────────────────────────
c1, c2 = st.columns(2)

with c1:
    st.subheader("📊 Grade Distribution")
    grade_counts = fdf["performance_grade"].value_counts().sort_index()
    fig_pie = px.pie(
        values=grade_counts.values,
        names=grade_counts.index,
        color_discrete_sequence=COLORS,
        hole=0.4,
    )
    fig_pie.update_traces(textposition="inside", textinfo="percent+label",
                          marker=dict(line=dict(color="#0f1117", width=2)))
    fig_pie.update_layout(
        paper_bgcolor="#1e2130", plot_bgcolor="#1e2130",
        font_color="#e8eaf6", showlegend=True,
        legend=dict(bgcolor="#1e2130", font_color="#e8eaf6"),
        margin=dict(t=20, b=10),
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with c2:
    st.subheader("📚 Study Category vs Avg Score")
    study_avg = (
        fdf.groupby("study_category", observed=True)["exam_score"]
        .mean()
        .reset_index()
    )
    fig_bar = px.bar(
        study_avg, x="study_category", y="exam_score",
        color="study_category",
        color_discrete_sequence=["#e57373", "#ffb74d", "#81c784"],
        text=study_avg["exam_score"].round(1),
    )
    fig_bar.update_traces(textposition="outside", marker_line_color="#0f1117",
                          marker_line_width=1)
    fig_bar.update_layout(
        paper_bgcolor="#1e2130", plot_bgcolor="#1e2130",
        font_color="#e8eaf6", showlegend=False,
        xaxis=dict(gridcolor="#2e3250"), yaxis=dict(gridcolor="#2e3250"),
        margin=dict(t=20, b=10),
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ─── Row 2: Scatter + Heatmap ────────────────────────────────────────────────
c3, c4 = st.columns(2)

with c3:
    st.subheader("🎯 Study Hours vs Exam Score")
    fig_sc = px.scatter(
        fdf, x="hours_studied", y="exam_score",
        color="attendance_percent",
        color_continuous_scale="YlOrRd",
        size="sleep_hours",
        hover_data=["student_id", "pass_fail", "performance_grade"],
        trendline="ols",
    )
    fig_sc.update_traces(marker=dict(line=dict(color="#0f1117", width=0.5)))
    fig_sc.update_layout(
        paper_bgcolor="#1e2130", plot_bgcolor="#1e2130",
        font_color="#e8eaf6",
        xaxis=dict(gridcolor="#2e3250"), yaxis=dict(gridcolor="#2e3250"),
        coloraxis_colorbar=dict(
            title=dict(text="Attend %", font=dict(color="#e8eaf6")),
            tickfont=dict(color="#e8eaf6"),
        ),
        margin=dict(t=20, b=10),
    )
    st.plotly_chart(fig_sc, use_container_width=True)

with c4:
    st.subheader("🔥 Correlation Heatmap")
    num_cols = ["hours_studied", "sleep_hours", "attendance_percent",
                "previous_scores", "exam_score"]
    corr = fdf[num_cols].corr().round(2)
    fig_heat = px.imshow(
        corr, text_auto=True, color_continuous_scale="RdBu_r",
        aspect="auto", zmin=-1, zmax=1,
    )
    fig_heat.update_layout(
        paper_bgcolor="#1e2130", plot_bgcolor="#1e2130",
        font_color="#e8eaf6",
        coloraxis_colorbar=dict(tickfont=dict(color="#e8eaf6")),
        margin=dict(t=20, b=10),
    )
    st.plotly_chart(fig_heat, use_container_width=True)

# ─── Row 3: Violin + Improvement Histogram ───────────────────────────────────
c5, c6 = st.columns(2)

with c5:
    st.subheader("😴 Sleep Quality vs Exam Score")
    fig_vio = px.violin(
        fdf, x="sleep_quality", y="exam_score",
        color="sleep_quality",
        color_discrete_sequence=["#e57373", "#ffb74d", "#81c784"],
        box=True, points="outliers",
        category_orders={"sleep_quality": ["Poor", "Fair", "Good"]},
    )
    fig_vio.update_layout(
        paper_bgcolor="#1e2130", plot_bgcolor="#1e2130",
        font_color="#e8eaf6", showlegend=False,
        xaxis=dict(gridcolor="#2e3250"), yaxis=dict(gridcolor="#2e3250"),
        margin=dict(t=20, b=10),
    )
    st.plotly_chart(fig_vio, use_container_width=True)

with c6:
    st.subheader("📈 Improvement Gap Distribution")
    fig_hist = px.histogram(
        fdf, x="improvement_gap", nbins=30,
        color_discrete_sequence=["#4fc3f7"],
    )
    fig_hist.add_vline(x=0, line_dash="dash", line_color="#e57373",
                       annotation_text="No Change", annotation_font_color="#e57373")
    fig_hist.add_vline(x=fdf["improvement_gap"].mean(), line_dash="dash",
                       line_color="#81c784",
                       annotation_text=f"Mean={fdf['improvement_gap'].mean():.1f}",
                       annotation_font_color="#81c784")
    fig_hist.update_layout(
        paper_bgcolor="#1e2130", plot_bgcolor="#1e2130",
        font_color="#e8eaf6",
        xaxis=dict(gridcolor="#2e3250"), yaxis=dict(gridcolor="#2e3250"),
        bargap=0.05, margin=dict(t=20, b=10),
    )
    st.plotly_chart(fig_hist, use_container_width=True)

# ─── Row 4: Attendance Bar + Top 10 ──────────────────────────────────────────
c7, c8 = st.columns(2)

with c7:
    st.subheader("🏫 Attendance Band vs Avg Score")
    att_avg = (
        fdf.groupby("attendance_band", observed=True)["exam_score"]
        .mean()
        .reset_index()
    )
    fig_att = px.bar(
        att_avg, x="attendance_band", y="exam_score",
        color="attendance_band",
        color_discrete_sequence=["#e57373", "#ffb74d", "#4fc3f7", "#81c784"],
        text=att_avg["exam_score"].round(1),
    )
    fig_att.update_traces(textposition="outside", marker_line_color="#0f1117",
                          marker_line_width=1)
    fig_att.update_layout(
        paper_bgcolor="#1e2130", plot_bgcolor="#1e2130",
        font_color="#e8eaf6", showlegend=False,
        xaxis=dict(gridcolor="#2e3250"), yaxis=dict(gridcolor="#2e3250"),
        margin=dict(t=20, b=10),
    )
    st.plotly_chart(fig_att, use_container_width=True)

with c8:
    st.subheader("🏆 Top 10 Students by Exam Score")
    top10 = fdf.nlargest(10, "exam_score")[
        ["student_id", "exam_score", "hours_studied", "attendance_percent"]
    ]
    fig_top = px.bar(
        top10.sort_values("exam_score"),
        x="exam_score", y="student_id",
        orientation="h",
        color="exam_score",
        color_continuous_scale="YlGn",
        text="exam_score",
        hover_data=["hours_studied", "attendance_percent"],
    )
    fig_top.update_traces(textposition="outside", marker_line_color="#0f1117")
    fig_top.update_layout(
        paper_bgcolor="#1e2130", plot_bgcolor="#1e2130",
        font_color="#e8eaf6",
        coloraxis_showscale=False,
        xaxis=dict(gridcolor="#2e3250"), yaxis=dict(gridcolor="#2e3250"),
        margin=dict(t=20, b=10),
    )
    st.plotly_chart(fig_top, use_container_width=True)

# ─── Raw Data Table ───────────────────────────────────────────────────────────
st.divider()
with st.expander("📋 View Raw / Filtered Data Table"):
    st.dataframe(
        fdf.reset_index(drop=True),
        use_container_width=True,
        height=350,
    )
    st.download_button(
        "⬇️ Download Filtered CSV",
        fdf.to_csv(index=False),
        file_name="filtered_students.csv",
        mime="text/csv",
    )

st.caption("Built with ❤️ using Streamlit + Plotly | Student Performance Dashboard")
