import socket
import sys
import time

def start_client():
    client_socket1 = socket.socket(socket.AF_INET,
    socket.SOCK_STREAM)
    client_socket1.connect(('127.0.0.1', 9000)) # Connect to the localhost server at port 9999
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 9001)) # specify host (itself) and port number 9999

    while True:
        message = input("")
        if message == "exit":
            break
        client_socket1.send(message.encode('utf-8')) # Send the message to the server
        response = client_socket1.recv(1024).decode('utf-8') # Receive the echo from the server
        if response != "forward":
            time.sleep(3)
            print(f"{response}")
        else:
            data = client_socket.recv(1024).decode('utf-8') # Receive one message from the client
            time.sleep(3)
            print(f"{data}")
    #print("closing")
    sys.exit()


if __name__ == "__main__":
    start_client()