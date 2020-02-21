#server.py

import socket
import selectors
import os
import time

#Local machine
HOST = "127.0.0.1"
#Port to listen on. Must be the same one specified by client.
PORT = 54321

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    print("Server started with IP " + HOST + " on port " + str(PORT) + ". Waiting for connection.")
    s.listen()
    
    while (True):
        conn, addr = s.accept()
        with conn:
            print("Connected to by", addr)
            while True:
                dataSent = conn.recv(1024)
                if not dataSent:
                    break
                commandSent = dataSent.decode().split(" ")
                #print(str(commandSent[0]))
                justTheCommand = commandSent[0]
                
                if (justTheCommand == "LIST"):
                    print("Client Requested LIST")
                    msg = os.listdir(".")
                    sendBack = '\n'.join(msg)
                    sendBack = sendBack.encode()
                elif (justTheCommand == "RETRIEVE"):
                    print ("Client Requested RETRIEVE")
                    msg = "File successfully retrieved."
                    sendBack = msg.encode()

                    try:
                        f = open (commandSent[1], "rb")
                    except:
                        msg = "File does not exist."
                        sendBack = msg.encode()
                        conn.sendall(sendBack)
                        time.sleep(1)
                        msg = "Please use a valid file name."
                        sendBack = msg.encode()
                        conn.sendall(sendBack)
                        continue
                    l = f.read(1024)
                    while (l):
                        conn.send(l)
                        l = f.read(1024)
                    conn.send("EOF".encode())
                    f.close()
                    print("File successfully sent.")
                    os.remove(commandSent[1])
                    time.sleep(1)

                elif (justTheCommand == "STORE"):
                    print ("Client Requested: " + str(commandSent))
                    fileName = str(commandSent[1])
                    f = open(fileName,'ab') #open in binary
                    # receive data and write it to file
                    while True:
                        print('receiving data...')
                        data = conn.recv(1024)
                        print('data=%s', (data))
                        if not data:
                            break
                        
                        if data.decode()[-3:] == "EOF":
                            # write data to a file
                            temp = data.decode()
                            temp = temp[:-3]
                            data = temp.encode()
                            f.write(data)
                            f.close()
                            msg = "File successfully stored."
                            sendBack = msg.encode()
                            break
                        else:
                            f.write(data)
                    f.close()
                    
                elif (justTheCommand == "QUIT"):
                    print ("Client Requested QUIT")
                    msg = "Disconnecting from the server now."
                    sendBack = msg.encode()
                else:
                    print ("Command not recognized")
                    msg = "Command not recognized"
                    sendBack = msg.encode()
                    
                conn.sendall(sendBack)
    s.close()
    
print("Server closed.")


