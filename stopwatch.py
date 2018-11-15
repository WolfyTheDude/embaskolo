
import time

class StopWatch:
    def __init__(self):
        self.start_time = time.time()
        self.end_time = 0

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.end_time = time.time()
        return self.end_time - self.start_time

    def runtime(self):
        return time.time() - self.start_time

    def get_time(self):
        return self.end_time - self.start_time
