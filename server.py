import socket
import threading
import os

HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", 55555))  # Railway gives us a random port

clients = []

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                clients.remove(client)

def handle_client(client_socket, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            print(f"{addr}: {message.decode()}")
            broadcast(message, client_socket)
        except:
            break
    print(f"[DISCONNECT] {addr} disconnected.")
    clients.remove(client_socket)
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[STARTED] Server running on {HOST}:{PORT}")
    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
