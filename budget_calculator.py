import sys
import os
import argparse
from dataclasses import dataclass
import random # used for some randomization testing

@dataclass
class Budget:
    def __init__(self, income, food, bills, fun):
        self.income = income
        self.food = food
        self.bills = bills
        self.fun = fun
        self.total = food + bills + fun
        self.remain = income - self.total

    def positive_test(self):
        if self.remain >= 0:
            return True
        else:
            return False

    def food_percent(self):
        return f"{(self.food / self.income):.0%}"

    def bills_percent(self):
        return f"{(self.bills / self.income):.0%}"

    def fun_percent(self):
        return f"{(self.fun / self.income):.0%}"

    def total_percent(self):
        return f"{(self.total / self.income):.0%}"

try:
    from rich import print
    from rich import box
    from rich.table import Table
    from rich.console import Console
except ImportError:
    print("""
This program requires the rich color module.
Please install the module by running one of the following commands in your command line:
- pip install rich
- py -m pip install rich

Thank you!
    """)
    sys.exit()

def opening_lines():
    os.system('cls')
    print("""
[black on yellow]$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
$                                              $
$   This is a small program intended to help   $
$   judge and manage finances by comparing     $
$   your provided monthly income against       $
$   your provided monthly income against       $
$   your provided monthly expenses. You can    $
$   also choose to add a savings option to     $
$   your total expenses, and see how much      $
$   you will have saved after a certain        $
$   amount of time.                            $
$                                              $
$   This program works best with your exact    $
$   monthly income and expenses, but will      $
$   function just as well with estimates.      $
$                                              $
$   Whenever the program prompts you for an    $
$   input, you can enter 'q' to quit the       $
$   program.                                   $
$                                              $
$   This program was created by Truman Forey   $
$   GitHub: [black on white]https://github.com/PigeonheadDev[/]   $
$                                              $
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$[/]
    """)
    confirm = "q"
    while confirm == "q":
        confirm = input("Enter any key to begin, or q to quit. >")
        print("")
        confirm = confirm.lower()
        if confirm == "q":
            exit_program()
            confirm == "q"

def take_inputs():
    month_income = input_cleaner("Please enter the dollar amount of your monthly income. >")
    print("")
    food_cost = input_cleaner("Please enter the dollar amount of your monthly food budget. >")
    print("")
    bills_cost = input_cleaner("Please enter the dollar amount you expect to pay in major bills on a monthly basis. >")
    print("")
    fun_cost = input_cleaner("Please enter the dollar amount of your monthly entertainment budget. >")
    ### SAVINGS CHECK ##########################################################
    savings_intro = False
    savings_check = False
    savings_choice = False
    print("""
Thank you, that is all the information required about expenses.
Now, would you like to have this program to calculate savings given the information you provided?
This program will subtract the total of all expenses from your monthly income,
and determine how much you can save in a month and how much you will have saved
in 1, 5, 10, 20, and 30 year intervals if you saved that same amount every month.
This program will only perform this action if your total expenses are larger than your income.
    """)
    while savings_check == False:
        if savings_intro == True:
            print("Would you like to have this program calculate savings?")
            savings_choice = input("Please choose yes or no. (y/n) >")
        else:
            savings_choice = input("Please choose yes or no to select your choice. (y/n) >")
            savings_intro = True
        match savings_choice:
            case "q"|"Q":
                exit_program()
            case "y"|"Y":
                savings_choice = True
                savings_check = True
            case "n"|"N":
                savings_choice = False
                savings_check = True
            case _:
                print("Your input was not recognized, please try again.")
    results(month_income, food_cost, bills_cost, fun_cost, savings_choice, False)

def results(income, food, bills, fun, savings_enabled, cli_check):
    os.system('cls')
    try:
        del budget_obj
    except:
        pass
    budget_obj = Budget(income, food, bills, fun)
    results_table = Table(title="[black on bright_yellow]$$$$$$$$$$$$$$$$$   Calculated Budget   $$$$$$$$$$$$$$$$$[/]", box=box.SIMPLE)

    results_table.add_column("Monthly Income/Expenses")
    results_table.add_column("Amount")
    results_table.add_column("Percentage of Income")

    results_table.add_row("Income", str(f"[green]${budget_obj.income:,.2f}[/]"), "X")
    results_table.add_row("Food", str(f"[red]${budget_obj.food:,.2f}[/]"), budget_obj.food_percent())
    results_table.add_row("Bills", str(f"[red]${budget_obj.bills:,.2f}[/]"), budget_obj.bills_percent())
    results_table.add_row("Entertainment", str(f"[red]${budget_obj.fun:,.2f}[/]"), budget_obj.fun_percent())
    results_table.add_row("Total Expenses", str(f"[red]${budget_obj.total:,.2f}[/]"), budget_obj.total_percent())

    console = Console()
    console.print(results_table)

    print("After spending $" + f"{budget_obj.total:,.2f}" + " - or " + str(budget_obj.total_percent()) + " of your budget - on combined expenses,")
    if budget_obj.positive_test() == True:
        if savings_enabled == True:
            print("You will have $" + f"{budget_obj.remain:,.2f}" + " remaining to add to your savings.")
        else:
            print("You will have $" + f"{budget_obj.remain:,.2f}" + " remaining to use as you wish.")
    else:
        print("you will have a defecit of $" + f"{budget_obj.remain:,.2f}" + ".")
    print("")
    ### MOVING ON TO SAVINGS SECTION ##########################################################
    if cli_check == True:
        if savings_enabled == True:
            savings_calc(budget_obj.remain, cli_check)
        sys.exit()
    conclude_intro = False
    conclude_check = False
    confirm = "x"
    while conclude_check == False:
        if savings_enabled == True and budget_obj.positive_test() == True:
            if conclude_intro == False:
                print("You've chosen to add any remaining income after expenses to add to savings.")
                print("Would you like to progress to the savings calculation section of this program?")
            confirm = input("Enter y to progress to savings calculator, n to restart program, or q to quit. >")
            match confirm:
                case "y" | "Y":
                    conclude_check = True # ENDS LOOP
                    print("")
                    savings_calc(budget_obj.remain, cli_check)
                case "n" | "N":
                    conclude_check = True # ENDS LOOP
                case "q" | "Q":
                    exit_program()
                case _:
                    print("Unrecognized command. Please enter a valid command.")
                    print("")
        else:
            if savings_enabled == True and budget_obj.positive_test() == False:
                if conclude_intro == False:
                    print("You've chosen to add any remaining income after expenses to add to savings. Unfortunately, there is no remaining amount to add.")
                else:
                    if conclude_intro == False:
                        print("You've elected not to use the savings function of this program.")
            confirm = input("Enter r to restart the program, or q to quit. >")
            match confirm:
                case "r" | "R":
                    conclude_check = True # ENDS LOOP
                case "q" | "Q":
                    exit_program()
                case _:
                    print("Unrecognized command. Please enter a valid command.")
                    print("")
        conclude_intro = True

def savings_calc(remainder, cli_check):
    print("The total amount of money you can add to savings every month is $" + f"{remainder:,.2f}" + ".")
    print("The following calucalations will assume a 5% interest on savings annually.")
    print("Assuming you save this amount every month, here is how much you will have saved after the following periods of time:")
    print("")

    savings_table = Table(title="[black on bright_yellow]$ Calculated Savings $[/]", box=box.SQUARE_DOUBLE_HEAD)
    
    savings_table.add_column("Time")
    savings_table.add_column("Amount Saved")

    savings_table.add_row("[bright_magenta]1 YEAR[/]", f"[yellow]${savings_estimate(remainder, 1):,.2f}[/]")
    savings_table.add_row("[bright_magenta]5 YEARS[/]", f"[yellow]${savings_estimate(remainder, 5):,.2f}[/]")
    savings_table.add_row("[bright_magenta]10 YEARS[/]", f"[yellow]${savings_estimate(remainder, 10):,.2f}[/]")
    savings_table.add_row("[bright_magenta]20 YEARS[/]", f"[yellow]${savings_estimate(remainder, 20):,.2f}[/]")
    savings_table.add_row("[bright_magenta]30 YEARS[/]", f"[yellow]${savings_estimate(remainder, 30):,.2f}[/]")

    console = Console()
    console.print(savings_table)

    if cli_check == True:
        sys.exit()
    final_intro = False
    final_check = False
    while final_check == False:
        if final_intro == False:
            pass
        confirm = input("Enter r to restart the program, or q to quit. >")
        match confirm:
            case "r" | "R":
                final_check = True # ENDS LOOP
            case "q" | "Q":
                exit_program()
            case _:
                print("Unrecognized command. Please enter a valid command.")
                print("")

def savings_estimate(monthly_savings, years):
    # 1yr=12, 5yr=60, 10yr=120, 20yr=240, 30yr=360 months
    annual_rate = 1.05
    total = 0
    for _ in range(years):
        total = (total + monthly_savings) * (annual_rate)
    return round(total, 2)

def input_cleaner(text):
    a = True
    while a == True:
        x = input(text)
        if x == "q" or x == "Q":
            exit_program()
        else:
            try:
                y = float(x)
                a = False
                return y
            except ValueError:
                print("Invalid input. Please enter a valid number.")

def exit_program():
    confirm = input("Are you sure you want to exit the program? Enter y to confirm. >")
    confirm = confirm.lower()
    if confirm == "y":
        os.system('cls')
        sys.exit()
    else:
        print("")

def program_loop():
    random_testing = False
    while random_testing == True:
        results(
            random.randint(1000,50000),
            random.randint(200,500),
            random.randint(500,5000),
            random.randint(100,1000),
            random.choice([True, False])
            )
    while True:
        take_inputs()
        os.system('cls')

def parse_given_arguments():
    parser = argparse.ArgumentParser(description="CLI Functionality")

    parser.add_argument("-i", "--income", type=float, default=0, help="Monthly Income")
    parser.add_argument("-f", "--food", type=float, default=0, help="Monthly Food Budget")
    parser.add_argument("-b", "--bills", type=float, default=0, help="Monthly Bill Payments")
    parser.add_argument("-e", "--entertainment", type=float, default=0, help="Monthly Entertainment Budget")
    parser.add_argument("-s", "--savings", action="store_true", help="Enable Savings Calculation")

    return parser.parse_args()

def validate_CLI_args(CLI_mode):
    try:
        if CLI_mode.income < 0:
            raise ValueError
        if CLI_mode.food < 0 or CLI_mode.bills < 0 or CLI_mode.entertainment < 0:
            raise ValueError
    except TypeError:
        print("ERROR -- One of your inputs was invalid.")
        print("Please try again.")
        sys.exit()
    except ValueError:
        print("ERROR -- Income must be higher than 0, and Expenses cannot be a negative number.")
        print("Please try again.")
        sys.exit()

def main():
    os.system('cls')
    CLI_mode = parse_given_arguments()
    #print("checking for CLI mode") ### TESTING PRINTS
    if CLI_mode.income is not None and CLI_mode.income > 0:
        #print("running CLI mode") # RUN CLI MODE
        #print(CLI_mode)
        validate_CLI_args(CLI_mode)
        results(
            CLI_mode.income,
            CLI_mode.food,
            CLI_mode.bills,
            CLI_mode.entertainment,
            CLI_mode.savings,
            True
            )
    else:
        # RUN INTERACTIVE MODE
        results(3550, 300, 1000, 100, True, False) # TESTING FUNCTION
        #print("running interactive mode")
        opening_lines()
        program_loop()

main()