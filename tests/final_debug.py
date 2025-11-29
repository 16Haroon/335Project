# final_debug.py
from assembler.pass1 import Pass1
from assembler.tables import OpcodeTable, RegisterTable
from assembler.pass2 import Pass2
import traceback

def test_functions():
    print("=== FINAL DEBUG: functions.txt ===")
    
    with open('examples/functions.txt', 'r') as f:
        lines = [line.rstrip() for line in f if line.strip() and not line.startswith('.')]

    # Run Pass 1
    pass1 = Pass1()
    intermediate, symtab, length = pass1.assemble(lines)
    print(f"✓ Pass 1: {len(intermediate)} lines, {len(symtab.symbols)} symbols")

    # Run Pass 2 with detailed error handling
    optab = OpcodeTable()
    regtab = RegisterTable()
    pass2 = Pass2(symtab, optab, regtab)
    
    print("Running Pass 2 assemble method...")
    try:
        object_program = pass2.assemble(intermediate, "COPY", 0x0000)
        print(" SUCCESS! Object program generated:")
        print(object_program)
    except Exception as e:
        print(f" ERROR in assemble method: {e}")
        print("Full traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    test_functions()