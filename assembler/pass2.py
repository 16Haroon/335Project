# assembler/pass2.py 
from assembler.objectwriter import ObjectWriter
from assembler.listing import ListingWriter

class Pass2:
    def __init__(self, symtab, optab, littab=None, regtab=None):
        self.symtab = symtab
        self.optab = optab
        self.littab = littab
        self.regtab = regtab
        self.obj_writer = ObjectWriter()
        self.base_value = None
        self.location_counter = 0
        self.program_start = 0

    def parse_operand(self, operand):
        """Parse operand to extract addressing mode information"""
        if not operand:
            return None, None, None, None, None, None
            
        # Handle format 2 instructions (register-register)
        if ',' in operand:
            parts = operand.split(',')
            if len(parts) == 2:
                return parts[0], parts[1], None, None, None, None
        
        # Handle addressing modes
        addressing_mode = 'simple'
        is_indirect = False
        is_immediate = False
        is_indexed = False
        is_format4 = False
        clean_operand = operand
        
        if operand.startswith('@'):
            is_indirect = True
            addressing_mode = 'indirect'
            clean_operand = operand[1:]
        elif operand.startswith('#'):
            is_immediate = True
            addressing_mode = 'immediate'
            clean_operand = operand[1:]
        elif operand.endswith(',X'):
            is_indexed = True
            addressing_mode = 'indexed'
            clean_operand = operand[:-2]
        elif operand.startswith('+'):
            is_format4 = True
            clean_operand = operand[1:]
            
        return clean_operand, addressing_mode, is_indirect, is_immediate, is_indexed, is_format4

    def calculate_displacement(self, target_address, pc_value, base_value, is_format4=False):
        """Calculate displacement for format 3/4 instructions"""
        if is_format4:
            return target_address, 'direct'
            
        # Format 3 - try PC-relative first
        disp = target_address - pc_value
        if -2048 <= disp <= 2047:
            return disp, 'p'  # PC-relative
            
        # Try base-relative
        if base_value is not None:
            disp = target_address - base_value
            if 0 <= disp <= 4095:
                return disp, 'b'  # Base-relative
                
        # If neither works, use format 4
        return target_address, 'direct'

    def generate_format1(self, opcode_hex):
        """Generate object code for format 1 instructions"""
        return f"{int(opcode_hex, 16):02X}"

    def generate_format2(self, opcode_hex, operand):
        """Generate object code for format 2 instructions"""
        opcode = int(opcode_hex, 16)
        
        if ',' in operand:
            reg1, reg2 = operand.split(',')
            r1 = self.regtab.get(reg1.strip()) if self.regtab else 0
            r2 = self.regtab.get(reg2.strip()) if self.regtab else 0
        else:
            r1 = self.regtab.get(operand.strip()) if self.regtab else 0
            r2 = 0
            
        return f"{opcode:02X}{r1:01X}{r2:01X}"

    def generate_format3_4(self, opcode_hex, operand, locctr, is_format4=False):
        """Generate object code for format 3/4 instructions"""
        opcode_val = int(opcode_hex, 16)
        
        # Parse operand for addressing modes
        clean_operand, _, is_indirect, is_immediate, is_indexed, _ = self.parse_operand(operand)
        
        # Set n,i bits based on addressing mode
        if is_immediate:
            n, i = 0, 1
        elif is_indirect:
            n, i = 1, 0
        else:
            n, i = 1, 1  # Simple addressing
            
        # Set x bit for indexed addressing
        x = 1 if is_indexed else 0
        
        # Set e bit for format 4
        e = 1 if is_format4 else 0
        
        # Calculate target address using SymbolTable
        target_addr = 0
        if clean_operand:
            # Try symbol table first
            sym_addr = self.symtab.lookup(clean_operand)
            if sym_addr is not None:
                target_addr = sym_addr
            else:
                # Try to parse as numeric value
                try:
                    if clean_operand.startswith('X'):  # Hexadecimal literal
                        target_addr = int(clean_operand[2:-1], 16)
                    elif clean_operand.startswith('C'):  # Character literal  
                        target_addr = ord(clean_operand[2:-1])
                    else:
                        target_addr = int(clean_operand)
                except:
                    target_addr = 0  # Default if cannot resolve
                
        # Calculate displacement and set b,p bits
        if is_format4:
            disp = target_addr
            b, p = 0, 0
        else:
            pc_value = locctr + 3  # PC points to next instruction
            disp, addr_mode = self.calculate_displacement(target_addr, pc_value, self.base_value)
            if addr_mode == 'p':
                b, p = 0, 1
            elif addr_mode == 'b':
                b, p = 1, 0
            else:  # direct
                b, p = 0, 0
                
        # Combine everything into object code
        first_byte = (opcode_val << 2) | (n << 1) | i
        second_byte = (x << 7) | (b << 6) | (p << 5) | (e << 4)
        
        if is_format4:
            # Format 4: 20-bit address
            obj_code = f"{first_byte:02X}{second_byte:01X}{target_addr:05X}"
        else:
            # Format 3: 12-bit displacement
            disp_12bit = disp & 0xFFF  # Ensure 12 bits
            obj_code = f"{first_byte:02X}{second_byte:01X}{disp_12bit:03X}"
            
        return obj_code

    def generate_object_code(self, operation, operand, locctr):
        """Main method to generate object code for any instruction"""
    
    # Handle assembler directives (no object code)
        if operation in ['BASE', 'RESW', 'RESB', 'WORD', 'BYTE', 'START', 'END', 'LTORG', 'USE']:
            return None
    
    # Handle format 4 instructions (preceded by '+')
        is_format4 = operation.startswith('+') if operation else False
        clean_operation = operation[1:] if is_format4 else operation
    
    # Check if it's an instruction using OpcodeTable
        opcode_info = self.optab.get(clean_operation)
        if not opcode_info:
            return None  # Not an instruction
        
        opcode_hex, format_type = opcode_info
    
    # Generate based on format
        try:
            if format_type == 1:
                return self.generate_format1(opcode_hex)
            elif format_type == 2:
                return self.generate_format2(opcode_hex, operand)
            elif format_type == 3:
            # Use format 4 if instruction has '+' prefix
                return self.generate_format3_4(opcode_hex, operand, locctr, is_format4)
        except Exception as e:
            print(f"ERROR generating object code for '{operation} {operand}' at {locctr:04X}: {e}")
        return None

        return None

    def assemble(self, intermediate_data, program_name="PROG", start_addr=0):
        """Main assembly method - works with Pass 1 intermediate format"""
        listing = ListingWriter("output_listing.txt")
        current_address = start_addr
        self.program_start = start_addr
    
        text_record_start = start_addr
        text_record_data = []
    
        for line in intermediate_data:
        # Handle both tuple and list formats from Pass 1
            if isinstance(line, (tuple, list)) and len(line) >= 4:
                locctr, label, operation, operand = line[:4]
            current_address = locctr
            
            # Generate object code with error handling
            try:
                obj_code = self.generate_object_code(operation, operand, locctr)
            except Exception as e:
                print(f"Warning: Could not generate object code for '{operation} {operand}' at {locctr:04X}: {e}")
                obj_code = None
            
            # Add to listing - handle None obj_code safely
            obj_code_str = str(obj_code) if obj_code is not None else ""
            listing.add_line(locctr, label or "", operation or "", operand or "", obj_code_str)
            
            # Handle text records - only add non-None obj_code
            if obj_code:
                text_record_data.append(obj_code)
                
                # If text record would exceed 30 bytes, write it and start new one
                if len(text_record_data) >= 10:
                    self.obj_writer.add_text_record(text_record_start, text_record_data)
                    text_record_start = locctr + len(obj_code) // 2
                    text_record_data = []
            else:
                # Write current text record if there's data and we hit a non-code line
                if text_record_data:
                    self.obj_writer.add_text_record(text_record_start, text_record_data)
                    text_record_start = locctr + 3  # Move to next instruction
                    text_record_data = []
    
    # Write any remaining text record data
        if text_record_data:
            self.obj_writer.add_text_record(text_record_start, text_record_data)
    
    # Calculate program length
        program_length = current_address - start_addr
    
    # Write header and end records
        self.obj_writer.write_header(program_name, start_addr, program_length)
        self.obj_writer.write_end(start_addr)
    
    # Write listing file
        listing.write()
    
        return self.obj_writer.generate()