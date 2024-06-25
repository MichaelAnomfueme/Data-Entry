import logging
import configparser
import time
import datetime
import openpyxl

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ConversationHandler, MessageHandler,
    CallbackQueryHandler, filters, CallbackContext
)

# Load configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# load configuration
TIME_LIMIT = config.getint('time', 'time_limit')
QUESTIONS_PATH = config.get('file_paths', 'questions_file_path')
OPTIONS_PATH = config.get('file_paths', 'options_file_path')
ANSWERS_PATH = config.get('file_paths', 'answers_file_path')
CANDIDATE_INFO_PATH = config.get('file_paths', 'candidate_info_path')
EXCEL_FILE_PATH = config.get('file_paths', 'excel_file_path')
TEST_NAME = config.get('test_info', 'test_name')

# Bot token
TOKEN: str = config.get('BOT_ID', 'bot_token')

# Define conversation states
(HANDLE_RESPONSE, START_TEST, ASK_QUESTION) = range(3)


def format_time() -> str:
    """Format the time limit into a human-readable string.
    Returns:
        str: Formatted time string.
    """
    if TIME_LIMIT < 3600:
        minute = TIME_LIMIT / 60
        if minute < 1:
            return f"{int(TIME_LIMIT)} seconds"
        else:
            return f"{int(minute)} minutes"
    else:
        hours = TIME_LIMIT // 3600
        minutes = (TIME_LIMIT % 3600) // 60
        if minutes > 0:
            return f"{hours} hour and {minutes} minutes"
        else:
            return f"{hours} hours"


# Read questions, options, and answers from text files
def load_files() -> None:
    global QUESTIONS, OPTIONS, ANSWERS, candidate_info
    try:
        with open(QUESTIONS_PATH, 'r') as file:
            QUESTIONS = file.read().splitlines()

        with open(OPTIONS_PATH, 'r') as file:
            OPTIONS = [line.split(',') for line in file.read().splitlines()]

        with open(ANSWERS_PATH, 'r') as file:
            ANSWERS = file.read().splitlines()

        with open(CANDIDATE_INFO_PATH, 'r') as file:
            candidate_info = {}
            for line in file.read().splitlines():
                exam_no, name = line.split(',')
                candidate_info[exam_no.strip()] = name.strip().upper()
    except Exception as e:
        print(f"one or more files may be missing {e}\nShutting down..")
        exit(1)


def save_result(candidate_name,
                candidate_exam_no,
                total_questions,
                attempted_questions,
                unattempted_questions,
                failed_questions,
                final_score, grade) -> None:
    try:
        # Load the workbook and sheet
        wb = openpyxl.load_workbook(EXCEL_FILE_PATH)
        ws = wb.active

        # Add the test results
        data = [
            TEST_NAME,
            datetime.datetime.now().strftime("%Y-%m-%d"),
            datetime.datetime.now().strftime("%H:%M:%S"),
            candidate_name,
            candidate_exam_no,
            total_questions,
            attempted_questions,
            unattempted_questions,
            failed_questions,
            final_score,
            grade
        ]

        ws.append(data)
        wb.save(EXCEL_FILE_PATH)
    except Exception as e:
        print(f"Error saving test {e}")
        return None


async def start(update: Update, _) -> int:
    """Function to ask the user their exam number"""
    await update.message.reply_text("Enter your exam number")
    return HANDLE_RESPONSE


async def handle_response(update: Update, context) -> int:
    """ Handle the exam number input from the user.
    Args:
        update (Update): Incoming update.
        context (ContextTypes.DEFAULT_TYPE): Context object.
    Returns:
        int: Next state for the conversation.
    """
    candidate_exam_no = update.message.text.strip()
    candidate_name = candidate_info.get(candidate_exam_no)

    if not candidate_name:
        await update.message.reply_text(
            f"Exam number {candidate_exam_no} not found. Perhaps you are not enrolled for this test.")
        return ConversationHandler.END
    else:
        context.user_data['candidate_exam_no'] = candidate_exam_no
        context.user_data['candidate_name'] = candidate_name

        keyboard = [[InlineKeyboardButton("START", callback_data='START')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f"Hi {candidate_name}! You have {len(QUESTIONS)} questions. "
            f"The duration of the test is {format_time()}.",
            reply_markup=reply_markup)
        return START_TEST


async def start_test(update: Update, context: CallbackContext) -> int:
    """ Function to start the test """
    query = update.callback_query
    await query.answer()
    if query.data == 'START':
        await query.edit_message_text("Your test has started. Good luck!")

        context.user_data['start_time'] = datetime.datetime.now()
        context.user_data['end_time'] = datetime.datetime.now() + datetime.timedelta(seconds=TIME_LIMIT)

        context.user_data['score'] = 0
        context.user_data['question_number'] = 1

        return ASK_QUESTION


def main():
    """ Main function to start the bot """
    # Load questions, options, and answers from files
    load_files()

    # Set up logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    # Create application
    app = ApplicationBuilder().token(TOKEN).build()

    # Create conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            HANDLE_RESPONSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_response)],
            START_TEST: [CallbackQueryHandler(start_test)],
            ASK_QUESTION: [CallbackQueryHandler(handle_answer)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    # Add handlers
    app.add_handler(conv_handler)

    # Print message indicating the bot has started.
    print("Bot Started...")

    # Start the bot
    app.run_polling()

async def cancel(update: Update, _) -> int:
    """Function to cancels the conversation"""
    await update.message.reply_text("Calculation cancelled.")
    return ConversationHandler.END

if __name__ == "__main__":
    main()
