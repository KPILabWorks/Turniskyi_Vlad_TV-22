import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("data/Data.csv", delimiter="\t")  

num_sessions = 6
total_rows = len(df)
rows_per_session = total_rows // num_sessions


df["Session"] = df.index // rows_per_session
df.loc[df["Session"] >= num_sessions, "Session"] = num_sessions - 1
df["Distance_cm"] = df["Session"] * 15


grouped = df.groupby("Distance_cm")["Absolute field (µT)"].mean().reset_index()

plt.figure(figsize=(8,6))
order = sorted(df["Distance_cm"].unique())
sns.boxplot(x="Distance_cm", y="Absolute field (µT)", data=df, showfliers=False, color="lightblue", order=order)

plt.plot(
    [order.index(x) for x in grouped["Distance_cm"]],
    grouped["Absolute field (µT)"],
    marker="o", color="red", label="Mean value"
)

plt.xticks(ticks=range(len(order)), labels=order) 
plt.title("Dependence of magnetic field on distance")
plt.xlabel("Distance to the device (cm)")
plt.ylabel("Absolute magnetic field (µT)")
plt.grid(True)
plt.legend()
plt.show()

