import socket
import sys
import threading
import time
storage = {}
mutex = threading.Lock()
exit_flag = False

def std_handler(client_socket1):
    global exit_flag
    while True:
        inp = input("")
        if inp == "exit":
            exit_flag = True
            break
        if inp == "dictionary":
            message = "primary {"
            for i in sorted(list(storage.keys())):
                if i != max(sorted(list(storage.keys()))):
                    message  += str((i, storage[i])) + ", "
                else:
                    message  += str((i, storage[i]))

            message += "}, "
            message1 = "dictionary"
            client_socket1.send(message1.encode('utf-8'))
            response = client_socket1.recv(1024).decode('utf-8')
            time.sleep(3)
            message += response
            print(f"{message}", end="")
    sys.exit()

def response_behavior(client_socket, client_num, client_socket1):
    while not exit_flag:
        data = client_socket.recv(1024).decode('utf-8') # Receive one message from the client
        time.sleep(3)
        if data:
            #print(f"Cmd: {data}")
            splitData = data.split()
            if int(splitData[1])%2 == 1:
                if splitData[0] == "insert":
                    storage[int(splitData[1])] = int(splitData[2])
                    print(f"Successfully inserted key {splitData[1]}")
                    client_response = "Success"
                elif splitData[0] == "lookup":
                    if int(splitData[1]) in storage:
                        print(f"{str(storage[int(splitData[1])])}") 
                        client_response = f"{str(storage[int(splitData[1])])}"
                    else:
                        print("NOT FOUND")
                        client_response = "NOT FOUND"
                else:
                    client_response = "wtf bro"
                client_socket.send(f"{client_response}".encode('utf-8')) # Echo the message back to the client

            else:
                print("Forwarding to secondary server")
                message = data + " " + str(client_num)
                client_socket1.send(message.encode('utf-8')) # Send the message to the server
                #response = client_socket1.recv(1024).decode('utf-8') # Receive the echo from the server
                #print(f"{response}")
                client_socket.send(f"forward".encode('utf-8')) # Echo the message back to the client
        if exit_flag:
            break
    client_socket.close() # Close the connection after echoing



def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 9000)) # specify host (itself) and port number 9999
    server_socket.listen(5)
    server_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket1.bind(('127.0.0.1', 9002)) # specify host (itself) and port number 9999
    server_socket1.listen(5)
    server_socket2 = socket.socket(socket.AF_INET,
    socket.SOCK_STREAM)
    server_socket2.bind(('127.0.0.1', 9004)) # Connect to the localhost server at port 9999
    server_socket2.listen(5)
    global exit_flag
    

    
    
    while True:
        if exit_flag == True:
            print("test")
            break
        client_socket1, client_address = server_socket2.accept()
    
        std_handler1 = threading.Thread(target = std_handler, args = (client_socket1,))
        std_handler1.daemon = True
        std_handler1.start()
        client_socket, client_address = server_socket.accept()
        client_handler = threading.Thread(target = response_behavior, args = (client_socket, 1, client_socket1))
        client_handler.daemon = True
        client_handler.start()
        client_socket11, client_address1 = server_socket1.accept()
        client_handler1 = threading.Thread(target = response_behavior, args = (client_socket11, 2, client_socket1))
        client_handler1.daemon = True
        client_handler1.start()
        

        
    #print("closing")
    exit_flag = True
    server_socket.close()
    sys.exit()
    
if __name__ == "__main__":
    start_server()
