# Declare CONSTANT vars
DEFAULT_N = 5

# help
# Prints a list of supported commands and sub-commands.
# For each command or sub-command, a brief description of
# its function and the syntax of usage are displayed
def printHelp():
    print("**This is a help menu, this menu can be brought up by typing the command help\n",
          "ag[N]\tPrints a list of Discussion groups\n\t\t\tN: 1 to N for the number of",
          "groups to be displayed\n\t\t\tDefault: 5\n",
          "sg[N]\tPrints a list of Subscribed groups\n\t\t\t",
          "N: 1 to N for the number of groups to be displayed\n\t\t\tDefault: 5\n",
          "rg[N]\tPrints a list of groups to read from\n\t\t\t",
          "N: 1 to N for the number of groups to be displayed\n\t\t\tDefault: 5\n",
          sep="")
    return

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
