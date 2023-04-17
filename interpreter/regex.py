import re
import sys

# Třída Regex obsahuje statické metody pro kontrolu specifických hodnot
# pomocí regulárních výrazů
class Regex:
    patterns = {
        "var": r"^(GF|TF|LF)@[a-zA-Z_\$&%*!?][\w\$&%*!?-]*$",
        "symb": r"^(int|GF|TF|LF|bool|string|nil)@(?!nil)(?:[-+]?[0-9]+|(?:[0-9a-fA-F]+)|(?:\b(?:true|false)\b)|(?:[^#\s\\\\]|(?:\\\\[0-9]{3}))*?)$",
        "label": r"^[a-zA-Z_\-\$&%\*\!?][\w\-\$&%\*\!?]*$",
        "type": r"^(int|bool|string|nil)$",
        "arg": r"^arg[1-3]$"
    }

    # @brief statická metoda porovnávající řetězec se vzorem proměnné
    # @param s řetězec
    @staticmethod
    def matchVar(s):
        return bool(re.match(Regex.patterns["var"], s))

    # @brief statická metoda porovnávající řetězec se vzorem symbolu
    # @param s řetězec
    @staticmethod
    def matchSymb(s):
        return bool(re.match(Regex.patterns["symb"], s))

    # @brief statická metoda porovnávající řetězec se vzorem návěští
    # @param s řetězec
    @staticmethod
    def matchLabel(s):
        return bool(re.match(Regex.patterns["label"], s))

    # @brief statická metoda porovnávající řetězec se vzorem typu
    # @param s řetězec
    @staticmethod
    def matchType(s):
        return bool(re.match(Regex.patterns["type"], s))

    # @brief statická metoda vracející rámec proměnné
    # @param arg proměnná
    @staticmethod
    def getArgFrame(arg):
        if arg.value.startswith("GF"):
            return "GF"
        elif arg.value.startswith("LF"):
            return "LF"
        elif arg.value.startswith("TF"):
            return "TF"

    # @brief statická metoda porovnávající řetězez se vzorem čísla
    # @param s řetězec
    @staticmethod
    def isNumber(s):
        return bool(re.match("[0-9]", str(s)))

    # @brief statická metoda porovnávající řetězec s boolean hodnotou
    # @param s řetězec
    @staticmethod
    def isBool(s):
        return s == "true" or s == "false"

    # @brief statická metoda porovnávající řetězec s hodnotou nil
    # @param s řetězec
    @staticmethod
    def isNil(s):
        return s == "nil"

    # @brief statická metoda kontrolující správnost návratového čísla
    # @param n návratové číslo
    @staticmethod
    def isExitNumber(n):
        if(not Regex.isNumber(n)):
            print("[chyba] neplatné číslo", file=sys.stderr)
            exit(57)
        return bool(re.match("[0-49]", str(n)))


    # @brief statická metoda porovnávající řetězec se vzorem tagu argumentu
    # @param arg argument
    @staticmethod
    def checkArgumentTag(arg):
        if(not bool(re.match(Regex.patterns["arg"], str(arg)))):
            print(f"[chyba] neznamý tag argumentu {arg}", file=sys.stderr)
            exit(32)

    # @brief nahradí escape sekvenci v řetězci za hodnotu znaku
    # @param text text
    @staticmethod
    def replace_escape_sequences(text):
        escape_regex = re.compile(r'\\(\d{3})')

        def replace_match(match):
            escape_code = int(match.group(1))

            if 0 <= escape_code <= 32 or escape_code == 35 or escape_code == 92:
                return chr(escape_code)
            else:
                return match.group(0)

        return escape_regex.sub(replace_match, text)
