import dask.dataframe as dd
import vaex
import numpy as np
import pandas as pd
from dask_ml.preprocessing import StandardScaler as DaskScaler
from dask_ml.cluster import KMeans as DaskKMeans
from sklearn.preprocessing import StandardScaler as SklearnScaler
from sklearn.cluster import KMeans as SklearnKMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from time import perf_counter
from dask.distributed import Client
from dask.diagnostics import ProgressBar

# ==========================================
# == STEP 1 - SETUP DATASET (Dask)  ==
# ==========================================
print("STEP 1 - SETUP DATASET (Dask)")

file_path = "household_power_consumption.txt"
df_dask = dd.read_csv(
    file_path,
    sep=";",
    na_values="?",
    dtype={
        "Date": "object",
        "Time": "object",
        "Global_active_power": "float64",
        "Global_reactive_power": "float64",
        "Voltage": "float64",
        "Global_intensity": "float64",
        "Sub_metering_1": "float64",
        "Sub_metering_2": "float64",
        "Sub_metering_3": "float64",
    },
    assume_missing=True
)

numerical_columns = [
    "Global_active_power", "Global_reactive_power", "Voltage",
    "Global_intensity", "Sub_metering_1", "Sub_metering_2", "Sub_metering_3"
]

df_dask = df_dask.dropna(subset=numerical_columns)

# Scale data
X_dask = df_dask[numerical_columns]
scaler_dask = DaskScaler()
X_dask_scaled = scaler_dask.fit_transform(X_dask)


# ==========================================
# == STEP 2 - USE (Dask) ==
# ==========================================
print("STEP 2 - USE (Dask)")
# client = Client()
# print(f"\n✅ Dask Dashboard available at: {client.dashboard_link}")

# # Включаем ProgressBar в консоль
# pbar = ProgressBar()
# pbar.register()


start_dask = perf_counter()
kmeans_dask = DaskKMeans(n_clusters=4, init_max_iter=5)
kmeans_dask.fit(X_dask_scaled)
end_dask = perf_counter()

print(f"Clustering time with Dask + Sklearn: {end_dask - start_dask:.2f} seconds")

labels_dask = kmeans_dask.predict(X_dask_scaled).compute()
unique_dask, counts_dask = np.unique(labels_dask, return_counts=True)
print(f"Dask clusters: {dict(zip(unique_dask, counts_dask))}")



# ==========================================
# == STEP 3 - SETUP DATASET (Vaex)  ==
# ==========================================
print("STEP 3 - SETUP DATASET (Vaex)") #household_power_consumption.txt

file_path = "household_power_consumption.txt"
numerical_columns = [
    'Global_active_power',
    'Global_reactive_power',
    'Voltage',
    'Global_intensity',
    'Sub_metering_1',
    'Sub_metering_2',
    'Sub_metering_3'
]


df_pd = pd.read_csv(
    file_path,
    sep=';',
    na_values=['?'],
    dtype={col: 'float64' for col in numerical_columns},
    low_memory=False
)

df_vaex = vaex.from_pandas(df_pd)

df_vaex_clean = df_vaex.dropna(column_names=numerical_columns)
X_vaex = df_vaex_clean[numerical_columns].to_pandas_df().values

scaler_vaex = SklearnScaler()
X_vaex_scaled = scaler_vaex.fit_transform(X_vaex)



# ==========================================
# == STEP 4 - USE (Vaex) ==
# ==========================================
print("STEP 4 - USE (Vaex)")

start_vaex = perf_counter()
kmeans_vaex = SklearnKMeans(n_clusters=4, n_init='auto')
kmeans_vaex.fit(X_vaex_scaled)
end_vaex = perf_counter()

print(f"Clustering time with Vaex + Sklearn: {end_vaex - start_vaex:.2f} seconds")

labels_vaex = kmeans_vaex.predict(X_vaex_scaled)
unique_vaex, counts_vaex = np.unique(labels_vaex, return_counts=True)
print(f"Vaex clusters: {dict(zip(unique_vaex, counts_vaex))}")


