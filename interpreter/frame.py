from regex import *

# Třída Frame slouží pro reprezentaci rámce, jež uchovává proměnné
class Frame:
    def __init__(self):
        self.variables = []

    # @brief metoda navrací proměnnou dle jména
    # pokud neexistuje, je navrácena hodnota None
    # @param name jméno hledané proměnné
    def get_variable(self, name):
        variable = None
        for d in self.variables:
            if d.get("name") == name:
                variable = d
                break
        return variable

    # @brief metoda aktualizuje hodnotu existující proměnné nebo tvoří novou
    # @param name jméno proměnné
    # @param value hodnota proměnné
    # @param type_t typ proměnné, pokud je předem určen
    def set_variable(self, name, value, type_t=None):
        # pokud není typ nastaven, určí se dle hodnoty
        if type_t != None or value != "":
            if Regex.isNumber(value):
                type_t = "int"
            elif Regex.isBool(value):
                type_t = "bool"
            elif Regex.isNil(value):
                type_t = "nil"
            else:
                type_t = "string"

        variable = self.get_variable(name)
        if variable:
            variable["value"] = value
            variable["type"] = type_t
        else:
            self.variables.append({"name": name, "value": value, "type": type_t})

    # @brief tisk proměnných v rámci
    def print_frame(self):
        print(self.variables)
