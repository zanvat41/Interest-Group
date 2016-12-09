import clientFunc
from socket import *

# Establish socket connection
serverName = 'localhost'
serverPort = 7257
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
print("Client is connected...")

# main function
def main():
    # Constant Var for N
    DEFAULT_N = 15

    # Log in status for user
    LOGGED_IN = False

    while(1):

        cmd = input("Client >> ").split()                           # takes user input and splits it into a list
                                                                     #       arg[0] will always be the cmd
        if cmd[0] == "help":                                        #       and all following items are ARGS
            clientFunc.printHelp()               # print help
        elif cmd[0] == "login":                 # log user in
            if LOGGED_IN == False:

                LOGGED_IN = clientFunc.login(cmd[1])
                print("User : " + cmd[1] + " is now logged in.")
                clientSocket.send(cmd[1].encode())
            else:
                print("You are already logged in.")

        elif cmd[0] == "ag":
            if LOGGED_IN == False:
                print("please login first")
            else:
                clientFunc.ag()
        elif cmd[0] == "sg":
            if LOGGED_IN == False:
                print("please login first")
            else:
                clientFunc.sg()
        elif cmd[0] == "rg":
            if LOGGED_IN == False:
                print("please login first")
            else:
                clientFunc.rg()
        elif cmd[0] == "logout":
            if LOGGED_IN == False:
                print("You are not logged in")
            else:
                clientFunc.logout(clientSocket)
        elif cmd[0] == "quit":
            print("Exiting...")
            clientSocket.close()
            exit()
        else:
            print("Invalid Command")
            clientFunc.printHelp()

# run main
if(__name__ == "__main__"):
    main()
