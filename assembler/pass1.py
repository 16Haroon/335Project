from assembler.tables import SymbolTable, LiteralTable, BlockTable

class Pass1:
    def __init__(self):
        self.symtab = SymbolTable()
        self.littab = LiteralTable()
        self.blocktab = BlockTable()
        self.locctr = 0
        self.start_addr = 0
        self.program_name = ""
        self.intermediate = []   # (LOCCTR, LABEL, OPCODE, OPERAND)

    def assemble(self, lines):
        """Perform Pass 1 of SIC/XE assembler."""
        # --- Handle START ---
        first = lines[0].split()
        if len(first) >= 3 and first[1].upper() == "START":
            label, opcode, operand = first[0], first[1], first[2]
            self.program_name = label
            self.start_addr = int(operand, 16)
            self.locctr = self.start_addr

            self.intermediate.append(
                (self.locctr, label, opcode, operand)
            )

            lines = lines[1:]  # Skip START line

        # --- Main Loop ---
        for line in lines:
            line = line.strip()
            if line == "" or line.startswith("."):
                continue

            parts = line.split()
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

            # Append BEFORE updating LOCCTR (important!)
            self.intermediate.append(
                (self.locctr, label, opcode, operand)
            )

            # --- LOCCTR Calculation ---
            if opcode == "WORD":
                self.locctr += 3

            elif opcode == "RESW":
                self.locctr += 3 * int(operand)

            elif opcode == "RESB":
                self.locctr += int(operand)

            elif opcode == "BYTE":
                if operand.upper().startswith("C'"):
                    # C'EOF' → length = # chars
                    self.locctr += len(operand.split("'")[1])
                elif operand.upper().startswith("X'"):
                    # X'F1' → 2 hex digits = 1 byte
                    self.locctr += len(operand.split("'")[1]) // 2

            elif opcode == "END":
                break

            else:
                # Default format 3 instruction
                self.locctr += 3

        program_length = self.locctr - self.start_addr
        return self.intermediate, self.symtab, program_length
