
Task 1 – Message Passing System:
Server.py:
import socket
import threading

HOST = "127.0.0.1"
PORT = 8000

clients = []

def handle_client(client_socket, addr):
    print(f"<Connected> {addr} connected.")

    while 1:
        data = client_socket.recv(1024).decode()
        print(f"<{addr}> {data}")

        if data.lower() == "bye":
            break

        # Broadcast to other clients.
        for c in clients:
            if c != client_socket:
                c.send(f"<{addr}> {data}".encode())
    
    print(f"<Disconnected> {addr} disconnected.")
    clients.remove(client_socket)
    client_socket.close()

# Driver Code!
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print(f"<server> Server listening {HOST} in {PORT}")

while 1:
    client_socket, addr = server.accept()
    clients.append(client_socket)

    thread = threading.Thread(target = handle_client, args=(client_socket, addr))
    thread.start()

Client.py:
import socket
import threading

HOST = 'localhost'
PORT = 8000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
print("<CONNECTED> to server.")

# Define a thread to simultaneously handle sending and receiving messages
def receive_messages(client):
    data = client.recv(1024).decode()
    print(f"<client> Received from Server {data}")

threading.Thread(target = receive_messages, args = (client,)).start()

while True:
    msg = input("Enter message to send to server: ")
    client.send(msg.encode())

    if msg.lower() == "bye":
        break

client.close()