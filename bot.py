#!/usr/bin/env python
# pylint: disable=C0116,W0613
"""===============================================================================

        FILE: bot.py

       USAGE: (not intended to be directly executed)

 DESCRIPTION: 

     OPTIONS: ---
REQUIREMENTS: ---
        BUGS: ---
       NOTES: ---
      AUTHOR: Alex Leontiev (alozz1991@gmail.com)
ORGANIZATION: 
     VERSION: ---
     CREATED: 2022-02-16T21:03:39.401218
    REVISION: ---

==============================================================================="""

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


# Enable logging
import logging
import os
from dotenv import load_dotenv
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import uuid
from os import path
import pymongo
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def _get_mongo_coll():
    mongo_client = pymongo.MongoClient(host="mongodb://root:example@mongo")
    mongo_coll = mongo_client["MessageURLBot"]["messages"]
    return mongo_coll


def start(update: Update, context: CallbackContext) -> None:
    _, message_uuid = update.message.text.split(" ")
    logger.warning(f"message_uuid: {message_uuid}")
    mongo_coll = _get_mongo_coll()
    r = mongo_coll.find_one({"message_uuid": message_uuid})
    logger.warning(f"r: {r}")
    update.message.chat.send_message(
        "reply test", reply_to_message_id=r["message_id"])


def echo(update: Update, context: CallbackContext) -> None:
    logger.warning(update)
    logger.warning(update.message.link)

    message_uuid = str(uuid.uuid4()).replace("-", "")
#    update.message.reply_text(f"`{message_uuid}`", parse_mode="Markdown")
    https: // t.me/MessageURLBot?start = ac4db9c594a341738ff6b717456ddeb3
    update.message.reply_text(
        f"https://t.me/MessageURLBot?start={message_uuid}", parse_mode="Markdown")

    r = {"message_uuid": message_uuid, "message_id": update.message.message_id}
    logger.warning(f"r: {r}")

    mongo_coll = _get_mongo_coll()
    mongo_coll.insert_one(r)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(os.environ["TELEGRAM_TOKEN"])

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(filters=Filters.all, callback=echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    if path.isfile(".env"):
        logger.warning("loading .env")
        load_dotenv()
    main()
