# debug_pass1.py
from assembler.pass1 import Pass1

with open('examples/basic.txt', 'r') as f:
    lines = [line.rstrip() for line in f if line.strip()]

print("Lines from basic.txt:")
for i, line in enumerate(lines):
    print(f"{i}: '{line}'")

print("\nTracing Pass 1 execution...")
pass1 = Pass1()
try:
    intermediate, symtab, length = pass1.assemble(lines)
    print("SUCCESS!")
    print(f"Intermediate: {len(intermediate)} lines")
    print(f"Symbols: {symtab.symbols}")
except Exception as e:
    print(f"ERROR: {e}")
    print("Let's check where it fails...")