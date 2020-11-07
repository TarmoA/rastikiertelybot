# encoding: utf-8
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging, json, os, sys, re

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# some conf values here, TODO move them elsewhere
# Which checkpoints are available?
activeCheckpoints = range(1,3)
dataDir = './data/'
instructionsDir = dataDir + 'instructions/'
hintsDir = dataDir + 'hints/'
mapLink = "TODO link to map here"

# parse checkpoint number from message and return it as number or None
def parseCheckpointNumber(update):
    if not update.message:
        return None
    text = update.message.text
    parts = text.split(" ")
    if len(parts) < 2:
        return None
    number = parts[1]
    try:
        return int(number)
    except ValueError:
        return None

# Get error message if checkpoint number is not valid
# return error message or None
def getCheckpointNumberError(checkpointNo):
    if checkpointNo == None:
        return "Please give the checkpoint number"
    if checkpointNo not in activeCheckpoints:
        return "Checkpoint number not found"
    return None

def getInstructions(number):
    try:
        file = open(instructionsDir + str(number)+ ".txt")
        text = file.read()
        return text
    except:
        return "ERROR: instructions not found"

def getHint(number):
    try:
        file = open(hintsDir + str(number)+ ".txt")
        text = file.read()
        return text
    except:
        return "ERROR: hints not found"

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    text = """TODO kuvaus"""
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

def helpMessage(update, context):
    text = """TODO mistä saa apua?"""
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

def mapMessage(update, context):
    text = mapLink
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

def register(update, context):
    text = """TODO rekisteröi"""
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

def arrive(update, context):
    checkpointNo = parseCheckpointNumber(update)
    error = getCheckpointNumberError(checkpointNo)
    if error:
        context.bot.send_message(chat_id=update.effective_chat.id, text=error)
        return

    reply = "Welcome to checkpoint " + str(checkpointNo) +"!\n\n" + getInstructions(checkpointNo)
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply)
    return

def complete(update, context):
    checkpointNo = parseCheckpointNumber(update)
    error = getCheckpointNumberError(checkpointNo)
    if error:
        context.bot.send_message(chat_id=update.effective_chat.id, text=error)
        return
    # TODO handle photo/video
    text = "Proof of completion received for checkpoint " + str(checkpointNo) + "."
    nextCheckpoint = checkpointNo + 1
    if nextCheckpoint in activeCheckpoints:
        text += " Here is the hint for checkpoint " + str(nextCheckpoint) + ": \n\n" + getHint(nextCheckpoint)
    else:
        text += " This was the last check point. TODO instructions here?"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    return

def hint(update, context):
    checkpointNo = parseCheckpointNumber(update)
    error = getCheckpointNumberError(checkpointNo)
    if error:
        context.bot.send_message(chat_id=update.effective_chat.id, text=error)
        return

    reply = "Here is the hint for checkpoint " + str(checkpointNo) + ": \n\n" + getHint(checkpointNo)
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
    dp.add_handler(CommandHandler("complete", complete))
    dp.add_handler(CommandHandler("hint", hint))
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