import requests
import time
import json
import os
from datetime import datetime
from typing import Union

MATCHES_URL = "https://api.opendota.com/api/publicMatches"
MATCH_URL = "https://api.opendota.com/api/matches/"
SAVE_FILE = "matches.jsonl"

def update_data(start: Union[int, str]):

    matches = []
    count = 0
    last_match_id = 0
    max_rows = 100000
    waiting_time = 18
    waiting_count = 0


    if isinstance(start, str):
        try:
            dt = datetime.strptime(start, "%Y-%m-%d")
            unix_time = int(dt.timestamp())
            
            while len(matches) < max_rows:
                params = {}
                if last_match_id:
                    params['less_than_match_id'] = last_match_id

                response = requests.get(MATCHES_URL, params=params)
                
                if response.status_code == 429:
                    print(f"Waiting... (10 seconds)")
                    time.sleep(10) 
                    continue
                    
                elif response.status_code != 200:
                    print(f"Request '/matches-date' error: {response.status_code}")
                    break

                data = response.json()
                if not data:
                    print("No more data")
                    break

                last_match_id = data[-1]["match_id"]
                last_time = data[-1]["start_time"]

                if unix_time > last_time:
                    break

                matches.extend(data)
                count = len(matches)
                print(f"Loaded: {count} matches")
                time.sleep(1) 

        except Exception as e:
            print(f'Date parsing error: {e}')
            return []
    elif isinstance(start, int):
        last_match_id = start
        while len(matches) < max_rows:
            params = {'less_than_match_id': last_match_id}
            response = requests.get("https://api.opendota.com/api/publicMatches", params=params)

            if response.status_code == 429:
                print(f"Waiting... (10 seconds)")
                time.sleep(10) 
                waiting_count += 1
                if waiting_count >= waiting_time:
                    break
                continue
                    
            elif response.status_code != 200:
                print(f"Request '/matches-int' error: {response.status_code}")
                break

            data = response.json()
            if not data:
                print("There are no new matches")
                break

            waiting_count = 0
            matches.extend(data)
            count = len(matches)
            print(f"Loaded: {count} matches (last match_id: {last_match_id})")
            last_match_id = data[-1]["match_id"]
            time.sleep(1)
    else:
        print("The start argument must be either the date “YYYY-MM-DD” or a numeric match_id")

    return matches


def load_existing_ids(save_file):
    existing_ids = set()
    if os.path.exists(save_file):
        with open(save_file, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    data = json.loads(line)
                    existing_ids.add(data.get("match_id"))
                except:
                    continue
    return existing_ids

def extract_simplified_public_match(match: dict) -> dict:
    return {
        "match_id": match.get("match_id"),
        "radiant_win": match.get("radiant_win"),
        "start_time": match.get("start_time"),
        "duration": match.get("duration"),
        "avg_rank_tier": match.get("avg_rank_tier"),
        "radiant_team": match.get("radiant_team", []),
        "dire_team": match.get("dire_team", []),
        "game_mode": match.get("game_mode"),
        "lobby_type": match.get("lobby_type"),
    }

def save_simplified_match(match: dict, existing_ids: set, save_file="matches.jsonl"):
    match_id = match.get("match_id")
    if match_id in existing_ids:
        # print(f"Match {match_id} already saved.")
        return False

    simplified = extract_simplified_public_match(match)

    with open(save_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(simplified) + "\n")

    existing_ids.add(match_id)
    return True



def check_unique(matches):
    # 1. Filter ids
    match_ids = [m['match_id'] for m in matches]
    unique_match_ids = set(match_ids)
    duplicates = set([id for id in match_ids if match_ids.count(id) > 1])

    if duplicates:
        print(f"‘Found duplicates match_id: {duplicates}")
    else:
        print("All match_ids are unique")

    # 2. Filter time
    # target_match_id = matches[-1]['match_id']
    dt = datetime.strptime("2025-06-04", "%Y-%m-%d")
    unix_time = int(dt.timestamp())
    later_count = sum(1 for m in matches if m['start_time'] > unix_time)

    print(f"Matches later unix_time {unix_time}: {later_count}")




# def main
existing_ids = load_existing_ids(SAVE_FILE)
min_id = min(existing_ids)
print(min_id)

# matches = update_data("2025-06-01")
matches = update_data(min_id)
print("Total number of matches:", len(matches))
check_unique(matches)
print([match["match_id"] for match in matches[:10]])


for match in matches:
    save_simplified_match(match, existing_ids)



