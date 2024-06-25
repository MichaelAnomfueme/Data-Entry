import string
import random


def main() -> None:
    """Main function to interactively generate a password based on user input.
    Prompts the user for password criteria and generates a password accordingly.
    """
    try:
        length = int(input("Enter the length of the psk: "))
    except ValueError:
        print("One or more invalid inputs. Please enter an integer!")
        main()
        return  # Ensure the function exits after recursion

    include_alphabet = input("Do you want to include alphabets? ('yes' or 'no'): ").lower()
    include_number = input("Do you want to include numbers? ('yes' or 'no'): ").lower()
    include_punctuation = input("Do you want to include special characters? ('yes' or 'no'): ").lower()
    alphabet_case = input("Select alphabet case (lower/upper/mixed): ").lower()

    generate_password(length, include_alphabet, include_number, include_punctuation, alphabet_case)
    option(length, include_alphabet, include_number, include_punctuation, alphabet_case)


def generate_password(length: int,
                      include_alphabet: str,
                      include_number: str,
                      include_punctuation: str,
                      alphabet_case: str) -> None:
    """Generates and prints a psk based on the given criteria.

    Args:
        length (int): The length of the psk.
        include_alphabet (str): Whether to include alphabets ('yes' or 'no').
        include_number (str): Whether to include numbers ('yes' or 'no').
        include_punctuation (str): Whether to include special characters ('yes' or 'no').
        alphabet_case (str): The case of the alphabets ('lower', 'upper', or 'mixed').
    """
    characters = ''

    # Include alphabets based on user preference
    if include_alphabet == "yes":
        if alphabet_case == "lower":
            characters += string.ascii_lowercase
        elif alphabet_case == "upper":
            characters += string.ascii_uppercase
        elif alphabet_case == "mixed":
            characters += string.ascii_letters
        else:
            characters += string.ascii_letters

    # Include numbers if selected by the user
    if include_number == "yes":
        characters += string.digits

    # Include special characters if selected by the user
    if include_punctuation == "yes":
        characters += "!@#$%&?"

    # Check if the character set is empty
    if not characters:
        print("Invalid input, please select at least one character type.")
        main()
        return  # Ensure the function exits after recursion

    # Generate the password
    password = ''.join(random.choice(characters) for _ in range(length))
    print("Your generated Psk is:", password)


def option(length: int,
           include_alphabet: str,
           include_number: str,
           include_punctuation: str,
           alphabet_case: str) -> None:
    """Offers the user an option to generate another password using the same or new criteria.

    Args:
        length (int): The length of the password.
        include_alphabet (str): Whether to include alphabets ('yes' or 'no').
        include_number (str): Whether to include numbers ('yes' or 'no').
        include_punctuation (str): Whether to include special characters ('yes' or 'no').
        alphabet_case (str): The case of the alphabets ('lower', 'upper', or 'mixed').

    Examples:
        ('yes', 'yes', 'yes', 'mixed')
        Prompts the user to generate another password or exit.
    """
    while True:
        choice = input("Do you want to generate another psk? ('yes' or 'no'): ").lower()
        if choice != 'yes':
            break
        elif choice == 'yes':
            use_previous_criteria = input("Do you want to use previous criteria? ('yes' or 'no'): ").lower()
            if use_previous_criteria == 'no':
                main()
            elif use_previous_criteria == 'yes':
                generate_password(length, include_alphabet, include_number, include_punctuation, alphabet_case)
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")


if __name__ == '__main__':
    main()
