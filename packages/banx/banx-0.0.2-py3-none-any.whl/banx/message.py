"""
This module provides some functions that print my message
"""

# def hi() -> None:
#     """
#     Just say hi
#     """
#     print("Hi there")


# def bye() -> None:
#     """
#     Just say goodbye
#     """
#     print("Goodbye")


def secret_message(*, name) -> str:
    """
    This functions contains my secret message. Call it with your name, and if you lucky, you'll get my message.

    Parameters:
    - name (str): Your name

    Returns:
    - message (str): My secret message
    """
    if name == "phoebe":
        return "Congratulations! You found my secret message ^^"
