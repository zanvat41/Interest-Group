from socket import *
import threading
import serverFunc

import time

# Set up TCP connection
serverPort = 7257
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(5)

clientList = []

def main():
    print("Server is running...")
    while (1):
        clientsocket, address = serverSocket.accept()
        print("Connection found")
        ID = clientsocket.recv(1024).decode()
        print("ID : " + ID + " has connected to the server")
        try:

            newThread = threading.Thread(target = handleClient, name = ("client" + ID), args = (ID, clientsocket,))
            newThread.daemon = True
            clientList.append(newThread)
            newThread.start()
        except:
            print("ERROR : unable to create thread for user " + ID)

        for x in clientList:
            x.join()                                          # loop thur list clientList
            print("thread joined")                          # and join them

def handleClient(ID, clientsocket):

    while (1):
        request = clientsocket.recv(1024).decode()

        if request == "sg":
            serverFunc.sg(ID, clientsocket)
        elif request == "rg":
            serverFunc.rg(ID, clientsocket)
        elif request == "lo":
            serverFunc.logout(ID)
            break
        else:
            # something went wrong
            print("Invalid request")


def exit():
    serverSocket.close()
    exit()

# run main
if(__name__ == "__main__"):
    main()
