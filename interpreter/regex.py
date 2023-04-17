import re
import sys


class Regex:
    patterns = {
        "var": r"^(GF|TF|LF)@[a-zA-Z_\$&%*!?][\w\$&%*!?-]*$",
        "symb": r"^(int|GF|TF|LF|bool|string|nil)@(?!nil)(?:[-+]?[0-9]+|(?:[0-9a-fA-F]+)|(?:\b(?:true|false)\b)|(?:[^#\s\\\\]|(?:\\\\[0-9]{3}))*?)$",
        "label": r"^[a-zA-Z_\-\$&%\*\!?][\w\-\$&%\*\!?]*$",
        "type": r"^(int|bool|string|nil)$",
        "arg": r"^arg[1-3]$"
    }

    @staticmethod
    def matchVar(s):
        return bool(re.match(Regex.patterns["var"], s))

    @staticmethod
    def matchSymb(s):
        return bool(re.match(Regex.patterns["symb"], s))

    @staticmethod
    def matchLabel(s):
        return bool(re.match(Regex.patterns["label"], s))

    @staticmethod
    def matchType(s):
        return bool(re.match(Regex.patterns["type"], s))

    @staticmethod
    def getArgFrame(arg):
        if arg.value.startswith("GF"):
            return "GF"
        elif arg.value.startswith("LF"):
            return "LF"
        elif arg.value.startswith("TF"):
            return "TF"

    @staticmethod
    def isNumber(s):
        return bool(re.match("[0-9]", str(s)))

    @staticmethod
    def isBool(s):
        return s == "true" or s == "false"

    @staticmethod
    def isNil(s):
        return s == "nil"

    @staticmethod
    def isExitNumber(n):
        if(not Regex.isNumber(n)):
            print("[chyba] neplatné číslo", file=sys.stderr)
            exit(57)
        return bool(re.match("[0-49]", str(n)))

    @staticmethod
    def checkArgumentTag(arg):
        if(not bool(re.match(Regex.patterns["arg"], str(arg)))):
            print(f"[chyba] neznamý tag argumentu {arg}", file=sys.stderr)
            exit(32)

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
