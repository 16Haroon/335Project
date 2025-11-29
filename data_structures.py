"""
Abdullah Haroon


Description: This module defines the main data structures used by our SIC/XE assembler. 
It implements the core tables needed by both Pass 1 and Pass 2 of the assembler, including:
- Symbol Table (SYMTAB)
- Opcode Table (OPTAB)
- Literal Table (LITTAB)
- Register Table (REGTAB)
- Block Table (BLOCKTAB)

Each class provides methods for insertion, lookup, and debugging display.
All classes are designed to be reusable and easily imported by other modules.
"""

class SymbolTable:
    #Stores symbol names with their corresponding memory addresses.
    def __init__(self):
        self.table = {}

    def add(self, label, address):
        if label in self.table:
            raise ValueError(f"Duplicate symbol detected: {label}")
        self.table[label] = address

    def lookup(self, label):
        return self.table.get(label)

    def display(self):
        print("\nSYMBOL TABLE")
        print("============")
        for sym, addr in self.table.items():
            print(f"{sym:<10} {addr:04X}")


class OpcodeTable:
    #Contains opcode and instruction format for all SIC/XE mnemonics.
    def __init__(self):
        # Mnemonic: (Opcode, Format)
        self.table = {
            "LDA": ("00", 3), "LDX": ("04", 3), "LDS": ("6C", 3),
            "STA": ("0C", 3), "STX": ("10", 3), "STCH": ("54", 3),
            "ADD": ("18", 3), "SUB": ("1C", 3), "MUL": ("20", 3),
            "DIV": ("24", 3), "COMP": ("28", 3), "J": ("3C", 3),
            "JEQ": ("30", 3), "JLT": ("38", 3), "JSUB": ("48", 3),
            "RSUB": ("4C", 3), "CLEAR": ("B4", 2), "TIXR": ("B8", 2),
            "COMPR": ("A0", 2), "TD": ("E0", 3), "RD": ("D8", 3),
            "WD": ("DC", 3), "STL": ("14", 3)
        }

    def get(self, mnemonic):
        return self.table.get(mnemonic)

    def display(self):
        print("\nOPCODE TABLE")
        print("============")
        for mnem, (op, fmt) in self.table.items():
            print(f"{mnem:<8} Opcode: {op:<3} Format: {fmt}")


class LiteralTable:
    #Stores literals and their assigned addresses.
    def __init__(self):
        self.literals = {}

    def add(self, literal):
        if literal not in self.literals:
            self.literals[literal] = None  # assigned later in Pass 1

    def assign(self, literal, address):
        if literal in self.literals:
            self.literals[literal] = address

    def display(self):
        print("\nLITERAL TABLE")
        print("=============")
        for lit, addr in self.literals.items():
            print(f"{lit:<10} {addr}")


class RegisterTable:
    #Maps register names to their numeric codes.
    def __init__(self):
        self.registers = {
            "A": 0, "X": 1, "L": 2, "B": 3,
            "S": 4, "T": 5, "F": 6, "PC": 8, "SW": 9
        }

    def get(self, reg):
        return self.registers.get(reg)

    def display(self):
        print("\nREGISTER TABLE")
        print("==============")
        for reg, code in self.registers.items():
            print(f"{reg:<3} = {code}")


class BlockTable:
    #Handles program blocks for use in Pass 1/2.
    def __init__(self):
        self.blocks = {"DEFAULT": 0}
        self.current_block = "DEFAULT"
        self.next_block_num = 1

    def add_block(self, name):
        if name not in self.blocks:
            self.blocks[name] = self.next_block_num
            self.next_block_num += 1

    def switch_block(self, name):
        if name in self.blocks:
            self.current_block = name

    def display(self):
        print("\nBLOCK TABLE")
        print("============")
        for name, num in self.blocks.items():
            current = "<-- current" if name == self.current_block else ""
            print(f"{name:<10} Block #: {num} {current}")

