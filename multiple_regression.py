import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# 1. Generate synthetic dataset with multiple features
np.random.seed(42)
X1 = 2 * np.random.rand(100, 1)
X2 = 3 * np.random.rand(100, 1)
X = np.hstack((X1, X2))  # Combine into a feature matrix with 2 features
y = 5 + 2 * X1 + 3 * X2 + np.random.randn(100, 1)

# 2. Train a multiple linear regression model
model = LinearRegression()
model.fit(X, y)

# 3. Make predictions
y_pred = model.predict(X)

# 4. Print model parameters
print(f"Intercept: {model.intercept_[0]:.2f}")
print(f"Coefficients: {model.coef_}")
print(f"Mean Squared Error: {mean_squared_error(y, y_pred):.2f}")
print(f"R^2 Score: {r2_score(y, y_pred):.2f}")

# 5. (Optional) Visualize predicted vs actual values
plt.figure(figsize=(8, 6))
plt.scatter(y, y_pred, color='green', edgecolor='black')
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--', lw=2)
plt.xlabel('Actual y')
plt.ylabel('Predicted y')
plt.title('Multiple Linear Regression: Actual vs Predicted')
plt.grid(True)
plt.show()
