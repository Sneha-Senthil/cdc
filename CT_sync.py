Clock and Time Synchronization

server.py

import socket
from datetime import datetime, timezone, timedelta

IST = timezone(timedelta(hours=5, minutes=30))

HOST = '127.0.0.1' 
PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))    
    s.listen()                   
    print(f"Time Server (IST) listening on {HOST}:{PORT}...")

    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")

            data = conn.recv(1024)
            if not data:
                break

            server_time = datetime.now(IST).timestamp()

            conn.sendall(str(server_time).encode('utf-8'))

            formatted = datetime.fromtimestamp(server_time, IST).strftime("%d-%m-%Y %H:%M:%S %p %Z")
            print(f"Sent server IST time: {formatted}")


client.py

import socket
from datetime import datetime, timezone, timedelta

# Define IST timezone
IST = timezone(timedelta(hours=5, minutes=30))

HOST = '127.0.0.1'
PORT = 12345

# Record t1: client send time (IST)
t1 = datetime.now(IST).timestamp()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"Requesting time")
    data = s.recv(1024)

# Record t4: client receive time (IST)
t4 = datetime.now(IST).timestamp()

server_time = float(data.decode('utf-8'))

# Cristian’s algorithm for clock offset
offset = ((server_time + (t4 - t1) / 2) - t4)

print(f"Client send time (t1): {t1}")
print(f"Server time received : {server_time}")
print(f"Client recv time (t4): {t4}")
print(f"Estimated clock offset: {offset:.6f} seconds")

# Adjusted synchronized time in IST
adjusted_time = datetime.fromtimestamp(t4 + offset, IST)
formatted_time = adjusted_time.strftime("%d-%m-%Y %I:%M:%S %p %Z")

print(f"Synchronized client time (IST): {formatted_time}")
