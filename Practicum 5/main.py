import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.metrics import f1_score

scaler = StandardScaler()

# STEP 1 - load dataset
df = pd.read_csv("diabetes.csv")

print(df.head())


# STEP 2 - prepare data
# print(df.isnull().sum())

cols_with_zeros = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']

df[cols_with_zeros] = df[cols_with_zeros].replace(0, np.nan)

df[cols_with_zeros] = df[cols_with_zeros].fillna(df[cols_with_zeros].median())

# print(df.isnull().sum())


X = df.drop('Outcome', axis=1)
y = df['Outcome']


# STEP 3 - separate data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# STEP 4 - train model
# # model = LogisticRegression(max_iter=1000, random_state=42)
# model = LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42)
# model.fit(X_train_scaled, y_train)


# # STEP 5 - testing
# y_pred = model.predict(X_test_scaled)
# accuracy = accuracy_score(y_test, y_pred)
# print(f"Accuracy: {accuracy:.4f}")

# cm = confusion_matrix(y_test, y_pred)
# print("Confusion Matrix:")
# print(cm)

# # Детальний звіт
# print("Classification Report:")
# print(classification_report(y_test, y_pred))

# STEP 4 - train model
models = {
    "Logistic Regression (balanced)": LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "XGBoost": XGBClassifier(eval_metric='logloss', random_state=42)
}

best_model = None
best_model_name = ""
best_f1 = 0

for name, model in models.items():
    model.fit(X_train_scaled, y_train)

    # STEP 5 - testing
    y_pred = model.predict(X_test_scaled)

    print(f"\n === {name}")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("Classification Report:")
    print(classification_report(y_test, y_pred))


    #best model
    y_pred = model.predict(X_test_scaled)
    f1 = f1_score(y_test, y_pred, pos_label=1)
    
    
    if f1 > best_f1:
        best_f1 = f1
        best_model = model
        best_model_name = name



# # STEP 6 - new patient
feature_names = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 
                 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']

new_patient = pd.DataFrame([[2, 130, 70, 25, 100, 28.0, 0.5, 40]], columns=feature_names) # Healthy
new_patient_scaled = scaler.transform(new_patient)
prediction = best_model.predict(new_patient_scaled)

result = "Diabetes" if prediction[0] == 1 else "Healthy"
print(f"\nPrognosis for a new patient: {result}")
