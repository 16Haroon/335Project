# debug_functions.py
from assembler.pass1 import Pass1
from assembler.tables import OpcodeTable

with open('examples/functions.txt', 'r') as f:
    lines = [line.rstrip() for line in f if line.strip() and not line.startswith('.')]

print("Checking functions.txt for REAL missing instructions...")
optab = OpcodeTable()

# List of assembler directives (not real instructions)
directives = {'START', 'END', 'RESW', 'RESB', 'BYTE', 'BASE', 'WORD', 'LTORG'}

for line in lines:
    parts = line.split()
    if len(parts) >= 2:
        # Get the operation (second token if 3 parts, first if 2 parts)
        if len(parts) == 3:
            label, opcode, operand = parts
        else:
            opcode, operand = parts[0], parts[1] if len(parts) > 1 else ""
        
        opcode = opcode.upper()
        
        # Skip labels and directives for this check
        if opcode in directives:
            continue
            
        # Check if instruction exists
        if optab.get(opcode):
            print(f" {opcode}: FOUND")
        else:
            print(f" {opcode}: MISSING - in line: {line}")

print("\nNow let's test the actual assembly...")
pass1 = Pass1()
try:
    intermediate, symtab, length = pass1.assemble(lines)
    print("✓ Pass 1 completes successfully")
    
    # Test Pass 2 on just the first few lines to see where it fails
    from assembler.pass2 import Pass2
    from assembler.tables import RegisterTable
    
    optab = OpcodeTable()
    regtab = RegisterTable()
    pass2 = Pass2(symtab, optab, regtab)
    
    print("Testing Pass 2 on first 10 lines...")
    for i, (loc, label, op, operand) in enumerate(intermediate[:10]):
        try:
            obj_code = pass2.generate_object_code(op, operand, loc)
            print(f"  {loc:04X} {op:<8} {operand:<10} -> {obj_code}")
        except Exception as e:
            print(f"  {loc:04X} {op:<8} {operand:<10} -> ERROR: {e}")
            
except Exception as e:
    print(f"✗ Pass 1 fails: {e}")