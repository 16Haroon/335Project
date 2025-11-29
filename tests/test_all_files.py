# test_all_files.py
from assembler.pass1 import Pass1
from assembler.tables import OpcodeTable, RegisterTable
from assembler.pass2 import Pass2
import os

print("=== TESTING ALL SAMPLE FILES ===")

files = ['basic.txt', 'functions.txt', 'literals.txt', 
         'prog_blocks.txt', 'control_section.txt', 'macros.txt']

for filename in files:
    print(f"\n--- Testing {filename} ---")
    try:
        with open(f'examples/{filename}', 'r') as f:
            lines = [line.rstrip() for line in f if line.strip() and not line.strip().startswith('.')]
        
        pass1 = Pass1()
        intermediate, symtab, length = pass1.assemble(lines)
        
        optab = OpcodeTable()
        regtab = RegisterTable()
        pass2 = Pass2(symtab, optab, regtab)
        
        # Use first word as program name
        prog_name = lines[0].split()[0] if lines else "TEST"
        object_program = pass2.assemble(intermediate, prog_name, 0x0000)
        
        print(f" {filename}: SUCCESS - {len(object_program)} chars")
        
    except Exception as e:
        print(f" {filename}: {e}")