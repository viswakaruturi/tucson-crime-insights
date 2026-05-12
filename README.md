# Tucson Crime Insights

An interactive Streamlit dashboard exploring and predicting crime patterns across Tucson, Arizona using statistical machine learning. Built as a final project for DATA 474: Introduction to Statistical Machine Learning at the University of Arizona, Spring 2026.

**Live app:** https://tucson-crime-insights.streamlit.app/

---

## Dataset

Source: [Tucson Police Department Open Data Portal](https://policeanalysis.tucsonaz.gov/pages/reported-crimes)

243,127 crime incident records spanning January 2018 through December 2025, covering 8 UCR crime categories, 4 police divisions, and 6 city wards. Variables include incident date, time of occurrence, geographic division, ward, UCR crime category, offense description, and call source.

---

## Project Structure

```
tucson-crime-insights/
├── app/
│   ├── main.py
│   ├── config.toml
│   ├── pages/
│   │   ├── 00_home.py
│   │   ├── 01_eda.py
│   │   ├── 02_classification.py
│   │   ├── 03_clustering_pca.py
│   │   └── 04_about.py
│   ├── utils/
│   │   └── data_loader.py
│   └── data/
│       ├── divisions.geojson
│       └── wards.geojson
├── data/
│   ├── raw/
│   │   └── TPD_OPEN_DATA_ReportedCrimesPublicDash.csv
│   └── processed/
│       └── tpd_2018_2025.csv
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_preprocessing.ipynb
│   ├── 03_classification.ipynb
│   └── 04_clustering_pca.ipynb
├── reports/
│   ├── Final Report.pdf
│   └── Project Proposal.pdf
├── results/
│   ├── 01/
│   ├── 02/
│   ├── 03/
│   └── 04/
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Methods

**Exploratory Data Analysis**
Interactive visualizations of crime type distribution, time patterns, geographic breakdowns using choropleth maps from Tucson and Pima County open data GeoJSON files, call source analysis, and year-over-year trends including COVID-19 impact.

**Supervised Classification**
Predicting UCR crime type (8 classes) from 22 features selected via Random Forest importances. Five models trained and evaluated with 5-fold stratified cross-validation: Logistic Regression, LDA, Decision Tree, Random Forest, and SVM. F1 Macro used as the primary metric due to heavy class imbalance (~70% Larceny).

**Unsupervised Learning**
PCA for dimensionality reduction and visualization, K-Means clustering with elbow method for k selection, and Ward linkage hierarchical clustering on a 500-sample subset.

---

## Results

Random Forest achieved the best performance with a CV F1 Macro of 0.209 and 56% test accuracy. Hour of day is the single most important feature at 0.34 importance, confirming that time of day is the strongest signal for crime type prediction. No strong natural clusters were found in the data: K-Means with k=2 largely separated Larceny from all other crime types, mirroring the class imbalance challenge seen in classification.

---

## Running Locally

```bash
git clone https://github.com/viswakaruturi/tucson-crime-insights.git
cd tucson-crime-insights
pip install -r requirements.txt
streamlit run app/main.py
```

---

## Tech Stack

- Python
- pandas
- scikit-learn
- Plotly
- Streamlit
- scipy

---

## Author

**Viswa Sushanth Karuturi**  
B.S. in Statistics & Data Science, B.S. in Computer Science  
University of Arizona

[LinkedIn](https://www.linkedin.com/in/viswakaruturi/) | [GitHub](https://github.com/viswakaruturi) | [Website](https://viswakaruturi.com/)

---

*DATA 474: Introduction to Statistical Machine Learning | University of Arizona | Spring 2026*
