"""This module provides a Telegram bot that generates random passwords
based on user preferences. The bot guides the user through a series
of prompts to select the desired password length,
character types (alphabets, numbers, special characters), and alphabet case.
"""

import string
import random
import logging
import configparser

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ConversationHandler, MessageHandler,
    CallbackQueryHandler, filters, CallbackContext
)

# Load configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# Bot token
TOKEN: str = config.get('BOT_ID', 'bot_token')

# Define conversation states
(HANDLE_RESPONSE, ALPHABET, ALPHABET_CASE, NUMBER, SPECIAL_CHARACTER,
 SAVE_SPECIAL_CH, GENERATE_PASSWORD, CHECK_AGAIN, PREVIOUS_CRITERIA) = range(9)


async def start(update: Update, _) -> int:
    """Function to start the conversation and ask the user
    if they want to begin.
    Args:
        update (Update): The Telegram update object.
        _: Unused argument.
    Returns:
        int: The next conversation state.
    """
    keyboard = [[InlineKeyboardButton("Yes", callback_data='yes'),
                 InlineKeyboardButton("No", callback_data='no')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Welcome! I am a simple password generator. Do you want to start?",
        reply_markup=reply_markup
    )
    return HANDLE_RESPONSE


async def handle_response(update: Update, _) -> int:
    """Function to handle the user's response to whether they want to start the
    calculation and get the desired password length.
    Args:
        update (Update): The Telegram update object.
        _: Unused argument.
    Returns:
        int: The next conversation state.
    """
    query = update.callback_query
    await query.answer()

    if query.data == 'yes':
        await query.edit_message_text(text="Enter the length of the password.")
        return ALPHABET
    if query.data == 'no':
        await query.edit_message_text(text="Bye!")
        return ConversationHandler.END


async def get_alphabet(update: Update, context: CallbackContext) -> int:
    """Function to handle the user's choice of including alphabets in the password
    Args:
        update (Update): The Telegram update object.
        context (CallbackContext): The Telegram context object.
    Returns:
        int: The next conversation state.
    """
    try:
        context.user_data['length'] = int(update.message.text)

        keyboard = [[InlineKeyboardButton("Yes", callback_data='yes'),
                     InlineKeyboardButton("No", callback_data='no')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "Do you want to include alphabets?", reply_markup=reply_markup
        )
        return ALPHABET_CASE

    except ValueError:
        await update.message.reply_text(
            "Invalid input! Please enter a numeric value for the password length."
        )
    return ALPHABET


async def get_alphabet_case(update: Update, context: CallbackContext) -> int:
    """Function to handle the user's desired alphabet case.
    Args:
        update (Update): The Telegram update object.
        context (CallbackContext): The Telegram context object.
    Returns:
        int: The next conversation state.
    """
    query = update.callback_query
    await query.answer()
    context.user_data['include_alphabet'] = query.data

    if context.user_data.get('include_alphabet') == 'yes':
        keyboard = [
            [InlineKeyboardButton("Upper", callback_data='upper')],
            [InlineKeyboardButton("Lower", callback_data='lower')],
            [InlineKeyboardButton("Mixed", callback_data='mixed')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Select alphabet case.", reply_markup=reply_markup)
        return NUMBER

    # Skip to the number inclusion step if "No" is selected
    return await get_number(update, context)


async def get_number(update: Update, context: CallbackContext) -> int:
    """Function to handle the user's choice of including numbers in the password.
    Args:
        update (Update): The Telegram update object.
        context (CallbackContext): The Telegram context object.
    Returns:
        int: The next conversation state.
    """
    query = update.callback_query
    await query.answer()
    context.user_data['alphabet_case'] = query.data

    keyboard = [[InlineKeyboardButton("Yes", callback_data='yes'),
                 InlineKeyboardButton("No", callback_data='no')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Do you want to include numbers?", reply_markup=reply_markup)
    return SPECIAL_CHARACTER


async def get_special_characters(update: Update, context: CallbackContext) -> int:
    """Function to handle the user's choice of including special characters in the password.
    Args:
        update (Update): The Telegram update object.
        context (CallbackContext): The Telegram context object.
    Returns:
        int: The next conversation state.
    """
    query = update.callback_query
    await query.answer()
    context.user_data['include_number'] = query.data

    keyboard = [[InlineKeyboardButton("Yes", callback_data='yes'),
                 InlineKeyboardButton("No", callback_data='no')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        "Do you want to include special characters?", reply_markup=reply_markup
    )
    return SAVE_SPECIAL_CH


async def save_special_ch(update: Update, context: CallbackContext):
    """Function to save the user's choice of including special characters in the password.
    Args:
        update (Update): The Telegram update object.
        context (CallbackContext): The Telegram context object.
    Returns:
        int: The next conversation state.
    """
    query = update.callback_query
    await query.answer()
    context.user_data['include_special_characters'] = query.data
    return await generate_password(update, context)


async def generate_password(update: Update, context: CallbackContext) -> int:
    """Function to generate the password based on the user's preferences.
    Args:
        update (Update): The Telegram update object.
        context (CallbackContext): The Telegram context object.
    Returns:
        int: The next conversation state.
    """
    length = context.user_data.get('length')
    include_alphabet = context.user_data.get('include_alphabet')
    include_number = context.user_data.get('include_number')
    include_punctuation = context.user_data.get('include_special_characters')
    alphabet_case = context.user_data.get('alphabet_case')

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
        await update.callback_query.edit_message_text(
            text="No characters selected pls try again.\nEnter the length of the password"
        )
        return ALPHABET

    password = ''.join(random.choice(characters) for _ in range(length))
    await update.callback_query.edit_message_text(text=f"Your generated Password is:\n\n{password}")

    keyboard = [[InlineKeyboardButton("Yes", callback_data='yes'),
                 InlineKeyboardButton("No", callback_data='no')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text(
        "Do you want to generate another password?",
        reply_markup=reply_markup
    )

    return CHECK_AGAIN


async def check_again(update: Update, _) -> int:
    """Function to ask the user if they want to generate another password.
    Args:
        update (Update): The Telegram update object.
        _: Unused argument.
    Returns:
        int: The next conversation state.
    """
    query = update.callback_query
    await query.answer()

    if query.data == 'yes':
        keyboard = [[InlineKeyboardButton("Yes", callback_data='yes'),
                     InlineKeyboardButton("No", callback_data='no')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "Do you want to use the previous criteria?",
            reply_markup=reply_markup
        )
        return PREVIOUS_CRITERIA
    if query.data == 'no':
        await query.edit_message_text(text="Bye!")
        return ConversationHandler.END


async def previous_criteria(update: Update, context: CallbackContext) -> int:
    """Function to handle the user's choice of using the previous criteria or starting over.
    Args:
        update (Update): The Telegram update object.
        context (CallbackContext): The Telegram context object.
    Returns:
        int: The next conversation state.
    """
    query = update.callback_query
    await query.answer()

    if query.data == 'yes':
        return await generate_password(update, context)
    if query.data == 'no':
        await query.edit_message_text(text="Enter the length of the password.")
        return ALPHABET


async def cancel(update: Update, _) -> int:
    """Function to cancel the password generation process.
    Args:
        update (Update): The Telegram update object.
        _: Unused argument.
    Returns:
        int: The conversation state indicating cancellation (ConversationHandler.END).
    """
    await update.message.reply_text("Password generation cancelled.")
    return ConversationHandler.END


def main() -> None:
    """Runs the Telegram bot"""
    # Create the Application and pass it your bot's token.
    application = ApplicationBuilder().token(TOKEN).build()

    # Define the conversation handler.
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            HANDLE_RESPONSE: [CallbackQueryHandler(handle_response)],
            ALPHABET: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_alphabet)],
            ALPHABET_CASE: [CallbackQueryHandler(get_alphabet_case)],
            NUMBER: [CallbackQueryHandler(get_number)],
            SPECIAL_CHARACTER: [CallbackQueryHandler(get_special_characters)],
            SAVE_SPECIAL_CH: [CallbackQueryHandler(save_special_ch)],
            GENERATE_PASSWORD: [CallbackQueryHandler(generate_password)],
            CHECK_AGAIN: [CallbackQueryHandler(check_again)],
            PREVIOUS_CRITERIA: [CallbackQueryHandler(previous_criteria)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    # Register handlers.
    application.add_handler(conv_handler)

    # Print message indicating the bot has started.
    print("Bot Started...")

    # logging
    set_logging()

    # Run the bot until program is stopped.
    application.run_polling()


def set_logging() -> None:
    """Function to set up logging for the bot."""
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        # Change this to INFO, WARNING, ERROR, or CRITICAL to increase or reduce messages
        level=logging.INFO
    )


if __name__ == '__main__':
    main()
