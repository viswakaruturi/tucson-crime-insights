import streamlit as st
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.data_loader import load_data
import plotly.express as px
 
st.title("🔍 Tucson Crime Insights")
st.markdown("**Data 474 Final Project** | Viswa Sushanth Karuturi | Spring 2026")
st.divider()
 
df = load_data()
 
# ── Top metrics ────────────────────────────────────────────────────────────────
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Incidents", f"{len(df):,}")
col2.metric("Years Covered", f"{df['Year'].min()} – {df['Year'].max()}")
col3.metric("Crime Types", df["UCRDescription"].nunique())
col4.metric("Divisions", df["Division"].nunique())
col5.metric("Wards", df[df["Ward"] != "0"]["Ward"].nunique())
 
st.divider()
 
# ── Two column layout: left = info, right = map ────────────────────────────────
left, right = st.columns([1, 1], gap="large")
 
with left:
    st.markdown("### About this project")
    st.markdown("""
This app explores crime incident records published by the **Tucson Police Department**
covering **2018 through 2025** (2026 excluded as the year is incomplete).
 
Two core questions drive the analysis:
- Can we **predict crime type** from features like time of day, day of week, division, ward, and call source?
- What **spatial and temporal patterns** emerge across different parts of the city?
""")
 
    st.markdown("### Years covered")
    year_counts = df.groupby("Year").size().reset_index(name="Incidents")
    fig_yr = px.bar(
        year_counts, x="Year", y="Incidents",
        color="Incidents", color_continuous_scale="Blues",
        text="Incidents",
    )
    fig_yr.update_traces(texttemplate="%{text:,}", textposition="outside")
    fig_yr.update_layout(
        coloraxis_showscale=False,
        height=260,
        margin=dict(l=0, r=0, t=10, b=20),
        yaxis_title="",
    )
    st.plotly_chart(fig_yr, width="stretch")
 
    st.markdown("### Crime types in this dataset")
    crime_counts = df["UCRDescription"].value_counts().reset_index()
    crime_counts.columns = ["Crime Type", "Incidents"]
    st.dataframe(crime_counts, use_container_width=True, hide_index=True)
 
with right:
    st.markdown("### Tucson Police Divisions")
    st.markdown("The dataset covers four geographic patrol divisions plus a small *Other Jurisdiction* category (excluded from analysis).")
 
    st.image("https://www.tucsonaz.gov/files/sharedassets/public/v/1/police/documents/maps/tpd-divisions.png?dimension=pageimage&w=480", use_container_width=True)
 
    st.markdown("### Incidents by division")
    div_counts = df["Division"].value_counts().reset_index()
    div_counts.columns = ["Division", "Incidents"]
    fig_div = px.bar(
        div_counts, x="Division", y="Incidents",
        color="Division",
        color_discrete_map={
            "West":    "#7CB9E8",
            "Midtown": "#B5D5C5",
            "East":    "#F5DEB3",
            "South":   "#F4A7B9",
        },
        labels={"Incidents": "Incidents"},
    )
    fig_div.update_layout(
        showlegend=False,
        height=220,
        margin=dict(l=0, r=0, t=10, b=20),
        yaxis_title="",
    )
    st.plotly_chart(fig_div, width="stretch")
 
st.divider()
st.caption("**Dataset source:** [Tucson Police Department Open Data Portal](https://policeanalysis.tucsonaz.gov/pages/reported-crimes) · **GitHub:** [viswakaruturi/tucson-crime-insights](https://github.com/viswakaruturi/tucson-crime-insights)")