import os
import time
import re

USR_PATH = "serverData/"
EXTENDSION = ".txt"


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


def sg(ID, socket):
    return

'''
rg
parameter ID, socket, group

client request to read groups.
'''
def rg(ID, clientsocket, serversocket, group):

    while(1):
        request = clientsocket.recv(1024).decode()

        if request == 'r':
            print('User has mark files as read, update users data')
        elif request == 'n':
            print('send next list of post in group')
        elif request == 'q':
            break
        else:
            # check if its a read command
            reg = re.compile('r /d*')
            match = re.match(request)
            if match:
                req = request.split(' ')
                postNum = req[1]
                readPost(serversocket,group,postNum)


    return

def readPost(serversocket, group, postnumber):
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

'''
logout

parameter ID

handle client disconnecting. Remove or clean up any thing they used.
'''
def logout(ID):
    print("Client has logged out : " + ID)
    return

'''
RUN THIS FUNCTION TO REBUILD
SERVER DATA DIR. NOT FOR USE OF
MAIN PROGRAM
'''
def createfiles():

    for i in groups.keys():
        fileName = USR_PATH + i + EXTENDSION
        file = open(fileName, 'w+')
        file.close()
    return
