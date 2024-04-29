import time


class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


class Timeout(Singleton):
    alpha = 0.25
    beta = 0.3

    def __init__(self):
        self.start = None
        self.end = None
        self.rtt = None
        self.dev_rtt = None

    def register_start(self):
        self.start = time.time()

    def register_end(self):
        self.end = time.time()
        duration = self.end - self.start
        self.update_rtt(duration)
        self.update_dev_rtt(duration)

    def update_rtt(self, sample):
        if self.rtt is None:
            self.rtt = sample
            return
        self.rtt = (1-self.alpha) * self.rtt + self.alpha * sample

    def update_dev_rtt(self, sample):
        if self.dev_rtt is None:
            self.dev_rtt = 0.25 * self.rtt
        self.dev_rtt = (1-self.beta)*self.dev_rtt + self.beta*abs(self.rtt - sample)

    def get_timeout(self):
        if self.rtt is None:
            return 2
        return self.rtt + 4 * self.dev_rtt
