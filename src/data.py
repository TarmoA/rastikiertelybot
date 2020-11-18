from databases import Database
import logging
import asyncio
from config import config
logger = logging.getLogger(__name__)


def getDB():
    return Database(config["dbConnectionString"])

async def init():
    async with getDB() as database:
        queries = [
            """CREATE TABLE IF NOT EXISTS registrations (userid INTEGER UNIQUE, teamname VARCHAR(100), teamid SERIAL)""",
            """CREATE TABLE IF NOT EXISTS completions (userid INTEGER, messageid INTEGER, checkpointno INTEGER)"""
        ]
        for q in queries:
            await database.execute(query=q)


async def registerUser(userId, teamName):
    async with getDB() as database:
        query = "INSERT INTO registrations VALUES (:userid, :teamname) ON CONFLICT (userid) DO UPDATE SET teamname = :teamname WHERE registrations.userid = :userid"
        await database.execute(query=query, values={ "userid": userId, "teamname": teamName})

async def getTeamName(userId):
    async with getDB() as database:
        query = "SELECT * from registrations where userid = :userid"
        row = await database.fetch_one(query=query, values={ "userid": userId})
        return row.get("teamname")

async def getTeamInfo(userId):
    async with getDB() as database:
        query = "SELECT * from registrations where userid = :userid"
        row = await database.fetch_one(query=query, values={"userid": userId})
        return row

def getUserId(teamName):
    pass

async def storeCompletion(userId, messageId, checkpointNo):
    async with getDB() as database:
        query = "INSERT INTO completions VALUES (:userid, :messageid, :checkpointno)"
        await database.execute(query=query, values={"userid": userId, "messageid": messageId, "checkpointno": checkpointNo})

async def getCompletions(userId):
    async with getDB() as database:
        query = "SELECT * from completions where userid = :userid"
        rows = await database.fetch_all(query=query, values={"userid": userId})
        return list(map(lambda r: {"messageId": r.get("messageid"), "checkpointNo": r.get("checkpointno")}, rows))
