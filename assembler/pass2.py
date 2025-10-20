# assembler/pass2.py
from assembler.tables import SymbolTable
from assembler.objectwriter import ObjectWriter
from assembler.listing import ListingWriter

class Pass2:
    def __init__(self, symtab: SymbolTable):
        self.symtab = symtab
        self.obj_writer = ObjectWriter()

    def generate_object_code(self, opcode, operand):
        """Simplified object-code generator."""
        if operand and operand in self.symtab.symbols:
            address = self.symtab.get(operand)
            return f"{opcode:02X}{address:04X}"
        elif operand is None:
            return f"{opcode:02X}0000"
        else:
            return f"{opcode:02X}FFFF"  # unknown symbol placeholder

    def assemble(self, intermediate, program_name="PROG", start_addr=0):
        listing = ListingWriter("output_listing.txt")
        obj_codes = []

        # First pass through intermediate (simulate real input) 
        for locctr, label, opcode, operand in intermediate:
            obj = self.generate_object_code(opcode, operand)
            obj_codes.append(obj)
            listing.add_line(locctr, label, opcode, operand, obj)

        # Write final object file
        self.obj_writer.write_header(program_name, start_addr, len(obj_codes) * 3)
        self.obj_writer.add_text_record(start_addr, obj_codes)
        self.obj_writer.write_end(start_addr)
        listing.write()

        return self.obj_writer.generate()