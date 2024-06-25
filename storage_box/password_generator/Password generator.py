import string
import random


def main():
    try:
        length = int(input("Enter the length of the password: "))
    except ValueError:
        print("One or more invalid input pls enter an integer! ")
        main()
    include_alphabet = input("Do you want to include alphabets? ('yes' or 'no'): ").lower()
    include_number = input("Do you want to include numbers? ('yes' or 'no'): ").lower()
    include_punctuation = input("Do you want to include Special characters? ('yes' or 'no'): ").lower()
    alphabet_case = input("Select alphabet case (lower/upper/mixed): ").lower()

    generate_password(length, include_alphabet, include_number, include_punctuation, alphabet_case)

    option(length, include_alphabet, include_number, include_punctuation, alphabet_case)


def generate_password(length, include_alphabet, include_number, include_punctuation, alphabet_case):

    characters = ''

    if include_alphabet == "yes":
        if alphabet_case == "lower":
            characters += string.ascii_lowercase
        elif alphabet_case == "upper":
            characters += string.ascii_uppercase
        elif alphabet_case == "mixed":
            characters += string.ascii_letters
        else:
            characters += string.ascii_letters
    if include_number == "yes":
        characters += string.digits
    if include_punctuation == "yes":
        characters += "!@#$%&?"
    if not characters:
        print("Invalid input please select at least one character type.")
        main()

    password = ''.join(random.choice(characters) for _ in range(length))
    print("Your generated Password is:", password)


def option(length, include_alphabet, include_number, include_punctuation, alphabet_case):
    while True:
        choice = input("Do you want to generate another password? ('yes' or 'no'): ").lower()
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


main()
