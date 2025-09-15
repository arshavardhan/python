import numpy as np
import pandas as pd
import random
from sklearn.model_selection import KFold
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.datasets import make_regression

# Set random seed
random.seed(42)

# Generate a random dataset
X, y = make_regression(n_samples=100, n_features=5, noise=0.1, random_state=random.randint(0, 1000))

# Convert to DataFrame for better handling
X = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(X.shape[1])])
y = pd.Series(y, name='target')

# Initialize KFold with 5 splits and a fixed random state
kf = KFold(n_splits=5, shuffle=True, random_state=random.randint(0, 1000))

mse_scores = []

# Perform 5-fold cross-validation
for train_index, test_index in kf.split(X):
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]
    
    # Train linear regression model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Predict and compute MSE
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    mse_scores.append(mse)

# Report mean and standard deviation of MSE
mean_mse = np.mean(mse_scores)
std_mse = np.std(mse_scores)

print(f'Mean MSE: {mean_mse:.4f}')
print(f'Standard Deviation of MSE: {std_mse:.4f}')
