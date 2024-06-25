def read_and_decode() -> None:
    filename = 'text2.txt'
    # Read the contents of the file
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Create a dictionary to store the words
    word_dict = {}

    # Process each line
    for line in lines:
        parts = line.strip().split()
        if len(parts) == 2:
            number, word = int(parts[0]), parts[1]
            word_dict[number] = word

    # Get the decoded message
    decoded_message = []
    current_number = 1
    while current_number in word_dict:
        decoded_message.append(word_dict[current_number])
        current_number += len(decoded_message) + 1

    print(' '.join(decoded_message))


if __name__ == '__main__':
    read_and_decode()
