# Define GuessGame
import random
import time
from gbwog.panel.Game import Game
from colorama import Fore, Style


class GuessGame(Game):
    # Any GuessGame has secret number of computer, guess number of user
    def __init__(self, diff, user):
        super().__init__(diff, user)
        self.secret_number = 0
        self.guess_number = 0
        self.statistics = ""
        self.rules = ""
        self.score = ""

    # Pull game play from Game class and start to play
    def play(self):
        super().play()
        return str(self.status)

    # ~~ Start of functions that define play() ~ #
    # 1. welcome user - pulled from Game class
    def welcome_player(self):
        super().welcome_player()

    # 2. show game rules - pulled from Game class but changed with self.rules variable
    def present_rules(self):
        self.rules = f"""{Fore.LIGHTYELLOW_EX}Game Rules:
Number of attempts : {self.diff + 2}
Approved range : any number from 1 to {self.diff + 1} \n{Style.RESET_ALL}"""
        super().present_rules()

    # 3. define game process generally
    def game_process(self):
        print(f"{Fore.LIGHTCYAN_EX}Ready?{Style.RESET_ALL}")
        # Generating a list of numbers due to level choice
        time.sleep(2)
        # First, generating number on the specific range due to level choice
        print(f'{Fore.CYAN}As a beginning, I think of a number between 1 to {self.diff + 1} \n {Style.RESET_ALL}')
        self.generate_number()
        time.sleep(2)
        # Get a guess from user
        print(f'\n{Fore.CYAN}Alright, now it is your turn. {Style.RESET_ALL}')
        time.sleep(2)
        self.get_guess_from_user()
        time.sleep(2)

    # ~ Start of functions that define game_process() ~ #
    # 3a. Function to make computer generate random number from chosen range
    def generate_number(self):
        self.secret_number = random.randrange(1, self.diff + 2)

    # 3b. Function to get a guess from the user
    def get_guess_from_user(self):
        diag = ""
        while diag != "True":
            self.guess_number = input(
                f'{Fore.LIGHTCYAN_EX}Please enter number between 1 and {self.diff + 1} {Style.RESET_ALL} ')
            if self.guess_number.isdigit():
                if int(self.guess_number) in range(1, self.diff + 2):
                    diag = "True"
                else:
                    print(f'{Fore.LIGHTRED_EX}Error - wrong choice! {Style.RESET_ALL}')
                    time.sleep(1)
            else:
                print(f'{Fore.LIGHTRED_EX}Error - wrong choice! {Style.RESET_ALL}')
                time.sleep(1)

    # ~ End of functions that define game_process() ~ #

    # 4. compare results of specific game
    def compare_results(self):
        if self.number_of_guesses == self.diff + 2:
            print(f"{Fore.LIGHTRED_EX}Say a little prayer, it is your last chance . . . {Style.RESET_ALL}")
            time.sleep(2)
        print(f"{Fore.YELLOW}Loading results . . .")
        time.sleep(3)
        # Check if user inputed a number at all
        if self.guess_number.isdigit():
            # Check if user inputed the same number as the computer generated
            if int(self.secret_number) == int(self.guess_number):
                self.winning = "True"
                self.number_of_wins += 1
            else:
                if int(self.guess_number) not in range(1, self.diff + 2):
                    self.guess_number = "Out_Of_Range_Number"
                self.winning = "False"
            if self.number_of_guesses == self.diff + 2:
                self.winning = self.winning + '- End_Of_Chances'
        else:
            self.guess_number = "Not_A_Number"
            self.winning = "False"

    # 5. announce results of the attempt
    def publish_results(self):
        super().publish_results()

    # 6. present game statistics - pulled from Game class but changed with self.statistics variable
    def present_statistics(self):
        self.statistics = f"""{Fore.LIGHTCYAN_EX}Statistics:
1.Level: {self.diff}
2.Computer number: {self.secret_number}
3.User number: {self.guess_number}
4.Numbers are equal: {self.winning.replace("- End_Of_Chances", "")}
5.Number of allowed attempts at this round: {self.diff + 2}
6.Number of attempts at this round: {self.number_of_guesses} {Style.RESET_ALL}"""
        super().present_statistics()

    # 7a. when user lose, check if he wants to retry - pulled from Game class
    def check_retry(self):
        super().check_retry()

    # 8a. If he wants, clear the relevant variables of a new attempt at the same round
    def clear_default_retry(self):
        # Clear variables which relate to only one attempt
        self.secret_number = ""
        self.guess_number = ""

    # 7b. when user wins or pass allowed attempts of a round, check if he wants to replay - pulled from Game class
    def check_replay(self):
        super().check_replay()

    # 8b. If he wants, clear the relevant variables of a new round
    def clear_default_replay(self):
        # Clear variables which relate to only one round
        self.clear_default_retry()
        self.number_of_guesses = 0

    # 9. Say goodbye to user if he wants to quit
    def say_goodbye(self):
        super().say_goodbye()

    # ~~ End of functions that define play() ~ #
