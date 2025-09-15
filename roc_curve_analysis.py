import numpy as np
import matplotlib.pyplot as plt
import random
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier

# Generate synthetic medical dataset
X, y = make_classification(n_samples=1000, n_features=20, random_state=random.randint(1, 1000))
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=random.randint(1, 1000))

# Train a classifier
clf = RandomForestClassifier(n_estimators=100, random_state=random.randint(1, 1000))
clf.fit(X_train, y_train)

# Get predicted probabilities
y_scores = clf.predict_proba(X_test)[:, 1]  # Get probabilities for the positive class

# Introduce randomness by shuffling the scores slightly
y_scores = [score + random.uniform(-0.02, 0.02) for score in y_scores]

# Compute ROC curve
fpr, tpr, _ = roc_curve(y_test, y_scores)
roc_auc = auc(fpr, tpr)

# Plot ROC curve
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='blue', lw=2, label=f'ROC Curve (AUC = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='grey', linestyle='--')  # Random classifier
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc='lower right')
plt.grid()
plt.show()

# Interpret AUC Score
print(f'AUC Score: {roc_auc:.2f}')
if roc_auc >= 0.9:
    print("Excellent model performance.")
elif 0.8 <= roc_auc < 0.9:
    print("Good model performance.")
elif 0.7 <= roc_auc < 0.8:
    print("Fair model performance.")
elif 0.6 <= roc_auc < 0.7:
    print("Poor model performance.")
else:
    print("Model performs close to random guessing.")
