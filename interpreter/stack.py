import sys


class Stack:
    def __init__(self):
        self.frames = []

    def push(self, frame):
        self.frames.append(frame)

    def pop(self):
        popped = self.frames.pop()
        return popped

    def get_variable(self, name):
        for frame in reversed(self.frames):
            value = frame.get_variable(name)
            return value

    def length(self):
        return len(self.frames)

    def set_variable(self, name, value, type_t=None):
        for frame in reversed(self.frames):
            if frame.get_variable(name) is not None:
                frame.set_variable(name, value, type_t=type_t)
                return
        print(f"[chyba] proměnná {name} není definována", file=sys.stderr)
        exit(54)

    def get_variable_from_last_frame(self, name):
        return self.frames[-1].get_variable(name)

    def set_variable_from_last_frame(self, name, value):
        self.frames[-1].set_variable(name, value)

    def isEmpty(self):
        if len(self.frames) == 0:
            return True
        return False
