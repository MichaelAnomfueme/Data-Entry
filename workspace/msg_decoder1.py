def decode_message() -> None:
    filename = 'text1.txt'
    # Read the file and store the contents in a list
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Split each line into a tuple of (number, word) and store in a list
    words = [line.split() for line in lines]

    # Sort the list of words based on the number
    words.sort(key=lambda x: int(x[0]))

    # Initialize an empty list to store the decoded message
    decoded_message = []

    # Initialize a counter to keep track of the triangular numbers
    triangular_number = 1
    counter = 1

    # Iterate over the sorted list of words
    for word in words:
        # If the current word's number is exactly equal to the triangular number, add it to the decoded message
        if int(word[0]) == triangular_number:
            decoded_message.append(word[1])
            # Update the triangular number and counter
            counter += 1
            triangular_number += counter

    # Join the decoded message into a string and print it
    print(' '.join(decoded_message))


# Call the function with the filename
if __name__ == '__main__':
    decode_message()
