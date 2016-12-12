import os
import math
from pathlib import Path

# Declare CONSTANT vars
DEFAULT_N = 5
USR_PATH = 'usrs/'
EXTENDSION = '.txt'

# Some global vars
userFile = ""


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
    print("**This is a help menu, this menu can be brought up by typing the command help\n\n",
          "login: \t logs user in to determine which discussion groups are subscribed to. \n\n",          
          "ag[N]: \t Prints a list of Discussion groups\n\t\t\tN: (optional) 1 to N for the number of ",
          "groups to be displayed\n\t\t\tDefault: 5\n\n",
          "\t\tSub-commands:\n\t\ts: Subscribe to one, or more, discussion groups numbered 1-to-N (ex. u 1 3)\n",
          "\t\tu: Unsubscribe to one, or more, discussion groups numbered 1-to-N. (ex. u 1 3)\n",
          "\t\tn: Lists next N discussion groups. If all discussion groups have been displayed, exit ag.\n",
          "\t\tq: Exit ag.\n\n",
          "sg[N]:\tPrints a list of Subscribed groups\n\t\t\t",
          "N: (optional) 1 to N for the number of groups to be displayed\n\t\t\tDefault: 5\n\n",          
          "rg[N]:\tPrints a list of groups to read from\n\t\t\t",
          "N: (optional) 1 to N for the number of groups to be displayed\n\t\t\tDefault: 5\n\n",
          "\t\tSub-commands:\n\t\tid: Displays the Nth post in a list. While displaying contents, has two sub-commands.",
          "\n\t\t\tn: Displays N more lines of content.\n\t\t\tq: Exits post without displaying further content.",
          "\n\t\tr: Marks a post, numbered one-to-N, as read. (ex. r 1)",
          "\n\t\tn: Lists next N posts. If all posts have been displayed, exist rg.",
          "\n\t\tp: Post to group. User is prompted to enter a one-line subject and then the content of the post.",
          "\n\t\t   To finish writing a post, enter '.' on a blank line.",
          "\n\t\tq: Exit rg. \n\nlogout:\t Logs the user out.",
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
    global userFile
    userFile = USR_PATH + str(ID) + EXTENDSION
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
    remain = total
    n = int(N)
    if n < remain:
        remain = remain - n
    else:
        n = remain
        remain = 0

    # First print out the first n groups
    for i in range(1, n+1):
        sub = " "
        if int(groups.get(keys[total - remain - n + i - 1])) == 1:
            sub = "s"
        print(str(i) + ". (" + sub + ") " + keys[total - remain - n + i - 1])


    # Then take sub-commands
    while (1):
        cmd = input("ag >> ").split()  # arg[0] will always be the cmd
        # and all following items are ARGS
        if cmd[0] == "s":
            if len(cmd) == 1:
                print("Command Error: s, too few arguments")
            else:
                # change the groups values
                for i in range (1, len(cmd)):
                    groups[keys[total - remain - n - 1 + int(cmd[i])]] = 1

                # then update and write back to the user file
                updateHisto()
        elif cmd[0] == "u":  # similar to s
            if len(cmd) == 1:
                print("Command Error: u, too few arguments")
            else:
                # change the groups values
                for i in range (1, len(cmd)):
                    groups[keys[total - remain - n - 1 + int(cmd[i])]] = 0

                # then update and write back to the user file
                updateHisto()
        elif cmd[0] == "n":
            if remain <= 0:
                print("No more groups")
                continue
            n = N
            if n < remain:
                remain = remain - n
            else:
                n = remain
                remain = 0

            # First print out the first n groups
            for i in range(1, n + 1):
                sub = " "
                if groups.get(keys[total - remain - n + i - 1]) == 1:
                    sub = "s"
                print(str(i) + ". (" + sub + ") " + keys[total - remain - n + i - 1])
        elif cmd[0] == "q":
            break
        else:
            print("Incorrect Command. Press q to quit ag.")
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
def rg(gname, N, clientSocket):
    # Check if given group name exists
    if str(gname) not in keys:
        print(str(gname) + " does not exist.")
        return

    # Send the server the group name
    clientSocket.send(gname)

    # And then N
    clientSocket.send(N)

    # Ask the server to give the newest N post, and then print if it is not empty
    clientSocket.send("n")
    for i in range(0, N):
        message = str(i) + ". "
        # First check if there are any post remained. If so, check if the post is read or not
        isRead = clientSocket.recv(1024)
        if isRead == "EOF":
            print("No more post")
            # end server side
            break
        elif isRead == "True":
            message += "  "
        else:
            message += "N "
        # Then get the date
        date = clientSocket.recv(1024)
        message += date
        # Finally the title
        title = clientSocket.recv(1024)
        message(title)

        print(message)

    numShown = 0  # The number of posts shown

    # Then take sub-commands
    while (1):
        cmd = input("rg >> ").split()  # arg[0] will always be the cmd
        # and all following items are ARGS
        if cmd[0] == "r":
            if len(cmd) == 1:
                print("Command Error: r, too few arguments")
            elif "-" in cmd[1]:
                # Get the max and min of the range, for example get 1 and 3 for input 1-3
                line = cmd[1].split("-")
                min = (int)(line[0])
                max = (int)(line[1])
                list = ""
                for i in range (min, max + 1):
                    list += str(i + numShown) + " "
                # send it to server
                clientSocket.send(list)
            else:
                arg = (int)(cmd[1]) + numShown
                clientSocket.send(str(arg))
        elif cmd[0] == "n":
            numShown += N
            # Ask the server to give the newest N post, and then print if it is not empty
            clientSocket.send("n")
            for i in range(0, N):
                message = str(i) + ". "
                # First check if there are any post remained. If so, check if the post is read or not
                isRead = clientSocket.recv(1024)
                if isRead == "EOF":
                    print("No more post")
                    break
                elif isRead == "True":
                    message += "  "
                else:
                    message += "N "
                # Then get the date
                date = clientSocket.recv(1024)
                message += date
                # Finally the title
                title = clientSocket.recv(1024)
                message(title)

                print(message)
        elif cmd[0] == "p":
            clientSocket.send("p")
            print("Please Type In Title:")
            postTitle = input()
            clientSocket.send(postTitle)
            print("Please Type In Content:")
            while(1):
                postLine = input()
                clientSocket.send(postLine)
                writeStatus = clientSocket.recv(1024)
                if writeStatus == "end":
                    break
        elif cmd[0] == "q":
            clientSocket.send("q")
            break
        else:
            while(1):
                # take sub-commands for read
                print("read")










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
updateHisto

update subscribed/unsubscribed group to user file
similar to createHisto
'''
def updateHisto():
    file = open(userFile, 'w')
    for key, value in groups.items():
        file.write(key)                                   # writes key name
        file.write(",")                                 # writes sep
        file.write(str(groups.get(key)))                  # writes value
        file.write("\n")                                # writes new line
    file.close()
    return



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

        file.write(key)                                    # writes group name
        file.write(",")                                    # writes sep
        #if key == 'Author':                                # gets the users name for post writing for first time users
         #   name = input('Please enter your name\n')
         #   file.write(name)
        #else:
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