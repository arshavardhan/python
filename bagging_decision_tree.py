# Import required libraries
import matplotlib.pyplot as plt
from sklearn.ensemble import BaggingClassifier, BaggingRegressor
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, plot_tree
from sklearn.datasets import load_iris, fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error

# Load the Iris dataset (for classification)
iris = load_iris()
X, y = iris.data, iris.target

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Single Decision Tree (For Comparison)
tree = DecisionTreeClassifier(random_state=42)
tree.fit(X_train, y_train)
y_pred_tree = tree.predict(X_test)

# Visualize the trained decision tree
plt.figure(figsize=(12, 8))
plot_tree(tree, filled=True, feature_names=iris.feature_names, class_names=iris.target_names, rounded=True)
plt.title("Single Decision Tree Visualization")
plt.show()

# Train a Bagging Classifier (Bootstrap Aggregating with Decision Trees)
bagging = BaggingClassifier(
    estimator=DecisionTreeClassifier(),  # Decision Tree as base model
    n_estimators=10,  # Number of trees
    bootstrap=True,  # Enable bootstrap sampling
    random_state=42
)
bagging.fit(X_train, y_train)
y_pred_bagging = bagging.predict(X_test)

# Calculate Accuracy for Classification
accuracy_tree = accuracy_score(y_test, y_pred_tree)
accuracy_bagging = accuracy_score(y_test, y_pred_bagging)

# Print the classification accuracy
print("Single Decision Tree Accuracy:", accuracy_tree)

# Print the bagging classifier accuracy
print("Bagging Classifier Accuracy:", accuracy_bagging)

# For Regression Example (California Housing dataset)
housing = fetch_california_housing()
X_reg, y_reg = housing.data, housing.target

# Split into training and testing sets for regression
X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(X_reg, y_reg, test_size=0.2, random_state=42)

# Train a Single Decision Tree Regressor (For Comparison)
tree_regressor = DecisionTreeRegressor(random_state=42)
tree_regressor.fit(X_train_reg, y_train_reg)
y_pred_tree_regressor = tree_regressor.predict(X_test_reg)

# Train a Bagging Regressor
bagging_regressor = BaggingRegressor(
    estimator=DecisionTreeRegressor(),  # Decision Tree as base model
    n_estimators=10,  # Number of trees
    bootstrap=True,
    random_state=42
)
bagging_regressor.fit(X_train_reg, y_train_reg)
y_pred_bagging_regressor = bagging_regressor.predict(X_test_reg)

# Calculate MSE for Regression
mse_tree = mean_squared_error(y_test_reg, y_pred_tree_regressor)
mse_bagging = mean_squared_error(y_test_reg, y_pred_bagging_regressor)

# Print the regression MSE
print("Single Decision Tree MSE:", mse_tree)
print("Bagging Regressor MSE:", mse_bagging)
