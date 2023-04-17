from frame import *
from stack import *
from regex import *
import sys


class Program:
    def __init__(self):
        self.labels = []
        self.globalFrame = Frame()
        self.programCounter = 0
        self.callStack = Stack()
        self.dataStack = Stack()
        self.localFrames = None
        self.tempFrame = None

    def appendLabels(self, newLabel):
        for label in self.labels:
            if label.get("name") == newLabel.get("name"):
                print(f"[Chyba] redefinice návěští {label}", file=sys.stderr)
                exit(52)
        self.labels.append(newLabel)

    def labelExists(self, searchLabel):
        for label in self.labels:
            if label.get("name") == searchLabel:
                return label
        print(f"[chyba] návěští {searchLabel} není definováno", file=sys.stderr)
        exit(52)

    def pushProgramStack(self, value):
        self.callStack.push(value)

    def popProgramStack(self):
        if self.callStack.isEmpty():
            print(f"[chyba] zásobník volání je prázdný", file=sys.stderr)
            exit(56)
        return self.callStack.pop()

    def getProgramCounter(self):
        return self.programCounter

    def setProgramCounter(self, value):
        self.programCounter = value

    def getGlobalFrame(self):
        return self.globalFrame

    def getLocalFrames(self):
        return self.localFrames

    def getTempFrame(self):
        return self.tempFrame

    def set_variable(self, variable, value, type_t=None):
        frame = variable.get("frame")
        variable = variable.get("value")
        if frame == "GF":
            self.globalFrame.set_variable(variable, value, type_t=type_t)
        elif frame == "LF":
            if self.localFrames != None:
                self.localFrames.set_variable(variable, value, type_t=type_t)
        elif frame == "TF":
            if self.tempFrame != None:
                self.tempFrame.set_variable(variable, value, type_t=type_t)

    def get_variable(self, variable):
        frame = variable.get("frame")

        variable = variable.get("value")
        if frame == "GF":
            return self.globalFrame.get_variable(variable)
        elif frame == "LF":
            if self.localFrames == None:
                print("[chyba] rámec neexistuje", file=sys.stderr)
                exit(55)
            return self.localFrames.get_variable(variable)
        elif frame == "TF":
            if self.tempFrame == None:
                print("[chyba] rámec neexistuje", file=sys.stderr)
                exit(55)
            return self.tempFrame.get_variable(variable)
