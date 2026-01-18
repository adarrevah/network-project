import socket
import threading


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"


SERVER_IP_TO_SHOW = get_local_ip()
BIND_IP = '0.0.0.0'
PORT = 5555

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((BIND_IP, PORT))
server_socket.listen(5)
clients = {}

def start_server():
    print(f"thr server listening to {SERVER_IP_TO_SHOW}:{PORT}...")
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"new connection from {client_address}")

        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

        print(f"number of active clients: {threading.active_count() - 1}")

def handle_client(client_socket):
    username = ""
    try:
        temp_name = client_socket.recv(1024).decode('utf-8')

        if temp_name in clients:
            client_socket.send(
                "System: Username already taken. Please reconnect with a different name.".encode('utf-8'))
            client_socket.close()
            return

        username = temp_name
        clients[username] = client_socket
        client_socket.send("Welcome to the chat!".encode('utf-8'))
        print(f"the user {username} successfully connected.")

        connect_msg = f"System: User {username} has connected."
        for name, socket_obj in clients.items():
            if name != username:
                try:
                    socket_obj.send(connect_msg.encode('utf-8'))
                    print(f"notifing {name} about user connect...")
                except:
                    print(f"exeption at notifing {name} about user connect...")
                    pass


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
            else:
                client_socket.send("Server: Invalid format. Please use recipient:message".encode('utf-8'))
    except:
        pass
    finally:
        if username and username in clients:
            del clients[username]
            print(f"The user {username} has disconnected.")

            disconnect_msg = f"System: User {username} has disconnected."
            for name, socket_obj in clients.items():
                try:
                    socket_obj.send(disconnect_msg.encode('utf-8'))
                except:
                    pass

        try:
            client_socket.close()
        except:
            pass
        print(f"Active clients remaining: {len(clients)}")
start_server()
import socket
import threading


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"


SERVER_IP_TO_SHOW = get_local_ip()
BIND_IP = '0.0.0.0'
PORT = 5555

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((BIND_IP, PORT))
server_socket.listen(5)
clients = {}

def start_server():
    print(f"thr server listening to {SERVER_IP_TO_SHOW}:{PORT}...")
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"new connection from {client_address}")

        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

        print(f"number of active clients: {threading.active_count() - 1}")

def handle_client(client_socket):
    username = ""
    try:
        temp_name = client_socket.recv(1024).decode('utf-8')

        if temp_name in clients:
            client_socket.send(
                "System: Username already taken. Please reconnect with a different name.".encode('utf-8'))
            client_socket.close()
            return

        username = temp_name
        clients[username] = client_socket
        client_socket.send("Welcome to the chat!".encode('utf-8'))
        print(f"the user {username} successfully connected.")

        connect_msg = f"System: User {username} has connected."
        for name, socket_obj in clients.items():
            if name != username:
                try:
                    socket_obj.send(connect_msg.encode('utf-8'))
                    print(f"notifing {name} about user connect...")
                except:
                    print(f"exeption at notifing {name} about user connect...")
                    pass


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
            else:
                client_socket.send("Server: Invalid format. Please use recipient:message".encode('utf-8'))
    except:
        pass
    finally:
        if username and username in clients:
            del clients[username]
            print(f"The user {username} has disconnected.")

            disconnect_msg = f"System: User {username} has disconnected."
            for name, socket_obj in clients.items():
                try:
                    socket_obj.send(disconnect_msg.encode('utf-8'))
                except:
                    pass

        try:
            client_socket.close()
        except:
            pass
        print(f"Active clients remaining: {len(clients)}")
start_server()
