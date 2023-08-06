# Define MemoryGame
import random
import time
from colorama import Fore, Style
from gbwog.panel.Utils import clear_screen
from gbwog.panel.Game import Game


class MemoryGame(Game):
    def __init__(self, diff, user):
        super().__init__(diff, user)
        self.generated_list = []
        self.user_list = []
        self.rules = ""
        self.statistics = ""
        self.score = ""

    # Pull game play from Game class and start to play
    def play(self):
        super().play()
        return str(self.status)

    # ~~ Start of functions that define play() ~~ #
    # 1. welcome user - pulled from Game class
    def welcome_player(self):
        super().welcome_player()

    # 2. show game rules - pulled from Game class but changed with self.rules variable
    def present_rules(self):
        self.rules = f"""{Fore.LIGHTYELLOW_EX}Game Rules:
Number of attempts : {self.diff + 2}
Approved range : {self.diff} numbers from 1 to 101 \n{Style.RESET_ALL}"""
        super().present_rules()

    # 3. define game process generally
    def game_process(self):
        print(f"{Fore.LIGHTCYAN_EX}Ready?{Style.RESET_ALL}")
        # Generating a list of numbers due to level choice
        time.sleep(2)
        print(f'{Fore.CYAN}As a beginning, I think of a list with {self.diff} numbers \n {Style.RESET_ALL}')
        self.generate_sequence()
        time.sleep(2)
        print(f"{Fore.CYAN}I am ready to reveal the list, so you should get ready too . . . {Style.RESET_ALL}")
        time.sleep(random.randrange(3, 7))
        print(self.generated_list)
        time.sleep(0.7)
        # Clearing the screen on python terminal
        clear_screen()
        # For pycharm we need to use this:
        # print("\n" * 80)
        # Ask the user to choose a list
        time.sleep(1)
        print(f"\n{Fore.CYAN}Alright, now it is your turn! {Style.RESET_ALL}")
        self.get_list_from_user()
        time.sleep(2)

    # ~ Start of functions that define game_process() ~ #
    # 3a. Function to generate a random list
    def generate_sequence(self):
        # Generate a list of numbers due to level choice
        for round in range(1, self.diff + 1):
            self.generated_list.append(random.randrange(1, 102))
            round += 1

    # 3c. Function to get a user guess of the list
    def get_list_from_user(self):
        # Ask the user to enter numbers due to level choice
        for round in range(1, self.diff + 1):
            diag = ""
            while diag != "True":
                num = input(f'{Fore.LIGHTYELLOW_EX}Enter number {round} {Style.RESET_ALL} ')
                if num.isdigit():
                    if int(num) in range(1, 102):
                        diag = "True"
                        self.user_list.append(int(num))
                        round += 1
                    else:
                        print(f'{Fore.LIGHTRED_EXE}Error - wrong choice! {Style.RESET_ALL}')
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
        if self.generated_list == self.user_list:
            self.winning = "True"
            self.number_of_wins += 1
        else:
            self.winning = "False"
        if self.number_of_guesses == self.diff + 2:
            self.winning = self.winning + '- End_Of_Chances'

    # 5. announce results of the attempt
    def publish_results(self):
        super().publish_results()

    # 6. present game statistics - pulled from Game class but changed with self.statistics variable
    def present_statistics(self):
        self.statistics = f"""{Fore.LIGHTCYAN_EX}Statistics:
1.Level: {self.diff}
2.Computer choice: {self.generated_list} 
3.User choice: {self.user_list}
4.Lists are equal: {self.winning.replace("- End_Of_Chances", "")}
5.Number of allowed attempts at this round: {self.diff + 2}
6.Number of attempts at this round: {self.number_of_guesses} \n {Style.RESET_ALL}"""
        super().present_statistics()

    # 7a. when user lose, check if he wants to retry - pulled from Game class
    def check_retry(self):
        super().check_retry()

    # 8a. If he wants, clear the relevant variables of a new attempt at the same round
    def clear_default_retry(self):
        # Clear variables which relate to only one attempt
        self.user_list.clear()
        self.generated_list.clear()

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

    # ~~ End of functions that define play() ~~ #
