import clientFunc
from socket import *

'''
TCP Discussion Group Client/Sever
Authors : Johnson Lu, Christopher Andrzejczyk, Zhe Lin

Python 3.5
'''
# Establish socket connection
serverName = 'localhost'                                # *** REMEMBER TO SWITCH THIS TO CONNECT TO A USER SELECTED IP
serverPort = 7257
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.setblocking(0)
clientSocket.settimeout(10)                                 # Socket will try to connect for 10 seconds and then time out
try:
    clientSocket.connect((serverName, serverPort))
except:
    print("Client could not connect to server, please try again")
    exit()

print("Client is connected...")

# main function
def main():
    # Constant Var for N
    DEFAULT_N = 5

    # Log in status for user
    LOGGED_IN = False

    while(1):

        cmd = input("Client >> ").split()                           # takes user input and splits it into a list
                                                               #       arg[0] will always be the cmd
        if cmd[0] == "help":                                        #       and all following items are ARGS
            clientFunc.printHelp()               # print help
        elif cmd[0] == "login":                 # log user in
            if LOGGED_IN == False:
                if(len(cmd) < 2):
                    print("No user ID provided")
                else:
                    LOGGED_IN = clientFunc.login(cmd[1])
                    print("User : " + cmd[1] + " is now logged in.\n")
                    clientSocket.send(cmd[1].encode())
            else:
                print("You are already logged in.\n")

        elif cmd[0] == "ag":
            if LOGGED_IN == False:
                print("please login first\n")
            else:
                if(len(cmd) == 1):
                    clientFunc.ag(DEFAULT_N)
                elif(len(cmd) == 2):
                    clientFunc.ag(cmd[1])
                else:
                    print("Command Error: ag, too many arguments")
        elif cmd[0] == "sg":
            if LOGGED_IN == False:
                print("please login first\n")
            else:
                if(len(cmd) == 1):
                    clientFunc.sg(DEFAULT_N, clientSocket)
                elif(len(cmd) == 2):
                    clientFunc.sg(cmd[1], clientSocket)
                else:
                    print("Command Error: sg, too many arguments")
        elif cmd[0] == "rg":
            if LOGGED_IN == False:
                print("please login first\n")
            else:
                if len(cmd) == 1:
                    print("Not enough arguments. Group name needed.")
                elif len(cmd) == 2:
                    clientSocket.send("rg".encode())
                    clientFunc.rg(cmd[1], DEFAULT_N, clientSocket)
                else:
                    clientSocket.send("rg".encode())
                    clientFunc.rg(cmd[1], cmd[2], clientSocket)
        elif cmd[0] == "logout":
            if LOGGED_IN == False:
                print("You are not logged in\n")
            else:
                clientSocket.send("lo".encode())
                clientFunc.logout(clientSocket)
        elif cmd[0] == "quit":
            print("Exiting...\n")
            clientSocket.send("lo".encode())
            clientSocket.close()
            exit()
        else:
            print("Invalid Command\n")
            clientFunc.printHelp()

# run main
if(__name__ == "__main__"):
    main()