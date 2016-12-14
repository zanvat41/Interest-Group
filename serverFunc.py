import os
import datetime
import threading
import select
import queue
from pathlib import Path

GROUP_PATH = "serverData/"
USER_PATH = "serverData/users/"
EXTENDSION = ".txt"

# ERROR MESSAGES
TimeOUTMESS = "A TIME OUT HAS OCCURRED"

currentPostID = 0
fileLock = threading.Lock()
buffLock = threading.Lock()
groupPostList = []                  # list to hold group post ID by index

'''
Group Map

Just a quick write up of a group map for all the discussion
groups that will be use. Can be cleaned up some.
This will mainly be used to make the user file.
Key : group name  ,   Value : subscribed boolean(0/1)
'''
groups = {
    'comp.programming': 0,
    'comp.lang.c': 0,
    'comp.lang.python': 0,
    'comp.lang.javascript': 0,
    'comp.lang.c++': 0,
    'comp.lang.java': 0,

    'math.crypto': 0,
    'math.algro': 0,
    'math.calc': 0,
    'math.stats': 0,

    'sb.cse114': 0,
    'sb.cse214': 0,
    'sb.cse219': 0,
    'sb.cse220': 0,
    'sb.cse300': 0,
    'sb.cse303': 0,
    'sb.cse310': 0,
    'sb.cse312': 0,
    'sb.cse320': 0
}

'''
Open user file for editing
return file
'''
def openUsrFile(ID):
    print("opening " + (USER_PATH + ID + EXTENDSION))

    file = Path(USER_PATH + ID + EXTENDSION)
    if file.is_file():
        # read file and import data
        file = open((USER_PATH + ID + EXTENDSION), 'r+')
    else:
        # else create the file
        print("User does not exist, creating user...\n")
        file = open((USER_PATH + ID + EXTENDSION), 'w+')

    return file

'''
Open group file for editing
'''
def openGroupFile(group):
    file = open((GROUP_PATH + group + EXTENDSION), "r+")
    return file
    
def openGroupFileA(group):
    file = open((GROUP_PATH + group + EXTENDSION), "a")
    return file    

'''
getCurrentPostID

gets the current postID from groups file in serverData
This ID will keep track of the new ID number a post can have

return current post ID
'''
def getCurrentPostID():
    file = open((GROUP_PATH + 'groups'), 'r')
    currentPostID = int(file.readline())
    file.close()
    return currentPostID

'''
writeCurrentPostID

stores the current postID to the group file in serverData
This should be called when ever a new post is added. So that
if another client connects they can an updated number.
'''
def getWritePostID(n):
    file = open((GROUP_PATH + 'groups'), 'w')
    file.write(str(n))
    file.close()
    return 0

'''
sg
Send client the number of new post for each of their subscribed
groups
'''
def sg(ID, clientsocket,messageBuffer):
    usrfile = openUsrFile(ID)  # open user file that will hold a list of postID's that the user has read
                               # if a post ID is found that's not in the users postID then that post is unread and therefore new
                               # to the user
    while(1):                                         # take sub commands
        sub = getMessage(messageBuffer)
        if sub == "n":
            postRead = 0
            group = getMessage(messageBuffer)                  # get groupName from client that it wants the num of new post for

            postCnt = countPost(group)
            idList = getPostIDList(group)             # get the list of ID in a group

            while(len(idList) != 0):
                idToCheck = idList.pop()              # remove a ID from the list and check to see if it was read by the user
                while(1):
                    line = usrfile.readline()
                    if line == "":  # end of file has been reached
                        break
                    if line == idToCheck:
                        postRead += 1
            newPost = postCnt - postRead
            clientsocket.send((str(newPost)+ "+").encode())  # send back the number of new post to the client for that group

        elif sub == "q":
            break

    return 0

'''
rg
parameter ID, socket, group

client request to read groups.
'''
def rg(ID, clientsocket, serversocket, group, messageBuffer):

    file = Path(GROUP_PATH + group + EXTENDSION)
    if file.is_file():
        groupFile = openGroupFile(group)
    else:
        return

    file = Path(USER_PATH + ID + EXTENDSION)
    if file.is_file():
        userFile = openUsrFile(ID)
    else:
        userFile = open((USER_PATH + ID + EXTENDSION), "w+")

    try:
        numToShow = int(getMessage(messageBuffer))                       # listens for incoming N
    except:
        print(TimeOUTMESS)
        return -1

    while(1):

        request = getMessage(messageBuffer)                           # listens for incoming cmds like n, q, [ID], p

        req = request.split(" ")                                                # req is the list of cmd, 0 being the cmd itself and the following is the args
        if req[0] == 'r':
            try:
                range = getMessage(messageBuffer)   # server listens for a range ex: 1 2 3 4 or just 1
            except:
                print(TimeOUTMESS)
                return
            range = range.split("-")                      # split range into an array
            markPost(range, ID)
        elif req[0] == 'n':
            showPost(ID, numToShow, clientsocket, groupFile)
        elif req[0] == 'p':
            postRequest(ID, clientsocket, serversocket, group,messageBuffer)
        elif req[0] == 'q':
            groupPostList.clear()
            groupFile.close()
            userFile.close()
            break
        elif isinstance(int(req[0]), int):                           # checks if it is an int:
            postIndex = req[0]
            readPost(clientsocket, ID, group, postIndex, messageBuffer)
        else:
            print('request was not valid')

    return 0

'''
showPost

This function is for the cmd rg, it sends the data for if a post is new,
the date of the post and the subject of the post. This is done for N
post
'''
def showPost(ID, numToShow, clientSocket, groupFile):                                                          # resets the groupPostList
    with fileLock:
        x = 0

        while x < numToShow:
            isNew = "True+"
            line = groupFile.readline()
            if line == '':                                                         # EOF has been reached
                # inform client
                clientSocket.send("EOF+".encode())
                break
            line = line.split(":")
            if line[0] == 'PostID':
                userFile = openUsrFile(ID)
                postID = line[1]
                groupPostList.append(postID)
                while (1):
                    ln = userFile.readline()
                    if ln == "":  # end of file has been reached
                        break
                    if ln == postID:
                        isNew = "False+"
                        break
                userFile.close()
                clientSocket.send(isNew.encode())                                            # sends isNew a bool for if a post is new or not
            if line[0] == 'Date':
                clientSocket.send((line[1] + "+").encode())                                 # sends date line
            if line[0] == 'Subject':
                clientSocket.send((line[1] + "+").encode())                                 # sends subject line
                x += 1
    return
'''
findNewPost

Finds the number of new post for a user
returns a list of post ID found in a group
'''
def getPostIDList(group):
    file = openGroupFile(group)
    postList = []
    with fileLock:
        while(1):
            line = file.readline()
            if line == "":
                break
            wordArr = line.split(":")
            if wordArr[0] == 'PostID':
                postList.append(wordArr[1])
    file.close()

    return postList
'''
countPost

counts the number of post found in a group file
returns the number of post for that group
'''
def countPost(group):
    postCount = 0
    file = openGroupFile(group)
    with fileLock:
        while(1):
            line = file.readline()

            if line == "":                                  # end of file reached
                break
            if line == "---ENDOFPOST---\n" or line == "---ENDOFPOST---":
                postCount += 1                              # post found increment

    file.close()
    return postCount
'''
markPost
Given a list of post to mark as read
'''
def markPost(markRange, ID):
    usrFile = open((USER_PATH + ID + EXTENDSION), 'a')
    if len(markRange) == 1:
        postID = groupPostList[int(markRange[0])-1]
        usrFile.write(postID + "\n")
    else:
        for i in range(0, len(markRange)-1):
            postID = groupPostList[i]
            usrFile.write(postID + "\n")

    usrFile.close()
    return

'''
postRequest
Will handle the request from the client to post
Will listen for in coming messages from client and
write it the a file for that group
'''
def postRequest(ID, clientsocket, serversocket, group, messageBuffer):
    # Lock file for writing
    with fileLock:
        file = openGroupFileA(group)
        try:
            subject = clientsocket.recv(1024).decode()
        except:
            print(TimeOUTMESS)
            return -1

        file.write("\nPostID: " + str(getCurrentPostID()) + "\n")
        date = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
        file.write("Author: " + ID + "\n")
        file.write("Date: " + date + "\n")
        file.write("Subject: " + subject + "\n")
        getWritePostID(getCurrentPostID() + 1)             # update the file named groups


        # counter to check if the user wants to end post
        try:
            line = getMessage(messageBuffer)
        except:
            print(TimeOUTMESS)
            return -1
        #user body post
        while(line != "."):
            if(line == "EOF"):
                continue

            file.write(line)
            file.write("\n")
            try:
                line = getMessage(messageBuffer)
            except:
                print(TimeOUTMESS)
                return -1
        file.write("---ENDOFPOST---\n")
        file.close()
    return 0

'''
STILL A WORK IN PROGRESS

User requested to read a post. Get the post and find it by ID
by search thru the file for the group and regex the file for
the the ids and compare
'''
def readPost(clientsocket, ID, group, postnumber, messageBuffer):
    with fileLock:
        file = openGroupFile(group)
        postFound = False
        postCount = 0;
        while not postFound:  # read FILE line by line
            postID = file.readline()                    # read post line
            tempbuf = postID.split(':')                 # get the ID of the post from file
            ID = tempbuf[0]                             # check if is the first line of a post

            if ID == 'PostID':
                postCount += 1

            if int(postCount) == int(postnumber):
                postFound = True
                #mark post!!!
                markPost(postnumber, ID)

                authorName = file.readline()
                postDate = file.readline()
                subject = file.readline()
                groupLine = "Group: " + group + "\n"

                firstfour = [groupLine, subject, authorName, postDate]

                linecount = 0

                while 1:  # waitting for sub commands
                    sub = getMessage(messageBuffer)
                    if sub == "n":
                        if linecount < 4:
                            clientsocket.send(firstfour[linecount].encode())
                            linecount += 1
                        else:
                            line = file.readline()
                            if line == "":  # end of file has been reached
                                clientsocket.send("---ENDOFPOST---".encode())
                                break
                            elif line == "---ENDOFPOST---\n":  # end of post reached
                                clientsocket.send("---ENDOFPOST---".encode())
                                break
                            else:
                                clientsocket.send(line.encode())
                    elif sub == "q":
                        break

    file.close()
    return 0

'''
logout

parameter ID

handle client disconnecting. Remove or clean up any thing they used.
'''
def logout(ID):
    print("Client has logged out : " + ID)
    return 0

def initMessageBuffer():
    messageBuffer = queue.Queue()  # queue to hold incoming messages
    return  messageBuffer

def getMessage(messageBuffer):
    while(1):
        message = messageBuffer.get()
        if message is not None:
            break
    return message
'''
THIS IS CALLED BY A THREAD, DO NOT CALL THIS IN
THE SERVERFUNC
'''
def listenForMessages(client,messageBuffer):

    while(1):
        ready = select.select([client], [], [], 500)  # waits for data to be in the buffer
        if ready[0]:  # item is found
            request = client.recv(1024).decode()  # recv item
            request = request.split(' ')
            for x in request:
                if x != '':
                    with buffLock:
                        messageBuffer.put(x)  # add it to the queue
                if x == 'lo':
                    break
    return
'''
RUN THIS FUNCTION TO REBUILD
SERVER DATA DIR. NOT FOR USE OF
MAIN PROGRAM
'''
def createfiles():

    for i in groups.keys():
        fileName = GROUP_PATH + i + EXTENDSION
        file = open(fileName, 'w+')
        file.close()
    return 0