# test_pass1_pass2_integration.py
from assembler.pass1 import Pass1
from assembler.tables import SymbolTable, OpcodeTable, RegisterTable
from assembler.pass2 import Pass2

print("=== TESTING PASS 1 → PASS 2 INTEGRATION ===")

# Sample assembly code (from basic.txt)
sample_assembly = [
    "COPY    START   0",
    "FIRST   STL     RETADR",
    "CLOOP   JSUB    RDREC", 
    "        LDA     LENGTH",
    "        COMP    #0",
    "        JEQ     ENDFIL",
    "        JSUB    WRREC",
    "        J       CLOOP",
    "ENDFIL  LDA     EOF",
    "        STA     BUFFER",
    "        LDA     #3",
    "        STA     LENGTH", 
    "        JSUB    WRREC",
    "        J       @RETADR",
    "EOF     BYTE    C'EOF'",
    "RETADR  RESW    1",
    "LENGTH  RESW    1", 
    "BUFFER  RESB    4096",
    "        END     FIRST"
]

# Run Pass 1 
print("Running Pass 1...")
pass1 = Pass1()
intermediate, symtab, length = pass1.assemble(sample_assembly)

print(f"Pass 1 generated {len(intermediate)} intermediate lines")
print(f"Symbol table has {len(symtab.symbols)} symbols")

# Run Pass 2 
print("Running Pass 2...")
optab = OpcodeTable()
regtab = RegisterTable()
pass2 = Pass2(symtab, optab, regtab)
object_program = pass2.assemble(intermediate, "COPY", 0x0000)

print("INTEGRATION SUCCESSFUL!")
print("Object program:")
print(object_program)