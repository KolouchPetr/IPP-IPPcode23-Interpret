from frame import *
from stack import *
from regex import Regex
import sys
import copy


def checkArgumentCount(argTypes, arguments, class_name):
    expectedArgLen = len(argTypes)
    argLen = len(arguments)
    if expectedArgLen != argLen:
        raise ValueError(
            f"[Chyba] instrukce {class_name} ocekavala {expectedArgLen}, ale dostala {argLen} argumentu!"
        )


class Instructions:
    def __init__(self, program):
        self.program = program
        self.types = {
            "MOVE": ["var", "symb"],
            "POPS": ["var"],
            "ADD": ["var", "int", "int"],
            "SUB": ["var", "int", "int"],
            "MUL": ["var", "int", "int"],
            "IDIV": ["var", "int", "int"],
            "LT": ["var", "symb", "symb"],
            "GT": ["var", "symb", "symb"],
            "EQ": ["var", "symb", "symb"],
            "AND": ["var", "bool", "bool"],
            "OR": ["var", "bool", "bool"],
            "NOT": ["var", "bool"],
            "INT2CHAR": ["var", "int"],
            "STRI2INT": ["var", "string", "int"],
            "CONCAT": ["var", "string", "string"],
            "STRLEN": ["var", "string"],
            "GETCHAR": ["var", "string", "int"],
            "SETCHAR": ["var", "int", "string"],
            "TYPE": ["var", "symb"],
            "READ": ["var", "type"],
        }

    def checkTypes(self, instruction, args):
        types = self.types[instruction]
        for i in range(len(types)):
            if types[i] == "symb":
                continue
            elif types[i] == "type":
                value = args[i].get("value")
                possibleTypes = ["int", "string", "bool"]
                if value not in possibleTypes:
                    print("[chyba] typ neni v typech", file=sys.stderr)
                    exit(57)

            elif types[i] == "var":
                if args[i].get("type") != "var":
                    print(
                        f"[chyba] instrukce {instruction} dostala špatné typy argumentů",
                        file=sys.stderr,
                    )
                    exit(53)
                if self.program.get_variable(args[i]) == None:
                    print("[chyba] proměnná není definována", file=sys.stderr)
                    exit(54)

            else:
                argType = self.getValue(args[i], "type")
                if argType != types[i]:
                    print(
                        f"[chyba] instrukce {instruction} dostala špatné typy argumentů",
                        file=sys.stderr,
                    )
                    exit(53)

    def getValue(self, arg, value):
        if arg.get("type") == "var":
            variable = self.program.get_variable(arg)
            if variable == None:
                print(f"[chyba] proměnná arg není definována", file=sys.stderr)
                exit(54)
            value = variable.get(value)
            if variable.get("type") == None:
                print(f"proměnná {variable} nemá definovanou hodnotu", file=sys.stderr)
                exit(56)
            return value
        return arg.get(value)

    def checkNumericValues(self, args):
        arg1Type = self.getValue(args[1], "type")
        arg2Type = self.getValue(args[2], "type")
        arg1Value = self.getValue(args[1], "value")
        arg2Value = self.getValue(args[2], "value")

        if arg1Type != "int" or arg2Type != "int":
            print("[chyba] nečíselná hodnota v numerické instrukci", file=sys.stderr)
            exit(53)
        if (not self.isNumber(arg1Value)) or (not self.isNumber(arg2Value)):
            print("[chyba] nečíselná hodnota v numerické instrukci", file=sys.stderr)
            exit(54)

        return

    def checkRelationValues(self, args):
        validTypes = ["int", "bool", "string"]
        arg1Type = self.getValue(args[1], "type")
        arg2Type = self.getValue(args[2], "type")

        if arg1Type != arg2Type:
            print(
                "[chyba] argumenty relační instrukce nemají stejný typ", file=sys.stderr
            )
            exit(53)

        if arg1Type not in validTypes or arg2Type not in validTypes:
            print("[chyba] nevalidní typ argumentu relační instrukce", file=sys.stderr)
            exit(53)

    def isNumber(self, n):
        try:
            float(n)
            return True
        except ValueError:
            print("[chyba] neplatné číslo v aritmetické instrukci", file=sys.stderr)
            exit(32)

    def MOVE(self, args):
        self.checkTypes("MOVE", args)
        value = self.getValue(args[1], "value")
        type_t = self.getValue(args[1], "type")
        self.program.set_variable(args[0], value, type_t=type_t)

    def CREATEFRAME(self, args):
        self.program.tempFrame = Frame()

    def PUSHFRAME(self, args):
        if self.program.tempFrame == None:
            print(f"[chyba] přístup k neexistujícímu rámci", file=sys.stderr)
            exit(55)

        if self.program.localFrames == None:
            self.program.localFrames = Stack()

        frameCopy = copy.copy(self.program.tempFrame)
        self.program.localFrames.push(frameCopy)
        self.program.tempFrame = None

    def POPFRAME(self, args):
        if self.program.localFrames == None:
            print("[chyba] přístup k neexistujícímu rámci", file=sys.stderr)
            exit(55)
        if self.program.localFrames.length() == 0:
            print(f"[chyba] lokální rámec je prázdný", file=sys.stderr)
            exit(55)
        newTempFrame = self.program.localFrames.pop()
        self.program.tempFrame = newTempFrame

    def DEFVAR(self, args):
        frame = args[0].get("frame")
        if frame == "GF":
            if self.program.get_variable(args[0]) != None:
                print(
                    f'[chyba] proměnná {args[0].get("value")} je již definována',
                    file=sys.stderr,
                )
                exit(52)
            self.program.set_variable(args[0], "")
        elif frame == "LF":
            if self.program.localFrames == None:
                self.program.localFrames = Stack()
            if self.program.localFrames.get_variable_from_last_frame(
                args[0].get("value") != None
            ):
                print(
                    f'[chyba] proměnná {args[0].get("value")} je již definována',
                    file=sys.stderr,
                )
                exit(52)
            self.program.localFrames.set_variable_from_last_frame(
                args[0].get("value"), ""
            )
        elif frame == "TF":
            if self.program.tempFrame == None:
                print("[chyba] dočasný rámec nebyl vytvořen", file=sys.stderr)
                exit(55)
            if self.program.tempFrame.get_variable(args[0].get("value")) != None:
                print(
                    f'[chyba] proměnná {args[0].get("value")} je již definována',
                    file=sys.stderr,
                )
                exit(52)
            self.program.set_variable(args[0], "")

    def CALL(self, args):
        self.program.pushProgramStack(self.program.getProgramCounter() + 1)
        label = self.program.labelExists(args[0].get("value"))
        self.program.setProgramCounter(int(label.get("order")) - 1)

    def RETURN(self, args):
        self.program.setProgramCounter(self.program.popProgramStack())

    def PUSHS(self, args):
        self.program.dataStack.push(self.getValue(args[0], "value"))

    def POPS(self, args):
        self.checkTypes("POPS", args)
        if self.program.dataStack.isEmpty():
            print(f"[chyba] datový zásobník je prázdný", file=sys.stderr)
            exit(56)
        value = self.program.dataStack.pop()
        self.program.set_variable(args[0], value)

    def ADD(self, args):
        self.checkTypes("ADD", args)
        self.checkNumericValues(args)
        self.isNumber(self.getValue(args[1], "value"))
        self.isNumber(self.getValue(args[2], "value"))
        addedValue = int(self.getValue(args[1], "value")) + int(
            self.getValue(args[2], "value")
        )
        self.program.set_variable(args[0], addedValue)

    def SUB(self, args):
        self.checkTypes("SUB", args)
        self.checkNumericValues(args)
        self.isNumber(self.getValue(args[1], "value"))
        self.isNumber(self.getValue(args[2], "value"))
        subbedValue = int(self.getValue(args[1], "value")) - int(
            self.getValue(args[2], "value")
        )
        self.program.set_variable(args[0], subbedValue)

    def MUL(self, args):
        self.checkTypes("MUL", args)
        self.checkNumericValues(args)
        self.isNumber(self.getValue(args[1], "value"))
        self.isNumber(self.getValue(args[2], "value"))
        mulledValue = int(self.getValue(args[1], "value")) * int(
            self.getValue(args[2], "value")
        )
        self.program.set_variable(args[0], mulledValue)

    def IDIV(self, args):
        self.checkTypes("IDIV", args)
        self.checkNumericValues(args)
        self.isNumber(self.getValue(args[1], "value"))
        self.isNumber(self.getValue(args[2], "value"))
        if int(self.getValue(args[2], "value")) == 0:
            print("[chyba] dělení nulou", file=sys.stderr)
            exit(57)
        divedValue = int(self.getValue(args[1], "value")) // int(
            self.getValue(args[2], "value")
        )
        self.program.set_variable(args[0], divedValue)

    def LT(self, args):
        self.checkTypes("LT", args)
        self.checkRelationValues(args)
        if self.getValue(args[1], "value") < self.getValue(args[2], "value"):
            self.program.set_variable(args[0], True)
        else:
            self.program.set_variable(args[0], False)

    def GT(self, args):
        self.checkTypes("GT", args)
        self.checkRelationValues(args)
        if self.getValue(args[1], "value") > self.getValue(args[2], "value"):
            self.program.set_variable(args[0], True)
        else:
            self.program.set_variable(args[0], False)

    def EQ(self, args):
        self.checkTypes("EQ", args)
        self.checkRelationValues(args)
        if self.getValue(args[1], "value") == self.getValue(args[2], "value"):
            self.program.set_variable(args[0], True)
        else:
            self.program.set_variable(args[0], False)

    def AND(self, args):
        self.checkTypes("AND", args)
        if self.getValue(args[1], "value") and self.getValue(args[2], "value"):
            self.program.set_variable(args[0], True)
        else:
            self.program.set_variable(args[0], False)

    def OR(self, args):
        self.checkTypes("OR", args)
        if self.getValue(args[1], "value") or self.getValue(args[2], "value"):
            self.program.set_variable(args[0], True)
        else:
            self.program.set_variable(args[0], False)

    def NOT(self, args):
        self.checkTypes("NOT", args)
        self.program.set_variable(args[0], not self.getValue(args[1], "value"))

    def INT2CHAR(self, args):
        self.checkTypes("INT2CHAR", args)
        value = self.getValue(args[1], "value")
        if not (isinstance(value, str) or value.isascii):
            print("[chyba] znak není validní ordinální znak")
            exit(58)

        self.program.set_variable(args[0], chr(int(value)))

    def STRI2INT(self, args):
        self.checkTypes("STRI2INT", args)
        index = int(self.getValue(args[2], "value"))
        string = self.getValue(args[1], "value")
        if index > len(string) - 1:
            print(f"[chyba] index {index} je mimo řetězec {string}", file=sys.stderr)
            exit(58)
        self.program.set_variable(
            args[0],
            int((string[index])),
        )

    def READ(self, args):
        self.checkTypes("READ", args)
        userInput = input()
        type_t = None
        castType = self.getValue(args[1], "value")
        if castType == "int":
            type_t = "int"
        elif castType == "bool":
            if userInput.lower() == "true":
                userInput = "true"
            else:
                userInput = "false"
            type_t = "bool"
        elif castType == None or castType == "":
            userInput = "nil"
            type_t = "nil"
        else:
            type_t = "string"

        self.program.set_variable(args[0], userInput, type_t=type_t)

    def WRITE(self, args):
        output = str(self.getValue(args[0], "value"))
        type_t = self.getValue(args[0], "type")
        output = Regex.replace_escape_sequences(output)
        coutput = output.lower()
        if coutput == "false":
            print("false", end="")
        elif coutput == "true":
            print("true", end="")
        elif type_t == "nil":
            print("", end="")
        else:
            print(output, end="")

    def CONCAT(self, args):
        self.checkTypes("CONCAT", args)
        self.program.set_variable(
            args[0], self.getValue(args[1], "value") + self.getValue(args[2], "value")
        )

    def STRLEN(self, args):
        self.checkTypes("STRLEN", args)
        self.program.set_variable(args[0], len(self.getValue(args[1], "value")))

    def GETCHAR(self, args):
        self.checkTypes("GETCHAR", args)
        index = int(self.getValue(args[2], "value"))
        string = self.getValue(args[1], "value")
        if index > len(string) - 1:
            print(f"[chyba] index {index} je mimo řetězec {string}", file=sys.stderr)
            exit(58)
        if self.program.get_variable(args[0]) == None:
            print("[chyba] proměnná není definována", file=sys.stderr)
            exit(54)
        self.program.set_variable(args[0], string[index])

    def SETCHAR(self, args):
        self.checkTypes("SETCHAR", args)
        index = int(self.getValue(args[1], "value"))
        newChar = self.getValue(args[2], "value")
        string = self.program.get_variable(args[0].get("value"))
        if index > len(string) - 1:
            print(f"[chyba] index {index} je mimo řetězec {string}", file=sys.stderr)
            exit(58)
        string[index] = newChar
        self.program.set_variable(args[0], string)

    def TYPE(self, args):
        self.checkTypes("TYPE", args)
        value = self.getValue(args[1], "value")
        type_t = self.getValue(args[1], "type")
        var = args[0]
        if Regex.isNumber(value):
            self.program.set_variable(var, "int")
        elif Regex.isBool(value):
            self.program.set_variable(var, "bool")
        elif Regex.isNil(value):
            self.program.set_variable(var, "nil", "nil")
        elif type_t == None:
            self.program.set_variable(var, "")
        else:
            self.program.set_variable(var, "string")

    def JUMP(self, args):
        label = self.program.labelExists(args[0].get("value"))
        self.program.setProgramCounter(int(label.get("order")) - 1)

    def JUMPIFEQ(self, args):
        arg1Type = self.getValue(args[1], "type")
        arg2Type = self.getValue(args[2], "type")
        arg1Value = self.getValue(args[1], "value")
        arg2Value = self.getValue(args[2], "value")
        if (
            (arg1Type == arg2Type)
            or (Regex.isNil(arg1Value))
            or (Regex.isNil(arg2Value))
        ):
            if str(arg1Value) == str(arg2Value):
                label = self.program.labelExists(args[0].get("value"))
                return self.program.setProgramCounter(int(label.get("order")) - 1)
        else:
            print("[chyba] neplatné typy argumentů v podmínce", file=sys.stderr)
            exit(53)

    def JUMPIFNEQ(self, args):
        arg1Type = self.getValue(args[1], "type")
        arg2Type = self.getValue(args[2], "type")
        arg1Value = self.getValue(args[1], "value")
        arg2Value = self.getValue(args[2], "value")
        if arg1Type == arg2Type or Regex.isNil(arg1Value) or Regex.isNil(arg2Value):
            if str(arg1Value) != str(arg2Value):
                label = self.program.labelExists(args[0].get("value"))
                return self.program.setProgramCounter(int(label.get("order")) - 1)
        else:
            print("[chyba] neplatné typy argumentů v podmínce", file=sys.stderr)
            exit(53)

    def EXIT(self, args):
        arg0Value = self.getValue(args[0], "value")
        arg0Type = self.getValue(args[0], "type")
        if arg0Type != "int":
            print("[chyba] argument instrukce EXIT není číslo", file=sys.stderr)
            exit(53)
        if not Regex.isExitNumber(arg0Value):
            print("[chyba] neplatný návratový kód", file=sys.stderr)
            exit(57)
        exit(int(arg0Value))

    def DPRINT(self, args):
        print(self.getValue(args[0], "value"), file=sys.stderr)

    def BREAK(self, args):
        programCounter = self.program.getProgramCounter()
        globalFrame = self.program.getGlobalFrame()
        localFrames = self.program.getLocalFrames()
        tempFrame = self.program.getTempFrame()

        print(
            f"programový čítač: {programCounter}\nglobální rámec: {globalFrame}\nlokální rámec: {localFrames}\ndočasný rámec: {tempFrame}",
            file=sys.stderr,
        )

    def LABEL(self, args):
        pass


def execute_instruction(instruction, args, program):
    instructions = Instructions(program)
    method_name = instruction.upper()
    method = getattr(instructions, method_name, None)
    if method:
        try:
            method(args)
        except IndexError:
            print("[chyba] Nesprávný počet instrukcí", file=sys.stderr)
            exit(52)
    else:
        print(f"[Chyba] neznama instrukce {instruction}", file=sys.stderr)
        exit(32)
