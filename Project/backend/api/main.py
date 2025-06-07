from enum import Enum
from typing import List, Dict
from enum import Enum
from collections import defaultdict
from fastapi import FastAPI
from pydantic import BaseModel
import json
import numpy as np
from fastapi.middleware.cors import CORSMiddleware

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.model import DotaMatchPredictor

class GameMode(int, Enum):
    ALL_PICK = 22
    TURBO = 4

class Rank(int, Enum):
    ALL = 0
    HERALD = 1
    GUARDIAN = 2
    CRUSADER = 3
    ARCHON = 4
    LEGEND = 5
    ANCIENT = 6
    DIVINE = 7
    TITAN = 8

class MatchData(BaseModel):
    radiant: list[int]
    dire: list[int]
    rank: int

def load_matches(file_path):
    matches = []
    with open(file_path, 'r') as f:
        for line in f:
            match = json.loads(line)
            matches.append(match)
    return matches


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

matches_data = load_matches("../data/matches.jsonl")
predictor = DotaMatchPredictor()
# predictor.load("../model/my_model.keras")

@app.get("/meta")
async def get_meta(gm: GameMode = GameMode.ALL_PICK, rank : Rank = Rank.ALL):
    hero_stats: Dict[int, Dict[str, int]] = defaultdict(lambda: {"matches": 0, "wins": 0})

    rank_start = rank.value * 10
    rank_end = (rank.value + 1) * 10
    for match in matches_data:
        if match["game_mode"] != gm.value:
            continue

        if rank.value != 0 and not (rank_start <= match["avg_rank_tier"] < rank_end):
            continue


        radiant_win = match["radiant_win"]
        for hero_id in match["radiant_team"]:
            hero_stats[hero_id]["matches"] += 1
            if radiant_win:
                hero_stats[hero_id]["wins"] += 1
        for hero_id in match["dire_team"]:
            hero_stats[hero_id]["matches"] += 1
            if not radiant_win:
                hero_stats[hero_id]["wins"] += 1

    result = [
        {
            "hero_id": hero_id,
            "matches": stats["matches"],
            "wr": round(stats["wins"] / stats["matches"] * 100, 2) if stats["matches"] > 0 else 0.0
        }
        for hero_id, stats in hero_stats.items()
    ]

    return result

@app.post("/predict")
def predict_match(data: MatchData):
    radiant = np.array([data.radiant], dtype=np.int32)
    dire = np.array([data.dire], dtype=np.int32)
    rank = np.array([[data.rank]], dtype=np.int32)


    prediction = predictor.predict(radiant, dire, rank)
    win_probability = float(prediction[0][0]) 

    return {
        "radiant_win_probability": win_probability
    }

@app.get("/")
async def root():
    return {"message": "Hello World"}
