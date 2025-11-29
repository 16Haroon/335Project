# test_integration.py
from assembler.tables import SymbolTable, OpcodeTable, RegisterTable
from assembler.pass2 import Pass2

def test_team_integration():
    print("Testing Pass 2 with Team's Data Structures...")
    
    # tables
    symtab = SymbolTable()
    optab = OpcodeTable()
    regtab = RegisterTable()
    
    # Add symbols 
    symtab.add("RETADR", 0x0030)
    symtab.add("LENGTH", 0x0033) 
    symtab.add("BUFFER", 0x0036)
    symtab.add("FIRST", 0x0000)
    symtab.add("CLOOP", 0x0003)
    symtab.add("ENDFIL", 0x0015)
    symtab.add("EOF", 0x0018)
    symtab.add("RDREC", 0x0020)
    symtab.add("WRREC", 0x0030)

    # Sample intermediate data from Pass 1
    intermediate_data = [
        (0x0000, "FIRST", "STL", "RETADR"),
        (0x0003, "CLOOP", "JSUB", "RDREC"),
        (0x0006, "", "LDA", "LENGTH"),
        (0x0009, "", "COMP", "#0"),
        (0x000C, "", "JEQ", "ENDFIL"),
        (0x000F, "", "JSUB", "WRREC"),
        (0x0012, "", "J", "CLOOP"),
        (0x0015, "ENDFIL", "LDA", "EOF"),
        (0x0018, "", "STA", "BUFFER"),
        (0x001B, "", "LDA", "#3"),
        (0x001E, "", "STA", "LENGTH"),
        (0x0021, "", "JSUB", "WRREC"),
        (0x0024, "", "J", "@RETADR"),
    ]

    # Run Pass 2 with team's data structures
    pass2 = Pass2(symtab, optab, regtab=regtab)
    object_program = pass2.assemble(intermediate_data, "COPY", 0x0000)

    print("Generated Object Program:")
    print(object_program)
    
    print("\nCheck output_listing.txt for the assembly listing!")
    
    # Display tables for verification
    symtab.display()
    optab.display()
    regtab.display()

if __name__ == "__main__":
    test_team_integration()