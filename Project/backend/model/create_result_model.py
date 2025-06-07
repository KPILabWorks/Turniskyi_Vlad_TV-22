import json
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score
import xgboost as xgb
import pandas as pd

HERO_COUNT = 138  

def load_matches(filename):
    matches = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            try:
                match = json.loads(line)
                if (match.get("radiant_team") and match.get("dire_team")
                    and len(match["radiant_team"]) == 5
                    and len(match["dire_team"]) == 5
                    and match["game_mode"] == 22):
                    matches.append(match)
            except:
                continue
    return matches

def match_to_features(match):
    vec = np.zeros(HERO_COUNT * 2 + 1)  # 138 radiant + 138 dier + 1 rank

    for hid in match["radiant_team"]:
        if 1 <= hid <= HERO_COUNT:
            vec[hid - 1] = 1

    for hid in match["dire_team"]:
        if 1 <= hid <= HERO_COUNT:
            vec[HERO_COUNT + hid - 1] = 1

    avg_rank = match.get("avg_rank_tier", 0)
    vec[-1] = avg_rank / 100  # normalise to the range [0,1.5]

    target = int(match["radiant_win"])
    return vec, target


def augment_data(X, y):
    X_aug = X.copy()
    
    X_aug[:, :138], X_aug[:, 138:276] = X[:, 138:276], X[:, :138] # Меняем местами Radiant <-> Dire
    y_aug = 1 - y  # инвертируем результат

    X_full = np.concatenate([X, X_aug], axis=0)
    y_full = np.concatenate([y, y_aug], axis=0)
    return X_full, y_full


#def main()
matches = load_matches("../data/matches.jsonl")
X, y = zip(*[match_to_features(m) for m in matches])
X = np.array(X)
y = np.array(y)

# Аугментация: зеркальный матч
print(f"len {len(X)}")
X, y = augment_data(X, y)
print(f"len {len(X)}")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LogisticRegression(max_iter=1000)
# model = xgb.XGBClassifier(eval_metric='logloss')
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

print(f"Accuracy: {accuracy_score(y_test, y_pred):.3f}")
print(f"ROC AUC:  {roc_auc_score(y_test, y_proba):.3f}")
