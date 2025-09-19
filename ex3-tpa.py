import threading, queue, time, random

N = 4  # number of processes in the ring
lock = threading.Lock()

def log(pid, msg):
    with lock:
        print(f"[{time.strftime('%H:%M:%S')}] P{pid}: {msg}")

class Process(threading.Thread):
    def __init__(self, pid, inbox, outbox):
        super().__init__(daemon=True)
        self.pid = pid
        self.inbox = inbox   # queue to receive token (or messages)
        self.outbox = outbox # queue of next process
        self.want_cs = False

    def run(self):
        while True:
            # random time before wanting CS
            time.sleep(random.uniform(2, 6))
            self.want_cs = True
            log(self.pid, "Wants CS (will wait for token)")

            # wait for token/message
            while True:
                try:
                    token = self.inbox.get(timeout=0.5)
                except queue.Empty:
                    continue
                # token is a dict; token['holder'] is pid that holds it now
                if token.get("type") == "TOKEN":
                    # we hold token
                    log(self.pid, "Received TOKEN")
                    if self.want_cs:
                        log(self.pid, "*** ENTER CS ***")
                        time.sleep(1)  # in critical section
                        log(self.pid, "*** EXIT  CS ***")
                        self.want_cs = False
                    # pass token to next
                    self.outbox.put({"type": "TOKEN"})
                    log(self.pid, "Passed TOKEN to next")
                    break
                else:
                    # ignore unknown messages
                    pass

def main():
    # create ring of queues
    queues = [queue.Queue() for _ in range(N)]
    procs = []
    for i in range(N):
        out = queues[(i+1) % N]
        p = Process(i, queues[i], out)
        procs.append(p)
    for p in procs:
        p.start()

    # inject initial token into process 0
    queues[0].put({"type": "TOKEN"})
    log("MAIN", "Initial TOKEN injected to P0")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopped.")

if __name__ == "__main__":
    main()
