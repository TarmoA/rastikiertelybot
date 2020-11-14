
def registerUser(userId, teamName):
    pass

def getTeamName(userId):
    pass

def getUserId(teamName):
    pass

completionStore = {}
def storeCompletion(userId, messageId, checkpointNo):
    items = completionStore.get(userId)
    newItem = {"messageId": messageId, "checkpointNo": checkpointNo}
    if not items:
        completionStore[userId] = []
    completionStore[userId].append(newItem)
    return True

def getCompletions(userId):
    items = completionStore.get(userId)
    if not items:
        return None
    return items
