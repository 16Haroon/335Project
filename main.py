# main.py
import sys
import os
from assembler.pass1 import Pass1
from assembler.tables import OpcodeTable, RegisterTable
from assembler.pass2 import Pass2

def assemble_file(filename):
    """Assemble a single SIC/XE file"""
    try:
        print(f" Assembling {filename}...")
        
        # Read input file
        with open(filename, 'r') as f:
            lines = [line.rstrip() for line in f if line.strip()]
        
        # Run Pass 1
        pass1 = Pass1()
        intermediate, symtab, length = pass1.assemble(lines)
        print(f"   ✓ Pass 1: {len(intermediate)} lines, {len(symtab.symbols)} symbols")
        
        # Run Pass 2
        optab = OpcodeTable()
        regtab = RegisterTable()
        pass2 = Pass2(symtab, optab, regtab)
        
        # Get program name and start address
        first_parts = lines[0].split()
        if len(first_parts) >= 3 and first_parts[1].upper() == "START":
            prog_name = first_parts[0]
            start_addr = int(first_parts[2], 16)
        else:
            prog_name = "PROGRAM"
            start_addr = 0
        
        object_program = pass2.assemble(intermediate, prog_name, start_addr)
        
        # Write object file
        base_name = os.path.splitext(filename)[0]
        obj_filename = f"{base_name}.obj"
        with open(obj_filename, 'w') as f:
            f.write(object_program)
        
        print(f"   Success! Object file: {obj_filename}")
        print(f"   Listing file: output_listing.txt")
        return True
        
    except Exception as e:
        print(f"   Failed: {e}")
        return False

def main():
    if len(sys.argv) > 1:
        # Assemble specific file
        filename = sys.argv[1]
        if not os.path.exists(filename):
            print(f"Error: File '{filename}' not found")
            return
        assemble_file(filename)
    else:
        # Assemble all example files
        print("=== SIC/XE ASSEMBLER ===")
        files = [
            'examples/basic.txt',
            'examples/functions.txt', 
            'examples/literals.txt',
            'examples/prog_blocks.txt',
            'examples/control_section.txt',
            'examples/macros.txt'
        ]
        
        success_count = 0
        for file in files:
            if os.path.exists(file):
                if assemble_file(file):
                    success_count += 1
                print()  # blank line between files
            else:
                print(f"File not found: {file}")
        
        print(f" Results: {success_count}/{len(files)} files assembled successfully!")

if __name__ == "__main__":
    main()
