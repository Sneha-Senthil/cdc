Ricart-Agrawala algorithm:
ricarata.py:
import socket
import threading
import time
import sys

HOST = 'localhost'
NODES = {
    1: 9001,
    2: 9002,
    3: 9003
} # Available ports for accessing the critical section.

replies_needed = 0
replies_received = 0
requesting_cs = False
timestamp = 0
deferred_replies = []

my_id = int(sys.argv[1])
my_port = NODES[my_id]

lock = threading.Lock()

def send_message(to_port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, to_port))
        s.sendall(message.encode())

def listen():
    global replies_received, deferred_replies

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, my_port))
    server.listen()

    while True:
        conn, addr = server.accept()
        msg = conn.recv(1024).decode()
        conn.close()

        if msg.startswith("REQUEST"):
            _, req_ts, sender_id = msg.split()
            req_ts, sender_id = int(req_ts), int(sender_id)
            print(f"[{my_id}] Got REQUEST from {sender_id} (ts={req_ts})")

            def reply_later():
                time.sleep(2)
                send_message(NODES[sender_id], f"REPLY {my_id}")

            with lock:
                if not requesting_cs or (req_ts, sender_id) < (timestamp, my_id):
                    send_message(NODES[sender_id], f"REPLY {my_id}")
                else:
                    threading.Thread(target=reply_later).start()

        elif msg.startswith("REPLY"):
            with lock:
                replies_received += 1
                print(f"[{my_id}] Got REPLY → {replies_received}/{replies_needed}")

def request_cs():
    global timestamp, requesting_cs, replies_received, replies_needed

    timestamp = int(time.time())
    requesting_cs = True
    replies_received = 0
    replies_needed = len(NODES) - 1

    print(f"[{my_id}] Requesting CS at time {timestamp}")
    for pid, port in NODES.items():
        if pid != my_id:
            send_message(port, f"REQUEST {timestamp} {my_id}")

    # Wait until all replies are received
    while replies_received < replies_needed:
        time.sleep(0.1)

    print(f"[{my_id}] ENTERING CS")
    time.sleep(3)
    print(f"[{my_id}] EXITING CS")

    requesting_cs = False

# Start the listener thread
threading.Thread(target=listen, daemon=True).start()

# Main interaction loop
time.sleep(1)  # Give server some time to start
while True:
    inp = input(f"[{my_id}] Press Enter to request CS or type 'exit': ")
    if inp.strip().lower() == "exit":
        break
    request_cs()