import argparse
import sys
from program import Program
from instructions import *
from xmlParser import *

program = Program()

# @brief Hlavní běhová část interpretu
# volá jednotlivé instrukce dle programového čítače
# @param code instrukce a argumenty celého programu
def executeInterpret(code):
    while int(program.getProgramCounter()) < len(code):
        instruction = code[int(program.getProgramCounter())]
        instructionName = instruction["instructionName"]
        args = instruction["args"]
        execute_instruction(instructionName, args, program)
        program.setProgramCounter(int(program.getProgramCounter()) + 1)

def main():
    sourceXML = ""

    # vytvoření parseru argumentů programu
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

    # nastavení zdroje programu
    if args.source is None:
        sourceXML = sys.stdin
    else:
        sourceXML = args.source

    # zisk instrukcí a argumentů pomocí statické metody XMLParser třídy
    code = XMLParser.parseXML(sourceXML, program)
    executeInterpret(code)


if __name__ == "__main__":
        main()
        exit(0)
