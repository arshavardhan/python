import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns

# Load the dataset
df = pd.read_csv(r"C:\Users\dumpa\Downloads\archive\survey.csv")

# Data Cleaning
df_clean = df.drop(columns=['Timestamp', 'comments'])  # Drop unnecessary columns

# Filter out unrealistic ages (if any)
df_clean = df_clean[(df_clean['Age'] >= 18) & (df_clean['Age'] <= 100)]

# Fill missing values
df_clean['self_employed'].fillna('No', inplace=True)
df_clean['work_interfere'].fillna("Don't know", inplace=True)
df_clean['state'].fillna('Unknown', inplace=True)

# Encode categorical features using LabelEncoder
label_encoders = {}
for column in df_clean.columns:
    if df_clean[column].dtype == 'object':
        le = LabelEncoder()
        df_clean[column] = le.fit_transform(df_clean[column])
        label_encoders[column] = le

# Define features and target
X = df_clean.drop(columns=['treatment'])
y = df_clean['treatment']

# Split the dataset into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the Random Forest model
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Predict on the test set
y_pred = rf_model.predict(X_test)

# Evaluation: Classification Report and Confusion Matrix
report = classification_report(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)
print("Classification Report:\n", report)
print("Confusion Matrix:\n", cm)

# Plotting the Confusion Matrix
plt.figure(figsize=(6, 4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False,
            xticklabels=["Predicted No", "Predicted Yes"], yticklabels=["Actual No", "Actual Yes"])
plt.title("Random Forest Confusion Matrix")
plt.ylabel("Actual")
plt.xlabel("Predicted")
plt.show()

# Plot Feature Importances
importances = rf_model.feature_importances_
features = X.columns
indices = np.argsort(importances)

plt.figure(figsize=(10, 6))
plt.title("Feature Importances from Random Forest")
plt.barh(range(len(indices)), importances[indices], color='b', align='center')
plt.yticks(range(len(indices)), [features[i] for i in indices])
plt.xlabel("Relative Importance")
plt.show()
