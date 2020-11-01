# encoding: utf-8
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging, json, os, sys, re

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Which checkpoints are available?
activeCheckpoints = range(1,3)

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    text = """TODO kuvaus"""
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

def helpMessage(update, context):
    text = """TODO mistä saa apua?"""
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

def mapMessage(update, context):
    text = """TODO anna kartta"""
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

def register(update, context):
    text = """TODO rekisteröi"""
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

def arrive(update, context):
    text = update.message.text
    parts = text.split(" ")
    if len(parts) < 2:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Anna rastinumero TODO")
        return

    checkpointNo = int(parts[1])
    reply = ""
    if checkpointNo and checkpointNo in activeCheckpoints:
        reply = "Tervetuloa rastille " + str(checkpointNo) + " TODO ohjeet"
    else:
        reply = "Error: checkpoint number " + str(checkpointNo) + " not found"
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply)


# def handlePhoto(bot, update):
#     """Handle a photo sent in by user"""
#     message = update.message
#     user = update.effective_user
#     if message.photo and len(message.photo):
#         # get full size photo
#         photoObj = message.photo[-1]
#         chatId = message.chat_id
#         messageId = message.message_id
#         filePath = BASE_FILE_PATH.format(chatId, messageId)
#         file = bot.get_file(photoObj.file_id)
#         file.download(filePath)


#     else:
#         update.message.reply_text('error')


# def error(update, context, error):
#     """Log Errors caused by Updates."""
#     logger.warning('Update "%s" caused error "%s"', update, error)



def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    token = json.loads(open("key.json").read())['key']

    updater = Updater(token=token)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", helpMessage))
    dp.add_handler(CommandHandler("map", mapMessage))
    dp.add_handler(CommandHandler("register", register))
    dp.add_handler(CommandHandler("arrive", arrive))
    # dp.add_handler(MessageHandler(Filters.photo & Filters.private, handlePhoto))

    # log all errors
    # dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
