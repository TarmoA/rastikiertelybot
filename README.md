# rastikiertelybot

Telegram bot that can be used to organise a checkpoint crawl.

## Build instructions

Running the bot is easiest with docker. Build with:
`docker build .`

Some environment variables are required:
| RASTIBOT_KEY | Telegram bot token |
| RASTIBOT_FORWARD_ID | Telegram group id where to forward checkpoint answers |
| RASTIBOT_DB_STRING | DB connection string, like "postgresql://user:password@postgres" |
| BOT_CONTACT_PERSON | Contact info for /help command, optional|

For example, if you have a postgres docker container with name "postgres" in network "network": docker run -d --network=network -e RASTIBOT_KEY="???" -e RASTIBOT_FORWARD_ID="???" -e RASTIBOT_DB_STRING="postgresql://postgres:password@postgres" -e BOT_CONTACT_PERSON="" imagename

I used PostgreSQL database, but any other might work as well.

## Data
The bot reads checkpoint instructions from data/instructions and the files are named like NUMBER.txt
