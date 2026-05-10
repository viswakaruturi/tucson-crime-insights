import streamlit as st
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.data_loader import load_data
import plotly.express as px

df = load_data()

# cleaning crime labels by removing prefixes and title-casing
def clean_crime(label):
    if " - " in label:
        return label.split(" - ", 1)[1].title()
    return label.title()

df["CrimeLabel"] = df["UCRDescription"].apply(clean_crime)

# header
st.title("Tucson Crime Insights")
st.markdown("**DATA 474** | Viswa Sushanth Karuturi | Spring 2026")
st.divider()

# 5 key metrics
m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Total Incidents", f"{len(df):,}")
m2.metric("Years Covered", f"{df['Year'].min()} - {df['Year'].max()}")
m3.metric("Crime Types", df["UCRDescription"].nunique())
m4.metric("Divisions", df["Division"].nunique())
m5.metric("Wards", df[df["Ward"] != "0"]["Ward"].nunique())

st.divider()

# tabs for detailed analysis
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Total Incidents", "Years Covered", "Crime Types", "Divisions", "Wards",
])

# tab 1: total incidents
with tab1:
    st.subheader("Total Incidents Overview")

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Incidents", f"{len(df):,}")
    c2.metric("Avg per Year", f"{len(df) // df['Year'].nunique():,}")
    c3.metric("Avg per Day", f"{len(df) // (df['Year'].nunique() * 365):,}")

    st.markdown("---")

    yearly = df.groupby("Year").size().reset_index(name = "Incidents")
    fig = px.line(yearly, x = "Year", y = "Incidents", markers = True,
        title = "Incidents over time")
    fig.add_vrect(x0 = 2019.5, x1 = 2021.5, fillcolor = "red", opacity = 0.08,
        annotation_text = "COVID-19", annotation_position = "top left")
    fig.update_layout(margin = dict(t = 40, b = 20))
    st.plotly_chart(fig, width = "stretch")

# tab 2: years covered
with tab2:
    st.subheader("Years Covered: 2018 – 2025")

    yearly = df.groupby("Year").size().reset_index(name = "Incidents")
    fig2 = px.bar(yearly, x = "Year", y = "Incidents",
        color = "Incidents", color_continuous_scale = "Blues",
        text = "Incidents", title = "Incidents per year")
    fig2.add_vrect(x0 = 2019.5, x1 = 2021.5, fillcolor = "red", opacity = 0.08,
        annotation_text = "COVID-19", annotation_position = "top left")
    fig2.update_traces(texttemplate = "%{text:,}", textposition = "outside")
    fig2.update_layout(coloraxis_showscale = False, margin = dict(t = 40, b = 20))
    st.plotly_chart(fig2, width = "stretch")

    yearly_type = df.groupby(["Year", "CrimeLabel"]).size().reset_index(name = "Incidents")
    fig3 = px.line(yearly_type, x = "Year", y = "Incidents", color = "CrimeLabel",
        markers = True, title = "Incidents per year by crime type",
        labels = {"CrimeLabel": "Crime Type"})
    fig3.add_vrect(x0 = 2019.5, x1 = 2021.5, fillcolor = "red", opacity = 0.08,
        annotation_text = "COVID-19", annotation_position = "top left")
    fig3.update_layout(margin = dict(t = 40, b = 20))
    st.plotly_chart(fig3, width = "stretch")

# tab 3: crime types
with tab3:
    st.subheader("Crime Types")

    counts = df.groupby("CrimeLabel").size().reset_index(name = "Incidents")
    counts = counts.sort_values("Incidents", ascending = False)

    col_a, col_b = st.columns([1, 1])

    with col_a:
        fig4 = px.bar(counts, x = "Incidents", y = "CrimeLabel",
            orientation = "h", color = "Incidents",
            color_continuous_scale = "Blues",
            labels = {"CrimeLabel": ""},
            title = "Incidents by crime type")
        fig4.update_layout(coloraxis_showscale = False,
            yaxis = dict(categoryorder = "total ascending"),
            margin = dict(t = 40, b = 20))
        st.plotly_chart(fig4, width = "stretch")

    with col_b:
        st.markdown("##### Breakdown")
        display_counts = counts.copy()
        display_counts["Incidents"] = display_counts["Incidents"].apply(lambda x: f"{x:,}")
        st.dataframe(display_counts, hide_index = True, width = "stretch")

# tab 4: divisions
with tab4:
    st.subheader("Police Divisions")

    _, center, _ = st.columns([1, 2, 1])
    with center:
        st.image("https://www.tucsonaz.gov/files/sharedassets/public/v/1/police/documents/maps/tpd-divisions.png?dimension=pageimage&w=480",
            caption = "Tucson Police Department Divisions", width = "stretch")

    col_c, col_d = st.columns([1, 1])

    with col_c:
        div_counts = df["Division"].value_counts().reset_index()
        div_counts.columns = ["Division", "Incidents"]
        fig5 = px.bar(div_counts, x = "Division", y = "Incidents",
            color = "Division",
            color_discrete_map = {
                "West": "#7CB9E8", "Midtown": "#8fb8a8",
                "East": "#c8b98a", "South": "#b88a96",
            },
            title = "Incidents by division")
        fig5.update_layout(showlegend = False, margin = dict(t = 40, b = 20))
        st.plotly_chart(fig5, width = "stretch")

    with col_d:
        div_type = df.groupby(["Division", "CrimeLabel"]).size().reset_index(name = "Incidents")
        fig6 = px.bar(div_type, x = "Division", y = "Incidents", color = "CrimeLabel",
            barmode = "stack", title = "Crime type breakdown by division",
            labels = {"CrimeLabel": "Crime Type"})
        fig6.update_layout(margin = dict(t = 40, b = 20))
        st.plotly_chart(fig6, width = "stretch")

# tab 5: wards
with tab5:
    st.subheader("City Council Wards")

    _, center2, _ = st.columns([1, 2, 1])
    with center2:
        st.image("https://www.arcgis.com/sharing/rest/content/items/9745a38738ab4ca5b85dfd38086bb1b0/resources/wards.jpg?v=1778198400081&w=400",
            caption = "Tucson City Council Wards", width = "stretch")

    col_e, col_f = st.columns([1, 1])

    with col_e:
        ward_df = df[df["Ward"] != "0"].copy()
        ward_counts = ward_df["Ward"].astype(str).value_counts().reset_index()
        ward_counts.columns = ["Ward", "Incidents"]
        ward_counts = ward_counts.sort_values("Ward")
        fig7 = px.bar(ward_counts, x = "Ward", y = "Incidents",
            color = "Incidents", color_continuous_scale = "Blues",
            title = "Incidents by ward", labels = {"Ward": "Ward"})
        fig7.update_layout(coloraxis_showscale = False, margin = dict(t = 40, b = 20))
        st.plotly_chart(fig7, width = "stretch")

    with col_f:
        ward_type = ward_df.groupby(["Ward", "CrimeLabel"]).size().reset_index(name = "Incidents")
        ward_type["Ward"] = ward_type["Ward"].astype(str)
        fig8 = px.bar(ward_type, x = "Ward", y = "Incidents", color = "CrimeLabel",
            barmode = "stack", title = "Crime type breakdown by ward",
            labels = {"CrimeLabel": "Crime Type"})
        fig8.update_layout(margin = dict(t = 40, b = 20))
        st.plotly_chart(fig8, width = "stretch")

st.divider()
st.caption("Data source: Tucson Police Department Open Data Portal — https://policeanalysis.tucsonaz.gov/pages/reported-crimes | GitHub: https://github.com/viswakaruturi/tucson-crime-insights")