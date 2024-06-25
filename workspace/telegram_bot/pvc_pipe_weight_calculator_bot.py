"""PVC Pipe Weight Calculator Telegram Bot

This module implements a Telegram bot that calculates the weight of a PVC pipe
based on user inputs for diameter, thickness, and length. The bot guides the
user through a conversation to gather the necessary inputs and performs the
calculation.
"""

import configparser
import logging
from math import pi

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application, CommandHandler, ContextTypes, MessageHandler,
    ConversationHandler, CallbackQueryHandler, filters
)

# Load configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# Bot token
BOT_TOKEN: str = config.get('BOT_ID', 'bot_token')

# Global constant
PVC_DENSITY: int = 1450  # kg/m^3

# Conversation states
HANDLE_RESPONSE, GET_THICKNESS, GET_LENGTH, RESULT = range(4)


async def start(update: Update, _) -> int:
    """Function to Start the conversation and asks the user
    if they want to begin the calculation.
    """
    keyboard = [
        [InlineKeyboardButton("Yes", callback_data='yes')],
        [InlineKeyboardButton("No", callback_data='no')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Welcome! I am a simple PVC Pipe weight Calculator. Do you want to start?",
        reply_markup=reply_markup
    )
    return HANDLE_RESPONSE


async def handle_response(update: Update, _) -> int:
    """Function to handle the user's response to whether they want to start the calculation.
    """
    query = update.callback_query
    await query.answer()
    if query.data == 'yes':
        await query.edit_message_text(text="Please enter the diameter (mm).")
        return GET_THICKNESS
    if query.data == 'no':
        await query.edit_message_text(text="Bye!")
        return ConversationHandler.END


async def get_thickness(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Gets the thickness of the PVC pipe from the user.
    """
    try:
        context.user_data['diameter_mm'] = float(update.message.text)
        await update.message.reply_text("Please enter the thickness (mm).")
        return GET_LENGTH
    except ValueError:
        await update.message.reply_text(
            "Invalid input! Please enter a numeric value for the diameter."
        )
        return GET_THICKNESS


async def get_length(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Gets the length of the PVC pipe from the user.
    """
    try:
        context.user_data['thickness_mm'] = float(update.message.text)
        await update.message.reply_text("Please enter the length (ft).")
        return RESULT
    except ValueError:
        await update.message.reply_text(
            "Invalid input! Please enter a numeric value for the thickness."
        )
        return GET_LENGTH


async def result(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Calculates and sends the weight of the PVC pipe based on user inputs.
    """
    try:
        context.user_data['length_ft'] = float(update.message.text)

        diameter_mm = context.user_data['diameter_mm']
        thickness_mm = context.user_data['thickness_mm']
        length_ft = context.user_data['length_ft']

        diameter_m = diameter_mm / 1000
        thickness_m = thickness_mm / 1000
        length_m = length_ft * 0.3048

        inner_diameter = diameter_m - (2 * thickness_m)
        volume = pi * (((diameter_m / 2) ** 2) - ((inner_diameter / 2) ** 2)) * length_m
        weight = volume * PVC_DENSITY

        response = f"Result!\nUnit Volume = {volume:.4f} m^3\nUnit Weight = {weight:.4f} Kg"

        await update.message.reply_text(response)

    except ValueError:
        await update.message.reply_text(
            "Invalid input! Please enter a numeric value for the length."
        )
        return RESULT

    keyboard = [
        [InlineKeyboardButton("Yes", callback_data='yes')],
        [InlineKeyboardButton("No", callback_data='no')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "\nDo you want to check again?",
        reply_markup=reply_markup
    )
    return HANDLE_RESPONSE


async def cancel(update: Update, _) -> int:
    """Function to cancels the conversation"""
    await update.message.reply_text("Calculation cancelled.")
    return ConversationHandler.END


def main() -> None:
    """Runs the Telegram bot"""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()

    # Define the conversation handler with the states DIAMETER, THICKNESS, and LENGTH
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            HANDLE_RESPONSE: [CallbackQueryHandler(handle_response)],
            GET_THICKNESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_thickness)],
            GET_LENGTH: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_length)],
            RESULT: [MessageHandler(filters.TEXT & ~filters.COMMAND, result)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
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
    """Set up logging"""
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        # Change this to INFO, WARNING, ERROR, or CRITICAL to increase or reduce messages
        level=logging.INFO
    )


if __name__ == '__main__':
    main()
