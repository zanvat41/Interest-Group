import os
import time

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

def rg(ID, socket):
    return
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
