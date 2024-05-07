import threading
import queue

candado = threading.Lock()
cola = queue.Queue()
