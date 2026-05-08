import streamlit as st
 
st.set_page_config(
    page_title = "Tucson Crime Insights",
    page_icon = "🔍",
    layout = "wide",
)
 
pages = [
    st.Page("pages/00_home.py",           title = "Home",             icon = "🏠"),
    st.Page("pages/01_eda.py",            title = "Exploration",      icon = "📊"),
    st.Page("pages/02_classification.py", title = "Classification",   icon = "🤖"),
    st.Page("pages/03_clustering_pca.py", title = "Clustering & PCA", icon = "🔵"),
]
 
pg = st.navigation(pages)
pg.run()
 