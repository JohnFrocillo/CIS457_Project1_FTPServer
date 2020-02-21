#client.py

import socket
import os
import argparse
import time

print("Client Started")

while(True):
    servStr = input("Please input a message (\"CLOSE\" to quit): ")
    servStr = servStr.replace(":", " ")
    servAddr = servStr.split(" ")
    if (servAddr[0] == "CLOSE"):
        break
    elif (servAddr[0] == "CONNECT" and len(servAddr) == 3):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            failedToConnect = False
            try:
                s.settimeout(5)
                print("Connecting...")
                s.connect((servAddr[1], int(servAddr[2])))
            except:
                failedToConnect = True
                print("Failed to connect.")
            if(not failedToConnect):
                print("Successfully Connected!")
                
            while (not failedToConnect):
                msg = input("Please input a message (\"QUIT\" to disconnect): ")
                msgs = msg.split(" ")
                if (msg == "QUIT"):
                    s.sendall(msg.encode())
                    data = s.recv(1024)
                    print(repr(data.decode()))
                    break
                elif (msg == "LIST"):
                    s.sendall(msg.encode())
                    data = s.recv(1024) #1024 is the number of bytes to receive
                    print(str(data.decode()))
                elif (msgs[0] == "RETRIEVE"):
                    s.sendall(msg.encode())
                    fileName = str(msgs[1])
                    data = s.recv(1024)
                    if (data.decode() == "File does not exist."):
                        print("> " + repr(data.decode()))
                        data = s.recv(1024)
                        print("> " + repr(data.decode()))
                        continue
                    else:
                        print("Retrieving file...")
                    f = open(fileName,'wb') #open in binary
                     # receive data and write it to file
                    while True:
                        if (data.decode() == "File does not exist."):
                            print("> " + repr(data.decode()))
                            break
                        #print('Receiving data. . .')
                        #print('data=%s', (data))
                        if not data:
                            break
                        if data.decode()[-3:] == "EOF":
                            # write data to a file
                            temp = data.decode()
                            temp = temp[:-3]
                            data = temp.encode()
                            f.write(data)
                            f.close()
                            break
                        else:
                            f.write(data)
                        data = s.recv(1024)
                    f.close()
                    data = s.recv(1024)
                    print("> " + repr(data.decode()))

                elif (msgs[0] == "STORE"):
                    try:
                        f = open (msgs[1], "rb")
                    except:
                        print("File does not exist.")
                        continue
                    s.sendall(msg.encode())
                    print("Storing file...")
                    time.sleep(1)
                    l = f.read(1024)
                    while (l):
                        s.send(l)
                        l = f.read(1024)
                    s.send("EOF".encode())
                    f.close()
                    #print("File successfully stored.")
                    os.remove(msgs[1])
                    data = s.recv(1024)
                    print("> " + repr(data.decode()))
                else:
                    print("Command not recognized")

print("Client disconnected.")
