# Budget-Calculator
A basic budget calculator using Python, integrating CLI.

This is a command-line budgeting application written in Python that calculates monthly expenses and savings projections. The application supports both interactive user input and command-line argument execution using python's argparse function, with formatted terminal output using Rich.

# How to Use:
Installing dependencies:
- `pip install rich`

Command-Line Interactive Mode:
- `py budget_calculator.py`

CLI Output Mode:
- `py budget_calculator.py -i x -f x -b x -e x -s`

OR

- `py budget_calculator.py --income x --food x --bills x -- entertainment x --savings`

((1: Substitute x for relevant numbers))
((2: Include -s or --savings for the CLI mode to run the optional savings calculation if possible; otherwise the program will only run the default budgeting calculation.))

# Features:
- Interactive command-line workflow.
- CLI support.
- Input cleaning and validation, and error handling.
- Modular functions.

# Technologies:
- Python
- argparse (Python)
- Rich
- OOP

