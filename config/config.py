import os

config = {
    "activeCheckpoints": range(1,17),
    "instructionsDir": "./data/instructions/",
    "hintsDir": "./data/hints/",
    "mapLink": "The map is in two parts. Otaniemi: https://drive.google.com/file/d/16Nn9f0cW4k-PoY_YCJqxhDzKhETjKeRL/view?usp=sharing City center: https://drive.google.com/file/d/1QP57LEE4OD_BiBWsLtVYWwouKMWm9nNx/view?usp=sharing",
}

config["key"] = os.environ["RASTIBOT_KEY"]
config["forwardId"] = int(os.environ["RASTIBOT_FORWARD_ID"])
config["dbConnectionString"] = os.environ["RASTIBOT_DB_STRING"]
# These 2 are not required
config["botContactPerson"] = os.environ.get("BOT_CONTACT_PERSON") or ""
config["help"] = ". For help with anything else, please ask in the Stadventures info Telegram group."
