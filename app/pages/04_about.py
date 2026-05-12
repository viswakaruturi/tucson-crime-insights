import streamlit as st

st.title("Conclusion & About")
st.divider()

# conclusion
st.subheader("Conclusion")

st.markdown("""
This project applied statistical machine learning to 243,127 Tucson crime incidents
spanning 2018 through 2025. The analysis covered three components: exploratory analysis,
supervised classification, and unsupervised clustering, each revealing different aspects
of crime patterns in the city.
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Exploration**")
    st.markdown("""
- Larceny dominates at ~70% of all incidents
- Crime activity follows strong hourly rhythms, different crimes peak at very different times of day
- West division has the highest incident count; East the lowest
- COVID-19 (2020-2021) caused a visible dip in total incidents, particularly in Larceny and Robbery
- Officer-initiated incidents have a very different crime type profile compared to call-for-service
""")

with col2:
    st.markdown("**Classification**")
    st.markdown("""
- Hour of day is the single strongest predictor of crime type (importance 0.34)
- L1 regularization was too aggressive, selecting only 3-4 features
- Random Forest performed best with CV F1 Macro of 0.209 and 56% accuracy
- Tree-based models outperform linear models, suggesting non-linear boundaries
- Class imbalance is the core challenge; Homicide and Arson remain hard to predict
""")

with col3:
    st.markdown("**Clustering & PCA**")
    st.markdown("""
- No strong natural clusters exist in the feature space
- PCA requires 18-19 components to explain 90% of variance; no dominant low-rank structure
- K-Means with k=2 rediscovers the class imbalance rather than new structure
- The 4-band PCA scatter is driven by the Hour feature
- Clustering results reinforce the classification challenge
""")

st.markdown("---")
st.markdown("#### Key Takeaways")

st.markdown("""
The most important takeaway is that crime type is genuinely hard to predict from
temporal and spatial features alone. Hour, day, month, division, ward, and call source
capture meaningful patterns, but they are not sufficient to reliably distinguish between
8 crime categories, especially rare ones like Homicide and Arson.

The consistency across all three analyses points to the same root cause: class imbalance
combined with feature overlap. Different crime types share similar temporal and spatial
profiles, making separation difficult for both supervised and unsupervised methods.

Despite the modest F1 scores, the project demonstrates a complete end-to-end machine
learning pipeline on a real, messy, imbalanced public safety dataset, from raw data
cleaning through EDA, feature selection, model comparison, and unsupervised exploration.
""")

st.markdown("---")
st.markdown("#### Future Work")

st.markdown("""
- Address class imbalance directly using SMOTE or other oversampling techniques
  to generate synthetic minority class samples for Homicide and Arson
- Incorporate geographic coordinates if the TPD releases lat/lon data, enabling
  true spatial density analysis and distance-based features
- Add offense-level granularity; the current target is the broad UCR category.
  Predicting specific offense sub-types may yield more actionable models
- Time series modeling: treating crime counts as a time series and forecasting
  future incident rates by division or ward
- DBSCAN clustering as an alternative to K-Means that does not require specifying k
  and can find non-spherical clusters
- Ensemble feature selection combining L1 and RF importances for a more robust
  feature subset
""")

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

# methods and tools
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

# report
st.subheader("Report")

st.markdown("**Final Report**")
with open("reports/Final Report.pdf", "rb") as f:
    st.download_button("Download Report (PDF)", data = f, file_name = "report.pdf")

st.divider()

# about
st.subheader("About")

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
st.caption("DATA 474: Introduction to Statistical Machine Learning | University of Arizona | Spring 2026")