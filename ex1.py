# ================== EX1 - IPC ====================
# data_object.py:
class DataObject:
    def __init__(self, values):
        self.values = values

# server.py:
import socket
import pickle
from data_object import DataObject

HOST = '127.0.0.1'
PORT = 8044

# Create server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"<SERVER> Listening on {HOST}:{PORT}")

conn, addr = server_socket.accept()
print(f"<SERVER> Connected by {addr}")

while True:
    raw_data = conn.recv(1024) # receive raw data

    data = pickle.loads(raw_data)

    if isinstance(data, str):
        conn.send("Connection Terminated..".encode())
        conn.close()
        print("<SERVER> Connection Terminated...")
        break

    print(f"<SERVER> Received: {data.values}")

    total = str(sum(data.values))

    conn.send(total.encode())


server_socket.close()

# client.py:
import socket
import pickle
from data_object import DataObject

HOST = '127.0.0.1'
PORT = 8044

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

print("<CLIENT> Connected to Server.")

values = [1, 2, 3, 4, 5, 6, 7, 8]
obj = DataObject(values=values)

# Send the serialized object
raw_data = pickle.dumps(obj)
client_socket.send(raw_data)

# Receive Response
total_value = client_socket.recv(1024).decode()
print(f"<SERVER> Response from server: {total_value}")

exit_msg = "exit"
raw_exit = pickle.dumps(exit_msg)
response = client_socket.send(raw_exit)
print(f"<SERVER> {response}")

client_socket.close()
