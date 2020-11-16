import os

config = {
    "activeCheckpoints": range(1,3),
    "instructionsDir": "./data/instructions/",
    "hintsDir": "./data/hints/",
    "mapLink": "TODO link to map here",
}

config["key"] = os.environ["RASTIBOT_KEY"]
config["forwardId"] =int(os.environ["RASTIBOT_FORWARD_ID"])
config["dbConnectionString"] = os.environ["RASTIBOT_DB_STRING"]
