import pandas as pd
import os
from sklearn.preprocessing import OneHotEncoder


df = pd.read_csv('../../data/processed/trainAbandonoE.csv', index_col = 'id')
df

df_ml = df.copy()
df_ml.info()

# Categorical
cat = df_ml.select_dtypes('O')

# Instance
ohe = OneHotEncoder(sparse = False)

# Training
ohe.fit(cat)

cat_ohe = ohe.transform(cat)

cat_ohe = pd.DataFrame(
    cat_ohe,
    columns = ohe.get_feature_names_out(input_features = cat.columns)
).reset_index(drop = True)

cat_ohe

num = df.select_dtypes('number').reset_index(drop = True)

# Final database
df_ml = pd.concat([cat_ohe, num], axis = 1)
df_ml


