import streamlit as st

st.title("About")
st.divider()

#  author 
st.subheader("Author")

col_a, col_b = st.columns(2)

with col_a:
    st.markdown("**Viswa Sushanth Karuturi**")
    st.markdown("B.S. in Statistics & Data Science")
    st.markdown("B.S. in Computer Science")
    st.markdown("University of Arizona")

with col_b:
    st.link_button("LinkedIn", url = "https://www.linkedin.com/in/viswakaruturi/")
    st.link_button("GitHub", url = "https://github.com/viswakaruturi")
    st.link_button("Website", url = "https://viswakaruturi.com/")

st.divider()

# dataset 
st.subheader("Dataset")
st.markdown("""
The dataset is published by the **Tucson Police Department** through their Open Data Portal.
It contains **243,127 crime incident records** spanning January 2018 through January 2026
with 14 variables including incident date, time, geographic division, ward, UCR crime category,
offense description, and call source.
""")
st.link_button("Tucson Police Department Open Data Portal",
    url = "https://policeanalysis.tucsonaz.gov/pages/reported-crimes")

st.divider()

# report and slides
st.subheader("Report & Slides")

col_c, col_d = st.columns(2)

with col_c:
    st.markdown("**Final Report**")
    st.download_button("Download Report (PDF)", data = b"", file_name = "report.pdf",
        disabled = True)

with col_d:
    st.markdown("**Presentation Slides**")
    st.download_button("Download Slides (PDF)", data = b"", file_name = "slides.pdf",
        disabled = True)

st.divider()

# ── methods ────────────────────────────────────────────────────────────────────
st.subheader("Methods & Tools")

col_e, col_f = st.columns(2)

with col_e:
    st.markdown("**Machine Learning**")
    st.markdown("""
- Logistic Regression
- Linear Discriminant Analysis (LDA)
- Decision Trees
- Random Forest
- Support Vector Machines (SVM)
- Logistic Regression with L1 penalty for feature selection
- K-fold cross-validation
- K-Means and hierarchical clustering
- Principal Component Analysis (PCA)
""")

with col_f:
    st.markdown("**Stack**")
    st.markdown("""
- Python
- pandas
- scikit-learn
- Plotly
- Streamlit
""")

st.divider()
st.caption("DATA 474: Introduction to Statistical Machine Learning | University of Arizona | Spring 2026")