# assembler/tables.py

class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def add(self, symbol, address):
        self.symbols[symbol] = address

    def get(self, symbol):
        return self.symbols.get(symbol)

    def __contains__(self, symbol):
        return symbol in self.symbols


class LiteralTable:
    def __init__(self):
        self.literals = {}

    def add(self, literal, address):
        self.literals[literal] = address


class BlockTable:
    def __init__(self):
        self.blocks = {}
