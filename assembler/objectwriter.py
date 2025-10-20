# assembler/objectwriter.py

class ObjectWriter:
    def __init__(self):
        self.header = ""
        self.text_records = []
        self.end_record = ""

    def write_header(self, program_name, start_addr, length):
        """Create header record."""
        self.header = f"H{program_name[:6].ljust(6)}{start_addr:06X}{length:06X}"

    def add_text_record(self, start_addr, obj_codes):
        """Create a single text record (max 30 bytes)."""
        record_str = "".join(obj_codes)
        length = len(record_str) // 2
        self.text_records.append(f"T{start_addr:06X}{length:02X}{record_str}")

    def write_end(self, first_exec_addr):
        """Add end record."""
        self.end_record = f"E{first_exec_addr:06X}"

    def generate(self):
        """Return complete object program as text."""
        return "\n".join([self.header] + self.text_records + [self.end_record])