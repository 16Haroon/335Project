# test_format4.py
from assembler.tables import OpcodeTable
from assembler.pass2 import Pass2
from assembler.pass1 import Pass1

# Test format 4 directly
print("Testing Format 4 instructions...")
optab = OpcodeTable()

# Check if +JSUB is found
print(f"+JSUB in OPTAB: {optab.get('+JSUB')}")
print(f"JSUB in OPTAB: {optab.get('JSUB')}")

# Test a simple format 4 case
test_code = ["TEST START 1000", "+JSUB SUBRTN", "SUBRTN RSUB", "END TEST"]

pass1 = Pass1()
intermediate, symtab, length = pass1.assemble(test_code)

optab = OpcodeTable()
from assembler.tables import RegisterTable
regtab = RegisterTable()
pass2 = Pass2(symtab, optab, regtab)

print("\nTesting object code generation:")
for loc, label, op, operand in intermediate:
    obj_code = pass2.generate_object_code(op, operand, loc)
    print(f"  {loc:04X} {op:<8} {operand:<10} -> {obj_code}")