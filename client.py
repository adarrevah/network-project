import socket
import threading

SERVER_IP = '127.0.0.1'
PORT = 5555

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, PORT))

username = input("enter your username: ")
client_socket.send(username.encode('utf-8'))

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            
            if message:
                print(f"\n{message}")
                print("enter message (recipient:message): ", end="")
            
            else:
                break
        
        except:
            print("the connection to the server was lost.")
            client_socket.close()
            break

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()
print("you are connected to the chat! to send a message, use the format: recipient:message")

while True:
    msg = input("enter message (recipient:message): ")

    if msg:
        client_socket.send(msg.encode('utf-8'))