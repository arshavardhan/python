import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster

# 1. Generate synthetic data
X, _ = make_blobs(n_samples=50, centers=3, random_state=42)

# 2. Perform hierarchical/agglomerative clustering
linked = linkage(X, method='ward')  # 'ward' minimizes variance within clusters

# 3. Plot dendrogram
plt.figure(figsize=(10, 6))
dendrogram(linked,
           orientation='top',
           distance_sort='descending',
           show_leaf_counts=True)
plt.title("Hierarchical Clustering Dendrogram")
plt.xlabel("Sample Index")
plt.ylabel("Distance")
plt.grid(True)
plt.show()

# 4. Optional: Form flat clusters (e.g., k=3)
clusters = fcluster(linked, t=3, criterion='maxclust')

# 5. Optional: Plot clustered data
plt.figure(figsize=(8, 6))
plt.scatter(X[:, 0], X[:, 1], c=clusters, cmap='rainbow', edgecolor='black')
plt.title("Data Colored by Hierarchical Clusters")
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.grid(True)
plt.show()
