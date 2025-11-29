# Example of how to use Pass 2
from assembler.tables import SymbolTable
from assembler.pass2 import Pass2

# Create symbol table with some symbols
symtab = SymbolTable()
symtab.add("RETADR", 0x0030)
symtab.add("LENGTH", 0x0033)
symtab.add("BUFFER", 0x0036)
symtab.add("FIRST", 0x0000)
symtab.add("CLOOP", 0x0003)

# Sample intermediate data (from Pass 1)
intermediate_data = [
    (0x0000, "FIRST", "STL", "RETADR"),
    (0x0003, "CLOOP", "JSUB", "RDREC"),
    (0x0006, "LDA", "", "LENGTH"),
    (0x0009, "COMP", "", "#0"),
    (0x000C, "JEQ", "", "ENDFIL"),
    (0x000F, "JSUB", "", "WRREC"),
    (0x0012, "J", "", "CLOOP"),
    (0x0015, "ENDFIL", "LDA", "EOF"),
]

# Run Pass 2
pass2 = Pass2(symtab)
object_program = pass2.assemble(intermediate_data, "COPY", 0x0000)

print("Generated Object Program:")
print(object_program)