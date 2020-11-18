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
        return "Please give a valid checkpoint number"
    if checkpointNo not in config["activeCheckpoints"]:
        return "ERROR: Checkpoint number not active"
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

def start(update, context):
    text = """Instructions
1. Register your team with "/register <teamName>". For example:
"/register Best team"

2. Go to checkpoint shown on /map

3. Get instructions with "/arrive <checkpointNumber>". For example: "/arrive 1"

4. Submit your task by sending a photo or video to the bot with check point number as caption. For example, send a photo with the caption "1"

5. Repeat instructions 2-4 for every checkpoint (or as many as you want to complete)

6. Once you have completed enough checkpoints, send the command /stop to send your task proofs for the organisers and end the crawl.

If you need help, please use the /help command.


Commands
/start - Show this help message
/register <name> - register your team name to the bot. Using this multiple times will change your team name.
/help - Get help
/map - Get link to map
/arrive <number> - Use this when you arrive to checkpoint to receive checkpoint instructions
/stop - This command will signify that you have completed the checkpoint crawl and your submissions will be sent to the organisers.
"""
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

def helpMessage(update, context):
    text = "If you have technical difficulties with the bot, please contact " + config["botContactPerson"] + ". For help with anything else, please contact " + config["contactPerson"]
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

# def hint(update, context):
#     checkpointNo = parseCheckpointNumber(update)
#     error = getCheckpointNumberError(checkpointNo)
#     if error:
#         context.bot.send_message(chat_id=update.effective_chat.id, text=error)
#         return

#     reply = "Here is the hint for checkpoint " + str(checkpointNo) + ": \n\n" + getHint(checkpointNo)
#     context.bot.send_message(chat_id=update.effective_chat.id, text=reply)

async def handlePhotoOrVideo(update, context):
    """Handle a photo sent in by user"""
    message = update.message
    user = update.effective_user
    messageId = message.message_id
    if not message.photo and len(message.photo) and not message.video:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="ERROR: no photo or video in message?")
        return
    if not message.caption:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Please give checkpoint number in caption")
        return
    try:
        checkpointNo = int(message.caption)
        error = getCheckpointNumberError(checkpointNo)
        if error:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text=error)
            return
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text="ERROR: invalid checkpoint thrown")
        return
    await data.storeCompletion(user.id, messageId, checkpointNo)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Completion proof received for checkpoint " + str(checkpointNo))


async def stop(update, context):
    completions = await data.getCompletions(update.effective_user.id)
    if not completions or not len(completions):
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="No completion proofs received yet. Please send at least one before using this command")
        return
    completions.sort(key=lambda i: i["checkpointNo"])
    teamName = await data.getTeamName(update.effective_user.id)
    context.bot.send_message(
        chat_id=config["forwardId"], text="Checkpoint completions for team: " + teamName)
    for item in completions:
        context.bot.forward_message(
            chat_id=config["forwardId"], from_chat_id=update.effective_chat.id, message_id=item.get("messageId"))
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Completions sent to organizers for review. Thank you for participating!")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="ERROR: Message caused bot error")


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
    dp.add_handler(MessageHandler(Filters.group, lambda a, b: None)) # ignore group chat messages
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", helpMessage))
    dp.add_handler(CommandHandler("map", mapMessage))
    dp.add_handler(CommandHandler("register", lambda a,b : asyncio.run(register(a,b)), run_async=True))
    dp.add_handler(CommandHandler("arrive", arrive))
    # dp.add_handler(CommandHandler("complete", complete))
    dp.add_handler(CommandHandler("stop", lambda a,b: asyncio.run(stop(a,b)), run_async=True))
    # dp.add_handler(CommandHandler("hint", hint))
    dp.add_handler(MessageHandler((Filters.video | Filters.photo) & Filters.private, lambda a, b: asyncio.run(handlePhotoOrVideo(a,b))))
    dp.add_handler(MessageHandler(Filters.all, logMessage)) # log messages that don't fit any other filter


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
