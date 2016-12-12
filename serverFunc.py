import os
import datetime
import threading
import select
import queue

GROUP_PATH = "serverData/"
USER_PATH = "serverData/users"
EXTENDSION = ".txt"

# ERROR MESSAGES
TimeOUTMESS = "A TIME OUT HAS OCCURRED"

currentPostID = 0
fileLock = threading.Lock()
groupPostList = []                  # list to hold group post ID by index
messageBuffer = queue.Queue()       # queue to hold incoming messages

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
    file = open((USER_PATH + ID + EXTENDSION), 'r+')
    return file

'''
Open group file for editing
'''
def openGroupFile(group):
    file = open((GROUP_PATH + group + EXTENDSION), "r+")
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
def getWritePostID():
    file = open((GROUP_PATH + 'groups'), 'w')
    file.write(currentPostID)
    file.close()
    return 0

'''
sg
Send client the number of new post for each of their subscribed
groups
'''
def sg(ID, clientsocket):
    usrfile = openUsrFile(ID)  # open user file that will hold a list of postID's that the user has read
                               # if a post ID is found that's not in the users postID then that post is unread and therefore new
                               # to the user
    while(1):                                         # take sub commands
        sub = getMessage()
        if sub == "n":
            postRead = 0
            try:
                group = getMessage()                  # get groupName from client that it wants the num of new post for

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
                clientsocket.send(str(newPost).encode())  # send back the number of new post to the client for that group

            except:
                print(TimeOUTMESS)  # Timed out of the all sub groups have been served
                break

        elif sub == "q":
            break

    return 0

'''
rg
parameter ID, socket, group

client request to read groups.
'''
def rg(ID, clientsocket, serversocket, group):
    groupFile = openGroupFile(group)
    userFile = openUsrFile(ID)

    try:
        numToShow = int(clientsocket.recv(1024).decode())                       # listens for incoming N
    except:
        print(TimeOUTMESS)
        return -1

    showPost(ID,numToShow,serversocket,groupFile,userFile)                      # handle showing post to client

    while(1):
        try:
            request = clientsocket.recv(1).decode()                          # listens for incoming cmds like n, q, [ID], p
        except:
            print(TimeOUTMESS)
            return -1
        req = request.split(" ")                                                # req is the list of cmd, 0 being the cmd itself and the following is the args
        if req[0] == 'r':
            try:
                range = clientsocket.recv(1024).decode()  # server listens for a range ex: 1 2 3 4 or just 1
            except:
                print(TimeOUTMESS)
                return
            range = range.split(" ")                      # split range into an array
            markPost(range, ID)
        elif req[0] == 'n':
            showPost(ID, numToShow, serversocket, groupFile, userFile)
        elif req[0] == 'p':
            postRequest(ID, clientsocket, serversocket, group)
        elif req[0] == 'q':
            groupFile.close()
            userFile.close()
            break
        elif isinstance(int(req[0]), int):                           # checks if it is an int:
            postIndex = req[0]
            readPost(clientsocket, serversocket, group, postIndex, numToShow)
        else:
            print('request was not valid')

    return 0

'''
showPost

This function is for the cmd rg, it sends the data for if a post is new,
the date of the post and the subject of the post. This is done for N
post
'''
def showPost(ID, numToShow, serversocket, groupFile, userFile):
    groupPostList.clear()                                                           # resets the groupPostList
    with fileLock:
        x = 0;
        while x < numToShow:
            isNew = "True"
            line = groupFile.readline()
            if line == ' ':                                                         # EOF has been reached
                # informe client
                serversocket.send("EOF")
                break
            line = line.split(":")
            if line[0] == 'PostID':
                postID = line[1]
                groupPostList.append(postID)
                while (1):
                    ln = userFile.readline()
                    if ln == "":  # end of file has been reached
                        break
                    if ln == postID:
                        isNew = "False"
                serversocket.send(isNew)                                            # sends isNew a bool for if a post is new or not
            if line[0] == 'Date':
                serversocket.send(line[1])                                          # sends date line
            if line[0] == 'Subject':
                serversocket.send(line[1])                                          # sends subject line
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
def markPost(markAsRead, ID):
    usrFile = openUsrFile(ID)
    while(len(markAsRead) != 0):
        postIndex = markAsRead.pop()
        postID = groupPostList[postIndex]
        usrFile.write(postID,'a')
    usrFile.close()
    return

'''
postRequest
Will handle the request from the client to post
Will listen for in coming messages from client and
write it the a file for that group
'''
def postRequest(ID, clientsocket, serversocket, group):

    # Lock file for writing
    with fileLock:
        file = openGroupFile(group)
        file.write("Group: " + group)
        try:
            subject = clientsocket.recv(1024).decode()
        except:
            print(TimeOUTMESS)
            return -1

        file.write("Subject: " + subject)
        file.write("Author: " + ID)
        date = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
        file.write("Date: " + date)

        # counter to check if the user wants to end post
        endpost = 0
        #user body post
        while(1):
            try:
                line = clientsocket.recv(1024).decode()
            except:
                print(TimeOUTMESS)
                return -1
            # find if user is trying to end post
            if (endpost == 1):
                if (line == "."):
                    endpost += 1
                else:
                    endpost = 0  # reset endpost

            if(line == "\n"):
                endpost += 1

            if(endpost == 3):
                file.write("---ENDOFPOST---")
                serversocket.send("end")                # inform the client writing ended
                break                                   # '\n.\n' was found, exit

            file.write(line)
            serversocket.send("writing")                # inform the client the server is writing
        file.close()
    return 0

'''
STILL A WORK IN PROGRESS

User requested to read a post. Get the post and find it by ID
by search thru the file for the group and regex the file for
the the ids and compare
'''
def readPost(clientsocket, serversocket, group, postnumber, N):
    with fileLock:
        file = open(group, 'w')
        postFound = False
        while postFound:  # read FILE line by line
            postID = file.readline()                    # read post line
            tempbuf = postID.split(':')                 # get the ID of the post from file
            ID = tempbuf[1]                             # check if post matches the ID that the user wants
            if (int)(ID) == (int)(postnumber):
                postFound = True
                serversocket.send(postID.encode())
                authorName = file.readline()
                serversocket.send(authorName.encode())
                postDate = file.readline()
                serversocket.send(postDate.encode())
                subject = file.readline()
                serversocket.send(subject.encode())

                while 1:  # waitting for sub commands
                    sub = clientsocket.recv(1024).decode()
                    if sub == "n":
                        for i in range(0, int(N)):
                            line = file.readline()
                            if line == "":  # end of file has been reached
                                serversocket.send("---ENDOFPOST---".encode())
                                break
                            elif line == "---ENDOFPOST---":  # end of post reached
                                serversocket.send("---ENDOFPOST---".encode())
                                break
                            else:
                                serversocket.send(line.encode())
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

def getMessage():
    while(1):
        message = messageBuffer.get()
        if message is not None:
            break
    return message
'''
THIS IS CALLED BY A THREAD, DO NOT CALL THIS IN
THE SERVERFUNC
'''
def listenForMessages(client):
    while(1):
        ready = select.select([client], [], [], 15)  # waits for date to be in the buffer
        if ready[0]:  # item is found
            request = client.recv(1024).decode()  # recv item
            request = request.split(' ')
            for x in request:
                if x != '':
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
