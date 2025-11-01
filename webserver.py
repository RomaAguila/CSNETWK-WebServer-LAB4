# webserver.py

from socket import *
import sys  # for exiting the program

# Step 1: Create a TCP socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# Step 2: Bind the socket to a port (door)
serverPort = 6789  # you can change this if you need to
serverSocket.bind(('', serverPort))  # '' means accept connections from any IP
serverSocket.listen(1)  # allow 1 connection at a time (for now)

print("Server is ready to serve...")

while True:
    # Step 3: Wait for a connection from a client (like a browser)
    connectionSocket, addr = serverSocket.accept()
    print("Connection from:", addr)

    try:
        # Step 4: Receive the HTTP request from the client
        message = connectionSocket.recv(1024).decode()
        print("Received message:", message)

        # Step 5: Parse the file name from the request
        filename = message.split()[1]
        print("Requested file:", filename)

        # Step 6: Open the requested file
        f = open(filename[1:])  # remove the '/' from the start
        outputdata = f.read()

        # Step 7: Send HTTP header (tells the browser the request was successful)
        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())

        # Step 8: Send the file content
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())

        # Step 9: Send an extra newline to mark end of message
        connectionSocket.send("\r\n".encode())

        # Step 10: Close the connection
        connectionSocket.close()

    except IOError:
        # Step 11: If file not found, send 404 response
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        connectionSocket.send("<html><body><h1>404 Not Found</h1></body></html>\r\n".encode())
        connectionSocket.close()

# Step 12: Close server socket (this line will actually never be reached)
serverSocket.close()
sys.exit()
Web