import sys, threading
from queue import Queue

class Buffer:
    def __init__(self):
        self.buffer = []
    
    def write(self, text):
        self.buffer.append(str(text) + "\n")
    
    def flush(self):
        sys.stdout.write("\033[H\033[J")  # Clear screen
        sys.stdout.write("".join(self.buffer))
        sys.stdout.flush()
        self.buffer = []

    def clear(self):
        self.buffer = []