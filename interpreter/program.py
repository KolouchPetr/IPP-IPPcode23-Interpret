from frame import *
from stack import *
from regex import *
import sys

# třída Program slouží k uchování informací o běhu programu
# a implementaci k tomu sloužících metod
class Program:
    def __init__(self):
        self.labels = []
        self.globalFrame = Frame()
        self.programCounter = 0
        self.callStack = Stack()
        self.dataStack = Stack()
        self.localFrames = None
        self.tempFrame = None

    # @brief metoda přidává nové návěští
    # @param newLabel návěští
    def appendLabels(self, newLabel):
        for label in self.labels:
            if label.get("name") == newLabel.get("name"):
                print(f"[Chyba] redefinice návěští {label}", file=sys.stderr)
                exit(52)
        self.labels.append(newLabel)

    # @brief metoda kontroluje, zda existuje návěští, a je tedy možné na něj skočit
    # @param searchLabel hledané návěští 
    def labelExists(self, searchLabel):
        for label in self.labels:
            if label.get("name") == searchLabel:
                return label
        print(f"[chyba] návěští {searchLabel} není definováno", file=sys.stderr)
        exit(52)

    # @brief metoda vloží hodnotu na vrchol zásobníku volání
    # @param value hodnota na vložení
    def pushProgramStack(self, value):
        self.callStack.push(value)

    # @brief vrátí hodnotu z vrcholu zásobníku volání
    def popProgramStack(self):
        if self.callStack.isEmpty():
            print(f"[chyba] zásobník volání je prázdný", file=sys.stderr)
            exit(56)
        return self.callStack.pop()

    # @brief vrátí hodnotu programového čítače
    def getProgramCounter(self):
        return self.programCounter

    # @brief nastaví hodnotu programového čítače
    # @param value nová hodnota programového čítače
    def setProgramCounter(self, value):
        self.programCounter = value

    # @brief vrátí globální rámec
    def getGlobalFrame(self):
        return self.globalFrame

    # @brief vrátí lokální rámec
    def getLocalFrames(self):
        return self.localFrames

    # @brief vrátí dočasný rámec
    def getTempFrame(self):
        return self.tempFrame

    # @brief nastaví hodnotu globálního rámce
    # @brief value nová hodnota globálního rámce
    def setGlobalFrame(self, value):
        self.globalFrame = value

    # @brief nastaví hodnotu lokálního rámce
    # @param value nová hodnota lokálního rámce
    def setLocalFrames(self, value):
        self.localFrames = value

    # @brief nastaví hodnotu dočasného rámce
    # @param value nová hodnota dočasného rámce
    def setTempFrame(self, value):
        self.tempFrame = value

    # @brief vrátí hodnotu datového zásobníku
    def getDataStack(self):
        return self.dataStack

    # @brief dle hodnoty určujcí rámec proměnné, zavolá metodu daného rámce
    # pro nastavení hodnoty proměnné
    # @param variable název proměnné
    # @param value nová hodnota proměnné
    # @param type_t typ nové hodnoty
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

    # @brief vrátí proměnnou ze specifického rámce
    # @brief variable proměnná obsahující rámec a název proměnné
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
