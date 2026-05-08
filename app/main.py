import streamlit as st
 
st.set_page_config(page_title = "Tucson Crime Insights", layout = "wide")
 
pages = [
    st.Page("pages/00_home.py", title = "Home", icon = ":material/home:"),
    st.Page("pages/01_eda.py", title = "Exploration", icon = ":material/bar_chart:"),
    st.Page("pages/02_classification.py", title = "Classification", icon = ":material/model_training:"),
    st.Page("pages/03_clustering_pca.py", title = "Clustering & PCA", icon = ":material/hub:"),
    st.Page("pages/04_about.py", title = "About", icon = ":material/info:"),
]
 
pg = st.navigation(pages)
pg.run()