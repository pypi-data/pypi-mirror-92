# Define CurrencyRoulette
import os
import random
import math
import time
import requests
import shutil
from gbwog.panel.Game import Game
from colorama import Fore,Style


class CurrencyRoulette(Game):
    def __init__(self, diff, user):
        super().__init__(diff, user)
        # From which coin to convert
        self.origin_coin = "USD"
        # coin to be converted to
        self.exchange_coin = "ILS"
        # Pull the info about currency of origin coin in exchange coin
        self.curr_api_acs = self.resolve_key().replace('\n','')
        self.rates_url = f'https://v6.exchangerate-api.com/v6/{self.curr_api_acs}/latest/{self.origin_coin}'
        self.coin_rate = requests.get(self.rates_url).json()['conversion_rates'][self.exchange_coin]
        # Initialize variable for computer action
        self.generated_usd = 0
        # Initialize variable for user guess
        self.guess_exchange_coins = 0
        # Compare results & statistics actions
        self.total_money_in_coin = ""
        self.interval = 0
        self.rules = ""
        self.statistics = ""
        self.score = ""

    # Resolve key for exchange api
    def resolve_key(self):
        file_path = os.path.dirname(__file__)
        if file_path != "":
            os.chdir(file_path)
        # Create git for decryption
        os.system('git init > gitint.txt')
        os.remove('gitint.txt')
        # Pull code to decryption
        with open(".git-easy-crypt-key", 'r') as file:
            sec_key = file.read()
        # Setting the decrypt code on gecrypt tool
        os.system(f'gecrypt setkey {sec_key} -y > setk.txt')
        os.remove("setk.txt")
        # Decrypt file and pass the value to another file
        os.system("gecrypt decrypt curr.key.sec > decr.txt")
        os.remove("decr.txt")
        # Get access to the decrypted file
        with open("curr.key", 'r') as file:
            norm_key = file.read()
        # Remove the decrypted file
        os.remove("curr.key")
        # Remove git
        shutil.rmtree(".git")
        return str(norm_key)

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
1. Number of attempts : {self.diff + 2}
2. Approved range to guess :
    {Fore.LIGHTRED_EX}Floored exact number - (5 - level) < Exact Number < Ceiled exact number + (5 - level)
    {Fore.LIGHTYELLOW_EX}For exmaple, 592.35 shekels in your level ({self.diff}) the approved range is:
    {Fore.LIGHTRED_EX}Between 592 - (5 - {int(self.diff)}) and 593 + (5 - {int(self.diff)}) \n{Style.RESET_ALL}"""
        super().present_rules()

    # 3. define game process generally
    def game_process(self):
        print(f"{Fore.LIGHTCYAN_EX}Ready?{Style.RESET_ALL}")
        # Generating a list of numbers due to level choice
        time.sleep(2)
        # First, generating amount of origin coin
        time.sleep(3)
        print(f'{Fore.CYAN}As a beginning, I think of a number of {self.origin_coin} coins... \n {Style.RESET_ALL}')
        # Calculates interval
        self.get_money_interval()
        time.sleep(2)
        # Ask the user to guess
        print(f'\n{Fore.CYAN}Alright, now it is your turn. {Style.RESET_ALL}')
        time.sleep(2)
        self.get_user_guess()
        time.sleep(2)

    # ~ Start of functions that define game_process() ~ #
    # 3a. Function to generate random number of origin coins and set interval to right answers
    def get_money_interval(self):
        # Calculate the range of right answers due to level choice
        self.generated_usd = random.randrange(1, 102)
        self.total_money_in_coin = self.coin_rate * self.generated_usd
        self.interval = range((math.floor(self.total_money_in_coin) - (5 - self.diff)),
                              (math.ceil(self.total_money_in_coin + (5 - self.diff)) + 1))

    # 3b. Function to get user guess for number of exchange coins
    def get_user_guess(self):
        diag = ""
        while diag != "True":
            self.guess_exchange_coins = input(f'{Fore.LIGHTYELLOW_EX}How much {self.generated_usd}'
                                              f' Dollars are worth in {self.exchange_coin}? {Style.RESET_ALL} ')
            if self.guess_exchange_coins.isdigit():
                    diag = "True"
            else:
                print(f'{Fore.LIGHTRED_EX}Error - wrong choice! {Style.RESET_ALL}')
                time.sleep(1)
        # Demand a guess from user due to exchange coin

    # ~ End of functions that define game_process() ~ #

    # 4. compare results of specific game
    def compare_results(self):
        if self.number_of_guesses == self.diff + 2:
            print(f"{Fore.LIGHTRED_EX}Say a little prayer, it is your last chance . . . {Style.RESET_ALL}")
            time.sleep(2)
        print(f"{Fore.YELLOW}Loading results . . .")
        time.sleep(3)
        # If user choice is a number at all
        if self.guess_exchange_coins.isdigit():
            # If user choice is in the right answers interval
            if int(self.guess_exchange_coins) in self.interval:
                self.winning = "True"
                self.number_of_wins += 1
            else:
                self.winning = "False"
            # If user crosses the maximum number of attempts due to level choice
            if self.number_of_guesses == self.diff + 2:
                self.winning = self.winning + '- End_Of_Chances'
        else:
            self.guess_exchange_coins = "Not_A_Number"

    # 5. announce results of the attempt
    def publish_results(self):
        super().publish_results()

    # 6. present game statistics - pulled from Game class but changed with self.statistics variable
    def present_statistics(self):
        self.statistics = f"""{Fore.LIGHTCYAN_EX}Statistics:
1.Level: {self.diff}
2.Amount of USD: {self.generated_usd}
3.User guess: {self.guess_exchange_coins}
4.Currency of USD in ILS: {self.coin_rate}
5.Total ILS in USD: {self.total_money_in_coin}
6.Guess is in correct range: {self.winning.replace("- End_Of_Chances","")}
7.Number of allowed attempts at this round: {self.diff + 2}
8.Number of attempts at this round: {self.number_of_guesses} \n {Style.RESET_ALL}"""
        super().present_statistics()

    # 7a. when user lose, check if he wants to retry - pulled from Game class
    def check_retry(self):
        super().check_retry()

    # 8a. If he wants, clear the relevant variables of a new attempt at the same round
    def clear_default_replay(self):
        # Clear variables which relate to one full round
        self.clear_default_retry()
        self.number_of_guesses = 0

    # 7b. when user wins or pass allowed attempts of a round, check if he wants to replay - pulled from Game class
    def check_replay(self):
        super().check_replay()

    # 8b. If he wants, clear the relevant variables of a new round
    def clear_default_retry(self):
        # Clear variables which relate to only one attempt
        self.total_money_in_coin = 0
        self.generated_usd = 0
        self.guess_exchange_coins = 0

    # 9. Say goodbye to user if he wants to quit
    def say_goodbye(self):
        super().say_goodbye()

    # ~~ End of functions that define play() ~~ #
