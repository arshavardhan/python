import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer

# 1. Create a sample dataset
data = {
    'Country': ['France', 'Spain', 'Germany', 'Spain', 'Germany', 'France', 'Spain'],
    'Gender': ['Female', 'Male', 'Female', 'Female', 'Male', 'Male', 'Female'],
    'Purchased': ['No', 'Yes', 'No', 'No', 'Yes', 'Yes', 'No']
}

df = pd.DataFrame(data)
print("Original DataFrame:\n", df)

# 2. Label Encoding for 'Gender' and 'Purchased'
le_gender = LabelEncoder()
df['Gender'] = le_gender.fit_transform(df['Gender'])  # Female=0, Male=1

le_purchased = LabelEncoder()
df['Purchased'] = le_purchased.fit_transform(df['Purchased'])  # No=0, Yes=1

# 3. One-Hot Encoding for 'Country'
ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), ['Country'])], remainder='passthrough')
df_encoded = ct.fit_transform(df)

# 4. Convert result back to DataFrame
column_names = ct.named_transformers_['encoder'].get_feature_names_out(['Country']).tolist() + ['Gender', 'Purchased']
df_final = pd.DataFrame(df_encoded, columns=column_names)

print("\nEncoded DataFrame:\n", df_final)
