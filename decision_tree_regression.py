import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.tree import plot_tree

# 1. Generate synthetic non-linear data
np.random.seed(42)
X = np.sort(5 * np.random.rand(80, 1), axis=0)
y = np.sin(X).ravel() + 0.1 * np.random.randn(80)

# 2. Train a Decision Tree Regressor
model = DecisionTreeRegressor(max_depth=4)
model.fit(X, y)

# 3. Predict on a smooth range for plotting
X_test = np.linspace(0, 5, 500).reshape(-1, 1)
y_pred = model.predict(X_test)

# 4. Evaluate
y_train_pred = model.predict(X)
print(f"Mean Squared Error: {mean_squared_error(y, y_train_pred):.2f}")
print(f"R^2 Score: {r2_score(y, y_train_pred):.2f}")

# 5. Plot results
plt.figure(figsize=(10, 6))
plt.scatter(X, y, color="darkorange", label="Actual Data", edgecolor='black')
plt.plot(X_test, y_pred, color="cornflowerblue", label="Decision Tree Prediction", linewidth=2)
plt.xlabel("X")
plt.ylabel("y")
plt.title("Decision Tree Regression")
plt.legend()
plt.grid(True)
plt.show()
plt.figure(figsize=(12, 6))
plot_tree(model, filled=True, feature_names=["X"])
plt.title("Decision Tree Structure")
plt.show()
