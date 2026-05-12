import streamlit as st
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.data_loader import load_data
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json

st.title("Exploration")
st.markdown("Tucson Crime Dataset | 2018 - 2025")
st.divider()

df = load_data()

# load geojsons
with open("app/data/divisions.geojson") as f:
    divisions_geojson = json.load(f)

with open("app/data/wards.geojson") as f:
    wards_geojson = json.load(f)

# add short division name to geojson for matching
for feat in divisions_geojson["features"]:
    feat["properties"]["DivisionShort"] = feat["properties"]["DIVISION"].replace("Operations Division ", "")

# sidebar filters
st.sidebar.header("Filters")
years = sorted(df["Year"].unique())
selected_years = st.sidebar.multiselect("Year", years, default = years)
divisions = sorted(df["Division"].unique())
selected_divisions = st.sidebar.multiselect("Division", divisions, default = divisions)

df_f = df[df["Year"].isin(selected_years) & df["Division"].isin(selected_divisions)]

if df_f.empty:
    st.warning("No data matches the current filters.")
    st.stop()

# section 1: crime type distribution
st.subheader("Crime Type Distribution")
st.info("**Key finding:** Larceny dominates with 170,264 incidents ( ~ 70% of all crimes), dwarfing every other category. Burglary, GTA, and Assault Aggravated are next at roughly 18 - 21k each. Homicide and Arson are the rarest with under 1,600 combined. This extreme imbalance is the central challenge for all modeling work.")

counts = df_f.groupby("CrimeLabel").size().reset_index(name = "Incidents")
counts = counts.sort_values("Incidents", ascending = False)

fig1 = px.bar(counts, x = "Incidents", y = "CrimeLabel",
    orientation = "h", color = "Incidents",
    color_continuous_scale = "Blues",
    labels = {"CrimeLabel": ""},
    title = "Incidents by crime type")
fig1.update_layout(coloraxis_showscale = False,
    yaxis = dict(categoryorder = "total ascending"),
    margin = dict(t = 40, b = 20))
st.plotly_chart(fig1, width = "stretch")

st.divider()

# section 2: time patterns
st.subheader("Time Patterns")
st.info("**Key finding:** The TimeOccur column had severe formatting inconsistencies in the raw data; entries like '113', '0428', '13:32', and invalid times like '24:55' all coexisted. A custom parser was written to standardize all formats to a clean 24-hour Hour integer before any analysis. After cleaning, incidents peak around noon - 3pm and stay elevated through the evening. Early morning hours (2am - 6am) are the quietest. Weekdays are all similarly busy with weekends slightly lower. Monthly distribution is nearly uniform, January and October see slightly higher counts but overall seasonality is weak.")

col1, col2 = st.columns(2)

with col1:
    hourly = df_f.groupby("Hour").size().reset_index(name = "Incidents")
    fig2 = px.bar(hourly, x = "Hour", y = "Incidents",
        color = "Incidents", color_continuous_scale = "Oranges",
        labels = {"Hour": "Hour of Day"},
        title = "Incidents by hour of day")
    fig2.update_layout(coloraxis_showscale = False, margin = dict(t = 40, b = 20))
    st.plotly_chart(fig2, width = "stretch")

with col2:
    day_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    daily = df_f.groupby("Day").size().reindex(day_order).reset_index(name = "Incidents")
    fig3 = px.bar(daily, x = "Day", y = "Incidents",
        color = "Incidents", color_continuous_scale = "Oranges",
        title = "Incidents by day of week")
    fig3.update_layout(coloraxis_showscale = False, margin = dict(t = 40, b = 20))
    st.plotly_chart(fig3, width = "stretch")

col3, col4 = st.columns(2)

with col3:
    month_order = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"]
    monthly = df_f.groupby("Month").size().reindex(month_order).reset_index(name = "Incidents")
    fig4 = px.bar(monthly, x = "Month", y = "Incidents",
        color = "Incidents", color_continuous_scale = "Oranges",
        title = "Incidents by month")
    fig4.update_layout(coloraxis_showscale = False, margin = dict(t = 40, b = 20))
    st.plotly_chart(fig4, width = "stretch")

with col4:
    pivot_hd = (df_f.groupby(["Hour", "Day"]).size()
        .unstack(fill_value = 0)
        .reindex(columns = day_order, fill_value = 0))
    fig5 = px.imshow(pivot_hd, aspect = "auto",
        color_continuous_scale = "Oranges",
        labels = dict(x = "Day", y = "Hour", color = "Incidents"),
        title = "Heatmap: hour vs day of week")
    fig5.update_layout(height = 380, margin = dict(t = 40, b = 20))
    st.plotly_chart(fig5, width = "stretch")

st.divider()

# section 3: geographic
st.subheader("Geographic Breakdown")
st.info("**Key finding:** GeoJSON boundary files for both police divisions and wards were sourced from the Tucson and Pima County open data portals, enabling choropleth maps directly on the actual division and ward boundaries. West division leads with 69,521 incidents, followed by South (62,998), Midtown (56,309), and East (54,299). Ward 3 has the highest count at 54,690 while Ward 4 has the lowest at 15,987. Larceny dominates every single division.The heatmap below shows Larceny cells are 5 - 10x darker than any other crime type across all divisions.")

crime_options = ["All"] + sorted(df_f["CrimeLabel"].unique())
selected_crime_geo = st.selectbox("Filter maps by crime type", crime_options, key = "geo_crime")

df_geo = df_f if selected_crime_geo == "All" else df_f[df_f["CrimeLabel"] == selected_crime_geo]

col5, col6 = st.columns(2)

# division and ward centroids for always-visible labels
div_centroids = {
    "East":    (32.1754, -110.8167),
    "Midtown": (32.2358, -110.8966),
    "South":   (32.1634, -110.9697),
    "West":    (32.2481, -111.0076),
}
ward_centroids = {
    "1": (32.2035, -111.0129),
    "2": (32.2448, -110.8187),
    "3": (32.2875, -110.9684),
    "4": (32.1312, -110.7916),
    "5": (32.1245, -110.9041),
    "6": (32.2268, -110.9235),
}

with col5:
    div_counts = df_geo["Division"].value_counts().reset_index()
    div_counts.columns = ["DivisionShort", "Incidents"]

    fig6 = px.choropleth_map(div_counts,
        geojson = divisions_geojson,
        locations = "DivisionShort",
        featureidkey = "properties.DivisionShort",
        color = "Incidents",
        color_continuous_scale = "Blues",
        map_style = "carto-darkmatter",
        zoom = 10, center = dict(lat = 32.22, lon = -110.97),
        title = "Incidents by division",
        labels = {"DivisionShort": "Division"})

    for _, row in div_counts.iterrows():
        name = row["DivisionShort"]
        if name in div_centroids:
            lat, lon = div_centroids[name]
            fig6.add_scattermap(
                lat = [lat], lon = [lon],
                mode = "text",
                text = [f"{name}<br>{row['Incidents']:,}"],
                textfont = dict(size = 12, color = "black"),
                showlegend = False)

    fig6.update_layout(margin = dict(t = 40, b = 0), height = 420)
    st.plotly_chart(fig6, width = "stretch")

with col6:
    ward_df = df_geo[df_geo["Ward"] != "0"].copy()
    ward_counts = ward_df["Ward"].astype(str).value_counts().reset_index()
    ward_counts.columns = ["WARD", "Incidents"]

    fig7 = px.choropleth_map(ward_counts,
        geojson = wards_geojson,
        locations = "WARD",
        featureidkey = "properties.WARD",
        color = "Incidents",
        color_continuous_scale = "Blues",
        map_style = "carto-darkmatter",
        zoom = 10, center = dict(lat = 32.22, lon = -110.97),
        title = "Incidents by ward",
        labels = {"WARD": "Ward"})

    for _, row in ward_counts.iterrows():
        ward = row["WARD"]
        if ward in ward_centroids:
            lat, lon = ward_centroids[ward]
            fig7.add_scattermap(
                lat = [lat], lon = [lon],
                mode = "text",
                text = [f"Ward {ward}<br>{row['Incidents']:,}"],
                textfont = dict(size = 12, color = "black"),
                showlegend = False)

    fig7.update_layout(margin = dict(t = 40, b = 0), height = 420)
    st.plotly_chart(fig7, width = "stretch")


# division x crime type heatmap
div_pivot = (df_f.groupby(["Division", "CrimeLabel"]).size()
    .unstack(fill_value = 0))
fig8 = px.imshow(div_pivot, aspect = "auto",
    color_continuous_scale = "Blues",
    labels = dict(x = "Crime Type", y = "Division", color = "Incidents"),
    title = "Heatmap: division vs crime type",
    text_auto = True)
fig8.update_layout(height = 300, margin = dict(t = 40, b = 20))
st.plotly_chart(fig8, width = "stretch")

st.divider()

# section 4: call source
st.subheader("Call Source")
st.info("**Key finding:** Web Reported (43.4%) and Call For Service (41.9%) account for nearly all incidents. Officer-Initiated is 11.8%. Strikingly, Web Reported incidents are almost exclusively Larceny (102,397 out of ~103k), online crime reporting is essentially a Larceny-only channel. Officer-Initiated incidents spread more evenly across crime types.")

col7, col8 = st.columns(2)

with col7:
    src_counts = df_f["CallSource"].value_counts().reset_index()
    src_counts.columns = ["CallSource", "Incidents"]
    fig9 = px.pie(src_counts, names = "CallSource", values = "Incidents",
        title = "Call source breakdown", hole = 0.4)
    fig9.update_layout(margin = dict(t = 40, b = 20))
    st.plotly_chart(fig9, width = "stretch")

with col8:
    src_pivot = (df_f.groupby(["CallSource", "CrimeLabel"]).size()
        .unstack(fill_value = 0))
    fig10 = px.imshow(src_pivot, aspect = "auto",
        color_continuous_scale = "Purples",
        labels = dict(x = "Crime Type", y = "Call Source", color = "Incidents"),
        title = "Heatmap: call source vs crime type",
        text_auto = True)
    fig10.update_layout(height = 300, margin = dict(t = 40, b = 20))
    st.plotly_chart(fig10, width = "stretch")

st.divider()

# section 5: trends 
st.subheader("Trends Over Time")
st.info("**Key finding:** Total incidents dropped sharply in 2020 (24k) during COVID-19 and partially recovered in 2021 (25k), then surged to a peak of 42,863 in 2022 before declining again. Larceny drives almost all of this variation, every other crime type remains relatively flat across all years.")

yearly = df_f.groupby("Year").size().reset_index(name = "Incidents")
fig11 = px.line(yearly, x = "Year", y = "Incidents", markers = True,
    title = "Total incidents per year")
fig11.add_vrect(x0 = 2019.5, x1 = 2021.5, fillcolor = "red", opacity = 0.08,
    annotation_text = "COVID-19", annotation_position = "top left")
fig11.update_layout(margin = dict(t = 40, b = 20))
st.plotly_chart(fig11, width = "stretch")

yearly_type = df_f.groupby(["Year", "CrimeLabel"]).size().reset_index(name = "Incidents")
fig12 = px.line(yearly_type, x = "Year", y = "Incidents", color = "CrimeLabel",
    markers = True, title = "Incidents per year by crime type",
    labels = {"CrimeLabel": "Crime Type"})
fig12.add_vrect(x0 = 2019.5, x1 = 2021.5, fillcolor = "red", opacity = 0.08,
    annotation_text = "COVID-19", annotation_position = "top left")
fig12.update_layout(margin = dict(t = 40, b = 20))
st.plotly_chart(fig12, width = "stretch")

st.divider()

# section 6: crime deep dive 
st.subheader("Crime Deep Dive")
st.caption("Select a crime type to see when, where, and how it occurs.")

selected_crime = st.selectbox("Select crime type", sorted(df_f["CrimeLabel"].unique()), key = "deep_dive")

dv = df_f[df_f["CrimeLabel"] == selected_crime]

total = len(dv)
peak_hour = int(dv["Hour"].value_counts().idxmax())
peak_day = dv["Day"].value_counts().idxmax()
peak_div = dv["Division"].value_counts().idxmax()

d1, d2, d3, d4 = st.columns(4)
d1.metric("Total Incidents", f"{total:,}")
d2.metric("Peak Hour", f"{peak_hour:02d}:00")
d3.metric("Peak Day", peak_day)
d4.metric("Top Division", peak_div)

st.markdown("---")

col9, col10 = st.columns(2)

with col9:
    h = dv.groupby("Hour").size().reset_index(name = "Incidents")
    fa = px.bar(h, x = "Hour", y = "Incidents",
        color = "Incidents", color_continuous_scale = "Reds",
        labels = {"Hour": "Hour of Day"},
        title = f"{selected_crime} - by hour of day")
    fa.update_layout(coloraxis_showscale = False, margin = dict(t = 40, b = 20))
    st.plotly_chart(fa, width = "stretch")

with col10:
    d = dv.groupby("Day").size().reindex(day_order).reset_index(name = "Incidents")
    fb = px.bar(d, x = "Day", y = "Incidents",
        color = "Incidents", color_continuous_scale = "Reds",
        title = f"{selected_crime} - by day of week")
    fb.update_layout(coloraxis_showscale = False, margin = dict(t = 40, b = 20))
    st.plotly_chart(fb, width = "stretch")

col11, col12 = st.columns(2)

with col11:
    div = dv["Division"].value_counts().reset_index()
    div.columns = ["Division", "Incidents"]
    fc = px.bar(div, x = "Division", y = "Incidents",
        color = "Incidents", color_continuous_scale = "Reds",
        title = f"{selected_crime} - by division")
    fc.update_layout(coloraxis_showscale = False, margin = dict(t = 40, b = 20))
    st.plotly_chart(fc, width = "stretch")

with col12:
    src = dv["CallSource"].value_counts().reset_index()
    src.columns = ["CallSource", "Incidents"]
    fd = px.pie(src, names = "CallSource", values = "Incidents",
        title = f"{selected_crime} - call source", hole = 0.4)
    fd.update_layout(margin = dict(t = 40, b = 20))
    st.plotly_chart(fd, width = "stretch")

col13, col14 = st.columns(2)

with col13:
    mo = dv.groupby("Month").size().reindex(month_order).reset_index(name = "Incidents")
    fe = px.bar(mo, x = "Month", y = "Incidents",
        color = "Incidents", color_continuous_scale = "Reds",
        title = f"{selected_crime} - by month")
    fe.update_layout(coloraxis_showscale = False, margin = dict(t = 40, b = 20))
    st.plotly_chart(fe, width = "stretch")

with col14:
    yr = dv.groupby("Year").size().reset_index(name = "Incidents")
    ff = px.line(yr, x = "Year", y = "Incidents", markers = True,
        title = f"{selected_crime} - trend by year")
    ff.add_vrect(x0 = 2019.5, x1 = 2021.5, fillcolor = "red", opacity = 0.08,
        annotation_text = "COVID-19", annotation_position = "top left")
    ff.update_layout(margin = dict(t = 40, b = 20))
    st.plotly_chart(ff, width = "stretch")

st.markdown("##### Hour vs Day of Week")
pivot_hd2 = (dv.groupby(["Hour", "Day"]).size()
    .unstack(fill_value = 0)
    .reindex(columns = day_order, fill_value = 0))
fg = px.imshow(pivot_hd2, aspect = "auto",
    color_continuous_scale = "Reds",
    labels = dict(x = "Day", y = "Hour", color = "Incidents"),
    title = f"{selected_crime} - hour vs day heatmap")
fg.update_layout(height = 420, margin = dict(t = 40, b = 20))
st.plotly_chart(fg, width = "stretch")

st.markdown("##### Division vs Hour of Day")
pivot_dh = (dv.groupby(["Division", "Hour"]).size()
    .unstack(fill_value = 0))
fh = px.imshow(pivot_dh, aspect = "auto",
    color_continuous_scale = "Reds",
    labels = dict(x = "Hour", y = "Division", color = "Incidents"),
    title = f"{selected_crime} - division vs hour heatmap",
    text_auto = True)
fh.update_layout(height = 320, margin = dict(t = 40, b = 20))
st.plotly_chart(fh, width = "stretch")