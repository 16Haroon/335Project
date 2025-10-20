# assembler/tables.py

class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def add(self, label, address):
        """Add a symbol with its address."""
        if label in self.symbols:
            raise ValueError(f"Duplicate symbol: {label}")
        self.symbols[label] = address

    def get(self, label):
        """Retrieve a symbol address if it exists."""
        return self.symbols.get(label, None)

    def __repr__(self):
        return str(self.symbols)


class LiteralTable:
    def __init__(self):
        self.literals = {}

    def add(self, literal, address=None):
        """Add literal; address is optional until assigned."""
        self.literals[literal] = address

    def assign_addresses(self, start_address):
        """Assign addresses sequentially to literals."""
        for lit in self.literals:
            if self.literals[lit] is None:
                self.literals[lit] = start_address
                start_address += 3
        return start_address

    def __repr__(self):
        return str(self.literals)


class BlockTable:
    def __init__(self):
        self.blocks = {"DEFAULT": 0}
        self.current = "DEFAULT"
        self.next_block_num = 1

    def add(self, name):
        """Create a new block name if not exists."""
        if name not in self.blocks:
            self.blocks[name] = self.next_block_num
            self.next_block_num += 1
        self.current = name

    def get(self, name):
        return self.blocks.get(name, 0)