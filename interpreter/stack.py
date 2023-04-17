import sys

# Třída implementující strukturu zásobníku k uchovávání rámců
class Stack:
    def __init__(self):
        self.frames = []

    # @brief vložení hodnoty do seznamu rámců
    # @param frame rámec
    def push(self, frame):
        self.frames.append(frame)

    # @brief vrátí poslední rámec ze zásobníku
    def pop(self):
        popped = self.frames.pop()
        return popped

    # @brief vrátí hodnotu proměnné
    # @param name název proměnné
    def get_variable(self, name):
        for frame in reversed(self.frames):
            value = frame.get_variable(name)
            return value

    # @brief vrátí počet uchováváných rámců
    def length(self):
        return len(self.frames)

    # @brief nastaví hodnotu existující proměnné v rámci
    # @param name název proměnné
    # @param value nová hodnota proměnné
    # @type_t nový typ proměnné
    def set_variable(self, name, value, type_t=None):
        for frame in reversed(self.frames):
            if frame.get_variable(name) is not None:
                frame.set_variable(name, value, type_t=type_t)
                return
        print(f"[chyba] proměnná {name} není definována", file=sys.stderr)
        exit(54)

    # @brief navrátí hodnotu z posledního rámce
    # @param name název proměné
    def get_variable_from_last_frame(self, name):
        return self.frames[-1].get_variable(name)

    # @brief nastaví hodnotu proměnné v posledním rámci
    # @param name název proměnné
    # @param value nová hodnota proměnné
    def set_variable_from_last_frame(self, name, value):
        self.frames[-1].set_variable(name, value)

    # @brief zjistí, zda je zásobník prázdný
    def isEmpty(self):
        if len(self.frames) == 0:
            return True
        return False
