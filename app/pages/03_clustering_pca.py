import streamlit as st
 
st.title("Clustering & PCA")
st.markdown("Unsupervised Learning on Tucson Crime Data")
st.divider()
 
RESULTS = "results/04"
 
# section 1: overview
st.subheader("1. Overview")
 
st.markdown("""
The unsupervised component of this project asks: without using crime type labels,
do natural groupings exist in the data based on time, location, and call source?
 
The same 22 features selected during classification were used here, scaled with
StandardScaler. Three techniques were applied: PCA for dimensionality reduction
and visualization, K-Means for partition-based clustering, and hierarchical
clustering to understand the data's nested structure.
""")
 
st.warning("""
**Honest Note:** The clustering results were not particularly strong. The elbow
method produced no clear elbow, and K-Means with k = 2 largely separated the data
by Larceny vs everything else, reflecting the same class imbalance issue seen
in classification. The PCA scatter shows overlapping clusters rather than clean
separation. These are meaningful findings in themselves.
""")
 
st.divider()
 
# section 2: pca
st.subheader("2. Principal Component Analysis (PCA)")
 
st.markdown("""
PCA was applied to all 22 scaled features to understand the variance structure
and reduce dimensionality for visualization.
""")
 
st.markdown("#### Cumulative Explained Variance")
 
_, img1, _ = st.columns([1, 3, 1])
with img1:
    st.image(f"{RESULTS}/pca_explained_variance.png")
 
st.markdown("""
18-19 components are needed to explain 90% of the variance (90% threshold shown
as the red dashed line). The curve is nearly linear with no sharp elbow, meaning
variance is spread roughly evenly across all 22 features. No single component
dominates; the feature space is genuinely high-dimensional with no obvious
low-rank structure.
""")
 
with st.expander("Reading the variance curve"):
    st.markdown("""
A sharp elbow in a PCA variance plot would suggest a small number of components
capture most of the signal, making dimensionality reduction straightforward.
The near-linear curve here means all 22 features contribute roughly equally to variance,
compressing to 2-3 components loses most information, the 2D PCA visualization is
useful for exploration but not representative of the full feature space, and this
also partly explains why clustering in the original 22D space is difficult to visualize.
""")
 
st.markdown("#### PCA 2D Scatter: First 2 Components")
 
_, img2, _ = st.columns([1, 3, 1])
with img2:
    st.image(f"{RESULTS}/pca_2d.png")
 
st.markdown("""
The first 2 PCA components capture roughly 20% of total variance (PC1 ~ 8%, PC2 ~ 12%).
The scatter shows 2 distinct horizontal bands rather than crime-type clusters.
Colors represent crime types (0-7) but all crime types appear mixed within each band,
confirming that the first two components do not separate crime types cleanly.
 
The two bands are driven by the CallSource feature: Web Reported crimes,
which are predominantly Larceny, form one band while crimes reported through all
other channels form the other. Within each band, the spread along PC1 is driven
by the Hour feature.
""")
 
with st.expander("What drives the two bands?"):
    st.markdown("""
The 2 horizontal bands are explained by the CallSource feature: Web Reported crimes
(overwhelmingly Larceny) occupy one band while all other call sources occupy the other.
This is consistent with the EDA finding that Web Reported incidents are almost exclusively
Larceny (102,000 out of ~103,000 records). Within each band, the spread along PC1 is
driven by the Hour feature, which at importance 0.34 is the single strongest predictor.
Crime types are completely mixed within each band, confirming no clean separation exists.
""")
 
st.divider()
 
# section 3: k-means
st.subheader("3. K-Means Clustering")
 
st.markdown("#### Elbow Method")
 
_, img3, _ = st.columns([1, 3, 1])
with img3:
    st.image(f"{RESULTS}/kmeans_elbow.png")
 
st.markdown("""
The elbow plot shows no clear elbow: inertia decreases linearly from k = 2 to k = 10
with no obvious inflection point. This suggests the data does not naturally partition
into a small number of compact, well-separated clusters in the 22-dimensional feature space.
 
Given the absence of a clear elbow, k = 2 was selected as the most interpretable
starting point.
""")
 
with st.expander("Continuous vs clustered data"):
    st.markdown("""
A clear elbow appears when adding more clusters stops meaningfully reducing
within-cluster variance, indicating natural grouping structure. The linear
decrease here means each additional cluster reduces inertia by a similar amount,
suggesting the data forms a continuous rather than clustered distribution.
 
This is consistent with the crime data: incidents are spread across 24 hours,
7 days, 12 months, and 4 divisions, creating a roughly uniform distribution
in feature space rather than isolated clusters.
""")
 
st.markdown("#### K-Means Clusters (k=2) on PCA Components")
 
col1, col2 = st.columns(2)
 
with col1:
    st.image(f"{RESULTS}/kmeans_clusters.png", width = "stretch")
 
with col2:
    st.image(f"{RESULTS}/kmeans_crime_distribution.png", width = "stretch")
 
st.markdown("""
**Cluster 0:** 137,730 incidents | Mean Hour = 12.56
 
**Cluster 1:** 105,397 incidents | Mean Hour = 14.02
 
The two clusters differ primarily by time of day: Cluster 0 captures earlier
incidents and Cluster 1 captures later ones. The crime type distribution chart
tells the real story: Cluster 1 is almost entirely Larceny (~ 97%) while
Cluster 0 has a more balanced distribution across crime types (~ 50% Larceny,
~ 14% Assault, ~ 14% Burglary, ~ 14% GTA).
 
This means K-Means essentially learned to separate Larceny vs non-Larceny incidents,
which directly mirrors the class imbalance problem seen in classification.
""")
 
with st.expander("Reading the k = 2 result"):
    st.markdown("""
The k = 2 result is interpretable but not particularly insightful: it rediscovers
the class imbalance rather than revealing new structure. A few key points:
 
The ~ 1.5 hour difference in mean Hour between clusters suggests Larceny
incidents peak later in the day compared to other crime types, which is
consistent with the EDA hour analysis. Higher k values (3, 4, 5) could potentially
reveal more structure but without a clear elbow, choosing k is arbitrary.
Clustering on a 22-dimensional one-hot encoded space where most features are
binary (0 or 1) is inherently difficult for distance-based methods like K-Means.
Future work could try DBSCAN or clustering on PCA-reduced features to find
more meaningful groupings.
""")
 
st.divider()
 
# section 4: hierarchical clustering
st.subheader("4. Hierarchical Clustering")
 
st.markdown("""
Ward linkage hierarchical clustering was applied to a random sample of 500 incidents
(full dataset is too large for hierarchical clustering) to understand the nested
merge structure.
""")
 
_, img4, _ = st.columns([1, 3, 1])
with img4:
    st.image(f"{RESULTS}/hierarchical_dendrogram.png")
 
st.markdown("""
The dendrogram shows merges occurring at relatively high and uniform distances
(12-37 range), with no single obvious cut point that produces a small number of
well-separated clusters. This is consistent with the K-Means elbow finding:
the data does not have strong natural cluster boundaries.
 
The color coding shows approximately 4-5 meaningful sub-clusters at a cut height
of around 15-17, but these groupings would need further profiling to interpret
meaningfully given the limited 500-sample view.
""")
 
with st.expander("Method and sample size notes"):
    st.markdown("""
Ward linkage minimizes the total within-cluster variance at each merge step,
making it well-suited for compact, roughly equal-sized clusters. It is the most
commonly used linkage for general-purpose hierarchical clustering.
 
500 samples was chosen because hierarchical clustering has O(n^2) memory
complexity: running on all 243,127 incidents would require ~ 470GB of memory
for the distance matrix. The 500-sample dendrogram provides a representative
structural view but results may differ from the full dataset.
""")
 
st.divider()
 
# section 5: conclusion
st.subheader("5. Conclusion")
 
st.markdown("""
- No strong natural clusters exist in the Tucson crime data based on temporal
and spatial features. Both the PCA variance plot and K-Means elbow confirm a
continuous rather than clustered distribution.
 
- PCA requires 18-19 components to explain 90% of variance, meaning the
feature space is genuinely high-dimensional with no dominant low-rank structure.
 
- K-Means with k = 2 rediscovers the class imbalance: the two clusters separate
Larceny-heavy incidents from more balanced crime type distributions, with a
~ 1.5 hour mean Hour difference between clusters.
 
- The 2D PCA scatter shows 2 horizontal bands driven by the CallSource feature: Web Reported crimes form one band, all other call sources form the other. Crime types are completely mixed within each band with no clean separation.
 
- These results complement classification: the difficulty of unsupervised
clustering mirrors the difficulty of supervised prediction, both pointing to
the same fundamental challenge: crime type is hard to separate from time and
location features alone.
""")