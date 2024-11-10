import socket
import sys
import threading
import time
storage = {}
exit_flag = False
#def response_behavior(client_socket):
    #while True:
        #if input("") == "exit":
        #    client_socket.close()
        #    sys.exit()
        #    break
def std_handler():
    global exit_flag
    while True:
        if input("") == "exit":
            exit_flag=True
            break
    sys.exit()


def thread_handler(client_socket, client_socket1, client_socket2):
    #print(f"Connection from {client_address}")
    while not exit_flag:
        data = ""
        try:
            data = client_socket.recv(1024).decode('utf-8') # Receive one message from the client
        except ConnectionResetError:
            data = ""
        time.sleep(3)
        if data:
            splitData = data.split()
            message = splitData[0]
            if splitData[0] != "dictionary":
                for i in range(len(splitData)):
                    if i < len(splitData)-2:
                        message += " " + splitData[i+1]
                #print(f"{message}")
            if splitData[0] == "dictionary":
                message = "secondary {"
                for i in sorted(list(storage.keys())):
                    if i != max(sorted(list(storage.keys()))):
                        message  += str((i, storage[i])) + ", "
                    else:
                        message  += str((i, storage[i]))
                
                message += "}\n"
                client_response = message
                client_socket3 = client_socket
            elif splitData[0] == "insert":
                storage[int(splitData[1])] = int(splitData[2])
                print(f"Successfully inserted key {splitData[1]}")
                client_response = "Success"
                if splitData[3] == "1":
                    client_socket3 = client_socket1
                else:
                    client_socket3 = client_socket2
            elif splitData[0] == "lookup":
                if int(splitData[1]) in storage:
                    print(f"{str(storage[int(splitData[1])])}") 
                    client_response = f"{str(storage[int(splitData[1])])}"
                else:
                    print("NOT FOUND")
                    client_response = "NOT FOUND"
                if splitData[2] == "1":
                    client_socket3 = client_socket1
                else:
                    client_socket3 = client_socket2
            else:
                client_response = "wtf bro"
            client_socket3.send(f"{client_response}".encode('utf-8')) # Echo the message back to the client
        if exit_flag:
            break

def start_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 9004)) # specify host (itself) and port number 9999
    server_socket1 = socket.socket(socket.AF_INET,
    socket.SOCK_STREAM)
    server_socket1.bind(('127.0.0.1', 9001)) # Connect to the localhost server at port 9999
    server_socket1.listen(5)
    server_socket2 = socket.socket(socket.AF_INET,
    socket.SOCK_STREAM)
    server_socket2.bind(('127.0.0.1', 9003)) # Connect to the localhost server at port 9999
    server_socket2.listen(5)

    global exit_flag
    #print("Server is listening on port 9999...")
    #print("Hostname: " + socket.gethostname())
    
    std_handler1 = threading.Thread(target = std_handler, args = ())
    std_handler1.daemon = True
    std_handler1.start()

    while True:
        client_socket1, clientaddr = server_socket1.accept()
        client_socket2, clientaddr = server_socket2.accept()
        handler = threading.Thread(target = thread_handler, args = (client_socket, client_socket1, client_socket2))
        handler.daemon = True
        handler.start()
        if exit_flag == True:
            break

    #print("closing")
    sys.exit()
        
    
if __name__ == "__main__":
    start_server()
