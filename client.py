import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print("\n" + message)
        except:
            print("Disconnected from server.")
            client_socket.close()
            break

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 12345))

    threading.Thread(target=receive_messages, args=(client,)).start()

    while True:
        message = input("")
        client.send(message.encode())

if __name__ == "__main__":
    main()
