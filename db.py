from deta import Deta
import deta
import os
deta = Deta(os.environ['key'])


Users = deta.Base("users")
Messages = deta.Base("messages")

Users.put("test", "something")


#deta = Deta('b0tybjyp_DdszECKrpRN9k6ewJGJJem9zvSexFTp1') # configure your Deta project
db = deta.Base('simpleDB')  # access your DB

#db.put(["partner username", ["message", "messag5e", "message4"], ["s", "r", "s"], imageNumber, password],"username")

def getPalUsername(username):
    try:
        item = db.get(username)
    except:
        return -1
    return item["value"][0]


def getPrevMessages(username):
    try:
        item = db.get(username)
    except:
        return -1
    return item["value"][1:3]


#This could update an existing user which could be a no no
def addUser(name, profilePicture, password):
    db.put([None, [], [], profilePicture, password], name)


def getProfilePicture(username):
    return db.get(username)["value"][3]


def getPassword(username):
    return db.get(username)["value"][4]

#PRECONDITION: Both pals exist in database
#Resets messages when pals are established
def makePals(pal1, pal2):
    db.put([pal2, [], [], getProfilePicture(pal1), getPassword(pal1)], pal1)
    db.put([pal1, [], [], getProfilePicture(pal2), getPassword(pal2)], pal2)


#PRECONDITION: pal1 and pal2 have been made pals
#Sends message from pal1 to pal2
def registerMessage(pal1, pal2, message):
    messages = getPrevMessages(pal1)
    prevMessages = messages[0]
    srChain = messages[1]
    rsChain = []
    srChain.append("s")
    for tag in srChain:
        if tag == "s":
            rsChain.append("r")
        else:
            rsChain.append("s")
    prevMessages.append(message)
    db.put([pal2, prevMessages, srChain, getProfilePicture(pal1), getPassword(pal1)], pal1)
    db.put([pal1, prevMessages, rsChain, getProfilePicture(pal2), getPassword(pal2)], pal2)


"""addUser("bob", 1, "password123")
addUser("lkewrghn jkersb", 2, "passwordrftrsd")

makePals("bob", "lkewrghn jkersb")

registerMessage("bob", "lkewrghn jkersb", "greetings to you")
registerMessage("lkewrghn jkersb", "bob", "go die")
registerMessage("bob", "lkewrghn jkersb", "no u")


print(getPalUsername("username"))
print(getPrevMessages("bob"))
print(getPrevMessages("lkewrghn jkersb"))
print(getProfilePicture("bob"))"""


