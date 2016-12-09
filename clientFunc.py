import os
import math
from pathlib import Path

# Declare CONSTANT vars
DEFAULT_N = 5
USR_PATH = 'usrs/'
EXTENDSION = '.txt'

'''
Group Map

Just a quick write up of a group map for all the discussion
groups that will be use. Can be cleaned up some.
This will mainly be used to make the user file.
Key : group name  ,   Value : subscribed boolean(0/1)
'''
groups = {
    'Author' : 'name',
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

"""
The keys in groups.
In convenience of ag, sg and rg
"""
keys = [
    'comp.programming',
    'comp.lang.c',
    'comp.lang.python',
    'comp.lang.javascript',
    'comp.lang.c++',
    'comp.lang.java',
    'math.crypto',
    'math.algro',
    'math.calc',
    'math.stats',
    'sb.cse114',
    'sb.cse214',
    'sb.cse219',
    'sb.cse220',
    'sb.cse300',
    'sb.cse303',
    'sb.cse310',
    'sb.cse312',
    'sb.cse320']


'''
help

Prints a list of supported commands and sub-commands.
For each command or sub-command, a brief description of
its function and the syntax of usage are displayed
'''
def printHelp():
    print("**This is a help menu, this menu can be brought up by typing the command help\n",
          "login",
          "ag[N]\tPrints a list of Discussion groups\n\t\t\tN: 1 to N for the number of",
          "groups to be displayed\n\t\t\tDefault: 5\n",
          "sg[N]\tPrints a list of Subscribed groups\n\t\t\t",
          "N: 1 to N for the number of groups to be displayed\n\t\t\tDefault: 5\n",
          "rg[N]\tPrints a list of groups to read from\n\t\t\t",
          "N: 1 to N for the number of groups to be displayed\n\t\t\tDefault: 5\n",
          sep="")
    return

'''
login

Parameters ID, user ID for log in

Allows the user to login using their ID number
returns true if the user was logged in and false if
the user was not logged in. Pretty much the way this
is written it will always return true, really no reason
for it not to.

Return : True if user logged in, False if user is not
'''
def login(ID):
    # Do login stuff
    file = Path(USR_PATH + ID + EXTENDSION)
    if file.is_file():
        # read file and import data
        fillHisto(ID)
    else:
        # else create the file
        print("User does not exist, creating user...\n")
        createHisto(ID)

    return True


'''
# ag

# this command stands for “all groups”. It takes an optional argument, N,
# and lists the names of all existing discussion groups, N groups at a time,
# numbered 1 to N.
'''
def ag(N):
    total = len(keys)
    remain = len(keys)
    n = N
    if n < remain:
        remain = remain - n
    else:
        n = remain

    # First print out the first n groups
    for i in range(1, n+1):
        sub = " "
        if groups.get(keys[i - 1]) == 1:
            sub = "s"
        print(str(i) + ". (" + sub + ") "+ keys[i - 1])


    # Then take sub-commands
    while (1):
        cmd = input("ag >> ").split()  # arg[0] will always be the cmd
        if cmd[0] == "s":  # and all following items are ARGS
            if len(cmd) == 1:
                print("Command Error: s, too few arguments")
            else:
                for i in range (1, len(cmd)):
                    groups[keys[total - remain - n - 1 + cmd[i]]] = 1

                # then update the user file
                # create a function like createHisto


        elif cmd[0] == "q":
            break





    return




'''
sg

this command stands for “subscribed groups”. It takes an optional argument, N,
and lists the names of all subscribed groups, N groups at a time, numbered 1 to N.
If N is not specified, a default value is used.
'''
def sg():
    return
''''
rg

this command stands for “read group”. It takes one mandatory argument, gname,
and an optional argument N, and displays the (status – new or not, time stamp, subject line)
of all posts in the group gname, N posts at a time. If N is not specified, a default value
is used. gname must be a subscribed group.
'''
def rg():
    return
'''
Logout

Function takes no arguments. It logs out the current user
closes the socket and terminates the client.py program
'''
def logout(socket):
    print("Logging out...")
    socket.close()
    exit()
'''
createHisto
Parameters ID, user ID to use for file name

If a user logs in and no file exist for the ID then create a new file for that user with the
ID as the file name
'''
def createHisto(ID):
    fileName = USR_PATH + str(ID) + EXTENDSION
    file = open(fileName, 'w')

    for key, value in groups.items():

        file.write(key)                                   # writes group name
        file.write(",")                                 # writes sep
        if key == 'Author':  # gets the users name for post writing
            name = input('Please enter your name\n')
            file.write(name)
        else:
            file.write(str(groups.get(key)))                  # writes sub bool for group
        file.write("\n")                                # writes new line

    file.close()
    return

'''
fillHisto

Parameters ID, user ID for opening a file using the id name

FillHisto opens the user's data file and it fills it with the current histo
if the user has no file this function will be called to write a default group
histo to the file.
Call this function to write to the data file with an updated histo
'''
def fillHisto(ID):
    fileName = USR_PATH + str(ID) + EXTENDSION
    file = open(fileName, 'r')

    while 1:
        line = file.readline()                          # read file line by line
        # end of file has been reached
        if line == "":
            break
        data = line.split(',')                          # breaks the line into its part by ','
        if data[0] in groups.keys():                    # checks if the data is correct
            groups[data[0]] = data[1]                   # sets the value
    file.close()