# assembler/pass1.py
from assembler.tables import SymbolTable, LiteralTable, BlockTable

class Pass1:
    def __init__(self):
        self.symtab = SymbolTable()
        self.littab = LiteralTable()
        self.blocktab = BlockTable()
        self.locctr = 0
        self.start_addr = 0
        self.program_name = ""
        self.intermediate = []  # (LOCCTR, LABEL, OPCODE, OPERAND)

    def assemble(self, lines):
        """Perform Pass 1 of SIC/XE assembler."""
        first_line = lines[0].split()
        if first_line[1].upper() == "START":
            self.program_name = first_line[0]
            self.start_addr = int(first_line[2], 16)
            self.locctr = self.start_addr
            self.intermediate.append((self.locctr, *first_line))
            lines = lines[1:]  # skip the START line

        # Main Pass 1 loop
        for line in lines:
            if line.strip() == "" or line.startswith('.'):
                continue  # skip comments or blank lines

            parts = line.strip().split()
            label, opcode, operand = "", "", ""

            if len(parts) == 3:
                label, opcode, operand = parts
            elif len(parts) == 2:
                opcode, operand = parts
            elif len(parts) == 1:
                opcode = parts[0]

            # Add label to SYMTAB
            if label:
                if label in self.symtab.symbols:
                    raise ValueError(f"Duplicate symbol: {label}")
                self.symtab.add(label, self.locctr)

            # Update LOCCTR based on instruction type
            if opcode == "WORD":
                self.locctr += 3
            elif opcode == "RESW":
                self.locctr += 3 * int(operand)
            elif opcode == "RESB":
                self.locctr += int(operand)
            elif opcode == "BYTE":
                if operand.startswith("C'"):
                    self.locctr += len(operand) - 3
                elif operand.startswith("X'"):
                    self.locctr += (len(operand) - 3) // 2
            elif opcode == "END":
                break
            else:
                # Assume 3-byte instruction for simplicity
                self.locctr += 3

            self.intermediate.append((self.locctr, label, opcode, operand))

        program_length = self.locctr - self.start_addr
        return self.intermediate, self.symtab, program_length
