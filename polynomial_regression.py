import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score

# 1. Generate synthetic non-linear data
np.random.seed(42)
X = 2 * np.random.rand(100, 1)
y = 5 + 2 * X + X**2 + np.random.randn(100, 1)

# 2. Transform input features to polynomial features
degree = 2
poly_features = PolynomialFeatures(degree=degree, include_bias=False)
X_poly = poly_features.fit_transform(X)

# 3. Fit the polynomial regression model
model = LinearRegression()
model.fit(X_poly, y)

# 4. Make predictions
y_pred = model.predict(X_poly)

# 5. Print model details
print(f"Intercept: {model.intercept_[0]:.2f}")
print(f"Coefficients: {model.coef_}")
print(f"Mean Squared Error: {mean_squared_error(y, y_pred):.2f}")
print(f"R^2 Score: {r2_score(y, y_pred):.2f}")

# 6. Plot results
X_sorted = np.sort(X, axis=0)
X_sorted_poly = poly_features.transform(X_sorted)
y_sorted_pred = model.predict(X_sorted_poly)

plt.figure(figsize=(8, 6))
plt.scatter(X, y, color='blue', label='Actual Data')
plt.plot(X_sorted, y_sorted_pred, color='red', linewidth=2, label=f'Polynomial Regression (degree={degree})')
plt.title('Polynomial Regression')
plt.xlabel('X')
plt.ylabel('y')
plt.legend()
plt.grid(True)
plt.show()
