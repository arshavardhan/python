import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, shapiro

# 1. Generate a normally distributed dataset
mean = 0
std_dev = 1
size = 1000
data = np.random.normal(loc=mean, scale=std_dev, size=size)

# 2. Plot the histogram with the probability density function (PDF)
plt.figure(figsize=(10, 6))
count, bins, ignored = plt.hist(data, bins=30, density=True, alpha=0.6, color='skyblue', edgecolor='black')

# Plot the PDF line
pdf = norm.pdf(bins, mean, std_dev)
plt.plot(bins, pdf, 'r', linewidth=2)

plt.title('Normal Distribution (mean=0, std=1)')
plt.xlabel('Value')
plt.ylabel('Probability Density')
plt.grid(True)
plt.show()

# 3. Perform a Shapiro-Wilk test for normality
stat, p_value = shapiro(data)
print(f"Shapiro-Wilk Test:\nStatistic = {stat:.4f}, p-value = {p_value:.4f}")

if p_value > 0.05:
    print("The data appears to be normally distributed (fail to reject H0).")
else:
    print("The data does not appear to be normally distributed (reject H0).")
