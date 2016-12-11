import os
import datetime
import threading
from pathlib import Path
import re

GROUP_PATH = "serverData/"
USER_PATH = "server/Data/users"
EXTENDSION = ".txt"

# ERROR MESSAGES
TimeOUTMESS = "A TIME OUT HAS OCCURRED"

currentPostID = 0
fileLock = threading.Lock()
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

    file = open((USER_PATH + ID + EXTENDSION), 'w+')
    return file

'''
Open group file for editing
'''
def openGroupFile(group):
    file = open((GROUP_PATH + group + EXTENDSION), "w+")
    return file
'''
sg
Send client the number of new post for each of their subscribed
groups
'''
def sg(ID, socket):
    return 0

'''
rg
parameter ID, socket, group

client request to read groups.
'''
def rg(ID, clientsocket, serversocket, group):

    while(1):
        try:
            request = clientsocket.recv(1024).decode()
        except:
            print(TimeOUTMESS)
            return -1
        req = request.split(" ")                                                # req is the list of cmd, 0 being the cmd itself and the following is the args
        if req[0] == 'r':
            markPost()
        elif req[0] == 'n':
            print('send next list of post in group')
        elif req[0] == 'p':
            postRequest(ID, clientsocket, group)
        elif req[0] == 'q':
            break
        else:
            # check if its a read command
            print("usr wants to read post")



    return 0

'''
markPost
Given a list of post to mark as read
'''
def markPost(markAsRead):
    while(len(markAsRead) != 0):
        postNum = markAsRead.pop()
        #make that post as read
    return

'''
postRequest
Will handle the request from the client to post
Will listen for in coming messages from client and
write it the a file for that group
'''
def postRequest(ID, clientsocket, group):

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
                break                                   # '\n.\n' was found, exit

            file.write(line)
        file.close()
    return 0

'''
User requested to read a post. Get the post and find it by ID
by search thru the file for the group and regex the file for
the the ids and compare
'''
def readPost(serversocket, group, postnumber):
    with fileLock:
        file = open(group, 'w')
        while 1:  # read FILE line by line
            postID = file.readline()                    # read post line
            tempbuf = postID.split(':')                 # get the ID of the post from file
            ID = tempbuf[1]                             # check if post matches the ID that the user wants
            if ID == postnumber:
                serversocket.send(postID.encode())
                authorName = file.readline()
                serversocket.send(authorName.encode())
                postDate = file.readline()
                serversocket.send(postDate.encode())
                subject = file.readline()
                serversocket.send(subject.encode())

                while 1:  # read POST and send post line by line till it reaches end of post
                    line = file.readline()
                    if line == "":  # end of file has been reached
                        break
                    if line == "---ENDOFPOST---":  # end of post reached
                        break
                    serversocket.send(line.encode())

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
