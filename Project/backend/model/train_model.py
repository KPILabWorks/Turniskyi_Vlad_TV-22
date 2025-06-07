
from keras.config import enable_unsafe_deserialization
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score
import numpy as np
import pandas as pd
import json
from model import DotaMatchPredictor
import os


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


enable_unsafe_deserialization()
matches = load_matches("../data/matches.jsonl")
# x_radiant = matches["radiant_team"]
# x_dire = matches["dire_team"]
# x_rank = matches["avg_rank_tier"]
# y = matches["radiant_win"]

matches_df = pd.DataFrame(matches)

radiant_ids = np.array(matches_df["radiant_team"].tolist())
dire_ids = np.array(matches_df["dire_team"].tolist())
ranks = matches_df["avg_rank_tier"].values.reshape(-1, 1)
y_array = matches_df["radiant_win"].values


radiant_train, radiant_test, dire_train, dire_test, rank_train, rank_test, y_train, y_test = train_test_split(
    radiant_ids, dire_ids, ranks, y_array,
    test_size=0.2, random_state=42, stratify=y_array
)

model = DotaMatchPredictor()
model_path = "my_model.keras"

if os.path.exists(model_path):
    model = model.load(model_path)
    print("The model has been successfully downloaded.")
else:
    print("Model file not found:", model_path)


model.fit(radiant_train, dire_train, rank_train, y_train, 256, 250)
preds = model.predict(radiant_test, dire_test, rank_test)


auc = roc_auc_score(y_test, preds)
# accuracy = accuracy_score(y_test, preds)
# print(f"Accuracy: {accuracy:.4f}")
print(f"Test ROC AUC: {auc:.4f}")

model.save("my_model.keras") 

# from tensorflow.keras.utils import plot_model
# plot_model(model.mode, to_file='model.png', show_shapes=True, show_layer_names=True)