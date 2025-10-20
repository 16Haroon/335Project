# assembler/listing.py

class ListingWriter:
    def __init__(self, file_path):
        self.file_path = file_path
        self.lines = []

    def add_line(self, locctr, label, opcode, operand, obj_code=""):
        """Append a formatted line to the listing."""
        formatted = f"{locctr:04X}\t{label:<10}{opcode:<10}{operand:<10}{obj_code}"
        self.lines.append(formatted)

    def write(self):
        """Save the listing file."""
        with open(self.file_path, "w") as f:
            for line in self.lines:
                f.write(line + "\n")