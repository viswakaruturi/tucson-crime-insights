import streamlit as st
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.data_loader import load_data
import plotly.express as px
import pandas as pd
 
st.title("📊 Exploratory Data Analysis")
st.caption("Explore crime patterns across Tucson from 2018 to 2025.")
 
df = load_data()
 
# ── Sidebar filters ────────────────────────────────────────────────────────────
st.sidebar.header("Filters")
 
years = sorted(df["Year"].unique())
selected_years = st.sidebar.multiselect("Year", years, default=years)
 
divisions = sorted(df["Division"].unique())
selected_divisions = st.sidebar.multiselect("Division", divisions, default=divisions)
 
df_f = df[df["Year"].isin(selected_years) & df["Division"].isin(selected_divisions)]
 
if df_f.empty:
    st.warning("No data matches the current filters.")
    st.stop()
 
# ── 1. Crime type distribution ─────────────────────────────────────────────────
st.subheader("Crime Type Distribution")
 
counts = df_f["UCRDescription"].value_counts().reset_index()
counts.columns = ["UCRDescription", "Count"]
 
fig = px.bar(
    counts,
    x="Count", y="UCRDescription",
    orientation="h",
    color="Count",
    color_continuous_scale="Blues",
    labels={"UCRDescription": "", "Count": "Incidents"},
    text="Count",
)
fig.update_traces(texttemplate="%{text:,}", textposition="outside")
fig.update_layout(
    coloraxis_showscale=False,
    yaxis=dict(categoryorder="total ascending"),
    height=400,
    margin=dict(l=0, r=40, t=20, b=20),
)
st.plotly_chart(fig, width="stretch")
 
# ── 2. Trend over time ─────────────────────────────────────────────────────────
st.subheader("Crime Trend by Year")
 
col1, col2 = st.columns(2)
 
with col1:
    yearly = df_f.groupby("Year").size().reset_index(name="Count")
    fig2 = px.line(
        yearly, x="Year", y="Count",
        markers=True,
        labels={"Count": "Incidents"},
        title="Total incidents per year",
    )
    fig2.add_vrect(x0=2019.5, x1=2021.5, fillcolor="red", opacity=0.1,
                   annotation_text="COVID", annotation_position="top left")
    fig2.update_layout(margin=dict(t=40, b=20))
    st.plotly_chart(fig2, width="stretch")
 
with col2:
    yearly_type = df_f.groupby(["Year", "UCRDescription"]).size().reset_index(name="Count")
    fig3 = px.line(
        yearly_type, x="Year", y="Count",
        color="UCRDescription",
        markers=True,
        labels={"Count": "Incidents", "UCRDescription": "Crime Type"},
        title="Crime type trend by year",
    )
    fig3.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=-0.6, xanchor="left", x=0),
        margin=dict(t=40, b=120),
    )
    st.plotly_chart(fig3, width="stretch")
 
# ── 3. Time of day ─────────────────────────────────────────────────────────────
st.subheader("Time Patterns")
 
col3, col4 = st.columns(2)
 
with col3:
    hourly = df_f.groupby("Hour").size().reset_index(name="Count")
    fig4 = px.bar(
        hourly, x="Hour", y="Count",
        color="Count",
        color_continuous_scale="Oranges",
        labels={"Count": "Incidents", "Hour": "Hour of Day"},
        title="Incidents by hour of day",
    )
    fig4.update_layout(coloraxis_showscale=False, margin=dict(t=40, b=20))
    st.plotly_chart(fig4, width="stretch")
 
with col4:
    day_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    daily = df_f.groupby("Day").size().reindex(day_order).reset_index(name="Count")
    fig5 = px.bar(
        daily, x="Day", y="Count",
        color="Count",
        color_continuous_scale="Oranges",
        labels={"Count": "Incidents"},
        title="Incidents by day of week",
    )
    fig5.update_layout(coloraxis_showscale=False, margin=dict(t=40, b=20))
    st.plotly_chart(fig5, width="stretch")
 
# ── 4. Hour x Crime type heatmap ───────────────────────────────────────────────
st.subheader("Crime Type by Hour of Day")
 
pivot_hour = (
    df_f.groupby(["Hour", "UCRDescription"])
    .size()
    .unstack(fill_value=0)
)
fig6 = px.imshow(
    pivot_hour,
    aspect="auto",
    color_continuous_scale="Blues",
    labels=dict(x="Crime Type", y="Hour", color="Count"),
    title="Heatmap: hour vs crime type",
)
fig6.update_layout(height=450, margin=dict(t=40, b=20))
st.plotly_chart(fig6, width="stretch")
 
# ── 5. Geography ───────────────────────────────────────────────────────────────
st.subheader("Geographic Breakdown")
 
col5, col6 = st.columns(2)
 
with col5:
    div_counts = df_f["Division"].value_counts().reset_index()
    div_counts.columns = ["Division", "Count"]
    fig7 = px.bar(
        div_counts,
        x="Division", y="Count",
        color="Count",
        color_continuous_scale="Teal",
        labels={"Count": "Incidents"},
        title="Incidents by division",
    )
    fig7.update_layout(coloraxis_showscale=False, margin=dict(t=40, b=20))
    st.plotly_chart(fig7, width="stretch")
 
with col6:
    ward_counts = df_f["Ward"].astype(str).value_counts().reset_index()
    ward_counts.columns = ["Ward", "Count"]
    ward_counts = ward_counts.sort_values("Ward")
    fig8 = px.bar(
        ward_counts,
        x="Ward", y="Count",
        color="Count",
        color_continuous_scale="Teal",
        labels={"Count": "Incidents"},
        title="Incidents by ward",
    )
    fig8.update_layout(coloraxis_showscale=False, margin=dict(t=40, b=20))
    st.plotly_chart(fig8, width="stretch")
 
div_pivot = (
    df_f.groupby(["Division", "UCRDescription"])
    .size()
    .unstack(fill_value=0)
)
fig9 = px.imshow(
    div_pivot,
    aspect="auto",
    color_continuous_scale="Blues",
    labels=dict(x="Crime Type", y="Division", color="Count"),
    title="Heatmap: division vs crime type",
    text_auto=True,
)
fig9.update_layout(height=350, margin=dict(t=40, b=20))
st.plotly_chart(fig9, width="stretch")
 
# ── 6. Call source ─────────────────────────────────────────────────────────────
st.subheader("How Crimes Were Reported")
 
col7, col8 = st.columns(2)
 
with col7:
    src_counts = df_f["CallSource"].value_counts().reset_index()
    src_counts.columns = ["CallSource", "Count"]
    fig10 = px.pie(
        src_counts, names="CallSource", values="Count",
        title="Call source breakdown",
        hole=0.4,
    )
    fig10.update_layout(margin=dict(t=40, b=20))
    st.plotly_chart(fig10, width="stretch")
 
with col8:
    src_type = (
        df_f.groupby(["CallSource", "UCRDescription"])
        .size()
        .unstack(fill_value=0)
    )
    fig11 = px.imshow(
        src_type,
        aspect="auto",
        color_continuous_scale="Purples",
        labels=dict(x="Crime Type", y="Call Source", color="Count"),
        title="Heatmap: call source vs crime type",
        text_auto=True,
    )
    fig11.update_layout(height=300, margin=dict(t=40, b=20))
    st.plotly_chart(fig11, width="stretch")
 
# ── 7. Monthly seasonality ─────────────────────────────────────────────────────
st.subheader("Monthly Seasonality")
 
month_order = ["January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]
monthly = df_f.groupby("Month").size().reindex(month_order).reset_index(name="Count")
fig12 = px.bar(
    monthly, x="Month", y="Count",
    color="Count",
    color_continuous_scale="Greens",
    labels={"Count": "Incidents"},
    title="Incidents by month",
)
fig12.update_layout(coloraxis_showscale=False, margin=dict(t=40, b=20))
st.plotly_chart(fig12, width="stretch")
 
# ── 8. COVID comparison ────────────────────────────────────────────────────────
st.subheader("COVID Period Comparison")
 
df_f2 = df_f.copy()
df_f2["Period"] = df_f2["Year"].apply(
    lambda x: "COVID (2020-2021)" if x in [2020, 2021] else "Non-COVID"
)
covid_type = (
    df_f2.groupby(["UCRDescription", "Period"])
    .size()
    .reset_index(name="Count")
)
fig13 = px.bar(
    covid_type,
    x="Count", y="UCRDescription",
    color="Period",
    orientation="h",
    barmode="group",
    labels={"UCRDescription": "", "Count": "Incidents"},
    title="Crime type: COVID vs non-COVID years",
    color_discrete_map={"COVID (2020-2021)": "#ef553b", "Non-COVID": "#636efa"},
)
fig13.update_layout(
    yaxis=dict(categoryorder="total ascending"),
    height=400,
    margin=dict(l=0, r=20, t=40, b=20),
)
st.plotly_chart(fig13, width="stretch")
 
# ── 9. Crime deep dive ─────────────────────────────────────────────────────────
st.divider()
st.subheader("🔎 Crime Deep Dive")
st.caption("Select a crime type to see when, where, and how it occurs.")
 
crime_types = sorted(df_f["UCRDescription"].unique())
selected_crime = st.selectbox("Select crime type", crime_types)
 
dv = df_f[df_f["UCRDescription"] == selected_crime]
 
# summary metrics
total = len(dv)
peak_hour = int(dv["Hour"].value_counts().idxmax())
peak_day  = dv["Day"].value_counts().idxmax()
peak_div  = dv["Division"].value_counts().idxmax()
 
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Incidents", f"{total:,}")
m2.metric("Peak Hour", f"{peak_hour:02d}:00")
m3.metric("Peak Day", peak_day)
m4.metric("Top Division", peak_div)
 
st.markdown("---")
 
# row 1: hour + day
c1, c2 = st.columns(2)
 
with c1:
    h = dv.groupby("Hour").size().reset_index(name="Count")
    f1 = px.bar(
        h, x="Hour", y="Count",
        color="Count", color_continuous_scale="Reds",
        labels={"Count": "Incidents", "Hour": "Hour of Day"},
        title=f"{selected_crime} — by hour of day",
    )
    f1.update_layout(coloraxis_showscale=False, margin=dict(t=40, b=20))
    st.plotly_chart(f1, width="stretch")
 
with c2:
    day_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    d = dv.groupby("Day").size().reindex(day_order).reset_index(name="Count")
    f2 = px.bar(
        d, x="Day", y="Count",
        color="Count", color_continuous_scale="Reds",
        labels={"Count": "Incidents"},
        title=f"{selected_crime} — by day of week",
    )
    f2.update_layout(coloraxis_showscale=False, margin=dict(t=40, b=20))
    st.plotly_chart(f2, width="stretch")
 
# row 2: division + call source
c3, c4 = st.columns(2)
 
with c3:
    div = dv["Division"].value_counts().reset_index()
    div.columns = ["Division", "Count"]
    f3 = px.bar(
        div, x="Division", y="Count",
        color="Count", color_continuous_scale="Reds",
        labels={"Count": "Incidents"},
        title=f"{selected_crime} — by division",
    )
    f3.update_layout(coloraxis_showscale=False, margin=dict(t=40, b=20))
    st.plotly_chart(f3, width="stretch")
 
with c4:
    src = dv["CallSource"].value_counts().reset_index()
    src.columns = ["CallSource", "Count"]
    f4 = px.pie(
        src, names="CallSource", values="Count",
        title=f"{selected_crime} — call source",
        hole=0.4,
    )
    f4.update_layout(margin=dict(t=40, b=20))
    st.plotly_chart(f4, width="stretch")
 
# row 3: month + year trend
c5, c6 = st.columns(2)
 
with c5:
    month_order = ["January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"]
    mo = dv.groupby("Month").size().reindex(month_order).reset_index(name="Count")
    f5 = px.bar(
        mo, x="Month", y="Count",
        color="Count", color_continuous_scale="Reds",
        labels={"Count": "Incidents"},
        title=f"{selected_crime} — by month",
    )
    f5.update_layout(coloraxis_showscale=False, margin=dict(t=40, b=20))
    st.plotly_chart(f5, width="stretch")
 
with c6:
    yr = dv.groupby("Year").size().reset_index(name="Count")
    f6 = px.line(
        yr, x="Year", y="Count",
        markers=True,
        labels={"Count": "Incidents"},
        title=f"{selected_crime} — trend by year",
    )
    f6.add_vrect(x0=2019.5, x1=2021.5, fillcolor="red", opacity=0.1,
                 annotation_text="COVID", annotation_position="top left")
    f6.update_layout(margin=dict(t=40, b=20))
    st.plotly_chart(f6, width="stretch")
 
# row 4: hour x day heatmap
st.markdown("##### Hour vs Day of Week")
pivot_hd = (
    dv.groupby(["Hour", "Day"])
    .size()
    .unstack(fill_value=0)
    .reindex(columns=day_order, fill_value=0)
)
f7 = px.imshow(
    pivot_hd,
    aspect="auto",
    color_continuous_scale="Reds",
    labels=dict(x="Day", y="Hour", color="Count"),
    title=f"{selected_crime} — hour vs day heatmap",
)
f7.update_layout(height=420, margin=dict(t=40, b=20))
st.plotly_chart(f7, width="stretch")
 
# row 5: division x hour heatmap
st.markdown("##### Division vs Hour of Day")
pivot_dh = (
    dv.groupby(["Division", "Hour"])
    .size()
    .unstack(fill_value=0)
)
f8 = px.imshow(
    pivot_dh,
    aspect="auto",
    color_continuous_scale="Reds",
    labels=dict(x="Hour", y="Division", color="Count"),
    title=f"{selected_crime} — division vs hour heatmap",
    text_auto=True,
)
f8.update_layout(height=350, margin=dict(t=40, b=20))
st.plotly_chart(f8, width="stretch")