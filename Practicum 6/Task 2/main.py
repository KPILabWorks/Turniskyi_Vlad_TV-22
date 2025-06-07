import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns

# ==== LOAD FILES ====
acc_low = pd.read_csv('data/Acceleration Low.csv', sep='\t')
acc_medium = pd.read_csv('data/Acceleration Medium.csv', sep='\t')
acc_high = pd.read_csv('data/Acceleration High.csv', sep='\t')

sound_low = pd.read_csv('data/Amplitudes Low.csv', sep='\t')
sound_medium = pd.read_csv('data/Amplitudes Medium.csv', sep='\t')
sound_high = pd.read_csv('data/Amplitudes High.csv', sep='\t')



# ==== INTERPOLATION DATA ====

def interpolation_df(acc_df, sound_df, level_label):
    # Prepare
    sound_df = sound_df.drop_duplicates(subset='Time (s)')
    sound_df = sound_df.sort_values('Time (s)')
    sound_df = sound_df.dropna()

    acc_df['Time (s)'] = acc_df['Time (s)'].astype(float)
    sound_df['Time (s)'] = sound_df['Time (s)'].astype(float)

    # interpolation
    acc_df['SPL (dB)'] = np.interp(
        acc_df['Time (s)'],
        sound_df['Time (s)'],
        sound_df['Sound pressure level (dB)']
    )

    # column edit
    acc_df['Level'] = level_label
    acc_df = acc_df.drop(columns=['Time (s)'])

    return acc_df


df_low = interpolation_df(acc_low, sound_low, 'low')
df_medium = interpolation_df(acc_medium, sound_medium, 'medium')
df_high = interpolation_df(acc_high, sound_high, 'high')

final_df = pd.concat([df_low, df_medium, df_high], ignore_index=True)

# check
print(final_df.head())
print(final_df['Level'].value_counts())


# ==== SPLIT DATA ====
X = final_df.drop(columns=['Level'])  # всі стовпці, крім цільового
y = final_df['Level']                 # цільовий стовпець

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,         # 20% для тесту
    random_state=42,       # для повторюваності
    stratify=y             # зберігає пропорції класів
)

print("Train shape:", X_train.shape)
print("Test shape:", X_test.shape)
print("Train class balance:\n", y_train.value_counts(normalize=True))
print("Test class balance:\n", y_test.value_counts(normalize=True))


# ==== CREATE MODEL ====

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("Classification Report:")
print(classification_report(y_test, y_pred))

# Матриця змішування
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=model.classes_, yticklabels=model.classes_)
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()



