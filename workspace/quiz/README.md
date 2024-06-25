## Telegram Test Bot

This repository contains a Telegram bot for conducting timed tests with multiple-choice questions. The bot reads questions, options, and answers from text files and saves the test results to an Excel file.

## Features

- Timed test with customizable duration.
- Multiple-choice questions.
- Results saved to an Excel file.
- Configurable through a `config.ini` file.

## Requirements

- Python 3.7+
- Libraries: `python-telegram-bot`, `openpyxl`

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/MichaelAnomfueme/telegram-test-bot.git
    cd telegram-test-bot
    ```

2. Install the required libraries:
    ```sh
    pip install python-telegram-bot openpyxl
    ```

3. Create a `config.ini` file in the root directory of the project with the following content:

    ```ini
    [time]
    time_limit = 3600  # Time limit in seconds

    [file_paths]
    questions_file_path = questions.txt
    options_file_path = options.txt
    answers_file_path = answers.txt
    candidate_info_path = candidates.txt
    excel_file_path = results.xlsx

    [test_info]
    test_name = Sample Test

    [BOT_ID]
    bot_token = YOUR_TELEGRAM_BOT_TOKEN
    ```

4. Create the required text files (`questions.txt`, `options.txt`, `answers.txt`, `candidates.txt`) and an Excel file (`database.xlsx`).

    - `questions.txt`: List of questions, one per line.
    - `options.txt`: List of options for each question, separated by commas. Each line corresponds to a question in `questions.txt`.
    - `answers.txt`: List of correct answers, one per line. Each line corresponds to a question in `questions.txt`.
    - `candidates.txt`: List of candidates, with each line containing the exam number and name, separated by a comma.

    Example:

    **questions.txt**
    ```
    What is the capital of France?
    Who developed the theory of relativity?
    ```

    **options.txt**
    ```
    A: Abuja,B: Lyon,C: Paris,D: Cape Town
    A: Newton,B: Einstein,C: Galileo,D: Bohr
    ```

    **answers.txt**
    ```
    A
    B
    ```

    **candidates.txt**
    ```
    12345,John Doe
    67890,Jane Smith
    ```

5. Initialize the Excel file (`database.xlsx`) with appropriate column headers:

    **results.xlsx**
    ```
    | Test Name  | Date       | Time     | Candidate Name | Exam No | Total Questions | Attempted Questions | Unattempted Questions | Failed Questions | Final Score | Grade |
    |------------|------------|----------|----------------|---------|-----------------|---------------------|-----------------------|------------------|-------------|-------|
    ```

## Usage

1. Run the bot:
    ```sh
    python quiz_bot.py
    ```

2. Start a conversation with the bot on Telegram and follow the prompts to take the test.

## Bot Commands

- `/start` - Begin the test.
- `/cancel` - Cancel the test.
