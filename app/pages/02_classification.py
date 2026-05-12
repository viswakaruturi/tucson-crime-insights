import streamlit as st
import pandas as pd

st.title("Classification")
st.markdown("Predicting Crime Type from Temporal and Spatial Features")
st.divider()

RESULTS = "results/03"

# section 1: problem setup
st.subheader("1. Problem Setup")

st.markdown("""
The goal is to predict **UCR crime type**: 8 classes (Homicide, Sexual Assault, Robbery,
Assault Aggravated, Burglary, Larceny, GTA, Arson), from features derived from time,
location, and how the crime was reported.
""")

st.warning("""
**Class imbalance:** Larceny accounts for ~ 70% of all incidents (170,264 out of 243,127).
This heavily skews model performance. We use **F1 Macro** (unweighted average across all
classes) rather than accuracy to fairly evaluate performance across all 8 crime types.
A model that just predicts Larceny every time would get 70% accuracy but F1 Macro near zero.
""")

st.divider()

# section 2: data prep
st.subheader("2. Data Preparation")

st.markdown("""
**Columns dropped:** IncidentID, UCR, Offense (identifiers or redundant codes, not predictive features)

**One-hot encoding** applied to: Division, CallSource, Ward, Month, Day

**Target encoding:** UCRDescription label-encoded to integers (0 - 7) using LabelEncoder

**Train-test split:** 80/20 stratified split to preserve class proportions
- Training set: ~ 194,500 samples
- Test set: ~ 48,626 samples
""")

with st.expander("Why stratified split?"):
    st.markdown("""
With heavy class imbalance, a random split risks putting all or most Homicide cases
in one set. Stratified splitting ensures each class appears in both train and test sets
at the same proportion as the full dataset. This is critical for reliable evaluation
of minority class performance.
""")

st.divider()

# section 3: feature selection
st.subheader("3. Feature Selection")

st.markdown("#### Attempt 1 - Logistic Regression with L1 Penalty")

st.markdown("""
The first approach was to use LogisticRegressionCV with L1 penalty (LASSO-style
regularization) to automatically shrink uninformative feature coefficients to zero.
""")

st.error("""
**Result:** L1 regularization was too aggressive, it reduced the feature set to only
3 - 4 features, discarding most of the temporal and spatial signals. A model trained on
3 features performed poorly and was not useful for meaningful crime type prediction.
""")

st.markdown("#### Attempt 2 - Random Forest Feature Importances")

st.markdown("""
A preliminary Random Forest trained on all features ranked them by Gini importance.
Features with importance **> 0.01** were retained, giving 22 features.
""")

st.image(f"{RESULTS}/feature_importances.png", width = "stretch")

st.markdown("""
**22 features selected:**
`Hour, Year, CallSource_Web Reported, CallSource_Officer-Initiated,
Day_Mon, Day_Thu, Day_Wed, Day_Tue, Day_Sat, Day_Sun,
Month_May, Month_March, Month_October, Month_January, Month_February,
Month_July, Month_August, Month_June, Month_September, Month_November,
Month_December, Division_Midtown`
""")

with st.expander("Key findings - feature importance"):
    st.markdown("""
- Hour is the strongest predictor (importance ~ 0.34). Time of day is the single
  best signal for what type of crime occurred
- Year (0.17) captures long-term crime pattern shifts over 2018 - 2025
- CallSource_Web Reported (0.165), crimes reported online have very different profiles
- CallSource_Officer-Initiated (0.025), officer-initiated incidents skew toward GTA and Assault
- Day of week features contribute modestly (~ 0.015 - 0.02 each)
- Division_Midtown is the only geographic feature that crossed the 0.01 threshold
""")

st.divider()

# section 4: scaling 
st.subheader("4. Scaling")

st.markdown("""
**StandardScaler** applied to the 22 selected features for models sensitive to feature
magnitude: Logistic Regression, LDA, and SVM.

Tree-based models (Decision Tree, Random Forest) use unscaled selected features
since they split on thresholds and are not affected by feature scale.
""")

st.divider()

# section 5: models trained
st.subheader("5. Models Trained")

st.markdown("""
Five classifiers trained on the selected features with balanced class weights
where supported to partially offset the Larceny dominance:

- **Multinomial Logistic Regression** - linear baseline, solver = lbfgs, balanced class weights
- **LDA** - linear discriminant analysis with uniform priors across 8 classes
- **Decision Tree** - non-linear, balanced class weights
- **Random Forest** - ensemble of 100 trees, balanced class weights
- **SVM** - RBF kernel, balanced class weights
""")

st.divider()

# section 6: best model
st.subheader("6. Best Model - Random Forest")

st.markdown("""
Random Forest is the best performing model with 56% accuracy and CV F1 Macro of 0.209.
It achieves the highest Larceny F1 (0.79) and best GTA F1 (0.20) of any model.
The ensemble approach reduces variance compared to a single Decision Tree, and balanced
class weights help distribute attention across crime types. Homicide (F1 0.04) and
Arson (F1 0.07) remain low, reflecting the fundamental difficulty of predicting rare
events from temporal and spatial features alone.
""")

col_a, col_b = st.columns(2)
with col_a:
    st.image(f"{RESULTS}/rf_classification_report.png", width = "stretch")
with col_b:
    st.image(f"{RESULTS}/rf_confusion_matrix.png", width = "stretch")

with st.expander("Confusion matrix interpretation - Random Forest"):
    st.markdown("""
Random Forest has the strongest diagonal of all models. Mid-frequency classes like
Assault Aggravated (802), Burglary (868), and GTA (855) show higher true positive
counts than any other model. This confirms the ensemble's superior ability to
separate overlapping crime type distributions in feature space.
""")

st.divider()

# section 7: other models 
st.subheader("7. Other Models")

tab_lr, tab_lda, tab_dt, tab_svm = st.tabs([
    "Logistic Regression", "LDA", "Decision Tree", "SVM"
])

with tab_lr:
    st.markdown("""
Logistic Regression achieves 45% accuracy and F1 Macro of 0.16.
It performs reasonably on Larceny (precision 0.97, F1 0.74) but nearly fails on
Homicide (F1 0.01) and Arson (F1 0.02). Even with balanced class weights, the linear
decision boundary cannot separate the highly overlapping feature distributions of rare crimes.
""")
    c1, c2 = st.columns(2)
    with c1:
        st.image(f"{RESULTS}/lr_classification_report.png", width = "stretch")
    with c2:
        st.image(f"{RESULTS}/lr_confusion_matrix.png", width = "stretch")
    with st.expander("Confusion matrix interpretation"):
        st.markdown("""
Strong off-diagonal pattern, the model collapses minority class predictions toward
Homicide and Robbery. Most non-Larceny incidents end up predicted as one of these
two classes, a symptom of the linear decision boundary failing to separate
overlapping crime type clusters.
""")

with tab_lda:
    st.markdown("""
LDA achieves 50% accuracy and CV F1 Macro of 0.178. It shows the best Homicide
recall (0.32) of all models. Larceny performance is strong (precision 0.95, F1 0.78).
However, GTA recall (0.08) is the lowest of any model. LDA assumes Gaussian features
and equal covariance, which limits its ability to capture non-linear boundaries.
""")
    c3, c4 = st.columns(2)
    with c3:
        st.image(f"{RESULTS}/lda_classification_report.png", width = "stretch")
    with c4:
        st.image(f"{RESULTS}/lda_confusion_matrix.png", width = "stretch")
    with st.expander("Confusion matrix interpretation"):
        st.markdown("""
LDA spreads errors more evenly than Logistic Regression. Many minority class incidents
get predicted as Homicide (top-left column heavily populated), reflecting the model's
tendency to predict extreme classes when uncertain.
""")

with tab_dt:
    st.markdown("""
Decision Tree achieves 52% accuracy and CV F1 Macro of 0.205, the second best overall.
Balanced performance across mid-frequency classes - Assault Aggravated (F1 0.19),
Burglary (F1 0.18), and GTA (F1 0.19) all meaningfully above zero. The tree structure
naturally handles non-linear interactions without scaling.
""")
    c5, c6 = st.columns(2)
    with c5:
        st.image(f"{RESULTS}/dt_classification_report.png", width = "stretch")
    with c6:
        st.image(f"{RESULTS}/dt_confusion_matrix.png", width = "stretch")
    with st.expander("Confusion matrix interpretation"):
        st.markdown("""
Healthier diagonal than linear models. Mid-frequency classes show more true positives,
reflecting the tree's ability to carve out feature-space regions for individual crime
types by splitting on Hour, Year, and CallSource thresholds.
""")

with tab_svm:
    st.markdown("""
SVM with RBF kernel achieves 47% accuracy and CV F1 Macro of 0.168. Despite the
non-linear kernel, SVM does not improve over tree-based models. The large dataset size
(~194k training samples) likely makes the RBF kernel less effective. Computational cost
was significantly higher than all other models.
""")
    c7, c8 = st.columns(2)
    with c7:
        st.image(f"{RESULTS}/svm_classification_report.png", width = "stretch")
    with c8:
        st.image(f"{RESULTS}/svm_confusion_matrix.png", width = "stretch")
    with st.expander("Confusion matrix interpretation"):
        st.markdown("""
The most diffuse confusion matrix errors spread across all predicted classes with
no clear pattern. The Larceny diagonal (21,223) is the lowest among all models,
meaning SVM also underperforms on the dominant class compared to others.
""")

st.divider()

# section 8: cv comparison 
st.subheader("8. 5-Fold Stratified CV Comparison")

cv_data = {
    "Model": ["Logistic Regression", "LDA", "Decision Tree", "Random Forest", "SVM"],
    "CV F1 Macro": [0.1637, 0.1780, 0.2045, 0.2090, 0.1683],
    "Test Accuracy": [0.45, 0.50, 0.52, 0.56, 0.47],
    "Test F1 Macro": [0.16, 0.18, 0.20, 0.21, 0.17],
}
cv_df = pd.DataFrame(cv_data)

col_c, col_d = st.columns([1, 1])
with col_c:
    st.image(f"{RESULTS}/model_comparison.png", width = "stretch")
with col_d:
    st.markdown("##### Scores at a glance")
    st.dataframe(cv_df, hide_index = True, width = "stretch")

with st.expander("Why F1 Macro over accuracy?"):
    st.markdown("""
Accuracy is misleading with imbalanced classes. A model that always predicts Larceny
would achieve ~70% accuracy while being completely useless for every other crime type.
F1 Macro gives equal importance to rare classes like Homicide and Arson, forcing the
model to demonstrate predictive ability across all crime types.
""")

st.divider()

# section 9: conclusion 
st.subheader("9. Conclusion")

st.markdown("""
- Crime type is genuinely hard to predict from temporal and spatial features alone.
  F1 Macro of 0.16 - 0.21 reflects the limits of what hour, day, month, division, and
  call source can tell us about crime type.
- L1 regularization was too aggressive, only 3-4 features selected, discarding
  too much signal. Random Forest importances gave a better 22-feature subset.
- Hour of day is the single most informative feature (importance 0.34), confirming
  the EDA finding that different crimes peak at very different times of day.
- Tree-based models outperform linear models because crime type boundaries in
  feature space are non-linear.
- Class imbalance is the core challenge. Even with balanced class weights and
  stratified CV, Homicide and Arson remain very hard to predict.
- Random Forest is the best model, highest F1 Macro (0.209) and accuracy (0.56).
""")