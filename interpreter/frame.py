from regex import *


class Frame:
    def __init__(self):
        self.variables = []

    def get_variable(self, name):
        variable = None
        for d in self.variables:
            if d.get("name") == name:
                variable = d
                break
        return variable

    def set_variable(self, name, value, type_t=None):
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

    def print_frame(self):
        print(self.variables)
