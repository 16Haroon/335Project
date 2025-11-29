from assembler.tables import SymbolTable, LiteralTable, BlockTable

class Pass1:
    def __init__(self):
        self.symtab = SymbolTable()
        self.littab = LiteralTable()
        self.blocktab = BlockTable()   # unused but must exist
        self.locctr = 0
        self.start_addr = 0
        self.program_name = ""
        self.intermediate = []   # (LOCCTR, LABEL, OPCODE, OPERAND)

    def assemble(self, lines):
        """Perform Pass 1 of the SIC/XE assembler."""

        # ----------------------------------------------------
        # HANDLE START
        # ----------------------------------------------------
        first = lines[0].strip().split()
        if len(first) >= 3 and first[1].upper() == "START":
            label, opcode, operand = first[0], first[1].upper(), first[2]
            self.program_name = label
            self.start_addr = int(operand, 16)
            self.locctr = self.start_addr

            # INTERMEDIATE FORMAT
            self.intermediate.append((self.locctr, label, opcode, operand))

            lines = lines[1:]  # skip START line

        # ----------------------------------------------------
        # MAIN LOOP
        # ----------------------------------------------------
        for line in lines:
            line = line.strip()
            if not line or line.startswith("."):
                continue   # skip comments

            parts = line.split()
            label = opcode = operand = ""

            # Parse label/opcode/operand
            if len(parts) == 3:
                label, opcode, operand = parts
                opcode = opcode.upper()
            elif len(parts) == 2:
                opcode, operand = parts
                opcode = opcode.upper()
            elif len(parts) == 1:
                opcode = parts[0].upper()

            # Add label to symbol table
            if label:
                if label in self.symtab:
                    raise ValueError(f"Duplicate symbol: {label}")
                self.symtab.add(label, self.locctr)

            # PUSH CURRENT LINE BEFORE CHANGING LOCCTR
            self.intermediate.append((self.locctr, label, opcode, operand))

            # ----------------------------------------------------
            # UPDATE LOCCTR
            # ----------------------------------------------------
            if opcode == "WORD":
                self.locctr += 3

            elif opcode == "RESW":
                self.locctr += 3 * int(operand)

            elif opcode == "RESB":
                self.locctr += int(operand)

            elif opcode == "BYTE":
                val = operand.split("'")[1]
                if operand.upper().startswith("C'"):
                    self.locctr += len(val)          # chars = bytes
                elif operand.upper().startswith("X'"):
                    self.locctr += len(val) // 2     # 2 hex digits = 1 byte

            elif opcode == "END":
                break

            else:
                # default: format 3 instruction (3 bytes)
                self.locctr += 3

        program_length = self.locctr - self.start_addr
        return self.intermediate, self.symtab, program_length
