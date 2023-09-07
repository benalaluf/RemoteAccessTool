import threading
import time

niga = threading.Lock()


p = niga.acquire(timeout=5)

while True:
    print(p, time.perf_counter())