import socket
import sys
import threading


PORT = 5555

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "127.0.0.1"



detected_ip = get_local_ip()
print(f"Detected local IP: {detected_ip}")
server_ip_input = input(f"Enter Server IP (press Enter to use {detected_ip}): ")

if server_ip_input == "":
    SERVER_IP = detected_ip
else:
    SERVER_IP = server_ip_input


try:
    print(f"Connecting to {SERVER_IP}:{PORT}...")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, PORT))
except:
    print(f"Could not connect to server at {SERVER_IP}.")
    sys.exit()

username = input("enter your username: ")
client_socket.send(username.encode('utf-8'))

try:
    response = client_socket.recv(1024).decode('utf-8')

    if "already taken" in response:
        print(f"\nError: {response}")
        client_socket.close()
        sys.exit()
    else:
        print(f"\n{response}")

except ConnectionResetError:
    print("Connection closed by server.")
    sys.exit()



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