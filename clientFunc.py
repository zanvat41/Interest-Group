import os
from pathlib import Path

# Declare CONSTANT vars
DEFAULT_N = 5
USR_PATH = 'usrs/'
EXTENDSION = '.txt'

# Group Map
# Just a quick write up of a group map for all the discussion
# groups that will be use. Can be cleaned up some.
# This will mainly be used to make the user file.
# Key : group name  ,   Value : subscribed boolean(0/1)
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

# help
# Prints a list of supported commands and sub-commands.
# For each command or sub-command, a brief description of
# its function and the syntax of usage are displayed
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

# login
# Allows the user to login using their ID number
def login(ID):
    # Do login stuff
    loggedIn = False;
    file = Path(USR_PATH + ID +EXTENDSION)
    if file.is_file():
        # read file and import data
        print("FILE IS HERE")
        fillHisto(ID)
    else:
        # else create the file
        print("FILE DOESNT EXIT")
        createHisto(ID)

    return loggedIn

# ag
# this command stands for “all groups”. It takes an optional argument, N,
# and lists the names of all existing discussion groups, N groups at a time,
# numbered 1 to N.  If N is not specified, a default value is used.
def ag():
    return

# sg
# this command stands for “subscribed groups”. It takes an optional argument, N,
# and lists the names of all subscribed groups, N groups at a time, numbered 1 to N.
# If N is not specified, a default value is used.
def sg():
    return

# rg
# this command stands for “read group”. It takes one mandatory argument, gname,
# and an optional argument N, and displays the (status – new or not, time stamp, subject line)
# of all posts in the group gname, N posts at a time. If N is not specified, a default value
# is used. gname must be a subscribed group.
def rg():
    return

# Logout
# Function takes no arguments. It logs out the current user
# closes the socket and terminates the client program
def logout(socket):
    print("Logging out...")
    socket.close()
    exit()

# createHisto
# If a user logs inand no file exist for the ID then create a new file for that user with the
# ID as the file name
def createHisto(ID):
    fileName = USR_PATH + str(ID) + EXTENDSION
    file = open(fileName, 'w')

    for i in groups.keys():
        file.write(i)                                   # writes group name
        file.write(",")                                 # writes sep
        file.write(str(groups.get(i)))                  # writes sub bool for group
        file.write("\n")                                # writes new line

    file.close()
    return

# fillHisto
#
#
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