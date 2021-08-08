#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from ovpn_manager import OpenVPNManager
import os

IP = "ENTER IP"
PORT = 5555




c = OpenVPNManager(IP,PORT)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )



def client_status(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    client_status = c.get_client_status()

    update.message.reply_text(
        client_status,
    )


def ovpn_status(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    p_status = c.get_ovpn_process_status()

    update.message.reply_text(
        p_status,
    )


def squid_status(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    p_status = c.get_squid_process_status()

    update.message.reply_text(
        p_status,
    )


def ovpn_restart(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    restart = c.restart_ovpn()

    update.message.reply_text(
        "restarting ovpn"
    )


def squid_restart(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    squid = c.restart_squid()

    update.message.reply_text(
        "restarting squid"
    )

def gen_config(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    print(context.args)
    if len(context.args) >= 1:
        new_config = c.gen_config(context.args[0])
        context.bot.send_document(chat_id=update.message.chat_id, document=open(new_config,"rb"))

    else:
        update.message.reply_text(
            "please provide a name for the client"
        )



def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(os.getenv("OVPN_BOT"))

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("status", client_status))
    dispatcher.add_handler(CommandHandler("ovpn_status", ovpn_status))
    dispatcher.add_handler(CommandHandler("squid_status", squid_status))
    dispatcher.add_handler(CommandHandler("ovpn_restart", ovpn_restart))
    dispatcher.add_handler(CommandHandler("ovpn_status", ovpn_restart))
    dispatcher.add_handler(CommandHandler("gen_config", gen_config, pass_args=True))


    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()