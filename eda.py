import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv(
    '..\data\AbandonoEmpleados.csv', sep =';',
    index_col='id',
    na_values='#N/D'
)
df

df.info()
miss = df.isna().sum().sort_values(ascending=False)
miss

miss_percentage = miss / len(df)
filtered = miss_percentage[miss_percentage != 0]
filtered

plt.figure(figsize=(6,3))
sns.barplot(
    x=filtered.values, y=filtered.index
)\
    .set(
        title='Percentage of missing values',
        ylabel='Variables'
    )

df.drop(columns=['anos_en_puesto','conciliacion'], inplace=True)
df.info()

obj =df.select_dtypes('O')
obj.shape[1]

from math import ceil

def eda_categorical_chart(cat):
    n_rows_subplot = ceil(cat.shape[1]/2)
    g,ax = plt\
            .subplots(
                nrows=n_rows_subplot,
                ncols= 2,
                figsize= (16, n_rows_subplot*6)
            )
    ax = ax.flat
    
    for my_index, my_column in enumerate(cat):
        cat[my_column]\
            .value_counts()\
            .plot.barh(ax=ax[my_index])
        ax[my_index]\
            .set_title(
                my_column,
                fontsize=12,
                fontweight='bold'
            )
        ax[my_index].tick_params(labelsize = 12)
        
eda_categorical_chart(df.select_dtypes('O'))

df.drop(columns = 'mayor_edad', inplace=True)
df['educacion'] = df['educacion'].fillna('Universitaria')
df['satisfaccion_trabajo'] = df['satisfaccion_trabajo'].fillna('Alta')
df['implicacion'] = df['implicacion'].fillna('Alta')

df.select_dtypes('number').describe()

def my_describe(num):
    des = num.describe().T
    des['median'] = num.median()
    #sorting columns
    des = des.iloc[:,[0,1,8,2,3,4,5,6,7]]
    return(des)

my_describe(df.select_dtypes('number'))

df.drop(
    columns=['empleados', 'sexo', 'horas_quincena'],
    inplace=True
)

abandonment_rate = df\
    .abandono\
    .value_counts(normalize = True) * 100
abandonment_rate

plt.figure(figsize=(3,2))
sns.barplot(
    x=abandonment_rate.index,
    y=abandonment_rate.values
)
df['abandono'] = df.abandono.map({'No':0, 'Yes':1})

temp = df\
    .groupby('educacion')\
    .abandono.mean()\
    .sort_values(ascending = False) * 100
plt.figure(figsize = (5, 2))
ax = temp.plot.bar()
ax.set_xticklabels(temp.index, rotation = 0)
plt.show()

temp = df\
    .groupby('estado_civil')\
    .abandono.mean()\
    .sort_values(ascending=False)*100
plt.figure(figsize=(5, 2))
ax = temp.plot.bar()
ax.set_xticklabels(temp.index, rotation = 0)
plt.show()

temp = df\
    .groupby('horas_extra')\
    .abandono.mean()\
    .sort_values(ascending=False)*100
plt.figure(figsize=(5, 3))
ax = temp.plot.bar()
ax.set_xticklabels(temp.index, rotation = 0)
plt.show()

temp = df\
    .groupby('puesto')\
    .abandono.mean()\
    .sort_values(ascending=False)*100
plt.figure(figsize=(15, 6))
ax = temp.plot.bar()
ax.set_xticklabels(temp.index, rotation = 15)
plt.show()

temp = df\
    .groupby('abandono')\
    .salario_mes.mean()\
    .sort_values(ascending=False)
plt.figure(figsize=(5, 3))
ax = temp.plot.bar()
ax.set_xticklabels(temp.index, rotation = 0)
plt.show()

df['salario_anual'] = df.salario_mes.transform(lambda x: x*12)
df[['salario_mes', 'salario_anual']]

conditions = [
    (df['salario_anual'] <= 30000),
    (df['salario_anual'] > 30000) & (df['salario_anual'] < 50000),
    (df['salario_anual'] > 50000) & (df['salario_anual'] <= 75000),
    (df['salario_anual'] > 75000)
]

results = [
    df.salario_anual * 0.161,
    df.salario_anual * 0.197,
    df.salario_anual * 0.204,
    df.salario_anual * 0.21
]

df['impacto_abandono'] = np.select(
    conditions,
    results,
    default = -999
)
df.head()

coste_total = df.loc[df.abandono == 1].impacto_abandono.sum()
coste_total

df.loc[
    (df.abandono == 1) & (df.implicacion == 'Baja')
].impacto_abandono.sum()

print(f"Reducir un 10% la fuga de empleados nos ahorraría {int(coste_total * 0.1)}$ cada año.")

print(f"Reducir un 20% la fuga de empleados nos ahorraría {int(coste_total * 0.2)}$ cada año.")

print(f"Reducir un 30% la fuga de empleados nos ahorraría {int(coste_total * 0.3)}$ cada año.")