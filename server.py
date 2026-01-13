import socket
import threading
IP = '127.0.0.1'
PORT = 5555

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((IP, PORT))
server_socket.listen(5)
clients = {}

def start_server():
    print(f"thr server listening to {IP}:{PORT}...")
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"new connection from {client_address}")

        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

        print(f"number of active clients: {threading.active_count() - 1}")

def handle_client(client_socket):
    try:
        username = client_socket.recv(1024).decode('utf-8')
        clients[username] = client_socket
        print(f"the user {username} successfully connected.")

        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            
            if ":" in data:
                target_user, message = data.split(":", 1)
                
                if target_user in clients:
                    recipient_socket = clients[target_user]
                    full_message = f"message from {username}: {message}"
                    recipient_socket.send(full_message.encode('utf-8'))
                
                else:
                    client_socket.send(f"the user {target_user} is not connected.".encode('utf-8'))

    except:
        pass
    finally:
        if username in clients:
            del clients[username]

        client_socket.close()
        print(f"the connection with {username} has ended.")
        
start_server()
