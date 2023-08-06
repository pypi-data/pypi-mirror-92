import getpass, time
from colorama import Fore,Style
from gbwog.panel.MemoryGame import MemoryGame
from gbwog.panel.GuessGame import GuessGame
from gbwog.panel.CurrencyRoulette import CurrencyRoulette
from gbwog.panel.Utils import clear_screen
from gbwog.panel.Utils import games

username = getpass.getuser()
game_status = ""


def welcome(name):
    print(f'{Fore.LIGHTCYAN_EX}Hello {name} and welcome to the World of Games (WoG)!'
          f'\nHere you can find incredibly cool games to play. \n{Style.RESET_ALL}')


def load_game():
    # Function for player choice to exit
    def say_goodbye():
        print(f'{Fore.LIGHTRED_EX}Goodbye {username}! {Style.RESET_ALL}')

    # Input variables for prevent complex code
    # try again note
    try_again = f"{Fore.LIGHTYELLOW_EX}Do you want to try again? \nEnter Y to try again and any other text to exit {Style.RESET_ALL}"
    # wrong choice note
    wrong = f"{Fore.LIGHTRED_EX}Wrong Choice! {Style.RESET_ALL}"
    # variable which determine if user want to retry or not
    retry = "Empty"
    # inserting game id tutorial
    game_id_tut = str(f"""{Fore.LIGHTCYAN_EX}List of games :
1. Memory Game - a sequence of numbers will appear for 1 second and you have to guess it back.
2. Guess Game - guess a number and see if the computer chose the same one as you.
3. Currency Roulette - try to guess the value of a random amount of USD in ILS

{Fore.LIGHTYELLOW_EX}Choose game number: {Style.RESET_ALL}""")
    # inserting game difficult tutorial
    game_diff_tut = str(f"{Fore.LIGHTYELLOW_EX}\nChoose level on scale of 1 (Easiest) to 5: {Style.RESET_ALL}")

    # Check if user start the game ("Empty") or want to retry("Y")
    while retry == "Empty" or retry == "Y" or retry == "y":
        # Asking for game id number
        game_id = input(game_id_tut)
        time.sleep(0.5)
        # Check if number is inserted
        if game_id.isdigit():
            # Check if number between 1 and 3 is inserted
            if 0 < int(game_id) < 4:
                game_diff = input(game_diff_tut)
                time.sleep(0.5)
                if game_diff.isdigit():
                    if 0 < int(game_diff) < 6:
                        retry = "Done"
                        game_id = int(game_id)
                        game_diff = int(game_diff)
                    else:
                        # Error - game_diff number is out of range, asking if the user want to retry choosing option
                        retry = input(wrong + "\n" + try_again)
                        time.sleep(1.5)
                else:
                    # Error - game_diff number wasn't inserted , asking if the user want to retry choosing option
                    retry = input(wrong + "\n" + try_again)
                    time.sleep(1.5)
            else:
                # Error - game_id number is out of range, asking if the user want to retry choosing option
                retry = input(wrong + "\n" + try_again)
                time.sleep(1.5)
        else:
            # Error - game_id number wasn't inserted, asking if the user want to retry choosing option
            retry = input(wrong + "\n" + try_again)
            time.sleep(1.5)
    # If user input check has finished successfully, start game
    if retry == "Done":
        # Defining the name of the game
        game_name = games[int(game_id)]
        print(f'{Fore.YELLOW}\nPlaying {game_name} on level {game_diff} . . . {Style.RESET_ALL}')
        time.sleep(2)
        clear_screen()
        # create Game class which will start the chosen game
        chosen_game = eval(f'{game_name}' + f'(diff={game_diff}, user="{username}")')
        game_status = chosen_game.play()
        return str(game_status)
    # Say goodbye if user doesnt want to retry
    elif retry != "Empty" and retry != "Y" and retry != "y":
        say_goodbye()
        return "Bye"
