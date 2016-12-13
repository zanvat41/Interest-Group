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
        try:
            ID = clientsocket.recv(1024).decode()
            print("ID : " + ID + " has connected to the server")
        except:
            print(serverFunc.TimeOUTMESS)
        try:
            newThread = threading.Thread(target = handleClient,
                                         name = ("client" + ID),
                                         args = (ID, clientsocket,serverSocket,))
            newThread.daemon = True
            clientList.append(newThread)
            newThread.start()
        except:
            print("ERROR : unable to create thread for user ")

        for x in clientList:
            x.join()                                          # loop thur list clientList
            print("thread joined")                          # and join them

def handleClient(ID, clientsocket, serversocket):
    currID = serverFunc.getCurrentPostID()
    print(currID)
    buff = serverFunc.initMessageBuffer()
    recvThread = threading.Thread(target = serverFunc.listenForMessages,
                                  name = ('messageQueue' + ID),
                                  args = (clientsocket,buff,))
    recvThread.daemon = True
    recvThread.start()

    while (1):
        try:
            request = serverFunc.getMessage(buff)                            # listen for incoming request like sg, rg, lo(logout)
            print(currID)
            if request == "sg":
                serverFunc.sg(ID, clientsocket,buff)
            elif request == "rg":
                group = serverFunc.getMessage(buff)                          # listens for incoming group name that the client wants to read
                serverFunc.rg(ID, clientsocket, serversocket, group,buff)
            elif request == "lo":
                recvThread.join()
                serverFunc.logout(ID)
                break
        except:
            print(serverFunc.TimeOUTMESS)
            break

def exit():
    serverSocket.close()
    exit()

# run main
if(__name__ == "__main__"):
    main()
