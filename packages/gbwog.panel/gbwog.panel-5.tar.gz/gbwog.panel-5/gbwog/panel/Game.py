# Import game modules and ABC class
from abc import ABC, abstractmethod
from colorama import Fore,Style
from gbwog.panel.Utils import clear_screen
from gbwog.panel.Score import add_score
import time


# Define General Game Class

class Game(ABC):

    # Any game has a name, difficulty level, playing username, number of guesses, number of wins, result
    def __init__(self, diff: int, user: str):
        self.user = user
        self.diff = diff
        self.number_of_guesses = 0
        self.number_of_wins = 0
        # retry and replay will be edited on specific game due choice
        self.retry = "NotDefined"
        self.replay = "NotDefined"
        self.winning = "NotDefined"
        self.status = "Start"

    @abstractmethod
    # Any game has a welcome message
    def welcome_player(self):
        print(f"""{Fore.LIGHTCYAN_EX}Hi {self.user}, welcome to {type(self).__name__}!
I am NumbeRobot and you chose to challenge me on level {self.diff}! \n {Style.RESET_ALL}""")

    @abstractmethod
    # Any game has rules
    def present_rules(self):
        print(self.rules)

    @abstractmethod
    # game progress of any game
    def play(self):
        # Welcome player
        self.welcome_player()
        time.sleep(2)
        # Check conditions in order to play
        while self.retry == "NotDefined" or self.retry == "Y" or self.retry == "y":
            # Present specific game rules
            self.present_rules()
            time.sleep(2)
            # game process of specific game
            self.game_process()
            self.number_of_guesses += 1
            time.sleep(1.5)
            self.compare_results()
            time.sleep(3)
            self.publish_results()
            time.sleep(1.5)
            # Present statistics at the end of attempt or round
            self.present_statistics()
            # Check if user chose to replay
            if self.winning.__contains__("True"):
                add_score(diff= self.diff, game= type(self).__name__)
                self.check_replay()
            # Check if user crossed the maximum number of attempts at the same round
            elif self.winning == "False- End_Of_Chances":
                print(f"{Fore.LIGHTRED_EX}Unfortunately, it was the last chance so you cant retry.")
                time.sleep(1)
                self.check_replay()
                # Check if user want to replay a new round
            else:
                # Check if user wants to retry after he failed
                self.check_retry()

    # Compare results based on the specific game compare_results()
    @abstractmethod
    def compare_results(self):
        pass

    # Announce results based on the specific game results
    @abstractmethod
    def publish_results(self):
        if self.winning.__contains__("True"):
            print(f"{Fore.GREEN}Yeepee Kay Yay! You did it! {Style.RESET_ALL} \n")
            time.sleep(1)
        else:
            print(f"{Fore.LIGHTRED_EX}Oops, you are wrong! {Style.RESET_ALL} \n")
            time.sleep(1)

    # Show round statistics based on the specific game self.statistics variable
    @abstractmethod
    # Present statistics at the end of specific game attempt
    def present_statistics(self):
        print(self.statistics)

    @abstractmethod
    # Check if user wants to try again at the same round
    def check_retry(self):
        self.retry = input(f"{Fore.LIGHTYELLOW_EX}Would you like to try again? type Y to retry {Style.RESET_ALL} ")
        if self.retry == "Y" or self.retry == "y":
            self.clear_default_retry()
            print(f"{Fore.YELLOW}Alright, let's do it one more time . . . \n {Style.RESET_ALL}")
            self.status = "Retry"
            time.sleep(2)
            clear_screen()
        else:
            self.check_replay()

    @abstractmethod
    # Actions to do before user retries - clearing variables
    def clear_default_retry(self):
        pass

    @abstractmethod
    # Check if user wants to replay after he won the round
    def check_replay(self):
        self.retry = "N"
        self.replay = input(f"{Fore.LIGHTYELLOW_EX}Do you want to play again? \nType Y to replay {Style.RESET_ALL} ")
        time.sleep(1.5)
        if self.replay == "Y" or self.replay == "y":
            self.clear_default_replay()
            self.status = "Replay"
            print(f"{Fore.GREEN}Fun in the sun!{Style.RESET_ALL}")
            time.sleep(1)
            print(f"{Fore.YELLOW}Returning to home panel . . . {Style.RESET_ALL}")
            time.sleep(2)
            clear_screen()
            return "Replay"
        else:
            self.status = "Exit"
            self.say_goodbye()
            return "Bye"

    @abstractmethod
    # Actions to do before user replays - clearing variables
    def clear_default_replay(self):
        pass

    @abstractmethod
    # Say goodbye to user when he chooses to exit
    def say_goodbye(self):
        print(f'{Fore.LIGHTRED_EX}Goodbye {self.user}!{Style.RESET_ALL}')
        exit()
