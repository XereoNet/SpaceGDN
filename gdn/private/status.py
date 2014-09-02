class Status():
    def __init__(self):
        self.status = 'idle'

    def get(self):
        return self.status

    def set(self, status):
        self.status = status

status = Status()