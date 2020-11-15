import json

config = {
    "activeCheckpoints": range(1,3),
    "instructionsDir": "./data/instructions/",
    "hintsDir": "./data/hints/",
    "mapLink": "TODO link to map here",
}

secrets = json.loads(open("secrets.json").read())

config["key"] = secrets["key"]
config["forwardId"] = secrets["forwardId"]
config["dbConnectionString"] = secrets["dbConnectionString"]
