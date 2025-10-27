import socket
import threading

clients = []
client_ids = {}   # Map socket to client ID
client_count = 0  # Incremental ID counter

def handle_client(client_socket):
    client_id = client_ids[client_socket]
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            formatted_message = f"{client_id}: {message}"
            print(formatted_message)
            broadcast(formatted_message, client_socket)
        except:
            print(f"{client_id} disconnected.")
            clients.remove(client_socket)
            del client_ids[client_socket]
            client_socket.close()
            break

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            client.send(message.encode())

def main():
    global client_count
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 12345))
    server.listen(5)
    print("Server listening on port 12345...")

    while True:
        client_socket, addr = server.accept()
        client_count += 1
        client_id = f"Client-{client_count} (socket-{client_socket.fileno()})"
        client_ids[client_socket] = client_id
        clients.append(client_socket)
        print(f"Connected to {addr} as {client_id}")
        client_socket.send(f"You are connected as {client_id}".encode())

        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    main()
