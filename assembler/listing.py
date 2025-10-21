# assembler/listing.py
class ListingWriter:
    def __init__(self, filename="listing.txt"):
        self.filename = filename
        self.lines = []

    def add_line(self, locctr, label, opcode, operand, obj_code=""):
        loc_str = f"{locctr:04X}" if isinstance(locctr, int) else str(locctr)
        label_str = label if label else ""
        opcode_str = opcode if opcode else ""
        operand_str = operand if operand else ""
        obj_str = obj_code if obj_code else ""
        self.lines.append((loc_str, label_str, opcode_str, operand_str, obj_str))

    def write(self):
        with open(self.filename, "w") as f:
            f.write("LOC   LABEL       OPCODE     OPERAND     OBJCODE\n")
            f.write("----  ----------  ----------  ----------  ----------\n")
            for loc, label, opcode, operand, obj in self.lines:
                f.write(f"{loc:<6}{label:<12}{opcode:<12}{operand:<12}{obj}\n")
