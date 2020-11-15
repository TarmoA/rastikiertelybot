# encoding: utf-8
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging, os, sys, re, asyncio
import data
from config import config

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


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
    if checkpointNo not in config["activeCheckpoints"]:
        return "Checkpoint number not found"
    return None

def getInstructions(number):
    try:
        file = open(config["instructionsDir"] + str(number)+ ".txt")
        text = file.read()
        return text
    except:
        return "ERROR: instructions not found"

def getHint(number):
    try:
        file = open(config["hintsDir"] + str(number)+ ".txt")
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
    text = config["mapLink"]
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def register(update, context):
    text = update.message.text
    teamName = text[9:].strip()
    if not teamName:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Empty name not allowed")
        return
    await data.registerUser(update.effective_user.id, teamName)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Registered team: " + teamName)

def arrive(update, context):
    checkpointNo = parseCheckpointNumber(update)
    error = getCheckpointNumberError(checkpointNo)
    if error:
        context.bot.send_message(chat_id=update.effective_chat.id, text=error)
        return

    reply = "Welcome to checkpoint " + str(checkpointNo) +"!\n\n" + getInstructions(checkpointNo)
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply)
    return

# def complete(update, context):
#     checkpointNo = parseCheckpointNumber(update)
#     error = getCheckpointNumberError(checkpointNo)
#     if error:
#         context.bot.send_message(chat_id=update.effective_chat.id, text=error)
#         return
#     text = "Proof of completion received for checkpoint " + str(checkpointNo) + "."
#     nextCheckpoint = checkpointNo + 1
#     if nextCheckpoint in activeCheckpoints:
#         text += " Here is the hint for checkpoint " + str(nextCheckpoint) + ": \n\n" + getHint(nextCheckpoint)
#     else:
#         text += " This was the last check point. TODO instructions here?"
#     context.bot.send_message(chat_id=update.effective_chat.id, text=text)
#     return

def hint(update, context):
    checkpointNo = parseCheckpointNumber(update)
    error = getCheckpointNumberError(checkpointNo)
    if error:
        context.bot.send_message(chat_id=update.effective_chat.id, text=error)
        return

    reply = "Here is the hint for checkpoint " + str(checkpointNo) + ": \n\n" + getHint(checkpointNo)
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply)

async def handlePhotoOrVideo(update, context):
    """Handle a photo sent in by user"""
    message = update.message
    user = update.effective_user
    messageId = message.message_id
    if not message.photo and len(message.photo) and not message.video:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="TODO no photo or video in message?")
        return
    if not message.caption:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Give checkpoint number in caption")
        return
    try:
        checkpointNo = int(message.caption)
        error = getCheckpointNumberError(checkpointNo)
        if error:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="TODO invalid checkpoint")
            return
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text="TODO invalid checkpoint throw")
        return
    await data.storeCompletion(user.id, messageId, checkpointNo)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Completion proof received for checkpoint " + str(checkpointNo))


async def stop(update, context):
    completions = await data.getCompletions(update.effective_user.id)
    if not completions:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="No completion proofs received yet")
        return

    teamName = await data.getTeamName(update.effective_user.id)
    context.bot.send_message(
        chat_id=config["forwardId"], text="Completion for user: " + teamName)
    for item in completions:
        context.bot.forward_message(
            chat_id=config["forwardId"], from_chat_id=update.effective_chat.id, message_id=item.get("messageId"))
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Completions sent to organizers for review. Thank you for participating!")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Message caused bot error")


def logMessage(update, context):
    logger.info(update.effective_chat.id)
    logger.info(update.message.text)

async def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    token = config['key']

    await data.init()

    updater = Updater(token=token)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.group, lambda: None)) # ignore group chat messages
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", helpMessage))
    dp.add_handler(CommandHandler("map", mapMessage))
    dp.add_handler(CommandHandler("register", lambda a,b : asyncio.run(register(a,b)), run_async=True))
    dp.add_handler(CommandHandler("arrive", arrive))
    # dp.add_handler(CommandHandler("complete", complete))
    dp.add_handler(CommandHandler("stop", lambda a,b: asyncio.run(stop(a,b)), run_async=True))
    dp.add_handler(CommandHandler("hint", hint))
    dp.add_handler(MessageHandler((Filters.video | Filters.photo) & Filters.private, lambda a, b: asyncio.run(handlePhotoOrVideo(a,b))))
    dp.add_handler(MessageHandler(Filters.all, logMessage))


    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    asyncio.run(main())
