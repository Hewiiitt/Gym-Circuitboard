class Trace:

    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.path = []

    def add(self, location):
        self.path.append(location)

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

    def get_path(self):
        return self.start, self.end, self.path
