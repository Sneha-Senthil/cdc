Token Passing Algorithm:

token-passing.py:
import socket
import threading
import time
import sys

class TokenRingNode:
    def __init__(self, port, next_host, next_port, has_token=False, request_cs=False):
        self.port = port
        self.next_host = next_host
        self.next_port = next_port
        self.has_token = has_token
        self.request_cs = request_cs
        self.running = True

    def listen(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('localhost', self.port))
        server.listen(5)
        print(f"[{self.port}] Listening for token...")

        while self.running:
            conn, _ = server.accept()
            token = conn.recv(1024).decode()
            conn.close()

            if token == "TOKEN":
                print(f"[{self.port}] Token received")
                self.has_token = True
                if self.request_cs:
                    self.enter_critical_section()
                self.send_token()
            time.sleep(1)

    def send_token(self):
        if self.has_token:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((self.next_host, self.next_port))
                s.send("TOKEN".encode())
                s.close()
                print(f"[{self.port}] Token passed to {self.next_port}")
                self.has_token = False
            except:
                print(f"[{self.port}] Failed to send token")

    def enter_critical_section(self):
        print(f"[{self.port}] >>> Entering critical section...")
        time.sleep(3)
        print(f"[{self.port}] <<< Exiting critical section...")
        self.request_cs = False

    def start(self):
        t = threading.Thread(target=self.listen)
        t.start()

        if self.has_token and self.request_cs:
            self.enter_critical_section()
            self.send_token()

        while self.running:
            user_input = input(f"[{self.port}] Type 'request' to enter CS or 'exit' to quit: ").strip()
            if user_input == 'request':
                self.request_cs = True
            elif user_input == 'exit':
                self.running = False
                break

        print(f"[{self.port}] Shutting down...")

if __name__ == "__main__":
    port = int(sys.argv[1])
    next_port = int(sys.argv[2])
    has_token = request_cs = False
    if len(sys.argv) > 3:
        has_token = (sys.argv[3] == "yes")
        request_cs = (sys.argv[4] == "yes")

    node = TokenRingNode(port, 'localhost', next_port, has_token, request_cs)
    node.start()