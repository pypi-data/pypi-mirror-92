from os import system
from os import sys
from pathlib import Path

home_dir = f"{Path.home()}"
SCORES_FILE_NAME = Path(f"{home_dir}/wog/score.json")
BAD_RETURN_CODE = 1998
games = {1: "MemoryGame", 2: "GuessGame", 3: "CurrencyRoulette"}
flask_url = "http://127.0.0.1:5000/scores"

# Function to clear user's screen
def clear_screen():
    # Clear the screen in order to avoid the user to cheat
    if sys.platform.__contains__('win'):
        system('cls')
    else:
        system('clear')
