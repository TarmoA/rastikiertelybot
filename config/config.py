import os

config = {
    "activeCheckpoints": range(1,6),
    "instructionsDir": "./data/instructions/",
    "hintsDir": "./data/hints/",
    "mapLink": "TODO link to map here",
}

config["key"] = os.environ["RASTIBOT_KEY"]
config["forwardId"] = int(os.environ["RASTIBOT_FORWARD_ID"])
config["dbConnectionString"] = os.environ["RASTIBOT_DB_STRING"]
# These 2 are not required
config["botContactPerson"] = os.environ.get("BOT_CONTACT_PERSON") or ""
config["contactPerson"] = "your Fuksi Captain/International Captain"
