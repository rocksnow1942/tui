"""Having fun with prompt_toolkit!"""

import prompt_toolkit as pt


if __name__ == "__main__":
    user_input = pt.prompt("Enter something: ")
    print(f"You entered: {user_input}")
