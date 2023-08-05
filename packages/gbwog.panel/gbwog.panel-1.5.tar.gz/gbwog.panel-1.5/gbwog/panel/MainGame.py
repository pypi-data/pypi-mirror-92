from gbwog.panel.Live import welcome, load_game, username
from gbwog.panel.Utils import clear_screen


def start_panel():
    # congratulate player for enter the WoG
    welcome(username)

    # Finally, force the user to choose a game and start playing
    return load_game()

clear_screen()
status = "Start"
while status == "Start" or status == "Replay":
    status = start_panel()
