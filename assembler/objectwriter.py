# assembler/objectwriter.py 
class ObjectWriter:
    def __init__(self):
        self.header = ""
        self.text_records = []
        self.end_record = ""
        self.modification_records = []

    def write_header(self, program_name, start_addr, length):
        """Create header record."""
        self.header = f"H{program_name[:6].ljust(6)}{start_addr:06X}{length:06X}"

    def add_text_record(self, start_addr, obj_codes):
        """Create text record from list of object codes."""
        if not obj_codes:
            return
            
        # Convert list to single hex string
        record_str = "".join(obj_codes)
        length = len(record_str) // 2  # Each byte = 2 hex chars
        
        # Ensure length fits in 1 byte (max 255)
        if length > 255:
            # Split into multiple records 
            length = 255
            record_str = record_str[:510]  # 255 * 2 hex chars
            
        self.text_records.append(f"T{start_addr:06X}{length:02X}{record_str}")

    def add_modification_record(self, address, length):
        """Add modification record for format 4 instructions."""
        self.modification_records.append(f"M{address:06X}{length:02X}")

    def write_end(self, first_exec_addr):
        """Add end record."""
        self.end_record = f"E{first_exec_addr:06X}"

    def generate(self):
        """Return complete object program as text."""
        records = [self.header] + self.text_records + self.modification_records + [self.end_record]
        return "\n".join(records)