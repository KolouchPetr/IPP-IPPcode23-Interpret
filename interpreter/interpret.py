import argparse
import sys
import xml.etree.ElementTree as ET

from program import Program
from instructions import *
from stack import Stack

program = Program()


def checkArgumentNumbers(args):
    i = 1
    for arg in args:
        string = "arg" + str(i)
        if arg.get("name") != string:
            print(f"[chyba] špatné číslování argumentu", file=sys.stderr)
            exit(32)
        i += 1


def checkDuplicitOrder(code):
    orders = []
    for line in code:
        order = line.get("order")
        if order in orders:
            print("[chyba] duplicitní order", file=sys.stderr)
            exit(32)
        orders.append(order)


if __name__ == "__main__":
    sourceXML = ""

    parser = argparse.ArgumentParser(
        prog="interpret.py",
        description="Implementace interpretu pro jazyk IPPCode2023",
    )
    parser.add_argument(
        "--source", type=str, help=" vstupní soubor s XML reprezentací zdrojového kódu"
    )
    parser.add_argument(
        "--input",
        type=str,
        help="soubor se vstupy pro samotnou interpretaci zadaného zdrojového kódu",
    )

    args = parser.parse_args()

    if args.source is None:
        sourceXML = sys.stdin
    else:
        sourceXML = args.source

    try:
        tree = ET.parse(sourceXML)
        root = tree.getroot()
        code = []

        for instruction in root.findall("instruction"):
            opcode = instruction.get("opcode")
            order = instruction.get("order")
            if opcode == None or order == None:
                print(
                    "[chyba] opcode nebo parametr není součástí instrukce",
                    file=sys.stderr,
                )
                exit(32)
            if not order.isnumeric():
                print("[chyba] opcode obsahuje nečíselnou hodnotu", file=sys.stderr)
                exit(32)
            arguments = []
            for arg in instruction:
                if(arg.text):
                    arg.text = arg.text.strip()
                Regex.checkArgumentTag(arg.tag)
                #if opcode.upper() == "LABEL":
                #    if arg.text == None:
                #        print("[chyba] label nemá název", file=sys.stderr)
                #        exit(32)
                #    label = {"order": order, "name": arg.text}
                 #   program.appendLabels(label)
                    # TODO add type and scope if its a variable
                if arg.get("type") == "var":
                    if arg.text == None:
                        print("[chyba] chybí název proměnné", file=sys.stderr)
                        exit(32)
                    var = arg.text.split("@")
                    value = var[1]
                    frame = var[0]
                    argument = {
                        "name": arg.tag,
                        "type": arg.get("type"),
                        "value": value,
                        "frame": frame,
                    }
                else:
                    value = arg.text
                    if value == None:
                        value = ""

                    argument = {
                        "name": arg.tag,
                        "type": arg.get("type"),
                        "value": value,
                    }
                arguments.append(argument)
            arguments = sorted(arguments, key=lambda x: x["name"])
            checkArgumentNumbers(arguments)
            codeLine = {"instructionName": opcode, "order": order, "args": arguments}
            code.append(codeLine)
        code = sorted(code, key=lambda x: int(x["order"]))
        checkDuplicitOrder(code)

        currentOrder = 0
        for line in code:
            order = int(line["order"].strip())
            if order != currentOrder + 1:
                order = currentOrder + 1
                line["order"] = str(order)
            currentOrder = order
        
        for instr in code:
            if instr["instructionName"].upper() == "LABEL":
                if instr["args"][0].get("value") == "":
                    print("[chyba] label nemá název", file=sys.stderr)
                    exit(32)
                label = {"order": instr["order"], "name": instr["args"][0].get("value")}
                program.appendLabels(label)
                

        i = 0
        while int(program.getProgramCounter()) < len(code):
            instruction = code[int(program.getProgramCounter())]
            instructionName = instruction["instructionName"]
            args = instruction["args"]
            execute_instruction(instructionName, args, program)
            program.setProgramCounter(int(program.getProgramCounter()) + 1)
        exit(0)

    except ET.ParseError as e:
        print(f"[Chyba] nastala chyba při načítání souboru: {e}", file=sys.stderr)
        exit(31)
