# assembler/tables.py - CORRECTED INDENTATION
class OPTAB:
    # SIC/XE Instruction Set - opcode in hex, format
    INSTRUCTIONS = {
        'ADD': ('18', 3), 'ADDF': ('58', 3), 'ADDR': ('90', 2),
        'AND': ('40', 3), 'CLEAR': ('B4', 2), 'COMP': ('28', 3),
        'COMPF': ('88', 3), 'COMPR': ('A0', 2), 'DIV': ('24', 3),
        'DIVF': ('64', 3), 'DIVR': ('9C', 2), 'FIX': ('C4', 1),
        'FLOAT': ('C0', 1), 'HIO': ('F4', 1), 'J': ('3C', 3),
        'JEQ': ('30', 3), 'JGT': ('34', 3), 'JLT': ('38', 3),
        'JSUB': ('48', 3), 'LDA': ('00', 3), 'LDB': ('68', 3),
        'LDCH': ('50', 3), 'LDF': ('70', 3), 'LDL': ('08', 3),
        'LDS': ('6C', 3), 'LDT': ('74', 3), 'LDX': ('04', 3),
        'LPS': ('D0', 3), 'MUL': ('20', 3), 'MULF': ('60', 3),
        'MULR': ('98', 2), 'NORM': ('C8', 1), 'OR': ('44', 3),
        'RD': ('D8', 3), 'RMO': ('AC', 2), 'RSUB': ('4C', 3),
        'SHIFTL': ('A4', 2), 'SHIFTR': ('A8', 2), 'SIO': ('F0', 1),
        'SSK': ('EC', 3), 'STA': ('0C', 3), 'STB': ('78', 3),
        'STCH': ('54', 3), 'STF': ('80', 3), 'STI': ('D4', 3),
        'STL': ('14', 3), 'STS': ('7C', 3), 'STSW': ('E8', 3),
        'STT': ('84', 3), 'STX': ('10', 3), 'SUB': ('1C', 3),
        'SUBF': ('5C', 3), 'SUBR': ('94', 2), 'SVC': ('B0', 2),
        'TD': ('E0', 3), 'TIO': ('F8', 1), 'TIX': ('2C', 3),
        'TIXR': ('B8', 2), 'WD': ('DC', 3)
    }  # ← MAKE SURE THIS BRACE IS HERE!

    @classmethod
    def get_opcode(cls, mnemonic):
        return cls.INSTRUCTIONS.get(mnemonic, (None, None))
    
    @classmethod
    def is_instruction(cls, mnemonic):
        return mnemonic in cls.INSTRUCTIONS

class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def add(self, label, address):
        if label in self.symbols:
            raise ValueError(f"Duplicate symbol: {label}")
        self.symbols[label] = address

    def get(self, label):
        return self.symbols.get(label, None)
    
    def lookup(self, label):
        return self.symbols.get(label, None)

    def __contains__(self, label): 
        return label in self.symbols

    def display(self):
        print("\nSYMBOL TABLE")
        print("============")
        for sym, addr in self.symbols.items():
            print(f"{sym:<10} {addr:04X}")

    def __repr__(self):
        return str(self.symbols)
    
class LiteralTable:
    def __init__(self):
        self.literals = {}

    def add(self, literal, address=None):
        self.literals[literal] = address

    def assign_addresses(self, start_address):
        for lit in self.literals:
            if self.literals[lit] is None:
                self.literals[lit] = start_address
                start_address += 3
        return start_address

    def get(self, literal):
        return self.literals.get(literal, None)

    def __repr__(self):
        return str(self.literals)

class BlockTable:
    def __init__(self):
        self.blocks = {"DEFAULT": 0}
        self.current = "DEFAULT"
        self.next_block_num = 1

    def add(self, name):
        if name not in self.blocks:
            self.blocks[name] = self.next_block_num
            self.next_block_num += 1
        self.current = name

    def get(self, name):
        return self.blocks.get(name, 0)
    

class OpcodeTable:
    """Compatibility class for tests that expect OpcodeTable instead of OPTAB"""
    def __init__(self):
        # Use the same data as OPTAB but in the expected format
        self.table = {
            "LDA": ("00", 3), "LDX": ("04", 3), "LDL": ("08", 3),
            "STA": ("0C", 3), "STX": ("10", 3), "STL": ("14", 3),
            "LDCH": ("50", 3), "STCH": ("54", 3), "ADD": ("18", 3),
            "SUB": ("1C", 3), "MUL": ("20", 3), "DIV": ("24", 3),
            "COMP": ("28", 3), "J": ("3C", 3), "JLT": ("38", 3),
            "JEQ": ("30", 3), "JGT": ("34", 3), "JSUB": ("48", 3),
            "RSUB": ("4C", 3), "TIX": ("2C", 3), "TIXR": ("B8", 2),
            "CLEAR": ("B4", 2), "COMPR": ("A0", 2), "ADDR": ("90", 2),
            "SUBR": ("94", 2), "MULR": ("98", 2), "DIVR": ("9C", 2),
            "LDB": ("68", 3), "LDS": ("6C", 3), "LDT": ("74", 3),
            "STB": ("78", 3), "STS": ("7C", 3), "STT": ("84", 3),
            "TD": ("E0", 3), "RD": ("D8", 3), "WD": ("DC", 3),
        }

    def get(self, mnemonic):
        return self.table.get(mnemonic)

    def display(self):
        print("\nOPCODE TABLE")
        print("============")
        for mnem, (op, fmt) in self.table.items():
            print(f"{mnem:<8} Opcode: {op:<3} Format: {fmt}")


class RegisterTable:
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