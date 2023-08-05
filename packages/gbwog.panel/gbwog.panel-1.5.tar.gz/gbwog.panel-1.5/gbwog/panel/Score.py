from os import path, mkdir
from gbwog.panel.Utils import SCORES_FILE_NAME, home_dir
from gbwog.panel.Utils import games
from pathlib import Path
import json

games_score = {}
for game in games:
    games_score[f'{games[game]}'] = 0
games_def_score = {"games": games_score}


def add_score(diff: int, game: str):
    points_of_winning = (diff * 3) + 5
    if path.exists(f"{SCORES_FILE_NAME}"):
        with open(f"{SCORES_FILE_NAME}","r+") as file:
            if not file.read().__contains__("games"):
                json.dump(games_def_score, file)

    else:
        if not path.exists(Path(f"{home_dir}/wog")):
            mkdir(Path(f"{home_dir}/wog"))
        else:
            with open(f"{SCORES_FILE_NAME}", "w") as file:
                json.dump(games_def_score, file)
        with open(f"{SCORES_FILE_NAME}", "w") as file:
            json.dump(games_def_score, file)
    with open(f"{SCORES_FILE_NAME}", 'r+') as score:
        games_score = json.loads(score.read())
    current_score = games_score['games'][f'{game}']
    if str(current_score).isdigit():
        games_score['games'][f'{game}'] = int(current_score) + int(points_of_winning)
    else:
        games_score['games'][f'{game}'] = int(points_of_winning)
    with open(f"{SCORES_FILE_NAME}", "w+") as score:
        json.dump(games_score, score)
