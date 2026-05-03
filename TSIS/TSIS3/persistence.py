import json
import os

# helper to load data from a file
def load_json(filename, default):
    # check if file exists on disk
    if not os.path.exists(filename):
        return default # return fallback if missing
    # open and parse json content
    with open(filename, "r") as f:
        return json.load(f)

# helper to save data to a file
def save_json(filename, data):
    # open file in write mode
    with open(filename, "w") as f:
        # save with 4-space indent for readability
        json.dump(data, f, indent=4)

# function to update the top scores
def add_score(name, score, distance):
    # get current leaderboard or empty list
    leaderboard = load_json("leaderboard.json", [])

    # create new entry dictionary
    new_entry = {"name": name, "score": score, "distance": int(distance)}
    # add to the local list
    leaderboard.append(new_entry)

    # sort list by score: highest first
    leaderboard = sorted(leaderboard, key=lambda x: x['score'], reverse=True)
    # keep only the best 10 players
    leaderboard = leaderboard[:10]

    # write updated list back to file
    save_json("leaderboard.json", leaderboard)